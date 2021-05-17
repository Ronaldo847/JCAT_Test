# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 22:04:26 2021

@author: Cris Gino Mesias
"""

import pyautogui as pag
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import time
import os
from datetime import date
import sys
import subprocess 

if date.today() >= date(2022,1,1):
    pag.alert(title="FATAL ERROR",text="Please contact JCAT_DEV."
              ,timeout=5000,iconbitmap='JCATi.ico')
    sys.exit()
else:
    #Core Function Set-up
    #Clipboard Function
    def addToClipBoard(text):
        command = 'echo ' + text.strip() + '| clip'
        os.system(command)
        
    #Image Look-up function
    def SearchUI(image_link):
        loc = pag.locateOnScreen(image_link)
        while True:
            if loc != None:
                break
            else:
                loc = pag.locateOnScreen(image_link)
                time.sleep(0.50)
    
    #Inverse Image Look-up function
    def InvSearchUI(image_link):
        loc = pag.locateOnScreen(image_link)
        while True:
            if loc == None:
                break
            else:
                loc = pag.locateOnScreen(image_link)
                time.sleep(0.50)

    #Main Program Window
    root = tk.Tk()
    root.title("JBH Commit Automation Tool")
    root.iconbitmap('JCATi.ico')
        
    def browseFiles():
        global location
        location = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select CSV File",
                                              filetypes = (("CSV files",
                                                            "*.csv*"),
                                                           ("all files",
                                                            "*.*")))
        loc_entry.delete(0, tk.END)
        loc_entry.insert(0, location)
    
    def proceed():
        global location
        location = str(loc_entry.get()).replace('"','')
        time.sleep(1)
        root.destroy()
            
    def QuitSession():
        response = tk.messagebox.askokcancel("JCAT Quit Confirmation",
                                             "Are you sure you want to quit?")
        if response == 1:
            root.destroy()
            time.sleep(0.50)
            sys.exit()
        else:
            root.mainloop()
    
    #Outer Frame
    out_frame = tk.LabelFrame(root, text = "JCAT v0.1" , padx =10, pady =10)
    out_frame.pack(padx=10, pady=10)
    
    #Browse File Frame
    bf_frame = tk.LabelFrame(out_frame, padx=10, pady=10)
    bf_frame.pack()
    
    label = tk.Label(bf_frame,
                    text = "Locate CSV File Path:").grid(
                        row=0,column=0,sticky='W', pady =5)
    
    loc_entry = tk.Entry(bf_frame,
                    width=100)
    loc_entry.insert(0,r"C:\Users\...")
        
    button_browse = tk.Button(bf_frame,
                            text = "Browse Files",
                            command = browseFiles,
                            width = 15)
    
    #Out Frame Buttons
    button_proceed = tk.Button(out_frame,
                               text = "Proceed",
                               command = proceed,
                               width = 15)
                    
    button_exit = tk.Button(out_frame,
                            text = "Quit Program",
                            command = QuitSession,
                            width = 15)
    
    #Shutdown Option
    turnoff = tk.IntVar()
    close = tk.Checkbutton(out_frame, 
                           text = "Shutdown PC when done",
                           variable=turnoff,
                           onvalue = 1, offvalue = 0)
    
    loc_entry.grid(row=1,column=0,columnspan=3)               
    button_browse.grid(row=2,column=2,sticky='E',pady=5)
    button_proceed.pack(pady=5, padx=11, anchor='e')
    close.pack(pady=5, padx=8, anchor='e')
    button_exit.pack()
    
    root.protocol("WM_DELETE_WINDOW", QuitSession)              
    root.mainloop()
    
    shutdownPC = turnoff.get()
        
    #Opening File Explorer
    subprocess.Popen('explorer.exe')
    time.sleep(3)
    pag.hotkey('win','right')
    
    #CSV to Pandas Dataframe
    df = pd.read_csv(location.replace('"',''))
    df['Status'] = ''
    df['Elapsed Time'] = ''
    spl = location.split(sep='.')
    newfile = (spl[0].replace('"',"")).replace("'","") + '_REPORT.csv'
    
    #Global Timer
    gstart = time.time()
    
    #Program Main Loop
    for i in range(len(df)):
        #Proceed Alert
        resp = pag.confirm(title="Loop Status", 
                           text="Do you want to proceed with the loop? \n"
                           "(Press 'Cancel' to break loop at current item)"
                           ,timeout = 5000, icon='JCATi.ico', _tkinter=True)
        
        if resp == 'Cancel':
            df['Status'][i] = 'User Interrupt!'
            df['Elapsed Time'][i] = 'N/A'
            df.to_csv(newfile)
            break
        
        else:   
            #Local Timer
            lstart = time.time()
        
            #To File Folder
            addToClipBoard(df['Commit Folder Link'][i])
            pag.click(1480,165)
            time.sleep(0.50)
            pag.click(1480,165)
            pag.hotkey('ctrl','a')
            pag.hotkey('ctrl', 'v')
            pag.press('enter')
        
            #Opening JBH File
            pag.click(1260,230)
            time.sleep(0.50)
            pag.click(1260,230)
            pag.press('enter')
            SearchUI('Project.png')
            time.sleep(2)
            pag.hotkey('win','up')
            time.sleep(2)
        
            #Commit Step
            pag.click(320,35) #Database Ribbon
            time.sleep(0.50)
            pag.click(345,240) #Commit Option
            time.sleep(0.50)
            pag.hotkey('win','up')
            time.sleep(0.25)
            SearchUI('CommitButton.png')
            
            #Commit Button
            pag.click(pag.center(pag.locateOnScreen('CommitButton.png'))) 
            time.sleep(0.25)
            pag.hotkey('win','up')
            SearchUI('Yes Button.png')
            pag.click(pag.center(pag.locateOnScreen('Yes Button.png')))
            pag.press('tab') #Commit Message
            Message = str(df['Node'][i]) + '_Commit'
            pag.write(Message)
            pag.click(1150,550) #Commit
            time.sleep(2)
        
            #Custom Stream Fatal Error Check
            pls = pag.locateOnScreen('PleaseWait.png')
            err = pag.locateOnScreen('ErrorOK.png')
            
            while True:
                if (pls == None or err != None):
                    break
                else:
                   pls = pag.locateOnScreen('PleaseWait.png')
                   err = pag.locateOnScreen('ErrorOK.png')
                   pag.moveTo(1500,900,tween=pag.easeOutQuad)
                   time.sleep(0.50)
                   pag.moveTo(1500,100,tween=pag.easeOutQuad)
                   time.sleep(1)
            if err != None:
                time.sleep(1)
                pag.click(pag.center(pag.locateOnScreen('ErrorOK.png')))
                time.sleep(1)
                pag.hotkey('alt','f4')
                time.sleep(0.50)
                pag.press('enter')
                df['Status'][i] = 'Commit Error!'
                lend = time.time()
                df['Elapsed Time'][i] = lend - lstart
                df.to_csv(newfile)
                continue
            else:
                Completion = Message + ' Complete!'
                pag.alert(title="Commit Status",
                          text=str(Completion),timeout=1000)
                time.sleep(2)
            
            #JBH HFD Generator
            pag.click(22,44)
            time.sleep(0.25)
            pag.click(65,260)
            SearchUI('Organize.png')
            pag.hotkey('alt','d')
            pag.hotkey('ctrl','v')
            pag.press('enter')
            time.sleep(0.50)
            pag.click(1550,940)
            pag.press('delete')
            HFDTag = str(df['Node'][i]) + ' - HFD_Commited'
            pag.write(HFDTag)
            pag.press('enter')
            SearchUI('Create.png')
            pag.hotkey('win','up')
            time.sleep(0.5)
            pag.click(1900,5)
            
            #JBH Close
            pag.click(1900,5)
            time.sleep(1)
            pag.click(1900,5)
            pag.press('enter')
            time.sleep(1)
            lend = time.time()
            df['Status'][i] = 'Done'
            df['Elapsed Time'][i] = lend - lstart
            pag.alert(text="JBH HFD Generated!",title="HFD Generation",
                      timeout=2000)
            df.to_csv(newfile)
 
    #Completion Message
    gend = time.time()
    totelapse = gend - gstart
    promptf = "Batch Commit Completed! \nElapsed Time: " + str(totelapse)
    pag.alert(title="Commit Status", text=promptf,
              timeout=2000)
    
    if shutdownPC == 1:
        os.system("shutdown /s /t 10")
    else:
        pass
