import PIL 
from PIL import ImageTk,Image
import tkinter as tk
import random
import json

   
root=tk.Tk() 
alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9"
alphanumeric = alphabet.split(" ")
# setting the windows size 
root.geometry("400x300") 

name=tk.StringVar() 
nickname=tk.StringVar()
location=tk.StringVar()
enumeration=tk.StringVar()
repetition=tk.StringVar()

labellist=[]
InstrumentPath = open("Instruments.json")
InstrumentDict = json.load(InstrumentPath)
InstrumentPath.close()
usedcodes = list(InstrumentDict.values())

def GenRandomString():
    usedletters=[]
    randomstring=""
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
    return randomstring


class label:
    def __init__(self, name, nickname, location, code):
        self.name=name
        self.nickname=nickname
        self.location=location
        self.code=code
        print([name, nickname, location, code])
        
        
def generate():
    if name.get() == "" or location.get() == "":
        return
    #check character overage
    #check if name is unique
    nicknamestr = ""
    noenum = True
    if nickname.get() == "":
        nicknamestr = name.get()
    else:
        nicknamestr = nickname.get()
    if enumeration.get() != "":
        twonums = enumeration.get().split('-')
        noenum=False
    else:
        noenum = True
        twonums = [1, 1]
    lastnickname = nicknamestr
    repeat = repetition.get()
    if repeat == "":
        repeat = 1
    else:
        repeat = int(repeat)
    for x in range(int(twonums[0]), int(twonums[1])+1):
        randomcode = GenRandomString()
        nicknamestr = lastnickname
        instname = ""
        if noenum:
            instname=name.get()
        else:
            instname = name.get() + " " + str(x)
            nicknamestr = nicknamestr + " " + str(x)
        for y in range(repeat):
            labellist.append(label(instname, nicknamestr, location.get(), randomcode))
        
    return
 
def printlabel():
    return
      
qrpreview = tk.Canvas(root, width = 175, height = 175)
name_label = tk.Label(root, text = 'Name', 
                      font=('calibre', 
                            10, 'bold')) 

name_entry = tk.Entry(root, textvariable = name,font=('calibre',10,'normal')) 
   

nickname_label = tk.Label(root, 
                       text = 'Nickname', 
                       font = ('calibre',10,'bold')) 
   
nickname_entry = tk.Entry(root, 
                       textvariable = nickname, 
                       font = ('calibre',10,'normal'))

location_label = tk.Label(root, 
                       text = 'Location', 
                       font = ('calibre',10,'bold')) 
   
location_entry=tk.Entry(root, 
                     textvariable = location, 
                     font = ('calibre',10,'normal'))

enumeration_label = tk.Label(root, 
                       text = 'Enumeration', 
                       font = ('calibre',10,'bold')) 
   
enumeration_entry=tk.Entry(root, 
                     textvariable = enumeration, 
                     font = ('calibre',10,'normal'))

repetition_label = tk.Label(root, 
                       text = 'Repetition', 
                       font = ('calibre',10,'bold')) 
   
repetition_entry=tk.Entry(root, 
                     textvariable = repetition, 
                     font = ('calibre',10,'normal')) 
   
 
generate_btn=tk.Button(root,text = 'Generate', 
                  command = generate)
print_btn=tk.Button(root,text = 'Print', 
                  command = printlabel) 
   
# placing the label and entry in 
# the required position using grid 
# method 
name_label.grid(row=1,column=0) 
name_entry.grid(row=1,column=1) 
nickname_label.grid(row=2,column=0) 
nickname_entry.grid(row=2,column=1)
location_label.grid(row=3,column=0) 
location_entry.grid(row=3,column=1)
enumeration_label.grid(row=4,column=0) 
enumeration_entry.grid(row=4,column=1)
repetition_label.grid(row=5,column=0) 
repetition_entry.grid(row=5,column=1)
qrpreview.grid(row=0, column=0)
generate_btn.grid(row=0,column= 1) 
print_btn.grid(row=0, column=2)

img = ImageTk.PhotoImage(Image.open("ursc.jpg"))
qrpreview.create_image(100, 100, image=img)
root.mainloop()
