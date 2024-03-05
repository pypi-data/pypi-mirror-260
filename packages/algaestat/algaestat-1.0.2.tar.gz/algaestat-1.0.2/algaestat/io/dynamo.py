import boto3
from getpass import getpass
import simplejson as json
import os
from typing import Optional
import importlib_resources
import pandas as pd
import logging
import types
import time


## New Flush

def _flush(self):
    logger = logging.getLogger('boto3.dynamodb.table')
    logger.setLevel(logging.DEBUG)
    items_to_send = self._items_buffer[:self._flush_amount]
    self._items_buffer = self._items_buffer[self._flush_amount:]
    self._response = self._client.batch_write_item(
        RequestItems={self._table_name: items_to_send})
    unprocessed_items = self._response['UnprocessedItems']

    if unprocessed_items and unprocessed_items[self._table_name]:
        # Any unprocessed_items are immediately added to the
        # next batch we send.
        self._items_buffer.extend(unprocessed_items[self._table_name])
    else:
        self._items_buffer = []
    logger.debug("Batch write sent %s, unprocessed: %s",
                 len(items_to_send), len(self._items_buffer))


class QueryDB:
    def __init__(self,
                 db_config_filepath: Optional[str | None] = None,
                 cred_filepath: Optional[str | None] = None,
                 access_key_id: Optional[str | None] = None,
                 secret_key: Optional[str | None] = None,
                 region_name: Optional[str] = 'us-west-2',
                 timeout: Optional[int] = 5
                 ):
        """
        if a cred filepath is declared, the access_keyid, secret and region name will be ignored.
        Please retrieve credentials securely, or use the default promts or credential file.
        :param db_config_filepath:
        :param cred_filepath:
        :param access_key_id:
        :param secret_key:
        :param region_name:
        """

        self.db_resource = None
        self.db_config = None
        if db_config_filepath is not None:
            if not os.path.isfile(db_config_filepath):
                raise "config file declared is missing"
            try:
                with open(db_config_filepath, 'r') as f:
                    self.db_config = json.load(f)
            except:
                raise "config is in an improper json format"
        else:
            config_dir = importlib_resources.files("algaestat") / "io"
            try:
                with open(os.path.join(config_dir, 'config.json'), 'r') as f:
                    self.db_config = json.load(f)
            except:
                raise "the defaultconfig is in an improper json format was it modified prior to compiling?"
        if cred_filepath is None:
            self.db_resource = self.init_dynamo_key_prompt(access_key_id=access_key_id,
                                                           secret_key=secret_key,
                                                           region_name=region_name,
                                                           timeout=timeout)
        else:
            if not os.path.isfile(cred_filepath):
                raise "Your cred_filepath file declared is missing"
            self.db_resource = self.init_dynamo_resource(filepath=cred_filepath,
                                                         timeout=timeout)

    def init_dynamo_key_prompt(self, access_key_id=None,
                               secret_key=None,
                               region_name='us-west-2',
                               timeout=5):
        """
        initialize dynamodb resource with prompt if variables are set to none (or not applied)
        :param access_key_id: option to pass credential
        :param secret_key: option to pass secret key if obtained by different method (google colab)
        :param region_name: region_name needs to be properly declared to a valid region
        :param timeout: time out to use for the resource dynamo query.
        :return: dynamodb: dynamodb resource
        """
        if (access_key_id is None) or (secret_key is None):
            access_key_id = getpass(prompt='Enter AWS Access Key ID: ')
            secret_key = getpass(prompt='Enter AWS Secret Key: ')
        if (region_name is None) or region_name.strip() == '':
            region_name = input('Enter region name ')

        # global dynamodb
        dynamodb = boto3.resource('dynamodb',
                                  region_name=region_name,
                                  aws_access_key_id=access_key_id,
                                  aws_secret_access_key=secret_key)
        dynamodb.meta.client.meta.config.connect_timeout = timeout
        return dynamodb

    def init_dynamo_resource(self, filepath=None, timeout=5):
        '''
        initialize dynamodb resource with cred file
        :param filepath:  full path to the credential file stored in a secure location
        :param timeout: dynamodb timeout length
        :return: dynamodb: dynamodb resource
        '''
        if filepath is None:
            raise 'filepath is required for init_dynamo_resource.'

        with open(filepath, 'r') as f:
            creds = json.load(f)

        dynamodb = boto3.resource('dynamodb',
                                  region_name=creds['region_name'],
                                  aws_access_key_id=creds['aws_access_key_id'],
                                  aws_secret_access_key=creds['aws_secret_access_key'])
        dynamodb.meta.client.meta.config.connect_timeout = timeout
        return dynamodb

    # Simple Metadata function for identifying the Primary Key Name for querying/scanning
    def get_table_metadata(self, table_name):
        table = self.db_resource.Table(table_name)
        return {
            'num_items': table.item_count,
            'primary_key_name': table.key_schema[0],
            'status': table.table_status,
            'bytes_size': table.table_size_bytes,
            'global_secondary_indices': table.global_secondary_indexes
        }

    def query_table_range(self,
                          table_name=None,
                          identifier_key=None,
                          identifier_name=None,
                          range_name=None,
                          start=None,
                          end=None,
                          exact=False,
                          as_dataframe=True):
        _key = boto3.dynamodb.conditions.Key
        table = self.db_resource.Table(table_name)
        data = []
        if self.db_resource is None:
            print('Missing valid boto3 dynamodb resource object')
            return []
        if table_name is None:
            print('Missing valid dynamodb table name')
            return []
        if identifier_key is None:
            print('Missing valid identifier_name (primary key column name)')
            return []
        if identifier_name is None:
            print('Missing valid identifier_name (primary keys value)')
            return []

        if range_name is None:
            query_expression = _key(identifier_key).eq(identifier_name)
        else:
            if (start is None) and (end is None):
                print('Missing valid range for range key (partition id)')
                return []
            elif (start is None) and (end is not None):
                if not exact:
                    query_expression = _key(identifier_key).eq(identifier_name) & _key(range_name).lte(end)
                else:
                    query_expression = _key(identifier_key).eq(identifier_name) & _key(range_name).eq(end)
            elif (start is not None) and (end is None):
                if not exact:
                    query_expression = _key(identifier_key).eq(identifier_name) & _key(range_name).gte(start)
                else:
                    query_expression = _key(identifier_key).eq(identifier_name) & _key(range_name).eq(start)
            else:
                query_expression = _key(identifier_key).eq(identifier_name) & _key(range_name).between(start, end)

        response = table.query(KeyConditionExpression=query_expression)
        if u'Items' not in response.keys():
            print('Bad Response.')
            return []

        for i in response[u'Items']:
            data.append(i)

        while 'LastEvaluatedKey' in response:
            response = table.query(KeyConditionExpression=query_expression,
                                   ExclusiveStartKey=response['LastEvaluatedKey'])
            for i in response['Items']:
                data.append(i)
        if not as_dataframe:
            return data
        return pd.DataFrame(data)

    def query_table_filter(self, table_name=None,
                           sort_key=None,
                           partition_key=None,
                           filter_expression_list=None):
        print({'sort_key': sort_key, 'partition_key': partition_key, 'filter_expression_list': filter_expression_list})
        table = self.db_resource.Table(table_name)
        data = []
        if self.db_resource is None:
            print('Missing boto3 dynamodb resource object')
        for filter_expression_i in filter_expression_list:
            response = table.query(KeyConditionExpression=filter_expression_i)
            if (u'ResponseMetadata' in response.keys()) and (u'HTTPStatusCode' in response['ResponseMetadata'].keys()):

                if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                    http_status_code = response['ResponseMetadata']['HTTPStatusCode']
                    print(f'Error: Bad Response, {http_status_code}')
                    return []

            if u'Items' not in response.keys():
                print('Bad Response.')
                return []
            for i in response[u'Items']:
                data.append(i)

            while 'LastEvaluatedKey' in response:
                response = table.query(KeyConditionExpression=filter_expression_i,
                                       ExclusiveStartKey=response['LastEvaluatedKey'])
                for i in response['Items']:
                    data.append(i)
        return data

    # Only perform table scans on experiment
    def scan_table(self, table_name, filter_key=None, filter_value=None):
        _key = boto3.dynamodb.conditions.Key
        """
        Perform a scan operation on table.
        Can specify filter_key (col name) and its value to be filtered.
        """
        if table_name not in ['experiment_meta']:
            raise 'This scan will be DB intensive and costly, please use query table'
        table = self.db_resource.Table(table_name)
        if filter_key is not None and filter_value is not None:
            filtering_exp = _key(filter_key).eq(filter_value)
            response = table.scan(FilterExpression=filtering_exp)
        else:
            response = table.scan()

        return response

    def get_pond_range_from_exp(self, identifier_key='ExperimentID', exp_name=None, table_name='experiment_meta'):
        if self.db_resource is None:
            print('Missing boto3 dynamodb resource object')
            return []
        if exp_name is None:
            print('Missing exp_name')
            return []
        data = self.query_table_range(table_name=table_name,
                                      identifier_key=identifier_key,
                                      identifier_name=exp_name)
        return data

    def generate_filter_from_pond_range(self, pond_range=None,
                                        table='',
                                        partition_key='PondID',
                                        sort_key='Timestamp'):

        if table not in ['miprobe', 'miprobe_cap', 'ysi', 'harvest', 'activity_log', 'lab_samples']:
            print('Error: Choose a valid dynamodb table from list: ',
                  ['miprobe', 'miprobe_cap', 'ysi', 'harvest', 'activity_log', 'lab_samples'])
            return None
        if pond_range is None:
            print('Error: Assign correct pond range data')
            return None
        _key = boto3.dynamodb.conditions.Key
        filter_expression_list = []
        for pr_i in pond_range:
            filter_expression_list.append(
                _key(sort_key).between(pr_i['Start_Timestamp'], pr_i['End_Timestamp']) & _key(partition_key).eq(
                    pr_i['PondID']))
        return {'table_name': table, 'sort_key': sort_key, 'partition_key': partition_key,
                'filter_expression_list': filter_expression_list}

    def get_all_data_from_exp_table(self, exp_name=None, table_name=None):
        pond_range = self.get_pond_range_from_exp(exp_name=exp_name)
        filter_dict = self.generate_filter_from_pond_range(pond_range=pond_range, table=table_name)
        data = self.query_table_filter(**filter_dict)
        return data

    def check_table_columns(self, df=None, table_name: Optional[str | None] = None):
        if (table_name is None) or (df is None):
            raise 'table_name and/or df must be defined and cannot be None'
        if table_name not in self.db_config['tables'].keys():
            raise 'table_name not in database or update algaestat for latest config'
        col_types = self.db_config['tables'][table_name]['column_types']
        col_list = list(col_types.keys())
        print('missing:', list(set(col_list) - set(list(df.columns))))
        print('extra', list(set(df.columns) - set(col_list)))
        df_types = df.dtypes.astype(str).to_dict()
        mistmatched_columns = []
        for k, v_type in df_types.items():
            if k in col_types.keys():
                v_compare = col_types[k]
                if v_compare.upper() in v_type.upper():
                    continue
                if v_compare.startswith("%Y-%m-%d") and v_type.startswith('datetime'):
                    continue
                if ('float' in v_compare) and ('int' in v_type):
                    continue
                if (v_compare == 'str') and (v_type == 'object'):
                    continue
                mistmatched_columns.append(k)
        if len(mistmatched_columns) > 0:
            print('Mismatched columns:')
            for k in mistmatched_columns:
                print('Column: {0}; DF type: {1}; Expected Type: {2}'.format(k, df_types[k], col_types[k]))
        return

    def upload_table(self, df=None,
                     table_name: Optional[str | None] = None,
                     rows_per_batch: Optional[int] = 25,
                     wait_per_batch: Optional[int] = 2,
                     line_start=0):
        """
        :param df: pd.DataFrame to upload, first check to ensure columns are correctly named with QueryDB.check_columns
        :param table_name: the table name you are uploading
        :param rows_per_batch: throttle your upload to avoid timing out the database, and charged more/query.
        :param wait_per_batch: throttle your upload to avoid timing out the database, and charged more/query.
        :return:
        This will upload all the data in the DataFrame.
        If the identifier key andor index/range name is missing it will error.
        This does not check if the data already exists and will save over data with an exact match to the identifier
        key and index
        """
        if (table_name is None) or (df is None):
            raise 'table_name and/or df must be defined and cannot be None'

        table = self.db_resource.Table(table_name)
        i = 0
        dict_list = []
        # type the Time columns, correctly with pandas
        if ('Timestamp' in df.columns) and ('LocalTime' in df.columns):
            df['Timestamp'] = df['Timestamp'].astype(str)
            df['LocalTime'] = df['LocalTime'].astype(str)
        else:
            raise 'missing columns Timestamp and/or LocalTime'
        df.drop_duplicates(subset=['PondID', 'Timestamp'], keep='last', inplace=True)
        for index, row in df.iterrows():
            i += 1
            if i < line_start:
                continue
            row_no_na = row.dropna()
            data_dict = row_no_na.to_dict()
            data_dict = {
                key: round(data_dict[key], 3) if (type(data_dict[key]) == int or type(data_dict[key]) == float) else
                data_dict[key] for key in data_dict}

            data_dict = json.loads(json.dumps(data_dict,
                                              indent=4,
                                              sort_keys=True,
                                              use_decimal=True),
                                   use_decimal=True)
            s = json.dumps(data_dict,
                           indent=4,
                           sort_keys=True,
                           use_decimal=True)

            dict_list.append(data_dict)
            if i % rows_per_batch == 0:
                with table.batch_writer() as batch:
                    batch._flush = types.MethodType(_flush, batch)
                    for data_dict in dict_list:
                        batch.put_item(
                            Item=data_dict
                        )
                print(i, batch._response)
                dict_list = []
                time.sleep(wait_per_batch)
        if len(dict_list) > 0:
            with table.batch_writer() as batch:
                batch._flush = types.MethodType(_flush, batch)
                for data_dict in dict_list:
                    batch.put_item(
                        Item=data_dict
                    )
            print(batch._response)
        return


def get_tableinfo(table_name: str, identifier_name: Optional[str | None] = None, q=None):
    ti_dict = q.db_config['tables'][table_name].copy()
    if identifier_name is None:
        ti_dict['identifier_name'] = ti_dict['identifier_name_list'][0]
    else:
        ti_dict['identifier_name'] = identifier_name
    for k in ['identifier_name_list', 'column_types', 'rows_per_batch', 'wait_per_batch']:
        if k in ti_dict.keys():
            del ti_dict[k]
    return ti_dict


def get_write_tableinfo(table_name: str, identifier_name: Optional[str | None] = None, q=None):
    ti_dict = q.db_config['tables'][table_name].copy()
    ti_write = {}
    for k in ['table_name', 'rows_per_batch', 'wait_per_batch']:
        ti_write[k] = ti_dict[k]

    return ti_write
