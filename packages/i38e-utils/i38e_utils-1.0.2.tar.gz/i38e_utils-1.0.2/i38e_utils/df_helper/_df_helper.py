#  Copyright (c) 2024. ISTMO Center S.A.  All Rights Reserved
#  IBIS is a registered trademark
#
import dask.dataframe as dd
from django.db.models import Q

from ..log_utils import Logger
from .config import *
from .io import read_frame
from .models import ParquetOptions, QueryConfig, ConnectionConfig, ParamsConfig

logger = Logger(log_dir='./logs/', logger_name=__name__, log_file=f'{__name__}.log')


class DfHelper:
    debug: bool = False
    verbose: bool = False
    parquet_options: ParquetOptions = None
    query_config: QueryConfig = None
    connection_config: ConnectionConfig = None

    def __init__(self, **kwargs):
        self.debug = kwargs.pop('debug', False)
        self.verbose = kwargs.pop('verbose', False)
        self.parquet_options = ParquetOptions(**kwargs)
        if self.parquet_options.use_parquet is False:
            self.connection_config = ConnectionConfig(**kwargs)
        # else:
        #    self.connection_config = None
        self.query_config = QueryConfig(**kwargs)
        self.params_config = ParamsConfig(**kwargs)

    def load(self, **options):
        return self._load(**options)

    def _load(self, **options: Dict[str, Union[str, bool, Dict, None]]) -> pd.DataFrame:
        # if options is not None:
        self.params_config.parse_params(options)
        if self.parquet_options.use_parquet is True:
            result = self.load_from_parquet()
        else:
            result = self._load_from_db()

        return result

    def load_from_parquet(self) -> pd.DataFrame:
        if self.debug:
            logger.info(f'Loading from parquet file...{self.parquet_options.parquet_full_path}')
            if self.verbose:
                print(f'Loading from parquet file...{self.parquet_options.parquet_full_path}')
        try:
            if self.parquet_options.parquet_folder_list:
                df = dd.read_parquet(self.parquet_options.parquet_folder_list)
            else:
                df = dd.read_parquet(self.parquet_options.parquet_full_path)
            df = self.parquet_options.apply_filters_dask(df, self.params_config.filters)
            if self.parquet_options.df_as_dask:
                return df
            else:
                return df.compute()
        except FileNotFoundError:
            if self.debug:
                logger.info(f'Parquet file {self.parquet_options.parquet_full_path} does not exist')
                if self.verbose:
                    print(f'Parquet file {self.parquet_options.parquet_full_path} does not exist')
            if self.parquet_options.df_as_dask:
                return dd.from_pandas(pd.DataFrame(), npartitions=1)
            return pd.DataFrame()

    def _load_from_db(self) -> pd.DataFrame:
        """
        Load data from the database based on the filters provided. If no filters are given, it loads only the first
        n_records.
            n_records: Number of records to load if no filters are provided.
            :return: A DataFrame loaded with data from the database.
        """
        if self.connection_config.model is None:
            if self.debug:
                logger.critical('Model must be specified')
                if self.verbose:
                    print('Model must be specified')
            raise ValueError('Model must be specified')
        df = self._build_and_load()
        if df is not None:
            df = self._process_loaded_data(df)
        return df

    def _build_and_load(self) -> pd.DataFrame:
        query = self.connection_config.model.objects.using(self.connection_config.connection_name)
        if self.debug:
            logger.debug(query.query)
            logger.debug(self.params_config.filters)
        if not self.params_config.filters:
            # IMPORTANT: if no filters are provided show only the first n_records
            # this is to prevent loading the entire table by mistake
            n_records = 100
            if self.debug:
                logger.info(f'No filters provided, showing first %s records, {n_records}')
                if self.verbose:
                    print(f'No filters provided, showing first {n_records} records')
            queryset = query.all()[:n_records]
        else:
            q_objects = self.build_q_objects(self.params_config.filters, self.query_config.use_exclude)
            queryset = query.filter(q_objects)[
                       :self.query_config.n_records] if self.query_config.n_records > 0 else query.filter(q_objects)

        if queryset is not None:
            if self.debug:
                logger.debug(queryset.query)
                if self.verbose:
                    print(queryset.query)

            df = read_frame(queryset, **self.params_config.df_params)
            # df = self.batched_read_frame(qs, 100, **self.dataframe_params)
            if self.debug:
                logger.debug(df.head())
                if self.verbose:
                    print(df.head())
            return df
        else:
            return pd.DataFrame()

    @staticmethod
    def build_q_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def _process_loaded_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._convert_columns(df)
        if self.params_config.field_map:
            if self.debug:
                logger.info(f'Renaming columns...{[col for col in self.params_config.field_map.keys()]}')
                if self.verbose:
                    print(f'Renaming columns...{[col for col in self.params_config.field_map.keys()]}')
            set_to_keep1 = set(self.params_config.field_map.keys())
            set_to_keep2 = set(self.params_config.df_params.get('column_names', []))
            columns_to_keep = list(set_to_keep1.union(set_to_keep2))
            cols_to_drop = [col for col in df.columns if col not in columns_to_keep]
            df.drop(columns=cols_to_drop, inplace=True)
            df.rename(columns=self.params_config.field_map, inplace=True)
        return df

    def _convert_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
                Convert the data types of columns in the DataFrame based on the field type in the Django model.

                :param df: DataFrame whose columns' data types are to be converted.
                :return: DataFrame with converted column data types.
        """
        if self.debug:
            logger.info(f'Converting columns:{[col for col in df.columns]}')
        model_fields = self.connection_config.model._meta.get_fields()
        for field in model_fields:
            field_name = field.name
            field_type = type(field).__name__
            if field_name in df.columns:
                if self.debug:
                    logger.debug(f"Found column {field_name} of type {field_type}")
                    if self.verbose:
                        print(f"Found column {field_name} of type {field_type}")
                if field_type in list(conversion_map.keys()):
                    try:
                        df[field_name] = conversion_map[field_type](df[field_name])
                        if self.debug:
                            logger.info(f"Converted column {field_name} of type {field_type}")
                            if self.verbose:
                                print(f"Converted column {field_name} of type {field_type}")
                    except Exception as e:
                        if self.debug:
                            logger.info(f"Error converting column {field_name} of type {field_type}")
                            logger.error(e)
                            if self.verbose:
                                print(f"Error converting column {field_name} of type {field_type}")
                else:
                    if self.debug:
                        logger.error(f"Field type {field_type} not found in conversion_map")
                        if self.verbose:
                            print(f"Field type {field_type} not found in conversion_map")
            else:
                if self.debug:
                    logger.error(f"Column {field_name} not found in df.columns")
                    if self.verbose:
                        print(f"Column {field_name} not found in df.columns")
        return df

    def save_to_parquet(self, df: pd.DataFrame, parquet_full_path, engine: str = 'auto') -> None:
        """IMPORTANT: This routine must be explicitly called to save the
        dataframe to a parquet file This is because sometimes the first generated df is not what we want to save but
        saving after cleaning data and after other merge operations
        """
        if self.debug:
            logger.info(f'Saving to parquet file...{parquet_full_path}')
            if self.verbose:
                print(f'Saving to parquet file...{parquet_full_path}')
        if not df.empty:
            try:
                df.to_parquet(parquet_full_path, engine=engine)
            except Exception as e:
                logger.error(f'Error while saving DataFrame to parquet: {e}')
                if self.verbose:
                    print(f'Error while saving DataFrame to parquet: {e}')
        else:
            logger.warning(f'Attempted to save an empty DataFrame to {parquet_full_path}')
            if self.verbose:
                print(f'Attempted to save an empty DataFrame to {parquet_full_path}')
