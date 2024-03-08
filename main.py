from google_sheet_api import GoogleSheetApi
import os
from dotenv import load_dotenv, find_dotenv


if __name__ == '__main__':
    
    load_dotenv(find_dotenv())
    API_KEY = os.environ.get("API_KEY")
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
    
    gs_api = GoogleSheetApi(API_KEY)
    res = gs_api.request(SPREADSHEET_ID, "Requested", "A1", "H215")
    print(res)