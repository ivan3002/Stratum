
import rtmidi
import sounddevice
import json

class KeysInterface:
    def __init__(self):
        self.midiout = rtmidi.MidiOut()
        self.connected_port = None
        self.available_devices = self.get_device_list()
        choose = input("Choose from list of devices: ").lower().replace(" ", "_")
        profile = self.load_json(choose)

    def get_device_list(self):
        device_list = []
        count = self.midiout.get_port_count()
        for i in range(count):
            print(f"{self.midiout.get_port_name(i)}")
            device_list.append(i)
        return device_list

    def load_json(self, device):
        
        try:
            with open(f"profiles/{device}.json", "r") as f:
                prof = json.load(f)
            print("Device MIDI data = ", prof)
        except FileNotFoundError:
            print("No profile for this device found")

        return prof
interface = KeysInterface()
