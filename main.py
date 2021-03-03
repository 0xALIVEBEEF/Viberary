import pygame
import time
import json
import os


def configLabels(L1,L2):
    text1 = font.render(L1, True, (0, 0, 0))
    text2 = font.render(L2, True, (0, 0, 0))
    screen.fill((255, 255, 255))
    screen.blit(text1, ((screenheight/2) -text1.get_width() // 2, ((screenwidth/2) - text1.get_height() // 2) - 100))
    screen.blit(text2, ((screenheight/2) -text2.get_width() // 2, (screenwidth/2) - text2.get_height() // 2))
    pygame.display.update()
    pygame.time.set_timer(pygame.USEREVENT, (ConfigData["employee_timeout"])*1000)
    
    
Barcode = False
BarcodeString = []

def GetKeyBoard(key):
    global Barcode
    global BarcodeString
    if key== "space":
        Barcode = True
    elif key != "space" and key != "return" and key != "left shift" and key != "right shift" and Barcode==True:
        BarcodeString.append(key)
    elif key == "return" and Barcode:
        Barcode = False
        string=""
        for digit in BarcodeString:
            string = string+str(digit)
        BarcodeString=[]
        CheckInOut(string)

def GetSerial():
    string=""
    RFID = True
    if ser.inWaiting():
        time.sleep(0.1)  # let buffer load
        while ser.inWaiting():
            char = ser.read()
            if char != b'\x02' and char != b'\r' and char != b'\n' and char != b'\x03':
                newchar = str(char)
                newchar = newchar[2:3]
                string += newchar
            if RFID and char == b'\x03':
                return string
    else:
        return

JSONFrequencyCounter = 0
def WebWrite(checkInOut, Item, Employee, Location):
    global JSONFrequencyCounter
    StampedTime = TimeStamp()
    if checkInOut:
        checkInOut="Checked In"
        configLabels("Successfully checked in", Item)
        time.sleep(1)
        configLabels(Item, "Goes " + Location)
    else:
        checkInOut="Checked Out"
        configLabels("You checked out", Item + "!")
    print(checkInOut + ", " + Item + ", " + Employee + ", " + StampedTime)
    if ConfigData["write_to_local_csv"]:
        WriteCSV(checkInOut, Item, Employee, StampedTime)
    if ConfigData["write_to_google_docs"]:
        WriteGoogle(checkInOut, Item, Employee, StampedTime)
        WriteGoogleStatus()
    if ConfigData["write_to_microsoft"]:
        WriteMicrosoft(checkInOut, Item, Employee, StampedTime)
    if ConfigData["write_to_JSON"]:
        if JSONFrequencyCounter == ConfigData["json_write_frequency"]:
            WriteJSON()
            JSONFrequencyCounter = 0
        else:
            JSONFrequencyCounter = JSONFrequencyCounter + 1
    eval(ConfigData["easter_egg"])
    return

def LogOutMessage():
    StampedTime = TimeStamp()
    if ConfigData["write_to_local_csv"]:
        WriteCSV("Viberary terminated","","", StampedTime)
    if ConfigData["write_to_google_docs"]:
        WriteGoogle("Viberary terminated","","", StampedTime)
    if ConfigData["write_to_microsoft"]:
        WriteMicrosoft("Viberary terminated","","", StampedTime)
    if ConfigData["write_to_JSON_at_termination"]:
        WriteJSON()
    return


def WriteJSON():
    try:
        path = open("Instruments.json", "w")
    except:
        path = open("/media/pi/VIBERARY/Viberary/Instruments.json", "w")
    json.dump(InstrumentDict, path)
    path.close()
    return

def TimeStamp():
    return time.strftime("%b %d %Y %r", time.localtime())


def WriteCSV(Val1, Val2, Val3, Val4):
    try:
        log = open("log.csv", "a")
    except:
        log = open("/media/pi/VIBERARY/Viberary/log.csv", "a")
    log.write(Val1 + "," + Val2 + "," + Val3 + "," + Val4 + "\r\n")
    log.close()
    return


def WriteGoogle(Val1, Val2, Val3, Val4):
    values = [[Val1, Val2, Val3, Val4]]
    DATA_LOCATION = "A1"
    VLSSID = ''
    VLsheet.values().append(spreadsheetId=VLSSID, valueInputOption='RAW', range=DATA_LOCATION, body={'values': values}).execute()
    return

def WriteGoogleStatus():
    result = VIsheet.values().get(spreadsheetId='', range="A2:C" + str(int(ConfigData["Number_of_instruments"])+1)).execute()
    values = result.get('values', [])
    NameLookup = {}
    keys = list(InstrumentDict.keys())
    for key in keys:
        Info = InstrumentDict[key]
        NameLookup[Info["name"]] = [Info["status"], Info["time"]]
    Modvalues=[]
    for row in values:
        Modrow = [0,0,0]
        LookedUp = NameLookup[row[0]]
        Modrow[0] = row[0]
        Modrow[1] = LookedUp[0]
        Modrow[2] = LookedUp[1]
        Modvalues.append(Modrow)
    VISSID = ''
    VIsheet.values().update(spreadsheetId=VISSID, range='A2', valueInputOption='RAW', body={'values':Modvalues}).execute()
    return
def GetGoogleData():
    result = VIsheet.values().get(spreadsheetId='', range="A2:C" + str(int(ConfigData["Number_of_instruments"])+1)).execute()
    values = result.get('values', [])
    keys = list(InstrumentDict.keys())
    ReverseDict={}
    for key in keys:
        name = InstrumentDict[key]["name"]
        ReverseDict[name]=key
    for row in values:
        key_ = ReverseDict[row[0]]
        Info = InstrumentDict[key_]
        Info["status"] = row[1]
        Info["time"] = row[2]
    return
def WriteMicrosoft(Val1, Val2, Val3, Val4):

    return

musiclist = []
def PlayMusic(file):
    import random
    global musiclist
    if file == "stop":
        pygame.mixer.music.stop()
        return
    randomness = False
    notsystemd = os.path.exists(file)
    path0 = ""
    if notsystemd:
        path0 = file
    else:
        path0 = "/media/pi/VIBERARY/Viberary" + file
    if os.path.isdir(path0):
        randomness = True
        for entry in os.scandir(path0):
            if entry.path.endswith(".ogg") and entry.is_file():
                musiclist.append(entry.path)
    pygame.mixer.music.set_volume(ConfigData["music_volume"])
    if randomness:
        music = musiclist[random.randint(0,len(musiclist)-1)]
    else:
        music = file
    try:
        pygame.mixer.music.load(music)
    except:
        pygame.mixer.music.load("/media/pi/VIBERARY/Viberary/" + music)
    pygame.mixer.music.play(loops=-1)
    return

def PlaySound(file):
    if file != "none":
        try:
            sound = pygame.mixer.Sound(file)
        except:
            sound = pygame.mixer.Sound("/media/pi/VIBERARY/Viberary/" + file)
        sound.play()

EmployeeInfo={}
Inst = ""
Employee = ""
def CheckInOut(code):
    global EmployeeInfo
    global Employee
    global Inst
    global imageindex
    global imagelist
    if code in EmployeeDict:
        EmployeeInfo = EmployeeDict[code]
        Employee = EmployeeInfo["name"]
        if Employee == "End Session":
            img = pygame.image.load(imagelist[imageindex])
            img = pygame.transform.scale(img, (ConfigData["window_height"], ConfigData["window_width"]))
            screen.blit(img, ((screenheight / 2) - ConfigData["window_height"] // 2, (screenwidth / 2) - ConfigData["window_width"] // 2))
            imageindex = imageindex + 1
            if imageindex > (len(imagelist) - 1):
                imageindex = 0
            Employee=""
            PlayMusic("stop")
            GetGoogleData()
        elif Employee == "Shutdown":
            LogOutMessage()
            from subprocess import call
            call("sudo shutdown -poweroff")
            quit()
        else:
            configLabels("Welcome, " + Employee, "Scan an instrument")
            if ConfigData["enable_music"]:
                PlayMusic(EmployeeInfo["music"])
    elif (code in InstrumentDict) and not Employee == "":
        InstInfo = InstrumentDict[code]
        if InstInfo["nickname"] == "same":
            Inst = InstInfo["name"]
        else:
            Inst = InstInfo["nickname"]
        if InstInfo["status"] == "Equipment Room":
            InstInfo["status"] = Employee
            InstInfo["time"] = TimeStamp()
            PlaySound(EmployeeInfo["OutSound"])
            WebWrite(False, Inst, Employee, InstInfo["place"])
        elif InstInfo["status"] != "Equipment Room":
            InstInfo["status"] = "Equipment Room"
            InstInfo["time"] = TimeStamp()
            PlaySound(EmployeeInfo["InSound"])
            WebWrite(True, Inst, Employee, InstInfo["place"])
    elif (code in InstrumentDict) and Employee == "":
        configLabels("That was an instrument ID", "Please scan your employee ID first")
    elif (code not in InstrumentDict) and (code not in EmployeeDict):
        configLabels("Unknown ID: " + code,  "Please scan again")
    else:
        configLabels("Unknown Error", "Please contact FYES")
    return

try:
    EmployeePath = open("Employees.json", "r")
    InstrumentPath = open("Instruments.json", "r")
    ConfigPath = open("Config.json", "r")
except:
    EmployeePath = open("/media/pi/VIBERARY/Viberary/Employees.json", "r")
    InstrumentPath = open("/media/pi/VIBERARY/Viberary/Instruments.json", "r")
    ConfigPath = open("/media/pi/VIBERARY/Viberary/Config.json", "r")

EmployeeDict = json.load(EmployeePath)
InstrumentDict = json.load(InstrumentPath)
ConfigData = json.load(ConfigPath)

EmployeePath.close()
InstrumentPath.close()
ConfigPath.close()

screenheight = ConfigData["window_height"]
screenwidth = ConfigData["window_width"]
if ConfigData["enable_serial"]:
    import serial
    ser = serial.Serial(

        port=ConfigData["serial_port"],
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screenheight,screenwidth), pygame.NOFRAME)
pygame.display.set_caption('Viberary')
font = pygame.font.SysFont("comicsansms", 72)
text1 = font.render("Viberary Loading", True, (0,0,0))
text2 = font.render("", True, (0,0,0))
screen.fill((255,255,255))
screen.blit(text1, ((screenheight/2) -text1.get_width() // 2, ((screenwidth/2) - text1.get_height() // 2)-100))
screen.blit(text2, ((screenheight/2) -text2.get_width() // 2, (screenwidth/2) - text2.get_height() // 2))
pygame.display.update()
    
if ConfigData["write_to_google_docs"]:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    import os

    VLJSONfull = '' #full path of google sheets secret json for "instruments" sheet
    VLJSONsmall = '' #name of google sheets secret json for "instruments" sheet

    scopes = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
    notsystemd = os.path.exists(VLJSONsmall)
    path = ""
    if notsystemd:
        path = VLJSONsmall
    else:
        path = VLJSONfull
    while True:
        try:
            creds = Credentials.from_service_account_file(path, scopes=scopes)
        except:
            continue
        else:
            break
    VLsheet = build('sheets', 'v4', credentials=creds).spreadsheets()

    VIJSONfull = '' #full path of google sheets secret json for "instruments" sheet
    VIJSONsmall = '' #name of google sheets secret json for "instruments" sheet


    notsystemd = os.path.exists(VIJSONsmall)
    path = ""
    if notsystemd:
        path = VIJSONsmall
    else:
        path = VIJSONfull
    while True:
        try:
            creds = Credentials.from_service_account_file(path, scopes=scopes)
        except:
            continue
        else:
            break
    VIsheet = build('sheets', 'v4', credentials=creds).spreadsheets()

imagelist = []
fullimagespath = '/media/pi/VIBERARY/Viberary/Images'
smallimagespath = '/Images'

notsystemd = os.path.exists(smallimagespath)
path_ = ""
if notsystemd:
    path_ = smallimagespath
else:
    path_ = fullimagespath
for entry in os.scandir(path_):
    if (entry.path.endswith(".jpg")
            or entry.path.endswith(".png")) and entry.is_file():
        imagelist.append(entry.path)
screensaver = True
imageindex=0
prevTime = time.time()
img = pygame.image.load(imagelist[imageindex])
img = pygame.transform.scale(img, (ConfigData["window_height"], ConfigData["window_width"]))
screen.blit(img, ((screenheight / 2) - ConfigData["window_height"] // 2, (screenwidth / 2) - ConfigData["window_width"] // 2))
pygame.time.set_timer(pygame.USEREVENT, (ConfigData["employee_timeout"]) * 1000)
if ConfigData["write_to_google_docs"]:
    GetGoogleData()

if ConfigData["write_to_JSON"]:
    WriteJSON()
prevtime=time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            LogOutMessage()
            quit()
        if event.type == pygame.KEYDOWN:
            GetKeyBoard(pygame.key.name(event.key))
        if event.type == pygame.USEREVENT:
            img = pygame.image.load(imagelist[imageindex])
            img = pygame.transform.scale(img, (ConfigData["window_height"], ConfigData["window_width"]))
            screen.blit(img, ((screenheight / 2) - ConfigData["window_height"] // 2, (screenwidth / 2) - ConfigData["window_width"] // 2))
            imageindex = imageindex+1
            if imageindex > (len(imagelist)-1):
                imageindex = 0
            pygame.time.set_timer(pygame.USEREVENT, (ConfigData["employee_timeout"]) * 1000)
            Employee = ""
            PlayMusic("stop")
            if ConfigData["write_to_google_docs"]:
                GetGoogleData()
            if ConfigData["write_to_JSON"]:
                WriteJSON()
    if ConfigData["enable_serial"]:
        RFID = GetSerial()
        if RFID is not None:
            CheckInOut(RFID)
    if time.time()-prevtime > ConfigData['mixer_reinit_time']:
        pygame.mixer.init()
        prevtime=time.time()
    pygame.display.update()
