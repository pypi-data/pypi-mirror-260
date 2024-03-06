#  Copyright (c) 2023. ISTMO Center S.A.  All Rights Reserved
#

import datetime
import os
import time
from typing import Any, Dict

import pandas as pd

from .df_utils import add_df_totals

timeseries_options: Dict = {
    'index_col': 'last_activity_dt',
    'rule': 'D',
    'cols': None,
    'vals': None,
    'totals': False,
    'aggfunc': 'count'
}


def convert_value_pairs(row):
    if row['value_type'] == "datetime":
        converted_value = datetime.datetime.strptime(row['value'], '%Y-%m-%d %H:%M:%S')
    elif row['value_type'] == 'str':
        converted_value = row['value']
    else:
        converted_value = eval(f"{row['value_type']}({row['value']})")
    return converted_value


def get_timeseries_params(df_params) -> Any:
    index_col = None
    ts_params = df_params
    if ts_params.get("datetime_index", False):
        index_col = ts_params.get('index_col', None)
        pop_cols = ['datetime_index', 'index_col']
        for p in pop_cols:
            ts_params.pop(p, None)
    return index_col, ts_params


def format_fields(df, format_options):
    for fld_name, fld_type in format_options.items():
        if fld_name in df.columns:
            df[fld_name] = df[fld_name].values.astype(fld_type)
    return df


def fillna_fields(df, fill_options):
    for fld_name, fill_value in fill_options.items():
        if fld_name in df.columns:
            df[fld_name].fillna(fill_value, inplace=True)
    return df


def cast_cols_as_categories(df, threshold=100):
    for col in df.columns:
        if df[col].dtype == object and len(df[col].unique()) < threshold:
            df[col] = df[col].astype(pd.CategoricalDtype())
    return df


def load_as_timeseries(df, **options):
    index_col = options.get("index_col", None)
    if index_col is not None and df.index.name != index_col:
        if index_col in df.columns:
            df.reset_index(inplace=True)
            df.set_index(index_col, inplace=True)
    rule = options.get("rule", "D")
    index = options.get("index", df.index)
    cols = options.get("cols", None)
    vals = options.get("vals", None)
    totals = options.get("totals", False)
    agg_func = options.get("agg_func", 'count')
    df = df.pivot_table(index=index, columns=cols, values=vals, aggfunc=agg_func).fillna(0)
    df = df.resample(rule=rule).sum()
    df.sort_index(inplace=True)
    if totals:
        df = add_df_totals(df)
    return df


def fix_fields(df, fields_to_fix, field_type):
    field_attributes = {
        'str': {'default_value': '', 'dtype': str},
        'int': {'default_value': 0, 'dtype': int},
        'date': {'default_value': pd.NaT, 'dtype': 'datetime64[ns]'},
        'datetime': {'default_value': pd.NaT, 'dtype': 'datetime64[ns]'}
    }

    if field_type not in field_attributes:
        raise ValueError("Invalid field type: {}".format(field_type))

    attr = field_attributes[field_type]
    fields = [field for field in fields_to_fix if field in df.columns]
    df[fields] = df[fields].fillna(attr['default_value']).astype(attr['dtype'])


class DataWrapper:
    def __init__(self, dataclass, date_field, data_path, parquet_filename, start_date, end_date,
                 verbose=False, load_params=None, reverse_order=False, overwrite=False):

        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self.ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.verbose = verbose
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.max_age_minutes = 0

        # Convert string dates to datetime.date objects if they are not already
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() if isinstance(start_date,
                                                                                                  str) else start_date
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() if isinstance(end_date,
                                                                                              str) else end_date

    @staticmethod
    def ensure_forward_slash(path):
        return path if path.endswith('/') else path + '/'

    @staticmethod
    def ensure_directory_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def process(self):
        current_date = self.end_date if self.reverse_order else self.start_date
        while (self.reverse_order and current_date >= self.start_date) or (
                not self.reverse_order and current_date <= self.end_date):
            self.process_date(current_date)
            current_date += datetime.timedelta(days=-1 if self.reverse_order else 1)

    @staticmethod
    def check_file_is_recent(file_path, age, unit='minutes'):
        if not os.path.exists(file_path):
            return False

        # Get file modification time (mtime)
        mtime = os.path.getmtime(file_path)
        current_time = time.time()

        # Convert age to seconds
        if unit == 'minutes':
            age_in_seconds = age * 60
        elif unit == 'hours':
            age_in_seconds = age * 60 * 60
        elif unit == 'days':
            age_in_seconds = age * 60 * 60 * 24
        else:
            raise ValueError(f"Unsupported unit: {unit}")

        # Check if file is recent
        return current_time - mtime <= age_in_seconds

    def process_date(self, date):
        folder = f'{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/'
        self.ensure_directory_exists(folder)
        full_parquet_filename = os.path.join(folder, self.parquet_filename)
        if self.overwrite:
            self.max_age_minutes = 10
        file_exists, file_is_recent = self.file_exists_and_recent(full_parquet_filename, self.max_age_minutes)

        if self.verbose:
            print(f"{full_parquet_filename}: File exists: {file_exists}, is recent: {file_is_recent}")

        if not file_exists or not file_is_recent and self.overwrite:
            if self.overwrite and self.verbose:
                print("Overwrite is on!")
            params = {
                'parquet_storage_path': folder,
                'use_parquet': True,
                'parquet_filename': self.parquet_filename,
                'parquet_max_age_minutes': self.max_age_minutes
            }
            params.update(self.load_params)
            data_object = self.dataclass(live=True, **params)
            if data_object.save_parquet:
                print(f"Saving {self.dataclass.__name__} data for {date.year}/{date.month:02d}/{date.day:02d}")
                self.load_params.update(
                    {f'{self.date_field}__year': date.year, f'{self.date_field}__month': date.month,
                     f'{self.date_field}__day': date.day})
                df = data_object.load(**self.load_params)
                if len(df.index) > 0:
                    data_object.save_to_parquet(df, engine='pyarrow')

    @staticmethod
    def file_exists_and_recent(path, max_age_minutes=0):
        exists = os.path.exists(path)
        is_recent = False
        if exists:
            file_age_minutes = (time.time() - os.path.getmtime(path)) / 60
            if max_age_minutes == 0:
                is_recent = True
            else:
                is_recent = file_age_minutes <= max_age_minutes
        return exists, is_recent

# Usage:
# wrapper = DataWrapper(dataclass=YourDataClass, date_field="created_at", data_path="/path/to/data", parquet_filename="data.parquet", start_date="2022-01-01", end_date="2022-12-31")
# wrapper.process()
