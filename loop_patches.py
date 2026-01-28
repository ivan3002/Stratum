import os
import rtmidi
import sounddevice
import json
import keyboard
import time

class KeysInterface:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.connected_port = None
        self.available_devices = self.get_device_list()
        # user input for port selection
        try:
            port_num = int(input("Enter number next to your device: "))
        except ValueError:
            print("Invalid number. Defaulting to 0.")
            port_num = 0
        self.device_name = None
        self.msb_cc_num = None
        self.lsb_cc_num = None
        self.preset_msb_max = None
        self.preset_lsb_max = None
        self.user_msb_max = None
        self.user_lsb_max = None 

        self.load_json(port_num)

         # STARTING POINT: 
        # We start directly at the Preset MSB (65), LSB 0, PC 0
        self.current_msb = self.preset_msb_max
        self.current_lsb = 0
        self.current_pc = 0

    def get_device_list(self):
        device_list = []
        count = self.midiout.get_port_count()
        for i in range(count):
            print(f"{self.midiout.get_port_name(i)}")
            device_list.append(i)
        return device_list

    def load_json(self, port_num):
        profile = None
        raw_port_name = self.midiout.get_port_name(port_num).lower().replace(" ", "_")
        try:
            for filename in os.listdir("profiles"):
                if filename.endswith(".json"):
                    search_term = filename.replace(".json", "").lower().replace(" ", "_") #remove .json
                    if search_term in raw_port_name: #if contains substring of port_name
                        with open(f"profiles/{filename}", "r") as f:
                            profile = json.load(f)
                        break
                else:
                    continue

        except FileNotFoundError:
            print("No profile for this device found")
            return
        
        #handle case where loop finishes but no profile was found
        if profile is None:
            print(f"No profile found for device: {raw_port_name}")
            return
        
        self.device_name = profile["device_name"]
        self.msb_cc_num = profile["msb_cc_num"]
        self.lsb_cc_num = profile["lsb_cc_num"]
        self.preset_msb_max = profile["preset_mappings"]["preset_msb_max"]
        self.preset_lsb_max = profile["preset_mappings"]["preset_lsb_max"]
        self.user_msb_max = profile["user_mappings"]["user_msb_max"]
        self.user_lsb_max = profile["user_mappings"]["user_lsb_max"]
        
        print(f"Opening device {self.device_name}...")
        self.midiout.open_port(port_num)
        print("Device Open!")

    def send_out(self, msb, lsb, pc):
        # track message
        print(f"Sending -> MSB: {msb} | LSB: {lsb} | PC: {pc}")
        
        channel = 0x01 # Channel 2
        
        # CC 0 (Bank Select MSB)
        self.midiout.send_message([0xB0 | channel, self.msb_cc_num, msb])
        # CC 32 (Bank Select LSB)
        self.midiout.send_message([0xB0 | channel, self.lsb_cc_num, lsb])
        # Program Change
        self.midiout.send_message([0xC0 | channel, pc])

    def cycle_patches(self):
        # 1. Send the CURRENT state
        # (This sends 65, 0, 0 on the very first press)
        self.send_out(self.current_msb, self.current_lsb, self.current_pc)

        # 2. Increment Program Change
        self.current_pc += 1

        # 3. Handle PC Overflow (> 127)
        if self.current_pc > 127:
            self.current_pc = 0
            self.current_lsb += 1
            print(f">>> PC Loop Done. Incrementing LSB to {self.current_lsb}")

            # 4. Check LSB limits based on which MSB we are currently on
            
            # --- CASE A: We are currently in PRESET Mode (MSB 65) ---
            if self.current_msb == self.preset_msb_max:
                # If LSB goes past 39...
                if self.current_lsb > self.preset_lsb_max:
                    print(">>> Preset Bank Complete. Switching to USER Bank (66).")
                    self.current_lsb = 0
                    self.current_msb = self.user_msb_max # Jump to 66
            
            # --- CASE B: We are currently in USER Mode (MSB 66) ---
            elif self.current_msb == self.user_msb_max:
                # If LSB goes past 4...
                if self.current_lsb > self.user_lsb_max:
                    print(">>> User Bank Complete. Resetting to PRESET Bank (65).")
                    self.current_lsb = 0
                    self.current_msb = self.preset_msb_max # Jump back to 65

           
interface = KeysInterface()

while True:
    if keyboard.is_pressed("space"):
        # This now handles all the math internally
        interface.cycle_patches() 
        
        # Debounce
        while keyboard.is_pressed('space'):
            time.sleep(0.01)
            
    if keyboard.is_pressed('esc'):
        break
    time.sleep(0.01)