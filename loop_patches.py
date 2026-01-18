import rtmidi
import sounddevice

class KeysInterface:
    def __init__(self):
        self.midiout = rtmidi.RtMidiOut()
        self.device = ""
        self.get_device_list()

    def get_device_list(self):
        device_list = []
        count = self.midiout.getPortCount()
        i=0
        while i < count:
            print(f"{self.midiout.getPortName(i)} - ({i})")
            self.device_list.append(i)
            i+=1



interface = KeysInterface()
