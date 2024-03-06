
import customtkinter
import json
import os
from multiprocessing import Process
import traceback
import re
import ast
import pandas as pd
import numpy as np

from ...util import PSORunner
from ...util import GraphGenerator
from ...util.CTkToolTip import CTkToolTip as ctt

def create_tab(self, tab):
    
    # URL
    tab.grid_columnconfigure(0, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    tab.grid_rowconfigure(1, weight=200)
    
    """
    self.url = customtkinter.CTkEntry(tab, textvariable=self.option_manager.get_arguments()['url'])
    self.url.grid(row=0, column=0, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    self.run_button = customtkinter.CTkButton(tab, text="Run", command=self.run)
    self.run_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
    ctt(self.run_button, delay=0.5, message="Start calibration...")
    
        self.stop_button = customtkinter.CTkButton(tab, text="Stop", command=self.stop)
    self.stop_button.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
    ctt(self.stop_button, delay=0.5, message="Stop calibration...")
    
    """
    
    self.progress_container = customtkinter.CTkFrame(tab)
    self.progress_container.grid_columnconfigure(0, weight=1)
    self.progress_container.grid_columnconfigure(1, weight=1)
    self.progress_container.grid_columnconfigure(2, weight=1)
    self.progress_container.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    
    # Add progress bar to progress container
    self.progress_message_left = customtkinter.CTkLabel(self.progress_container, text="")
    self.progress_message_left.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="w")
    
    self.progress_message_middle = customtkinter.CTkLabel(self.progress_container, text="Calibration not running...")
    self.progress_message_middle.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
    
    self.progress_message_right = customtkinter.CTkLabel(self.progress_container, text="")
    self.progress_message_right.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="e")
    
    #self.progress_bar = customtkinter.CTkProgressBar(self.progress_container)
    #self.progress_bar.grid(row=1, column=0, columnspan=3, padx=(10, 10), pady=(10, 10), sticky="ew")
    #self.progress_bar.set(0)
    #ctt(self.progress_bar, delay=0.5, message="Current calibration progress")
    
    self.textbox = customtkinter.CTkTextbox(tab)
    self.textbox.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
    self.textbox.insert("0.0", "Welcome to the CSIP PSO Calibration Tool!\n\nUse the Calibration tab to define steps and calibration parameters. Use this tab to run and observe calibration progress. Once finished, use the Visualization tab to generate figures and graphs.")
        