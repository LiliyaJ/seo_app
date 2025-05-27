from flask import Flask, request, make_response
import os
import json
import traceback
import google.auth
from googleapiclient.discovery import build
from google.cloud import bigquery
from data.client import RestClient
from helper import (
    get_data_from_gs,
    fetch_historical_search_volume,
    extract_search_volume_rows,
    upload_rows_to_sheet,
    upload_search_volume_bigquery
)

app = Flask(__name__)


try:
    scopes = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/cloud-platform"
    ]
    credentials, _ = google.auth.default(scopes=scopes)

    spreadsheet_id = os.environ["spreadsheet_id"]
    project_id = os.environ["project_id"]
    dataset_id = os.environ["dataset_id"]
    table_id = os.environ["table_id"]
    DFS_LOGIN = os.environ["DFS_LOGIN"]
    DFS_KEY = os.environ["DFS_KEY"]

    client = RestClient(DFS_LOGIN, DFS_KEY)
    bq_client = bigquery.Client(credentials=credentials, project=project_id)
    service = build("sheets", "v4", credentials=credentials)

except Exception as e:
    print("Startup error:", e)
    traceback.print_exc()

@app.route("/", methods=["POST"])
def handle_request():
    try:
        gs_data = get_data_from_gs(spreadsheet_id, service)
        make_api_call = fetch_historical_search_volume(gs_data, client)
        api_response = extract_search_volume_rows(make_api_call)
        upload_rows_to_sheet(service, spreadsheet_id, "output!A1", api_response)
        upload_search_volume_bigquery(api_response, bq_client, dataset_id, table_id)

        return make_response(json.dumps({"result": "Successfully uploaded the data"}), 200)

    except Exception as e:
        print("Error in request:", e)
        traceback.print_exc()
        return make_response(json.dumps({"error": str(e)}), 500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
