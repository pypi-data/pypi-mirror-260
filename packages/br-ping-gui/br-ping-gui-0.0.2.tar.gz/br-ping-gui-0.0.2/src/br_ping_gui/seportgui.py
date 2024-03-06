import sys
import customtkinter
from brping import Ping1D
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton, CTkRadioButton, CTkFrame, CTkCheckBox, CTkTextbox
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import threading
import datetime as dt
from serial.tools.list_ports import comports
from functools import partial


gain = {0: 0.6,
        1: 1.8,
        2: 5.5,
        3: 12.9,
        4: 30.2,
        5: 66.1,
        6: 144}


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Initialize Ping2D!
        self.title("Ping2D GUI")
        self.geometry("1000x1000")
        self._filename = None
        self._record_flag = threading.Event()
        self._record_thread = None
        self.host = "192.168.2.2"
        self.port = 9090
        self.connect_buttons = []
        self.ping1d = None
        self.sonar_lock = threading.Lock()
        self._spin_thread = None
        self._spin_flag = threading.Event()
        self._profile_data = None
        self._speed_of_sound_data = None
        # Variables to store user inputs
        self.speed_of_sound_var = ctk.IntVar()
        self.scan_start_var = ctk.IntVar()
        self.scan_length_var = ctk.IntVar()
        self.gain_setting_var = ctk.IntVar()
        self.ping_interval_var = ctk.IntVar()
        self.pulse_duration_var = ctk.IntVar()
        self.ping_enabled_var = ctk.BooleanVar()
        self.auto_mode_var = ctk.BooleanVar()
        self.createwidgets()

    def call_until_complete(self, func, *args, **kwargs):
        val = func(*args, **kwargs)
        while val is None or not val:
            val = func(*args, **kwargs)
            time.sleep(0.01)
        return val

    def get_configuration(self):
        """
        Set all of the configuration labels in the GUI from the sonar
        :return:
        """
        with self.sonar_lock:
            # Get configuration data from the sonar
            speed_of_sound_data = self.call_until_complete(self.ping1d.get_speed_of_sound)
            range_data = self.call_until_complete(self.ping1d.get_range)
            gain_setting_data = self.call_until_complete(self.ping1d.get_gain_setting)
            ping_interval_data = self.call_until_complete(self.ping1d.get_ping_interval)
            ping_enabled_data = self.call_until_complete(self.ping1d.get_ping_enable)
            pulse_duration_data = self.call_until_complete(self.ping1d.get_transmit_duration)
            auto_mode_data = self.call_until_complete(self.ping1d.get_mode_auto)

        # Update CustomTkinter variables and labels
        if speed_of_sound_data is not None:
            self.speed_of_sound_var.set(speed_of_sound_data['speed_of_sound'])
        if range_data is not None:
            self.scan_start_var.set(range_data['scan_start'])
            self.scan_length_var.set(range_data['scan_length'])
        if gain_setting_data is not None:
            self.gain_setting_var.set(gain_setting_data['gain_setting'])
        if ping_interval_data is not None:
            self.ping_interval_var.set(ping_interval_data['ping_interval'])
        if pulse_duration_data is not None:
            self.pulse_duration_var.set(pulse_duration_data["transmit_duration"])
        if auto_mode_data is not None:
            self.auto_mode_var.set(bool(auto_mode_data["mode_auto"]))
        if ping_enabled_data is not None:
            self.ping_enabled_var.set(bool(ping_enabled_data['ping_enabled']))

    def createwidgets(self):
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame.grid_columnconfigure(0, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Options",
                                                             font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=30, pady=30)

        self.connect_options_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Configure Connection",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.connect_options_event)
        self.connect_options_button.grid(row=1, column=0, sticky="ew")


        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Configure Profile Data",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=2, column=0, sticky="ew")

        self.frame_1_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Print Profile Data",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_1_button_event)
        self.frame_1_button.grid(row=3, column=0, sticky="ew")


        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Plot Profile Data",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=4, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Record Data",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=5, column=0, sticky="ew")

        # create main entry and button
        self.errorbox = customtkinter.CTkTextbox(self.navigation_frame, width=180, height=10, text_color='red')
        self.errorbox.grid(row=6, column=0)
        self.errorbox.insert("0.0", "Error Box")

        self.appearance_mode_label = customtkinter.CTkLabel(self.navigation_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=8, column=0, padx=10, pady=10, sticky="s")

        self.connect_options_fr()

        # create home frame
        self.home_fr()

        # create second frame
        self.firstfr()

        # create second frame
        self.secondfr()

        # create third frame
        self.thirdfr()

        # select default frame
        self.select_frame_by_name("connect options")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.second_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.shutdown)

    def connect_options_fr(self):
        self.connect_options_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.connect_options_frame.grid_columnconfigure(0, weight=1)

        self.info_label = customtkinter.CTkLabel(self.connect_options_frame,
                                                 text="Please select the connection method for the Ping1D sonar device:")
        self.info_label.grid(row=1, column=0, padx=20, pady=10)

        self.connect_button1 = customtkinter.CTkButton(self.connect_options_frame, text="Serial", command=self.serial_button)
        self.connect_button1.grid(row=2, column=0, padx=20, pady=10)

        self.connect_button2 = customtkinter.CTkButton(self.connect_options_frame, text="UDP", command=self.udp_button)
        self.connect_button2.grid(row=3, column=0, padx=20, pady=10)

        self.disconnect_button = customtkinter.CTkButton(self.connect_options_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=3, column=1, padx=20, pady=10)
        self.disconnect_button.configure(state="disabled")

    def udp_button(self):
        self.ping1d = Ping1D()
        self.ping1d.connect_udp(self.host, self.port)
        while not self.ping1d.initialize():
            time.sleep(0.1)
            self.errorbox.delete("1.0", "end")
            self.errorbox.insert("0.0", "Failed to initialize Ping2D!")
        self.errorbox.delete("1.0", "end")
        self.get_configuration()
        self.connect_button1.configure(state="disabled")
        self.connect_button2.configure(state="disabled")
        self.disconnect_button.configure(state="normal")
        self._spin_flag.set()
        self._spin_thread = threading.Thread(target=self.spin_sonar)
        self._spin_thread.start()

    def serial_button(self):
        # Serial connection settings
        self.info_label2 = customtkinter.CTkLabel(self.connect_options_frame,
                                                 text="Select your Device:")
        devices = comports()
        self.info_label2.grid(row=4, column=0, padx=20, pady=10)

        self.connect_buttons = []
        for i, device in enumerate(devices):
            button = customtkinter.CTkButton(self.connect_options_frame, text=f"{device.description}: {device.device}",
                                                       command=partial(self.serial_connect, device))
            button.grid(row=5+i, column=0, padx=20, pady=10)
            button.configure(state='normal')
            self.connect_buttons.append(button)

    def serial_connect(self, device):
        # Connection to Ping2D
        self.ping1d = Ping1D()
        self.ping1d.connect_serial(device.device, 115200)
        while not self.ping1d.initialize():
            time.sleep(1)
            self.errorbox.delete("1.0", "end")
            self.errorbox.insert("0.0", "Failed to initialize Ping2D!")
        self.errorbox.delete("1.0", "end")
        self.get_configuration()
        self.connect_button1.configure(state="disabled")
        self.connect_button2.configure(state="disabled")
        self.disconnect_button.configure(state="normal")
        [b.configure(state='disabled') for b in self.connect_buttons]
        self._spin_flag.set()
        self._spin_thread = threading.Thread(target=self.spin_sonar)
        self._spin_thread.start()

    def disconnect(self):
        if self._record_flag.is_set():
            self.stop_record_ping_data()
        if self._spin_flag.is_set():
            self._spin_flag.clear()
            self._spin_thread.join(timeout=10.0)
        with self.sonar_lock:
            self.ping1d = None
        if len(self.connect_buttons):
            [b.destroy() for b in self.connect_buttons]
            self.info_label2.destroy()
        self.connect_button1.configure(state="normal")
        self.connect_button2.configure(state="normal")
        self.disconnect_button.configure(state="disabled")

    def home_fr(self):
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.speed_of_sound_label = customtkinter.CTkLabel(self.home_frame, text="Speed of sound:", anchor="w")
        self.speed_of_sound_label.grid(row=1, column=0, padx=1, pady=(1, 0))
        self.speed_of_sound_entry = customtkinter.CTkEntry(self.home_frame, textvariable=self.speed_of_sound_var)
        self.speed_of_sound_entry.grid(row=1, column=1, padx=1, pady=(1, 0))

        self.scan_start_label = customtkinter.CTkLabel(self.home_frame, text="Scan start:", anchor="w")
        self.scan_start_label.grid(row=3, column=0, padx=1, pady=(1, 0))
        self.scan_start_entry = customtkinter.CTkEntry(self.home_frame, textvariable=self.scan_start_var)
        self.scan_start_entry.grid(row=3, column=1, padx=1, pady=(1, 0))

        self.scan_length_label = customtkinter.CTkLabel(self.home_frame, text="Scan Length:", anchor="w")
        self.scan_length_label.grid(row=5, column=0, padx=1, pady=(1, 0))
        self.scan_length_entry = customtkinter.CTkEntry(self.home_frame, textvariable=self.scan_length_var)
        self.scan_length_entry.grid(row=5, column=1, padx=1, pady=(1, 0))

        self.ping_interval_label = customtkinter.CTkLabel(self.home_frame, text="Ping Interval:", anchor="w")
        self.ping_interval_label.grid(row=7, column=0, padx=1, pady=(1, 0))
        self.ping_interval_entry = customtkinter.CTkEntry(self.home_frame, textvariable=self.ping_interval_var)
        self.ping_interval_entry.grid(row=7, column=1, padx=1, pady=(1, 0))

        self.pulse_duration_label = customtkinter.CTkLabel(self.home_frame, text="Pulse Duration:", anchor="w")
        self.pulse_duration_label.grid(row=9, column=0, padx=1, pady=(1, 0))
        self.pulse_duration_entry = customtkinter.CTkEntry(self.home_frame, textvariable=self.pulse_duration_var)
        self.pulse_duration_entry.grid(row=9, column=1, padx=1, pady=(1, 0))

        self.gain_setting_label = customtkinter.CTkLabel(self.home_frame, text="Gain Setting")
        self.gain_setting_label.grid(row=11, column=0, padx=(10, 5), pady=(10, 5))
        self.gain_checkbox = ctk.CTkCheckBox(self.home_frame, text="Auto", variable=self.auto_mode_var, onvalue=True,
                                             offvalue=False)
        self.gain_checkbox.grid(row=11, column=1, padx=(10, 5), pady=(10, 5))
        for i in range(7):
            self.gain_setting_button = customtkinter.CTkRadioButton(self.home_frame, text=str(i), variable=self.gain_setting_var,
                                                  value=i)
            self.gain_setting_button.grid(row=12 + i, column=1, padx=1, pady=(0, 2))

        self.ping_enabled_label = customtkinter.CTkLabel(self.home_frame, text="Ping Enabled")
        #self.ping_enabled_var = ctk.StringVar(value="1")  # Inicialized in 1
        self.ping_enabled_label.grid(row=20, column=0, padx=1, pady=(1, 0))
        self.checkbox = ctk.CTkCheckBox(self.home_frame, text="", variable=self.ping_enabled_var, onvalue=True,
                                        offvalue=False)
        self.checkbox.grid(row=21, column=1, padx=1, pady=(1, 0))

        self.ff=customtkinter.CTkFrame(self.home_frame, width=10, height=30, fg_color='transparent')
        self.ff.grid(row=22, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Configure", command=self.configure_data)
        self.home_frame_button_1.grid(row=23, column=0, padx=20, pady=10)

    def firstfr(self):
        self.first_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.first_frame.grid_columnconfigure(0, weight=1)
        self.data_label = customtkinter.CTkLabel(self.first_frame, text="Information about the data will be displayed here")
        self.data_label.grid(row=1, column=0, padx=20, pady=10)
        self.data_label2 = customtkinter.CTkLabel(self.first_frame, text="Information about the speed of sound will be displayed here")
        self.data_label2.grid(row=3, column=0, padx=20, pady=10)

    def secondfr(self):
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)


    def thirdfr(self):
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)

        self.third_frame_button1 = customtkinter.CTkButton(self.third_frame, text="Start Recording Data", command=self.start_record_ping_data)
        self.third_frame_button1.grid(row=1, column=0, padx=20, pady=10)

        self.third_frame_button2 = customtkinter.CTkButton(self.third_frame, text="Stop Recording Data", command=self.stop_record_ping_data)
        self.third_frame_button2.grid(row=2, column=0, padx=20, pady=10)
        self.third_frame_button2.configure(state="disabled")

        self.recordbox = customtkinter.CTkTextbox(self.third_frame, width=220, height=10)
        self.recordbox.grid(row=5, column=0)
        self.recordbox.insert("0.0", "Data will be recorded in csv format")

    def plot_profile_data(self):
        # Request profile data
        with self.sonar_lock:
            data = self._profile_data
            speed_of_sound = self.call_until_complete(self.ping1d.get_speed_of_sound)

        if data and speed_of_sound:
            # Extract relevant information for plotting
            profile_data = data['profile_data']
            scan_start = data['scan_start']  # mm
            scan_length = data['scan_length']  # mm
            # Convert bytes to NumPy array
            profile_data_array = np.frombuffer(profile_data, dtype=np.uint8)  # normalized + quantized dB
            speed_of_sound = speed_of_sound['speed_of_sound']  # mm/s
            # Calculate time values using the formula t=(Distance*2)/speed of sound in ms
            tstart = scan_start / speed_of_sound  # one way travel time (s)
            tend = (scan_length + scan_start) / speed_of_sound  # one way travel time (s)
            time_values = np.linspace(tstart, tend, len(profile_data_array))

            # Calculate distance values in meters
            distance_values = np.linspace(scan_start / 1000, (scan_length + scan_start) / 1000, 10)

            # Clear the previous plot
            self.ax.clear()

            # Create a new plot for profile data
            self.ax.plot(time_values * 1000, profile_data_array, label='Profile Data')
            t = np.linspace(tstart, tend, 10) * 1000
            self.ax.set_xticks(t)
            # for real data adquisition 1 way Time and distance, take out the 2 down
            self.ax.set_xticklabels(
                [f"{2 * d:.1f}" for d in t])
            self.ax.set_xlabel('2-way Time (ms)')
            self.ax.set_ylabel('Profile Data')
            self.ax.set_title('Profile Data over Time and Distance')
            self.fig.subplots_adjust(top=0.85)  # Adjust the top margin to leave more space for the title

            # Create a twin Axes for the second x-axis
            secax = self.ax.secondary_xaxis('top')

            secax.set_xticks(t)
            secax.set_xlabel('Distance (m)')
            secax.set_xticklabels(
                [f"{d:.1f}" for d in distance_values])

            # Update the plot on the user interface
            self.canvas.draw()

            self.errorbox.delete("1.0", "end")

        else:
            self.errorbox.delete("1.0", "end")
            self.errorbox.insert("0.0", "Failed to plot profile data")

    def configure_data(self):
        # Get user-input parameters
        speed_of_sound = self.speed_of_sound_var.get() or None
        scan_start = self.scan_start_var.get() or None
        scan_length = self.scan_length_var.get() or None
        gain_setting = self.gain_setting_var.get() or None
        ping_interval = self.ping_interval_var.get() or None
        ping_enabled = self.ping_enabled_var.get() or None
        auto_mode = self.auto_mode_var.get() or None

        with self.sonar_lock:
            # Set parameters in Ping1D
            if auto_mode is not None:
                self.call_until_complete(self.ping1d.set_mode_auto, auto_mode, verify=True)
            if speed_of_sound is not None:
                self.ping1d.set_speed_of_sound(speed_of_sound, verify=True)
            if scan_start is not None and scan_length is not None:
                self.ping1d.set_range(scan_start, scan_length)
            if gain_setting is not None:
                self.call_until_complete(self.ping1d.set_gain_setting,gain_setting,verify=True)
            if ping_interval is not None:
                self.ping1d.set_ping_interval(ping_interval)
            if ping_enabled is not None:
                self.ping1d.set_ping_enable(ping_enabled)


    def spin_sonar(self):
        while self._spin_flag.is_set():
            with self.sonar_lock:
                self._profile_data = self.call_until_complete(self.ping1d.get_profile)
                self._speed_of_sound_data = self.call_until_complete(self.ping1d.get_speed_of_sound)
                interval = self.call_until_complete(self.ping1d.get_ping_interval)
            self.receive()
            self.plot_profile_data()
            speed_of_sound_info = f"Speed of Sound: {self._speed_of_sound_data['speed_of_sound']} mm/s"
            self.data_label2.configure(text=speed_of_sound_info)

            time.sleep(interval['ping_interval'] / 2000)

    def receive(self):
        # Request profile data
        data = self._profile_data

        if data:
            distance_info1 = f"Distance: {data['distance']}mm"
            distance_info2 = f"Confidence: {data['confidence']}%"
            transmit_duration_info = f"Transmit Duration: {data['transmit_duration']} us"
            ping_number_info = f"Ping Number: {data['ping_number']}"
            scan_start_info = f"Scan Start: {data['scan_start']} mm"
            scan_length_info = f"Scan Length: {data['scan_length']} mm"
            gain_setting_info = f"Gain Setting: {data['gain_setting']}"

            # Build a string with all the information
            full_info = f"{distance_info1}\n{distance_info2}\n{transmit_duration_info}\n{ping_number_info}\n{scan_start_info}\n{scan_length_info}\n{gain_setting_info}"

            # Update the label in the GUI with the information
            self.data_label.configure(text=full_info)
            self.errorbox.delete("1.0", "end")

        else:
            self.errorbox.delete("1.0", "end")
            self.errorbox.insert("0.0", "Failed to print profile data")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        if self._record_flag.is_set():
            self.frame_3_button.configure(fg_color="red")
        else:
            self.frame_3_button.configure(fg_color="transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

        if name == "connect options":
            self.connect_options_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.connect_options_frame.grid_forget()

        if name == "frame_1":
            self.first_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.first_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def start_record_ping_data(self):
        self._record_flag.set()
        self._filename = dt.datetime.utcnow().strftime("ping_recording_%Y%m%dT%H%M%S.csv")
        self._record_thread = threading.Thread(target=self._record)
        self._record_thread.start()
        self.recordbox.delete("1.0", "end")
        self.recordbox.insert("0.0", "Recording Data")
        #disable botton
        self.third_frame_button1.configure(state="disabled")
        self.third_frame_button2.configure(state="normal")
        #change the recording color button
        self.frame_3_button.configure(fg_color="red")

    def stop_record_ping_data(self):
        self._record_flag.clear()
        self._record_thread.join(timeout=10.0)
        # TODO I don't know why, but the record thread exits but the join doesn't notice.
        if self._record_thread.is_alive():
            print("didn't join properly :(")
        self._record_thread = None
        self.recordbox.delete("1.0", "end")
        self.recordbox.insert("0.0", "Data Recorded Successfully")
        # disable botton
        self.third_frame_button2.configure(state="disabled")
        self.third_frame_button1.configure(state="normal")
        self.frame_3_button.configure(fg_color="transparent")

    def _record(self):
        fieldnames = ["Ping Number", "Distance", "Confidence", "Transmit Duration",
                                                      "Scan Start",
                                                      "Scan Length", "Gain Setting"] + [f"sample_{i}" for i in range(200)]
        with open(self._filename, mode='w') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            old_data = {}
            while self._record_flag.is_set():
                data = self._profile_data
                if data and data != old_data:
                    ping_number = data["ping_number"]
                    distance = data["distance"]
                    confidence = data["confidence"]
                    transmit_duration = data["transmit_duration"]
                    scan_start = data["scan_start"]
                    scan_length = data["scan_length"]
                    gain_setting = data["gain_setting"]
                    row = {"Ping Number": ping_number, "Distance": distance,
                           "Confidence": confidence, "Transmit Duration": transmit_duration,
                           "Scan Start": scan_start, "Scan Length": scan_length, "Gain Setting": gain_setting}
                    profile_data = data["profile_data"]
                    samples = {f"sample_{i}": int(p) for i, p in enumerate(profile_data)}
                    row.update(samples)
                    writer.writerow(row)
                    old_data = data
                time.sleep(0.05)


    def connect_options_event(self):
        self.select_frame_by_name("connect options")

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_1_button_event(self):
        self.select_frame_by_name("frame_1")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def shutdown(self):
        self.disconnect()
        sys.exit(0)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
