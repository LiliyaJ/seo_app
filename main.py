# from flask import Flask, request, make_response
# from webserver import app
# import requests
# import json
# import os
# import pandas as pd
# from data.client import RestClient
# from google.oauth2 import service_account
# import google.auth
# from googleapiclient.discovery import build
# from google.cloud import bigquery
# from helper import get_data_from_gs, fetch_historical_search_volume, extract_search_volume_rows, upload_rows_to_sheet, upload_search_volume_bigquery


# ### for local debugging
# #Authentication with service account for bigquery
# # credentials = service_account.Credentials.from_service_account_file(
# #      'bq_service_account.json', scopes=[
# #          "https://www.googleapis.com/auth/drive",
# #          "https://www.googleapis.com/auth/cloud-platform"],
# #  )

# ##
# ## for cloud functions or cloud run deployment
# ##Authentication with service account for bigquery
# scopes = [
#     "https://www.googleapis.com/auth/drive",            # Full access to Drive files (read/write)
#     "https://www.googleapis.com/auth/spreadsheets",     # Required for reading and writing Sheets
#     "https://www.googleapis.com/auth/cloud-platform"    # Needed for BigQuery, etc.
# ]
# credentials, _ = google.auth.default(scopes = scopes)
# ##

# spreadsheet_id = os.environ['spreadsheet_id']
# project_id = os.environ['project_id']
# dataset_id = os.environ['dataset_id']
# table_id = os.environ['table_id']

# DFS_LOGIN = os.environ['DFS_LOGIN']
# DFS_KEY = os.environ['DFS_KEY']

# client = RestClient(DFS_LOGIN, DFS_KEY)
# bq_client = bigquery.Client(credentials=credentials, project=project_id)
# service = build('sheets', 'v4', credentials=credentials)

# # Flask setup
# app = Flask(__name__)

# @app.route("/", methods=["POST"])
# def handle_request():
#     gs_data = get_data_from_gs(spreadsheet_id, service)
#     make_api_call = fetch_historical_search_volume(gs_data, client)
#     api_response = extract_search_volume_rows(make_api_call)
#     upload_rows_to_sheet(service, spreadsheet_id, 'output!A1', api_response)
#     upload_search_volume_bigquery(api_response, bq_client, dataset_id, table_id)
#     return make_response(json.dumps({'result': 'Successfully uploaded the data'}), 200)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host="0.0.0.0", port=port)

from flask import Flask
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
    return "✅ Flask is running in Cloud Run", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
