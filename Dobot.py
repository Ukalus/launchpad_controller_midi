from flask import Flask, request
import pickle
import json


app = Flask(__name__)


move_mode = {
    "MOVE": 50,
    "SLOW_MOVE": 10,
    "FAST_MOVE": 100
}

# This should be given by the dobot
grid_start_location = [132,144]


def init_dobot():
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])
    dType.SetHOMEParams(api,250,0,50,0, isQueued = 1)
    print(dType.GetHOMEParams(api))

def move_dobot(commandJSON: json):
    if (state == dType.DobotConnect.DobotConnect_NoError):
        dobot_coords = translate_position(commandJSON['coords'], 40)
        dType.SetQueuedCmdClear(api)
        dType.SetPTPCmd(api,dType.PTPMode.PTPMOVLXYZMode,dobot_coords[0],dobot_coords[0],100,0,isQueued= 1)
        dType.SetQueuedCmdStartExec(api)
    else:
        dType.DisconnectDobot(api)

def translate_position(coords, grid_size):
    for i in range(len(coords)):
        coords[i] = coords[i] * grid_size + grid_start_location[i]
    print(coords)
    return coords


@app.route("/", methods=["POST"])
def result(): 
    handleInput(request.data)
    return "Request gotten"

def handleInput(commandJSON):
    command = json.loads(commandJSON)
    move_dobot(command)
    print(dobot_coords)