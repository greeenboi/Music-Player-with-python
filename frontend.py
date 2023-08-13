# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 19:06:25 2023

@author: suvan
"""

import tkinter
import tkinter.messagebox
import customtkinter
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

try:
    cred = credentials.Certificate("./music-app-ffa78-firebase-adminsdk-kmam4-ad67931c2b.json")
    firebase_admin.initialize_app(cred)
    print("Database connected successfully")

except:
    print("Error in connecting to database")


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("purple")  # Themes: "blue" (standard), "green", "dark-blue"

db=firestore.client()
collection = db.collection('songlist')

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1), weight=1)
        
        self.grid_rowconfigure((1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)   
        
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.read)
        self.main_button_1.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        
      
        # create slider frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=3, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)     
        
        
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="nsew")   
        
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, orientation="vertical", command=self.changeVol)
        self.slider_2.grid(row=0, column=1, rowspan=3, padx=(10, 10), pady=(10, 10), sticky="ns")
        
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0,  padx=(20, 10), pady=(10, 10), sticky="ew")

        # set default values
             
           
        self.slider_2
        
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def read(self):
        docs = collection.stream()
        for doc in docs:
            print('{} => {} '.format(doc.id, doc.to_dict()))
            
    def changeVol(self,args):
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        value=self.slider_2.get()     
        
        currentVol=(1 - value) * minVol + value * maxVol
        
        volume.SetMasterVolumeLevel(currentVol, None)

if __name__ == "__main__":
    app = App()
    app.mainloop()