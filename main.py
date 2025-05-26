import requests
import json
import os
from data.client import RestClient
from google.oauth2 import service_account
import pandas as pd
from googleapiclient.discovery import build
from google.cloud import bigquery
from flask import make_response
from helper import get_data_from_gs, fetch_historical_search_volume, extract_search_volume_rows, upload_rows_to_sheet, upload_search_volume_bigquery


### for local debugging
#Authentication with service account for bigquery
credentials = service_account.Credentials.from_service_account_file(
     'bq_service_account.json', scopes=[
         "https://www.googleapis.com/auth/drive",
         "https://www.googleapis.com/auth/cloud-platform"],
 )

###
### for cloud functions or cloud run deployment
#Authentication with service account for bigquery
# scopes=[
#             "https://www.googleapis.com/auth/drive.readonly",
#             "https://www.googleapis.com/auth/spreadsheets",
#             "https://www.googleapis.com/auth/cloud-platform"]
# credentials, _ = google.auth.default(scopes = scopes)
###

spreadsheet_id = os.environ['spreadsheet_id']
project_id = os.environ['project_id']
dataset_id = os.environ['dataset_id']
table_id = os.environ['table_id']

DFS_LOGIN = os.environ['DFS_LOGIN']
DFS_KEY = os.environ['DFS_KEY']

client = RestClient(DFS_LOGIN, DFS_KEY)
bq_client = bigquery.Client(credentials=credentials, project=project_id)
service = build('sheets', 'v4', credentials=credentials)

def main(request):

    gs_data = get_data_from_gs (spreadsheet_id, build('sheets', 'v4', credentials=credentials))

    print(gs_data)

    make_api_call = fetch_historical_search_volume(gs_data, client)

    print (make_api_call)

    api_response = extract_search_volume_rows(make_api_call)

    print(api_response)

    upload_rows_to_sheet(service, spreadsheet_id, 'output!A1', api_response)

    upload_search_volume_bigquery(api_response, bq_client, dataset_id, table_id)

    return make_response(json.dumps({'result': 'Successfully uploaded the data'}))