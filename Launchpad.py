from rtmidi.midiutil import open_midiinput
import rtmidi
import logging
import sys
import time
import requests
import json

midi_to_coords = {
    "104": "MOVE",
    "105": "SLOW_MOVE",
    "106": "FAST_MOVE",
    "81": [0,0], "82": [0,1], "83": [0,2], "84": [0,3],
    "71": [1,0], "72": [1,1], "73": [1,2], "74": [1,3],
    "61": [2,0], "62": [2,1], "63": [2,2], "64": [2,3],
    "51": [3,0], "52": [3,1], "53": [3,2], "54": [3,3],
}

class Command:
    type = "MOVE"
    coords = [0,0] 
    def __init__(self,type: str, coords: []):
        self.type = type
        self.coords = coords

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class LaunchpadAPI:

    endpoint_url = "http://127.0.0.1:5000"
    midi_out: rtmidi.MidiOut
    midi_in: rtmidi.MidiIn
    midi_out_port: int = 0
    midi_in_port = ""
    available_ports = []
    command: Command
    def __init__(self):
        
        self.midi_out = rtmidi.MidiOut()
        # This enables logging on debug level
        self.log = logging.getLogger('midi_in_poll')
        logging.basicConfig(level=logging.DEBUG)

        # If the User specifies a port use that port 
        self.midi_out_port = sys.argv[1] if len(sys.argv) > 1 else None

        # if not show all ports and let them choose
        self.available_out_ports = self.midi_out.get_ports()
        if self.available_ports:
            self.midi_out.open_port(1)
        try:
            self.midi_in, self.midi_in_port = open_midiinput(self.midi_out_port)
        except (EOFError, KeyboardInterrupt):
            sys.exit()
        self.command = Command("MOVE",[0,0])
    def run(self):
        
        print("Entering main loop. Press Control-C to exit.")
        try:
            self.handle_input()
        except KeyboardInterrupt:
            print('Ctrl+C program interrupted')
        finally:
            print("Exit.")
            self.midi_in.close_port()
            del self.midi_in
    def send_command(self):
        try:
            header = {'Content-Type': 'application/json'}
            r = requests.post(url=self.endpoint_url, data=self.command.toJSON(), headers=header)
            print(f"Robot responded: {r.text}")
            return 0
        except:
            print(f"ERROR: couldn't reach robot endpoint. ({self.endpoint_url})")
            return 0
    def handle_input(self):
        timer = time.time()
        while True:
            msg = self.midi_in.get_message()
            if msg:
                message, deltatime = msg
                timer += deltatime
                    
                if message[2] != 0 and message[1]:
                    
                    try:
                        if message[1] >= 104 and message[1] <= 111:
                            print(f"change command to {midi_to_coords[str(message[1])]}")
                            self.command.type = midi_to_coords[str(message[1])]
                        else:
                            self.command.coords= midi_to_coords[str(message[1])] 
                            print(f"sending command to robot...")
                            print(f"{self.command.type} to {self.command.coords}")
                            self.send_command()
                    except:
                        print("Key not mapped")
                  
                        
        

Launchpad = LaunchpadAPI()
Launchpad.run()
