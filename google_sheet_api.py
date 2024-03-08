from googleapiclient.discovery import build

class GoogleSheetApi:
    def __init__(self, api_key: str):
        self.sheet_connection = build('sheets', 'v4', developerKey=api_key).spreadsheets()
    
    def request(self, spreadsheet_id: str, sheet_name: str, range_start: str, range_end: str) -> list:
        range_name = f'{sheet_name}!{range_start}:{range_end}'
        result = self.sheet_connection.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values
                