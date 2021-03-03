import tkinter as tk

Barcode = False
BarcodeString = []

def GetKeyBoard(key):
    global Barcode
    global BarcodeString
    if key== Key.space:
        Barcode = True
    elif key != Key.space and key != Key.enter and key != Key.shift and Barcode==True:
        BarcodeString.append(key)
    elif key == Key.enter:
        Barcode = False
        string=""
        for digit in BarcodeString:
            string = string+str(digit)[1:2]
        BarcodeString=[]
        print(string)

class App(tk.Tk): 
    def __init__(self): 
        super().__init__() 
        entry = tk.Entry(self) 
        entry.bind("<FocusIn>", self.print_type)  
        entry.bind("<Key>", self.print_key) 
        entry.pack(padx=20, pady=20)
 
    def print_type(self, event): 
        print(event.type) 
 
    def print_key(self, event): 
        args = event.keysym, event.keycode, event.char 
        print("Symbol: {}, Code: {}, Char: {}".format(*args)) 
 
if __name__ == "__main__": 
    app = App() 
    app.mainloop() 


