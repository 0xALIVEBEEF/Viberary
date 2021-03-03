import qrcode
import sys
import random
import json
InstrumentPath = open("Instruments.json")
InstrumentDict = json.load(InstrumentPath)
InstrumentPath.close()
usedcodes = list(InstrumentDict.values())
alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9"
alphanumeric = alphabet.split(" ")
codes = []
autowrite = True #sys.argv[2]
numcodes = 1 #sys.argv[1]
if autowrite:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    scopes = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
    VIJSON = '' #name of google sheets secret json for "instruments" sheet
    while True:
        try:
            creds = Credentials.from_service_account_file(VIJSON, scopes=scopes)
        except:
            continue
        else:
            break
    VIsheet = build('sheets', 'v4', credentials=creds).spreadsheets()
for i in range(int(numcodes)):
    usedletters = []
    randomstring = ""
    for b in range(4):
        char = str(alphanumeric[random.randint(0,len(alphanumeric)-1)])
        while char in usedletters:
            char = str(alphanumeric[random.randint(0,len(alphanumeric)-1)])
        randomstring = randomstring + char
        usedletters.append(char)
    while (randomstring in usedcodes):
        for b in range(4):
            char = str(alphanumeric[random.randint(0,len(alphanumeric)-1)])
            while char in usedletters:
                char = str(alphanumeric[random.randint(0,len(alphanumeric)-1)])
            randomstring = randomstring + char
            usedletters.append(char)
    usedcodes.append(randomstring)
    if autowrite:
        print(", \r\n "+'"'+randomstring+'"'+': {"place": "on shelf ", "name":"", "nickname":"", "status": "Equipment Room", "time": "?"}', end = '')
        values = [["", "Equipment Room", "?"]]
        DATA_LOCATION = "A1"
        VISSID = ''
        #VIsheet.values().append(spreadsheetId=VISSID, valueInputOption='RAW', range=DATA_LOCATION, body={'values': values}).execute()
        with open("Instruments.json", 'w') as file:
            InstrumentDict[randomstring] = {"place": "on shelf ?", "name":"", "nickname":"same", "status": "Equipment Room", "time": "?"}
            json.dump(InstrumentDict, file, indent = 4)
    img = qrcode.make(randomstring)
    out = img.resize((147,147), box = (40,40,250,250))
    out.save(randomstring+".jpg")
