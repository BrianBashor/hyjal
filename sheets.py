import re
import json
import time
import urllib.request
import urllib.parse

from player import Player
from blizzard import Blizzard
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from googleapiclient import discovery


scope = ["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/drive.readonly","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name('cred/hvfd_cred.json', scope)
client = gspread.authorize(creds)

sheet = client.open('HVFD').sheet1

hvfd = sheet.get_all_records()[0][0]

# print(sheet.spreadsheet)
pprint(hvfd)





