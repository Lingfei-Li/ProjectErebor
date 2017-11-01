import boto3
import json
from config import app_config
from accountTransactionModel import Transaction
import time
from utils import Logger as log
import datetime


kinesis_client = boto3.client('kinesis', region_name='us-west-2')

stream_name = app_config['TransactionDataStreamName']

def describe_stream():
    response = kinesis_client.describe_stream(StreamName=stream_name)
    log.plain(response)


def put_transactions(transactions):
    log.info("Putting {} transactions to Kinesis stream".format(len(transactions)))
    if len(transactions) == 0:
        return

    records = []
    for t in transactions:
        records.append({
            'Data': json.dumps(t.getItem()),
            'PartitionKey': t.getField('UUID')
        })

    put_response = kinesis_client.put_records(StreamName=stream_name, Records=records)
    return put_response

# Testing: put a mock record to the kinesis stream
if __name__ == '__main__':
    uuid_base = int(datetime.datetime(2020, 8, 2).timestamp())
    uuid_base_time = int(time.time())
    t = int(datetime.datetime(2020, 8, 2).timestamp())
    transactions = []
    for i in range(10):
        trans = Transaction(TransactionDateSec=t, UUID='UUID-'+str(uuid_base+i), UserId='UserId-1234', AccountType='AccountType-checking',
                        Amount=1, BankName='chase', Description='Description-something',
                        TransactionType='TransactionType-debit')
        transactions.append(trans)
    put_response = put_transactions(transactions)
    if put_response['FailedRecordCount'] != 0:
       log.error( "Failed to put record to Kinesis. Message: " )
    else:
       log.success("Successfully put data to Kinesis")


