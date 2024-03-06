#!/usr/local/bin/python3.9

import os 
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
print(dir_path)

# minikube kubectl -- create -f ../start.yaml ; sleep 60 ; minikube service pf8087-csu-csip-oms -n csip

import requests

import tkinter as tk
import tkinter.messagebox
import customtkinter
import json
import os
from PIL import Image, ImageTk
import traceback
from multiprocessing import Process
from multiprocessing import Queue
import re
import pandas as pd
import numpy as np
import ast
import platform
import time

from queue import Empty

from ..util import PSORunner
from ..util import GraphGenerator

import subprocess
import plotly.express as px
import plotly.graph_objs as go

from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

from . import OptionManager as om

from .SetupTab import SetupTab as st
from .PlatformTab import PlatformTab as pt
from .RunTab import RunTab as rt
from .VisualizeTab import VisualizeTab as vt

from ..util.CTkToolTip import CTkToolTip as ctt

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

results_queue = Queue()
stdout_queue = Queue()
stderr_queue = Queue()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.option_manager = om.OptionManager()
        
        self.running_config = None
        self.selected_graph_name = None

        self.train_process = None
        self.minikube_process = None
        self.data_x = [0]
        self.data_y = [0]
        
        self.image_width = 1280
        self.image_height = 720

        # configure window
        self.title("CSIP PSO")
        self.geometry(f"{1920}x{1080}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header_padding_x = (5, 5)
        header_padding_y = (10, 10)
        
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CSIP PSO", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=(20, 10), pady=header_padding_y)
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save", width=60, command=self.save_project)
        self.save_button.grid(row=0, column=1, padx=header_padding_x, pady=header_padding_y)
        self.load_button = customtkinter.CTkButton(self.sidebar_frame, text="Load", width=60, command=self.load_project)
        self.load_button.grid(row=0, column=2, padx=header_padding_x, pady=header_padding_y)
        
        # 4 is service URL
        self.service_label = customtkinter.CTkLabel(self.sidebar_frame, text="Service:", anchor="w")
        self.service_label.grid(row=0, column=3, padx=(80, 5), pady=header_padding_y)
        self.service_url = customtkinter.CTkEntry(self.sidebar_frame, textvariable=self.option_manager.get_arguments()['url'])
        self.service_url.grid(row=0, column=4, columnspan=1, padx=header_padding_x, pady=header_padding_y, sticky="nsew")
        refresh_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "refresh.png")), size=(20, 20))
        self.refresh_button = customtkinter.CTkButton(self.sidebar_frame, text=None, width=30, image=refresh_image, command=self.load)
        self.refresh_button.grid(row=0, column=5, padx=(5, 80), pady=header_padding_y)
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scale:", anchor="w")
        self.scaling_label.grid(row=0, column=6, padx=header_padding_x, pady=header_padding_y)
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["50%", "75%", "100%", "125%", "150%", "175%", "200%"], width=60,
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=0, column=7, padx=header_padding_x, pady=header_padding_y)
        self.scaling_optionemenu.set("100%")
        
        expand_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "expand.png")), size=(20, 20))
        self.new_window = customtkinter.CTkButton(self.sidebar_frame, text=None, width=30, image=expand_image, command=self.new_window)
        self.new_window.grid(row=0, column=8, padx=(5, 20), pady=header_padding_y)
        
        self.tabview = customtkinter.CTkTabview(self, bg_color="transparent", fg_color="transparent")
        self.tabview.grid(row=1, column=0, padx=(0, 0), pady=(10, 10), sticky="nsew")
        tab1 = "Platform"
        tab2 = "Setup"
        tab3 = "Logs"
        tab4 = "Results"
        #tab5 = "Results"
        
        self.tabview.add(tab1)
        self.tabview.add(tab2)
        self.tabview.add(tab4)
        self.tabview.add(tab3)
        #self.tabview.add(tab5)
        
        #self.tabview.configure(state="disabled")
        
        pt.create_tab(self, self.tabview.tab(tab1))
        st.create_tab(self, self.tabview.tab(tab2))
        rt.create_tab(self, self.tabview.tab(tab3))
        vt.create_tab(self, self.tabview.tab(tab4))
        
        self.footer_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.footer_frame.grid(row=2, column=0, sticky="nsew")
        self.footer_frame.grid_columnconfigure(4, weight=1)
        
        self.footer_progress_label = customtkinter.CTkLabel(self.footer_frame, text="Stopped", width=150, font=customtkinter.CTkFont(size=16, weight="bold"), anchor="w")
        self.footer_progress_label.grid(row=0, column=0, padx=(20, 5), pady=header_padding_y)

        self.footer_progress_bar = customtkinter.CTkProgressBar(self.footer_frame)
        self.footer_progress_bar.grid(row=0, column=4, padx=(50, 100), pady=header_padding_y, sticky="ew")
        self.footer_progress_bar.set(0)
        
        play_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "play.png")), size=(20, 20))
        self.new_window = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=play_image, command=self.run)
        self.new_window.grid(row=0, column=7, padx=(5, 5), pady=header_padding_y)
        
        stop_image = customtkinter.CTkImage(Image.open(os.path.join("./images", "stop.png")), size=(20, 20))
        self.new_window = customtkinter.CTkButton(self.footer_frame, text=None, width=30, image=stop_image, command=self.stop)
        self.new_window.grid(row=0, column=8, padx=(5, 20), pady=header_padding_y)

    def _resize_image(self, event):
        self.graph_label.update_idletasks()
        new_width = self.graph_label.winfo_width()
        new_height = self.graph_label.winfo_height()
        
        alt_width = new_height * 1.77778
        alt_height = new_width / 1.77778
        
        if (new_width < new_height):
            new_height = alt_height
        else:
            new_width = alt_width
        
        self.image_width = new_width
        self.image_height = new_height
        
        self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(new_width, new_height))
        self.graph_label.configure(image=self.graph_image)
        self.graph_label.update_idletasks()

    def callback_test(self, *args):
        print("callback_test called")
            
    def update_graph(self, value):
        selected_graph = self.graph_selector_value.get()
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        if (selected_graph == "Best Cost Stacked"):
            self.selected_graph_name = "best_cost_stacked"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Best Cost by Round"):
            self.selected_graph_name = "best_cost_by_round"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Iteration Table"):
            self.selected_graph_name = "table"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
        elif (selected_graph == "Calibrated Parameters"):
            self.selected_graph_name = "calibrated_params_by_round"
            image_path = os.path.join(folder, self.selected_graph_name + ".png")
            if not os.path.exists(image_path):
                image_path = os.path.join("./images", "up.png")
            self.graph_image_obj = Image.open(image_path)
            self.graph_image = customtkinter.CTkImage(self.graph_image_obj, size=(self.image_width, self.image_height))
            self.graph_label.configure(image=self.graph_image)
            
    def save_project(self):
        metrics = self.option_manager.get_metrics()
        filename = asksaveasfilename(filetypes=[("JSON", "*.json")], initialfile="config", defaultextension="json", title="Save Project")
        
        try:
        
            # Convert metrics to json and save to file with proper spacing
            with open(filename, "w") as f:
                f.write(json.dumps(metrics, indent=4))
                
            self.save_button.configure(text="Saved!")
            self.after(3000, lambda: self.save_button.configure(text="Save"))
        except Exception as e:
            self.save_button.configure(text="Error!")
            print(e)
            self.after(3000, lambda: self.save_button.configure(text="Save"))
    
    def new_window(self):
        # Shell out and run ./main.py
        subprocess.Popen(["python3", "../mgpsogui.py"])
    
    def load_project(self):
        
        filename = askopenfilename(filetypes=[("JSON", "*.json")], title="Open Project", multiple=False)
        print(filename)
        
        try:
        
            # Load config.json and convert to metrics
            with open(filename, "r") as f:
                metrics = json.loads(f.read())
            
            self.option_manager.set_path(filename)
            
            if "arguments" in metrics:
                metrics["arguments"]["calibration_parameters"] = metrics["calibration_parameters"]
            
            if "service_parameters" in metrics:
                self.option_manager.set_service_parameters(metrics["service_parameters"])
                self.tabview.configure(state="enabled")
            
            print(metrics)
            
            self.option_manager.clear()
            self.option_manager.add_arguments(metrics["arguments"])
            self.option_manager.add_steps(metrics["steps"])
            
            self.steps_frame.clear()
            self.steps_frame.render()

            self.static_param_frame.clear()
            self.static_param_frame.render()
            
            self.calib_param_frame.clear()
            self.calib_param_frame.render()
            
            self.load_button.configure(text="Loaded!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))
            
        except Exception as e:
            print(e)
            self.load_button.configure(text="Error!")
            self.after(3000, lambda: self.load_button.configure(text="Load"))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def make_request(self):
        service_url = self.service_url.get()
        try:
            response = requests.get(service_url)
                
            response_json = json.loads(response.text)
            status = response.status_code
            
            self.option_manager.set_service_parameters(response_json)
            
            self.service_status.delete('0.0', tk.END)
            self.service_status.insert(text=str(status), index='0.0')
            self.service_name.delete('0.0', tk.END)
            self.service_name.insert(text=str(response_json["metainfo"]["name"]), index='0.0')
            self.service_description.delete('0.0', tk.END)
            self.service_description.insert(text=str(response_json["metainfo"]["description"]), index='0.0')
            self.service_details.delete('0.0', tk.END)
            self.service_details.insert(text=json.dumps(response_json, indent=4), index='0.0')
            
            self.refresh_button.configure(fg_color="green")
        except Exception as e:
            self.refresh_button.configure(fg_color="red")
        
    
    def load(self):
        # Make HTTP request to service_url and save the result to bounds.json
        
        self.default_button_color = self.refresh_button.cget("fg_color")
        
        self.refresh_button.configure(fg_color="gray")
        
        self.after(10, self.make_request)
        self.after(3000, lambda: self.refresh_button.configure(fg_color=self.default_button_color))
        
    def run(self):
        metrics = self.option_manager.get_metrics()
        self.running_config = metrics
        
        #self.progress_bar.configure(mode="indeterminnate")
        #self.progress_bar.start()
        self.footer_progress_bar.configure(mode="indeterminnate")
        self.footer_progress_bar.start()
        
        self.data_x = [0]
        self.data_y = [0]
        
        self.progress_message_middle.configure(text="Calibration starting...")
        self.footer_progress_label.configure(text="Starting...")
        
        self.textbox.insert("0.0", "Starting calibration...\n\n")
        self.textbox.insert("0.0", "Calibration Parameters:\n")
        self.textbox.insert("0.0", json.dumps(metrics, indent=4) + "\n\n")
        try:
            info = self.option_manager.get_project_data()
            folder = os.path.join(info['path'], info['name'])
            
            self.train_process = Process(target=PSORunner.run_process, args=(stdout_queue, stderr_queue, results_queue, metrics, folder))
            self.train_process.daemon = True
            self.train_process.start()
            self.after(1000, self.watch_loop)
            self.string_cache = ""
            self.data_cache = ""
            
        except Exception as e:
            self.textbox.insert("0.0", "An exception occurred!\n Exception: " + str(e) + "\n\n")
            self.textbox.insert("0.0", "Stack trace:\n")
            self.textbox.insert("0.0", traceback.format_exc())
            self.textbox.insert("0.0", "\n\n")
            self.textbox.insert("0.0", "Calibration failed!")
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration failed! See error log below.")
            self.progress_message_right.configure(text="")
            self.footer_progress_label.configure(text="Failed")
            #self.progress_bar.stop()
            self.footer_progress_bar.stop()
            #self.progress_bar.configure(mode="determinate")
            self.footer_progress_bar.configure(mode="determinate")
            #self.progress_bar.set(0)
            self.footer_progress_bar.set(0)
            
    def stop(self):
        print("Stopping...")
        self.train_process.terminate()
        
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
            
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Stop the process
        if (os.path.exists(os.path.join(folder, 'output.txt'))):
            os.remove(os.path.join(folder, 'output.txt'))
        
        if (os.path.exists(os.path.join(folder, 'error.txt'))):
            os.remove(os.path.join(folder, 'error.txt'))
            
        self.textbox.insert("0.0", "\nCalibration terminated!\n")
        #self.progress_bar.stop()
        self.footer_progress_bar.stop()
        #self.progress_bar.configure(mode="determinate")
        self.footer_progress_bar.configure(mode="determinate")
        #self.progress_bar.set(0)
        self.footer_progress_bar.set(0)
        self.progress_message_left.configure(text="")
        self.progress_message_middle.configure(text="Calibration stopped!")
        self.footer_progress_label.configure(text="Stopped")
        self.progress_message_right.configure(text="")
        
    def watch_loop(self):
        # Check if file exists:
        
        info = self.option_manager.get_project_data()
        folder = os.path.join(info['path'], info['name'])
            
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        while True:
            try:
                stdout_line = stdout_queue.get_nowait()
                
                print("# " + stdout_line)
                with open(os.path.join(folder, 'output.txt'), 'a') as f:
                    f.write(stdout_line)
                
            except Empty:
                break
            
        while True:
            try:
                stderr_line = stderr_queue.get_nowait()
                
                print("? " + stderr_line)
                with open(os.path.join(folder, 'error.txt'), 'a') as f:
                    f.write(stderr_line)
                
            except Empty:
                break
        
        if (os.path.exists(os.path.join(folder, 'output.txt'))):
            with open(os.path.join(folder, 'output.txt'), 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                
                new_characters = lines_string.replace(self.string_cache, "")
                # Update the textbox with characters not in self.string_cache
                self.textbox.insert('0.0', new_characters)
                self.string_cache = lines_string
                print(new_characters, end="")
                
            try:
                with open(os.path.join(folder, "output.txt"), "r") as f:
                    text = f.read()

                calibrated_params_pattern = r"calibrated params: ({.*?})"
                best_particle_values_pattern = r"best particle values: (\[.*?\])"
                progress_pattern = r"Progress -  best_round_cost:(.*?), rel_round_tol:(.*?), rtol:(.*?)\n"

                calibrated_params = re.findall(calibrated_params_pattern, text)
                best_particle_values = re.findall(best_particle_values_pattern, text)
                progress_values = re.findall(progress_pattern, text)

                for index, pp in enumerate(best_particle_values):
                    pp = pp.strip()
                    pp = pp.replace('[ ', '[')
                    pp = pp.replace('  ', ',')
                    pp = pp.replace(' ', ',')
                    best_particle_values[index] = pp

                calibrated_params = [ast.literal_eval(i) for i in calibrated_params]
                best_particle_values = [ast.literal_eval(i) for i in best_particle_values]
                progress_values = [tuple(map(float, i)) for i in progress_values]
                
                print(calibrated_params)
                
                GraphGenerator.calibrated_params_by_round(self.running_config['steps'], calibrated_params, self.option_manager)
                self.update_graph("")
            except Exception as e:
                # Print stack trace
                traceback.print_exc()
                
                print(e)
                
        if (os.path.exists(os.path.join(folder, 'error.txt'))):
            with open(os.path.join(folder, 'error.txt'), 'r') as f:
                lines = f.readlines()
                lines_string = "".join(lines)
                self.data_cache = lines_string
                
                pattern = r'(\d+)%\|.*\|(\d+)/(\d+)(?:,\sbest_cost=(\d+\.\d+))?' # The magic of AI
                matches = re.findall(pattern, self.data_cache)
                filtered_matches = [match for match in matches if match[3] != '']
                matches = filtered_matches

                if len(matches) > 0:
                    df = pd.DataFrame(matches, columns=['percent', 'completed_rounds', 'total_rounds', 'best_cost'], dtype=float)
                    df = df[df['best_cost'] != '']
                    df = df.dropna()
                    df = df.drop_duplicates()
                    df['round_step'] = (df['completed_rounds'].diff() < 0).cumsum()
                    df = df.drop_duplicates(subset=['completed_rounds', 'round_step'])

                    GraphGenerator.best_cost_stacked(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.best_cost_by_round(self.running_config['steps'], df, self.option_manager)
                    GraphGenerator.table(self.running_config['steps'], df, self.option_manager)
                    self.update_graph("")

                    match = matches[-1]
                    percent = int(match[0])
                    completed_rounds = int(match[1])
                    total_rounds = int(match[2])
                    best_cost = float(match[3]) if match[3] else None
                    
                    if (percent > 0):
                        #self.progress_bar.stop()
                        self.footer_progress_bar.stop()
                        #self.progress_bar.configure(mode="determinate")
                        self.footer_progress_bar.configure(mode="determinate")
                        #self.progress_bar.set(percent/100)
                        self.footer_progress_bar.set(percent/100)
                        self.progress_message_left.configure(text="Percent Complete: " + str(percent) + "%")
                        self.progress_message_middle.configure(text=str(completed_rounds) + "/" + str(total_rounds))
                        self.footer_progress_label.configure(text=str(completed_rounds) + "/" + str(total_rounds))
                        self.progress_message_right.configure(text="Best Cost: " + str(best_cost))
                    else:
                        #self.progress_bar.configure(mode="indeterminate")
                        self.footer_progress_bar.configure(mode="indeterminate")
                        #self.progress_bar.start()
                        self.footer_progress_bar.start()
                        self.progress_message_left.configure(text="")
                        self.progress_message_middle.configure(text="Starting new round...")
                        self.footer_progress_label.configure(text="Continuing...")
                        self.progress_message_right.configure(text="")
                
                
                
        if self.train_process.is_alive():
            self.after(1000, self.watch_loop)
        else:
            # Check if queue is empty
            """
            if (self.process_queue.empty()):
                print("PROCESS FINISHED BUT WE GOT NO OBJECTS :(")
                self.footer_progress_label.configure(text="Failed")
            else:
                self.final_results = self.process_queue.get()
                print("PROCESS FINISHED WE GOT THINGS")
                print(self.final_results)
                self.footer_progress_label.configure(text="Finished")
            """
            
            #self.progress_bar.stop()
            self.footer_progress_bar.stop()
            #self.progress_bar.configure(mode="indeterminate")
            self.footer_progress_bar.configure(mode="indeterminate")
            #self.progress_bar.start()
            self.footer_progress_bar.start()
            self.progress_message_left.configure(text="")
            self.progress_message_middle.configure(text="Calibration finished!")
            self.progress_message_right.configure(text="")
            self.textbox.insert("0.0", "\nCalibration finished!\n")

def start():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()