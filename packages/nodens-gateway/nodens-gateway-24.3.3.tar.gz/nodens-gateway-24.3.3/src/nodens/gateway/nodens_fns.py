## Update: cb="" in MESH.multiline_payload()

import json
import logging
import time
import configparser
import datetime as dt
import numpy as np
from pprint import pprint
import base64
import nodens.gateway as nodens
from nodens.gateway import nodens_mesh as ndns_mesh
from platformdirs import user_log_dir

# Get config from file #
def get_config(config, SECTION, CONFIG, CONFIG_str):
    try:
        output = config.get(SECTION, CONFIG_str).partition('#')[0]
    except:
        output = CONFIG
        nodens.logger.debug('{} not specified in config file. Default value used.'.format(CONFIG_str))
    else:
        output = config.get(SECTION, CONFIG_str).partition('#')[0].rstrip()
        nodens.logger.debug('CONFIG: {} = {}'.format(CONFIG_str, config.get(SECTION, CONFIG_str).partition('#')[0].rstrip()))
    
    return(output)

class radar_config_params:
    """Stores radar configuration information for the current sensor"""
    def __init__(self):
        ## ~~~~~~~ DEFAULT CONFIGURATION ~~~~~~~ ##
        # Radar config #
        self.cfg_idx = 0
        self.cfg_sensorStart = 1
        self.config_radar = [
                "dfeDataOutputMode 1",  # 0
                "channelCfg 15 7 0",
                "adcCfg 2 1",
                "adcbufCfg -1 0 1 1 1",
                "lowPower 0 0",
                "bpmCfg -1 1 0 2",  # 5
                "profileCfg 0 60.75 30.00 25.00 59.10 0 0 54.71 1 96 2950.00 2 1 36 ",
                "chirpCfg 0 0 0 0 0 0 0 5",
                "chirpCfg 1 1 0 0 0 0 0 2",
                "chirpCfg 2 2 0 0 0 0 0 5",
                "frameCfg 0 2 48 0 55.00 1 0",  # 10
                "dynamicRACfarCfg -1 4 4 2 2 8 12 4 8 4.00 8.00 0.40 1 1",
                "staticRACfarCfg -1 6 2 2 2 8 8 6 4 5.00 15.00 0.30 0 0",
                "dynamicRangeAngleCfg -1 0.75 0.0010 1 0",
                "dynamic2DAngleCfg -1 1.5 0.0300 1 0 1 0.30 0.85 8.00",
                "staticRangeAngleCfg -1 0 8 8", # 15
                "fineMotionCfg -1 1",
                "antGeometry0 0 -1 -2 -3 -2 -3 -4 -5 -4 -5 -6 -7",
                "antGeometry1 -1 -1 -1 -1 0 0 0 0 -1 -1 -1 -1",
                "antPhaseRot 1 1 1 1 1 1 1 1 1 1 1 1",
                "fovCfg -1 70.0 20.0",  # 20
                "compRangeBiasAndRxChanPhase 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0",
                "staticBoundaryBox -2 2 2 5.5 0 3",
                "boundaryBox -2.5 2.5 0.5 6 0 3",
                "sensorPosition 1 0 0",
                "gatingParam 3 2 2 2 4",    # 25
                "stateParam 3 3 20 65500 5 65500",
                "allocationParam 40 100 0.025 50 0.8 20",
                "maxAcceleration 0.1 0.1 0.1",
                "trackingCfg 1 2 800 20 46 96 55",
                "presenceBoundaryBox -4 4 0.5 6 0 3",   # 30
                "sensorStart"
                ]
        
        # Sensor target # 
        self.SENSOR_TARGET = []
        self.SENSOR_ROOT = '807d3abc9ba0'
        self.SENSOR_TOPIC = 'mesh/' + self.SENSOR_ROOT + '/toDevice'
        self.SENSOR_PORT = 1883

        # Scanning config #
        self.SCAN_TIME = 60 # Seconds between scans
        self.FULL_DATA_FLAG = 0 # 1 = Capture full-data for diagnostics
        self.FULL_DATA_TIME = 60 # Seconds between full-data captures

        # Radar config #
        self.RADAR_SEND_FLAG = 0 # 1 = Send radar config
        # Note: Sensor located at origin (X,Y) = (0,0). Z-axis is room height. By default, sensor points along Y-axis.
        self.ROOM_X_MIN = "-5"
        self.ROOM_X_MAX = "5"
        self.ROOM_Y_MIN = "0.25"
        self.ROOM_Y_MAX = "10"
        self.ROOM_Z_MIN = "-0.5"
        self.ROOM_Z_MAX = "2"
        # Static monitoring area
        self.MONITOR_X = str(float(self.ROOM_X_MIN) + 0.5) + "," + str(float(self.ROOM_X_MAX) - 0.5)
        self.MONITOR_Y = "0.5 ," + str(float(self.ROOM_Y_MAX) - 0.5)
        self.MONITOR_Z = "-0.5, 2" #str(self.ROOM_Z_MIN + 0.5) + "," + str(self.ROOM_Z_MAX - 0.5)
        # Notes on sensor orientation. 
        # Default: (Yaw,Pitch) = (0,0) which points along the Y-axis.
        # Units: degrees.
        # Yaw: rotation around Z-axis (side-to-side). Clockwise is +ve.
        # Pitch: rotation around X-axis (up-down). Upwards is +ve.
        self.SENSOR_YAW = 0
        self.SENSOR_PITCH = 0
        self.SENSITIVITY = 1
        self.OCC_SENSITIVITY = 1

        # Entry config #
        self.ENTRY_FLAG = 0
        self.ENTRY_X = []
        self.ENTRY_Y = []

        # Bed config #
        self.BED_FLAG = 0
        self.BED_X = []
        self.BED_Y = []

        # Entry config #
        self.CHAIR_FLAG = 0
        self.CHAIR_X = []
        self.CHAIR_Y = []

    def config_dim(self, radar_dim):
        if radar_dim == 3:
            self.config_radar = [
                "dfeDataOutputMode 1",  # 0
                "channelCfg 15 7 0",
                "adcCfg 2 1",
                "adcbufCfg -1 0 1 1 1",
                "lowPower 0 0",
                "bpmCfg -1 1 0 2",  # 5
                "profileCfg 0 60.75 30.00 25.00 59.10 0 0 54.71 1 96 2950.00 2 1 36 ",
                "chirpCfg 0 0 0 0 0 0 0 5",
                "chirpCfg 1 1 0 0 0 0 0 2",
                "chirpCfg 2 2 0 0 0 0 0 5",
                "frameCfg 0 2 48 0 55.00 1 0",  # 10
                "dynamicRACfarCfg -1 4 4 2 2 8 12 4 8 5.00 8.00 0.40 1 1",
                "staticRACfarCfg -1 6 2 2 2 8 8 6 4 5.00 15.00 0.30 0 0",
                "dynamicRangeAngleCfg -1 0.75 0.0010 1 0",
                "dynamic2DAngleCfg -1 1.5 0.0300 1 0 1 0.30 0.85 8.00",
                "staticRangeAngleCfg -1 0 8 8", # 15
                "fineMotionCfg -1 1",
                "antGeometry0 0 -1 -2 -3 -2 -3 -4 -5 -4 -5 -6 -7",
                "antGeometry1 -1 -1 -1 -1 0 0 0 0 -1 -1 -1 -1",
                "antPhaseRot 1 1 1 1 1 1 1 1 1 1 1 1",
                "fovCfg -1 70.0 20.0",  # 20
                "compRangeBiasAndRxChanPhase 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0",
                "staticBoundaryBox -2 2 2 5.5 0 3",
                "boundaryBox -2.5 2.5 0.5 6 0 3",
                "sensorPosition 1.2 0 0",
                "gatingParam 3 2 2 2 4",    # 25
                "stateParam 20 3 200 500 50 6000",
                "allocationParam 80 200 0.1 40 0.5 20",
                "maxAcceleration 0.1 0.1 0.1",
                "trackingCfg 1 2 800 20 46 96 55",
                "presenceBoundaryBox -4 4 0.5 6 0 3",   # 30
                "sensorStart"
                ]
        else:
            self.config_radar = [
                "dfeDataOutputMode 1",
                "channelCfg 15 5 0",
                "adcCfg 2 1",
                "adcbufCfg 0 1 1 1",
                "profileCfg 0 62.00 30 10 69.72 0 0 28.42 1 128 2180 0 0 24",
                "chirpCfg 0 0 0 0 0 0 0 1",
                "chirpCfg 1 1 0 0 0 0 0 4",
                "frameCfg 0 1 128 0 50 1 0",
                "lowPower 0 0",
                "guiMonitor 1 1 1 1",
                "cfarCfg 6 4 4 4 4 8 12 4 8 20 33 0",
                "doaCfg 600 666 30 1 1 1 300 4 2",
                "AllocationParam 0 200 0.1 15 0.5 20",
                "GatingParam 3 1.5 1.5 0",
                "StateParam 3 3 10 1200 5 12000",
                "SceneryParam -5 5 0.25 10",
                "FilterParam 2.0 0.5 1.5",
                "trackingCfg 1 2 300 15 67 105 50 90",
                "classifierCfg 1 1 3 500 0.8 1.0 0.95 10",
                "sensorStart"
                ]

    def receive_config(self, raw):
        if self.cfg_idx == 0:
            self.config_radar = []
        if self.cfg_idx < len(self.config_radar):
            self.config_radar[self.cfg_idx] = raw
        else:
            self.config_radar.append(raw)
        if raw == "sensorStart":
            self.cfg_idx = 0
            self.cfg_sensorStart = 1
        else:
            self.cfg_idx+=1

        if "boundaryBox" in raw:
            temp = raw[len("boundaryBox")+1:]
            temp = temp.split(" ")

            self.ROOM_X_MIN = temp[0].strip()
            self.ROOM_X_MAX = (temp[1]).strip()
            self.ROOM_Y_MIN = (temp[2]).strip()
            self.ROOM_Y_MAX = (temp[3]).strip()
            self.ROOM_Z_MIN = (temp[4]).strip()
            self.ROOM_Z_MAX = (temp[5]).strip()

        if "staticBoundaryBox" in raw:
            temp = raw[len("staticBoundaryBox")+1:]
            temp = temp.split(" ")

            self.MONITOR_X = temp[0].strip() + "," + temp[1].strip()
            self.MONITOR_Y = temp[2].strip() + "," + temp[3].strip()
            self.MONITOR_Z = temp[4].strip() + "," + temp[5].strip()


# Parse updated sensor configuration file #
def parse_config(config_file, EntryWays, rcp, cp, rate_unit = 0.5):
    ## ~~~~~~~ UPDATE CONFIGURATION ~~~~~~~ ##
    #rcp = ndns_fns.radar_config_params()
    #ndns_fns.rcp = ndns_fns.radar_config_params()

    if config_file is None:
        nodens.logger.warning('No config file. Default values used.')
    elif config_file.is_file():
        config = configparser.RawConfigParser()
        config.read(config_file)
        nodens.logger.debug(config['Sensor target']['SENSOR_ID'])

        # Sensor target #
        rcp.SENSOR_ROOT = (get_config(config,'Sensor target', rcp.SENSOR_ROOT, 'ROOT_ID'))
        rcp.SENSOR_TARGET = (get_config(config,'Sensor target', rcp.SENSOR_TARGET, 'SENSOR_ID'))
        try:
            rcp.SENSOR_TOPIC = config.get('Sensor target', 'SENSOR_TOPIC').partition('#')[0]  
        except:
            rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'
            nodens.logger.debug('{} not specified in config file. Default value used: {}'.format('SENSOR_TOPIC', rcp.SENSOR_TOPIC))
        else:
            rcp.SENSOR_TOPIC = config.get('Sensor target', 'SENSOR_TOPIC').partition('#')[0].rstrip()
        if not bool(rcp.SENSOR_TOPIC):
            rcp.SENSOR_TOPIC = '#'
        nodens.logger.debug('Topic = {}'.format(rcp.SENSOR_TOPIC))

        # Scanning config #
        rcp.SCAN_TIME = float(get_config(config,'Scanning config', rcp.SCAN_TIME, 'SCAN_TIME'))
        rcp.FULL_DATA_FLAG = int(get_config(config,'Scanning config', rcp.FULL_DATA_FLAG, 'FULL_DATA_FLAG'))
        rcp.FULL_DATA_TIME = float(get_config(config,'Scanning config', rcp.FULL_DATA_TIME, 'FULL_DATA_TIME'))

        # Radar config #
        rcp.RADAR_SEND_FLAG = int(get_config(config,'Radar config', rcp.RADAR_SEND_FLAG, 'RADAR_SEND_FLAG'))
        rcp.ROOM_X_MIN = (get_config(config,'Radar config', rcp.ROOM_X_MIN, 'ROOM_X_MIN'))
        rcp.ROOM_X_MAX = (get_config(config,'Radar config', rcp.ROOM_X_MAX, 'ROOM_X_MAX'))
        rcp.ROOM_Y_MIN = (get_config(config,'Radar config', rcp.ROOM_Y_MIN, 'ROOM_Y_MIN'))
        rcp.ROOM_Y_MAX = (get_config(config,'Radar config', rcp.ROOM_Y_MAX, 'ROOM_Y_MAX'))
        rcp.ROOM_Z_MIN = (get_config(config,'Radar config', rcp.ROOM_Z_MIN, 'ROOM_Z_MIN'))
        rcp.ROOM_Z_MAX = (get_config(config,'Radar config', rcp.ROOM_Z_MAX, 'ROOM_Z_MAX'))
        rcp.MONITOR_X = (get_config(config,'Radar config', rcp.MONITOR_X, 'MONITOR_X'))
        rcp.MONITOR_Y = (get_config(config,'Radar config', rcp.MONITOR_Y, 'MONITOR_Y'))
        rcp.MONITOR_Z = (get_config(config,'Radar config', rcp.MONITOR_Z, 'MONITOR_Z'))
        rcp.SENSOR_YAW = float(get_config(config,'Radar config', rcp.SENSOR_YAW, 'SENSOR_YAW'))
        rcp.SENSOR_PITCH = float(get_config(config,'Radar config', rcp.SENSOR_PITCH, 'SENSOR_PITCH'))
        rcp.SENSITIVITY = (get_config(config,'Radar config', rcp.SENSITIVITY, 'SENSITIVITY'))
        rcp.OCC_SENSITIVITY = (get_config(config,'Radar config', rcp.OCC_SENSITIVITY, 'OCC_SENSITIVITY'))

        # Entry config #
        rcp.ENTRY_FLAG = int(get_config(config,'Entry config', rcp.ENTRY_FLAG, 'ENTRY_FLAG'))
        rcp.ENTRY_X = get_config(config,'Entry config', rcp.ENTRY_X, 'ENTRY_X')
        rcp.ENTRY_Y = get_config(config,'Entry config', rcp.ENTRY_Y, 'ENTRY_Y')
  
    else:
        nodens.logger.warning('No config file. Default values used.')

    # Check sensor version and update config #
    #sv.request(client, rcp.SENSOR_TOPIC, rcp.SENSOR_TARGET)
    sendCMDtoSensor.request_version(rcp,cp,sv)
    if len(rcp.config_radar) == 0:
        rcp.config_dim(sv.radar_dim)
    
    # Parse Publish rates to payload #
    # rate_unit = Baseline data transmission rate
    config_pub_rate = "CMD: PUBLISH RATE: " + str(round(rcp.SCAN_TIME/rate_unit))
    payload_msg = [{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_pub_rate + "\n"}]

    if rcp.FULL_DATA_FLAG:
        config_full_data = "CMD: FULL DATA ON. RATE: " + str(max(1,rcp.FULL_DATA_TIME/rcp.SCAN_TIME))
        print(f"\nrate_unit: {rate_unit}s. SCAN TIME: {rcp.SCAN_TIME}s. PUBLISH RATE: {str(round(rcp.SCAN_TIME/rate_unit))}. FULL DATA RATE: {str(max(1,rcp.FULL_DATA_TIME/rcp.SCAN_TIME))}.\n")
    else:
        config_full_data = "CMD: FULL DATA OFF."
        print(f"\nrate_unit: {rate_unit}s. SCAN TIME: {rcp.SCAN_TIME}s. PUBLISH RATE: {str(round(rcp.SCAN_TIME/rate_unit))}. FULL DATA OFF.\n")
        
    payload_msg.append({ "addr" : [rcp.SENSOR_TARGET],
                    "type" : "json",
                    "data" : config_full_data + "\n"})
        
    # Send radar config #
    if rcp.RADAR_SEND_FLAG:
        # Occupant tracker sensitivity #
        # NOTE: only implemented for 2D so far
        if sv.radar_dim == 2:
            param_temp = rcp.config_radar[12].split(" ")
            param_temp[1] = str(round(np.exp(1.8/float(rcp.OCC_SENSITIVITY)+2.1)))
            param_temp[2] = str(round(np.exp(0.7/float(rcp.OCC_SENSITIVITY)+5.3)))
            param_temp[4] = str(round(np.exp(0.7/float(rcp.OCC_SENSITIVITY)+2)))
            rcp.config_radar[12] = " ".join(param_temp)
            nodens.logger.debug(rcp.config_radar[12])

        # Radar sensitivity #
        if sv.radar_dim == 2:
            param_temp = rcp.config_radar[10].split(" ")
            param_temp[10] = str(round(np.exp(0.7/float(rcp.SENSITIVITY)+2.3)))
            param_temp[11] = str(round(np.exp(0.5/float(rcp.SENSITIVITY)+3)))
            rcp.config_radar[10] = " ".join(param_temp)
            nodens.logger.debug(rcp.config_radar[10])
         
        # Room size #
        if sv.radar_dim == 2:
            param_temp = rcp.config_radar[15].split(" ")
            param_temp[1:5] = [str(rcp.ROOM_X_MIN), str(rcp.ROOM_X_MAX), str(rcp.ROOM_Y_MIN), str(rcp.ROOM_Y_MAX)]
            rcp.config_radar[15] = " ".join(param_temp)
            nodens.logger.debug(rcp.config_radar[15])
        elif sv.radar_dim == 3:
            # Static - 22
            i = 0
            while True:
                if i == len(rcp.config_radar):
                    nodens.logger.warning("Config error: {} not found!)".format("staticBoundaryBox "))
                    break
                elif "staticBoundaryBox " in rcp.config_radar[i]:  
                    param_temp = rcp.config_radar[i].split(" ")
                    temp_x = rcp.MONITOR_X.split(',')
                    temp_y = rcp.MONITOR_Y.split(',')
                    temp_z = rcp.MONITOR_Z.split(',')
                    param_temp[1:7] = [temp_x[0], temp_x[1], temp_y[0], temp_y[1], temp_z[0], temp_z[1]]
                    rcp.config_radar[i] = " ".join(param_temp)
                    nodens.logger.debug(rcp.config_radar[i])
                    break
                else:
                    i+=1
                    

            # Boundary - 23
            i = 0
            print("len:{}.".format(len(rcp.config_radar)))
            while True:
                if i == len(rcp.config_radar):
                    nodens.logger.warning("Config error: {} not found!)".format("boundaryBox "))
                    break
                elif "boundaryBox " in rcp.config_radar[i]:  
                    print("len:{}. cfg:{}".format(len(rcp.config_radar),rcp.config_radar[i]))
                    param_temp = rcp.config_radar[i].split(" ")
                    param_temp[1:7] = [str(rcp.ROOM_X_MIN), str(rcp.ROOM_X_MAX), str(rcp.ROOM_Y_MIN), str(rcp.ROOM_Y_MAX), str(rcp.ROOM_Z_MIN), str(rcp.ROOM_Z_MAX)]
                    rcp.config_radar[i] = " ".join(param_temp)
                    nodens.logger.debug(rcp.config_radar[i])
                    break
                else:
                    i+=1

            # Presence - 30 (use bed if on, or static boundary otherwise)
            i = 0
            while True:
                if i == len(rcp.config_radar):
                    nodens.logger.warning("Config error: {} not found!)".format("presenceBoundaryBox "))
                    break
                elif "presenceBoundaryBox " in rcp.config_radar[i]:  
                    param_temp = rcp.config_radar[i].split(" ")
                    temp_x = rcp.MONITOR_X.split(',')
                    temp_y = rcp.MONITOR_Y.split(',')
                    temp_z = rcp.MONITOR_Z.split(',')
                    param_temp[1:7] = [temp_x[0], temp_x[1], temp_y[0], temp_y[1], temp_z[0], temp_z[1]]
                    rcp.config_radar[i] = " ".join(param_temp)
                    nodens.logger.debug(rcp.config_radar[i])
                    break
                else:
                    i+=1
            
        # Parse config to payload #
        for i in range(len(rcp.config_radar)):
            payload_msg.append({ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : rcp.config_radar[i] + "\n"})


        payload_msg.append({ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : "CMD: TI RESET" + "\n"})

    # Update entry points #
    if rcp.ENTRY_FLAG:
        # Check for sensor id
        if (rcp.SENSOR_TARGET not in EntryWays.id):
            EntryWays.id.append(rcp.SENSOR_TARGET)
            EntryWays.x.append([])
            EntryWays.y.append([])
            EntryWays.count.append(0)
        sen_idx = EntryWays.id.index(rcp.SENSOR_TARGET)

        temp = rcp.ENTRY_X
        temp = temp.split(';')
        temp_parse = []
        for i in range(len(temp)):
            temp_split = temp[i].split(',')
            if len(temp_split) == 2:
                (temp_parse.append(float(temp_split[0])))
                (temp_parse.append(float(temp_split[1])))
                nodens.logger.debug('Entryway x: {},{}.'.format(float(temp_split[0]),float(temp_split[1])))
            else:
                nodens.logger.warning('WARNING! Incorrect format provided: {}. Format should be two numbers separated with a comma, e.g. \'-1,1\''.format(temp[i]))
        EntryWays.x[sen_idx] = temp_parse

        temp = rcp.ENTRY_Y
        temp = temp.split(';')
        temp_parse = []
        for i in range(len(temp)):
            temp_split = temp[i].split(',')
            if len(temp_split) == 2:
                (temp_parse.append(float(temp_split[0])))
                (temp_parse.append(float(temp_split[1])))
                nodens.logger.debug('Entryway y: {},{}.'.format(float(temp_split[0]),float(temp_split[1])))
            else:
                nodens.logger.warning('WARNING! Incorrect format provided: {}. Format should be two numbers separated with a comma, e.g. \'-1,1\''.format(temp[i]))
        EntryWays.y[sen_idx] = temp_parse

    # OUTPUT #
    return(payload_msg,rcp,EntryWays)

# Store current mesh state #
class SensorMesh:
    def __init__(self):
        self.sensor_id = []  # ID of all connected sensors
        self.root_id = []    # ID of the root sensor
        self.last_time_connected = []    # timestamp of last detection
        self.layer_number = []   # Layer number
        self.room_id = []    # FUTURE: Room location
        self.site_id = []    # FUTURE: Site location
        self.user_id = []    # FUTURE: User that the sensor is assigned to

    # Update sensor mesh info
    # data - top level json data received via mqtt. Already checked that it's not the full data stream
    def update(self, data):
        addr = data["addr"]
        try:
            data_data = json.loads(base64.b64decode(data['data']))

            if addr in self.sensor_id:
                sens_idx = self.sensor_id.index(addr)
                self.sensor_id[sens_idx] = addr
                self.last_time_connected[sens_idx] = data_data["timestamp"]
                if "type" in data_data:
                    self.root_id[sens_idx] = data_data["root"]
                    self.layer_number[sens_idx] = data_data["layer"]

            else:
                self.sensor_id.append(addr)
                self.last_time_connected.append(data_data["timestamp"])
                if "type" in data_data:
                    self.root_id.append(data_data["root"])
                    self.layer_number.append(data_data["layer"])
                else:
                    self.root_id.append("")
                    self.layer_number.append("")

        except:
            nodens.logger.error("data: {}".format(data))

# OTA update for ESP #
def ota_esp(config_params):
    addr = config_params.SENSOR_ID

    payload_msg = [{ "addr" : [addr],
                        "type" : "json",
                        "data" : "CMD: UPGRADE ROOT" + "\n"}]

    return(payload_msg)


# Sensor info #
class SensorInfo:
    """Information on the connected sensors."""
    def __init__(self):
        self.connected_sensors = []     # List of all connected sensors
        self.num_occ = []               # Number of occupants per sensor
        self.max_occ = []               # Max occ per sensor
        self.last_occ = []              # Not used?
        self.last_t = []                # Time of last payload received
        self.period_t = []              # Time of last payload to Cloud
        self.period_N = []              # Num of frames received since last sent to Cloud
        self.period_sum_occ = []        # Sum of occupancies since last sent to Cloud
        self.period_max_occ = []        # Max occ since last sent to Cloud
        self.ew_period_sum_occ = []     # As above for entryways
        self.ew_period_max_occ = []     # As above for entryways

    def check(self, mqttData):
        addr = mqttData['addr']
        if isinstance(addr, list):
            addr = addr[0]
        if (addr not in self.connected_sensors):
            T = dt.datetime.now(dt.timezone.utc)
            self.connected_sensors.append(addr)
            self.num_occ.append(0)
            self.max_occ.append(0)
            self.last_occ.append(0)
            self.last_t.append(T)
            self.period_t.append(T)
            self.period_N.append(1)
            self.period_sum_occ.append(0)
            self.period_max_occ.append(0)
            self.ew_period_sum_occ.append(0)
            self.ew_period_max_occ.append(0)

        sen_idx = self.connected_sensors.index(addr)

        return(sen_idx)
    
    def update_short(self, sen_idx, T, mqttData):
        self.last_t[sen_idx] = T

        if ('Number of Occupants' in mqttData):
            self.num_occ[sen_idx] = mqttData['Number of Occupants']

             # Update max number of occupants
            if (self.num_occ[sen_idx] > self.max_occ[sen_idx]):
                self.max_occ[sen_idx] = self.num_occ[sen_idx]

    def update_full(self, sen_idx, T, sensor_data):
        self.last_t[sen_idx] = T

        self.num_occ[sen_idx] = sensor_data.track.num_tracks

        # Update max number of occupants
        if (self.num_occ[sen_idx] > self.max_occ[sen_idx]):
            self.max_occ[sen_idx] = self.num_occ[sen_idx]

    def update_refresh(self, sen_idx, send_idx_e, T, entryway):
        self.period_N[sen_idx] += 1
        self.period_sum_occ[sen_idx] += self.num_occ[sen_idx]
        self.ew_period_sum_occ[sen_idx] += entryway.count[send_idx_e]
        if (self.num_occ[sen_idx] > self.period_max_occ[sen_idx]):
            self.period_max_occ[sen_idx] = self.num_occ[sen_idx]
        if (entryway.count[send_idx_e] > self.ew_period_max_occ[sen_idx]):
            self.ew_period_max_occ[sen_idx] = entryway.count[send_idx_e]

    def cloud_send_refresh(self, sen_idx, send_idx_e, T, entryway):
        self.update_refresh(sen_idx, send_idx_e, T, entryway)

        self.period_t[sen_idx] = T
        self.period_N[sen_idx] = 1
        self.period_sum_occ[sen_idx] = self.num_occ[sen_idx]
        self.period_max_occ[sen_idx] = self.num_occ[sen_idx]
        self.ew_period_sum_occ[sen_idx] = entryway.count[send_idx_e]
        self.ew_period_max_occ[sen_idx] = entryway.count[send_idx_e]

    

# Sensor version #
class sensor_version:
    """Sensor version. Reads both the radar firmwave version and the ESP firmware version. This is used to determine which version of code to use."""
    def __init__(self):
        self.string = []
        self.wifi_version = []
        self.radar_version = []
        self.radar_dim = 3

    def parse(self, str):
        #TODO: update to provide more flexibility with string
        if len(str) > 0:
            self.string = str
            if str[0] == 'C':
                self.wifi_version = str[0:7]
            else:
                nodens.logger.debug("VERSIONING ERROR. Mismatched Wi-Fi version. Expected 'CXX...'. Detected %s.", str)
                self.radar_dim = 2
            if (str[8] == 'R' and str[10] == 'D'):
                self.radar_version = str[8:]
                temp = int(str[9])
                if (temp == 2 or temp == 3):
                    self.radar_dim = temp
                else:
                    nodens.logger.debug("VERSIONING ERROR. Mismatched RADAR dimensions. Expected '...RXD...'. Detected %s.", str)
            else:
                nodens.logger.debug("VERSIONING ERROR. Mismatched RADAR version. Expected 'RXD...' where X=2/3. Detected %s. Revert to 2D.", str)
                self.radar_dim = 2
            print(self.wifi_version, self.radar_version)
        else:
            nodens.logger.debug("VERSIONING ERROR. No version provided. Defaulting to 2D config.")
            self.radar_dim = 2
    def request(self, client, root_topic, sensor_target):

        print("trying request")
        json_message = { "addr" : [sensor_target],
                    "type" : "json",
                    "data" : "CMD: REQUEST VERSION" + "\n"}
        json_message = json.dumps(json_message)
        client.publish(root_topic, json_message)

        nodens.logger.debug("Published sensor version request")
        temp = 0
        while (1):
            if self.string != []:
                nodens.logger.debug("Version received. Version = {}. Dimensions = {}.".format(self.string, self.radar_dim))
                break
            elif temp < 20:
                nodens.logger.debug("Waiting... {}".format(self.string))
                temp += 1
                time.sleep(0.2)
            else:
                nodens.logger.debug("No response to version request. Continue...")
                break

# Entry way info #
class EntryWays:
    def __init__(self):
        self.id = [] # Sensor ID
        self.x = [] # Array of 2-pules, i.e [[xa1, xa2],[xb1,xb2],...]
        self.y = [] # Same as x
        self.count = [] # Integer vector

    def update(self,new_id):
        self.id.append(new_id) # Add a new sensor
        self.x.append([])
        self.y.append([])
        self.count.append(0)

# Occupant track history #
class OccupantHist:
    """Historical positions (X,Y) of occupants (tracks)."""
    def __init__(self, num_hist_frames=10, flag_time_based_record=0):
        """Initialises track histories"""
        self.sens_idx = []
        self.id = [] # track id
        self.x0 = [] # previous
        self.y0 = []
        self.x1 = [] # current
        self.y1 = []

        # Save inputs internally
        self.num_hist_frames = num_hist_frames
        self.flag_time_based_record = flag_time_based_record

        # History over last num_hist_frames
        self.xh = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=3) # record of last num_hist_frames values
        self.yh = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=3)

        # Energy statistics
        self.e_ud_h = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=2) # sd.ud.signature_energy
        self.e_pc_h = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=2) # sd.pc.energy

        # Activity statistics
        self.tot_dist = []  # Total distance moved over num_hist_frames
        self.max_dist = [] # Maximum movement over num_hist_frames
        self.flag_active = [] # Flag to identify whether occupant (track) is active or not (1 = active)
        self.time_inactive_start = []   # Time to mark start of inactive period

        # General inactivity stats per sensor
        self.most_inactive_track = []
        self.most_inactive_time = []

        # Prepare outputs
        self.outputs = self.Outputs()
        
    # Use this to refresh the histories
    def refresh(self, sensor_id):
        # Check for this specific sensor
        ind_s = self.sens_idx.index(sensor_id)

        self.id[ind_s] = [] 

        self.xh[ind_s] = np.empty([self.xh.shape[1],self.xh.shape[2]], dtype=object)
        self.yh[ind_s] = np.empty([self.yh.shape[1],self.yh.shape[2]], dtype=object)

        self.e_ud_h[ind_s] = np.empty([self.e_ud_h.shape[1]], dtype=object)
        self.e_pc_h[ind_s] = np.empty([self.e_pc_h.shape[1]], dtype=object)

        self.tot_dist[ind_s] = []
        self.max_dist[ind_s] = [] 
        self.flag_active[ind_s] = []
        self.time_inactive_start[ind_s] = [] 
    
    # Use this to update a track location everytime one is detected.
    def update(self, sensor_id, track_id=[], X=[], Y=[], sensor_data=[]):
        if (sensor_id in self.sens_idx):
            # Check for this specific sensor
            ind_s = self.sens_idx.index(sensor_id)

            if (track_id == []):
                pass
            elif (track_id in self.id[ind_s]):
                # Check for this specific track
                ind_t = self.id[ind_s].index(track_id)

                # Update coordinates
                self.x0[ind_s][ind_t] = self.x1[ind_s][ind_t]
                self.y0[ind_s][ind_t] = self.y1[ind_s][ind_t]
                self.x1[ind_s][ind_t] = X
                self.y1[ind_s][ind_t] = Y

                # Update location histories
                self.xh[ind_s][ind_t] = np.roll(self.xh[ind_s][ind_t],1)
                self.xh[ind_s][ind_t][0] = X
                self.yh[ind_s][ind_t] = np.roll(self.yh[ind_s][ind_t],1)
                self.yh[ind_s][ind_t][0] = Y

                # Update energy  - UD currently only has one sig. TODO: check tid and then find other sigs + don't forget to add to new_track
                if sensor_data != []:       # Process only if receiving full data packet.
                    self.e_ud_h[ind_s] = np.roll(self.e_ud_h[ind_s],1)
                    self.e_ud_h[ind_s][0] = sensor_data.ud.signature_energy
                    self.e_pc_h[ind_s] = np.roll(self.e_pc_h[ind_s],1)
                    self.e_pc_h[ind_s][0] = sensor_data.pc.energy[0]


                # Update activity statistics
                self.activity_detection(sensor_id, track_id)

            else:
                # Record new values if track did not previously exist
                #if track_id != []:
                self.new_track(sensor_id,track_id,X,Y,new_sensor_flag=0)
        else:
            self.new_sensor(sensor_id)
            if track_id != []:
                self.new_track(sensor_id,track_id,X,Y,new_sensor_flag=1)


    # Procedure to when a new track is detected
    def new_track(self,sensor_id,track_id,X,Y,new_sensor_flag):
        ind_s = self.sens_idx.index(sensor_id)
        # if new_sensor_flag == 0:
        self.id[ind_s].append(track_id)

        self.x0[ind_s].append(X)
        self.y0[ind_s].append(Y)
        self.x1[ind_s].append(X)
        self.y1[ind_s].append(Y)

        self.tot_dist[ind_s].append(0)
        self.max_dist[ind_s].append(0)
        self.flag_active[ind_s].append(1)   # By default mark them as active
        self.time_inactive_start[ind_s].append(dt.datetime.now(dt.timezone.utc))

        # else:
        #     # self.id.append([track_id])
        #     self.id[ind_s].append(track_id)

        #     self.x0.append([X])
        #     self.y0.append([Y])
        #     self.x1.append([X])
        #     self.y1.append([Y])

        #     self.tot_dist.append([0])
        #     self.max_dist.append([0])
        #     self.flag_active.append([1])    # By default mark them as active
        #     self.time_inactive_start.append([dt.datetime.now(dt.timezone.utc)])
        
        ind_t = self.id[ind_s].index(track_id)
        if ind_t > self.xh.shape[1]-1:
            new_track = np.empty((self.xh.shape[0],self.xh.shape[1],self.num_hist_frames),dtype=object)
            self.xh = np.concatenate((self.xh,new_track),axis=1)
            self.yh = np.concatenate((self.yh,new_track),axis=1)
        self.xh[ind_s][ind_t][0] = X
        self.yh[ind_s][ind_t][0] = Y
        
    # Proedure when a new sensor is detected
    def new_sensor(self,sensor_id):
        #self.max_tracks.append(0)
        self.sens_idx.append(sensor_id)
        self.most_inactive_track.append(None)
        self.most_inactive_time.append(None)
        if len(self.sens_idx) == 1:
            self.xh = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=3)
            self.yh = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=3)
            self.e_ud_h = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=2)
            self.e_pc_h = np.array(np.empty((self.num_hist_frames,),dtype=object), ndmin=2)
        else:
            new_sensor = np.empty((1,self.xh.shape[1],self.xh.shape[2]),dtype=object)
            self.xh = np.concatenate((self.xh,new_sensor),axis=0)
            self.yh = np.concatenate((self.yh,new_sensor),axis=0)
            new_sensor = np.empty((1,self.e_ud_h.shape[1]),dtype=object)
            self.e_ud_h = np.concatenate((self.e_ud_h,new_sensor),axis=0)
            self.e_pc_h = np.concatenate((self.e_pc_h,new_sensor),axis=0)

        self.id.append([])
        self.x0.append([])
        self.y0.append([])
        self.x1.append([])
        self.y1.append([])

        self.tot_dist.append([])
        self.max_dist.append([])
        self.flag_active.append([])    # By default mark them as active
        self.time_inactive_start.append([])
    
    # Use this to check entryways and see if anyone has entered/left the room
    def entryway(self, sensor_id, track_id, ew):
        if (sensor_id in ew.id):
            ind_s = self.sens_idx.index(sensor_id)
            ind_e = ew.id.index(sensor_id)
            ind_t = self.id[ind_s].index(track_id)
            [sx0,sx1] = [self.x0[ind_s][ind_t],self.x1[ind_s][ind_t]]
            [sy0,sy1] = [self.y0[ind_s][ind_t],self.y1[ind_s][ind_t]]
            
            try:
                if abs(sx0-sx1)+abs(sy0-sy1) > 0:
                    # if len(ew.x[ind_e]) == 0:
                    #     nodens.logger.debug('No entries defined')
                    for i in range(int(len(ew.x[ind_e])/2)):
                
                        [ex0,ex1] = [ew.x[ind_e][2*i],ew.x[ind_e][2*i+1]]
                        [ey0,ey1] = [ew.y[ind_e][2*i],ew.y[ind_e][2*i+1]]
                        t = ((sx0-ex0)*(ey0-ey1) - (sy0-ey0)*(ex0-ex1))/((sx0-sx1)*(ey0-ey1) - (sy0-sy1)*(ex0-ex1))
                        u = ((sx1-sx0)*(sy0-ey0) - (sy1-sy0)*(sx0-ex0))/((sx0-sx1)*(ey0-ey1) - (sy0-sy1)*(ex0-ex1))
                        if (0<=t<=1) and (0<=u<=1):
                            if (sx0**2 + sy0**2) > (sx1**2 + sy1**2):
                                ew.count[ind_e] += 1
                                nodens.logger.info('Entered room at entry {} with (t,u)=({},{}). Occupancy = {}.'.format(i,t,u,ew.count[ind_e]))
                            else:
                                ew.count[ind_e] -= 1
                                if ew.count[ind_e] < 0:
                                    ew.count[ind_e] = 0
                                    nodens.logger.warning('Warning! Count dropped below 0 and was reset.')
                                nodens.logger.info('Leaving room at entry {} with (t,u)=({},{}). Occupancy = {}.'.format(i,t,u,ew.count[ind_e]))
            except:
                nodens.logger.warning('Entryway update issue. (sx0,sx1)=({},{}). (sy0,sy1)=({},{})'.format(sx0,sx1,sy0,sy1))
    
    # Track activity/inactivity statistics
    def activity_detection(self, sensor_id, track_id, tot_dist_thresh=1, max_dist_thresh=1):
        ind_s = self.sens_idx.index(sensor_id)
        ind_t = self.id[ind_s].index(track_id)
        
        # Non-None values from history
        xh =  [val for i,val in enumerate(self.xh[ind_s][ind_t]) if val is not None]
        yh =  [val for i,val in enumerate(self.yh[ind_s][ind_t]) if val is not None]

        # Take oldest values
        xi = xh[-1]
        yi = yh[-1]

        # Calculate distances for each frame
        try:
            xd = np.subtract(xh[1:],xh[0:-1])
            yd = np.subtract(yh[1:],yh[0:-1])
            rd = (xd**2 + yd**2)**0.5

            # Find statistics
            self.tot_dist[ind_s][ind_t] =  np.sum(rd)
            self.max_dist[ind_s][ind_t] = np.max(rd)

            # Check if active
            if self.tot_dist[ind_s][ind_t] > tot_dist_thresh:
                self.flag_active[ind_s][ind_t] = 1
                #print("Active!)")
            elif self.max_dist[ind_s][ind_t] > max_dist_thresh:
                self.flag_active[ind_s][ind_t] = 1
                #print("Active!)")
            else:
                if (self.flag_active[ind_s][ind_t] == 1):
                    self.time_inactive_start[ind_s][ind_t] = dt.datetime.now(dt.timezone.utc)
                self.flag_active[ind_s][ind_t] = 0

        except Exception as e:
            nodens.logger.error(f"""Error {e.args}.""")
            #print("Inactive since {} for track: {} with dist: {}".format(self.time_inactive_start[ind_s][ind_t], track_id, self.tot_dist[ind_s][ind_t], self.max_dist[ind_s][ind_t]))

        # Calculate total energies for each frame
        # try:
        #     ud_e = [val for val in self.e_ud_h[ind_s][ind_t] if val is not None]
        #     print(f"ud: {ud_e}")


    # Calculate general activity statistics
    def sensor_activity(self, sensor_id):
        ind_s = self.sens_idx.index(sensor_id)
        inactive_tracks = [self.time_inactive_start[ind_s][i] for i,val in enumerate(self.flag_active[ind_s]) if val==0]
        if len(inactive_tracks) == 0:
            self.most_inactive_track[ind_s] = None
            self.most_inactive_time[ind_s] = None
        else:
            inactive_idx = min(range(len(inactive_tracks)), key=inactive_tracks.__getitem__)
            self.most_inactive_track[ind_s] = self.id[ind_s][inactive_idx]
            self.most_inactive_time[ind_s] = dt.datetime.now(dt.timezone.utc) - self.time_inactive_start[ind_s][inactive_idx]

    # Calculate outputs
    def calculate_outputs(self, thresh_distance = 0, energy_threshold = 0):
        # Re-initialise outputs
        self.outputs.__init__()

        for idx, sensor in enumerate(self.sens_idx):    # For each sensor
            if len(self.id[idx]) > 0:
                # Determine track to send
                if max(self.tot_dist[idx]) >= thresh_distance: # Distance threshold at 0 for now, until UD sig tid is found.
                    tid = self.tot_dist[idx].index(max(self.tot_dist[idx]))

                    self.outputs.track_id = self.id[idx][tid]

                    # Record parameters
                    self.outputs.track_X = self.x1[idx][tid]
                    self.outputs.track_Y = self.y1[idx][tid]
                    self.outputs.distance_moved = self.tot_dist[idx][tid]

                    # Energy statistics (for scene not track)
                    ud_e = [val for val in self.e_ud_h[idx] if val is not None]
                    self.outputs.ud_energy = sum(ud_e)
                    if self.outputs.ud_energy > energy_threshold:
                        self.outputs.was_active = 1
                    else:
                        self.outputs.was_active = 0
                    pc_e = [val for val in self.e_pc_h[idx] if val is not None]
                    self.outputs.pc_energy = sum(pc_e)
                else:
                    pass
                    #tid = self.ud_energy[idx].index(max(self.ud_energy[idx]))
                    


    
    # Class to define outputs
    class Outputs:
        def __init__(self) -> None:
            self.track_id = []  # tid with highest distance walked, or if under threshold then highest energy
            self.track_X = []   # corresponding location for tid
            self.track_Y = []
            self.distance_moved = []   # total distance moved
            self.was_active = []        # check if ud_energy over threshold
            self.ud_energy = []
            self.pc_energy = []

        
                    
                
        



class RX_Data:
    def __init__(self, header, data):
        self.header = header
        self.data = data
        
    def frame_num(self):
        self.frame_num = self.header[24] + 256*self.header[25] + 65536*self.header[26] + 16777216*self.header[27]

        
class point_cloud:
    """An old point cloud TLV"""
    def __init__(self,raw):
        self.num_obj = int((np.uint8(raw[4:8]).view(np.uint32) - 8 - 16)/6)
        self.angle_unit = np.array(raw[8:12], dtype='uint8').view('<f4')
        self.dopp_unit = np.array(raw[12:16], dtype='uint8').view('<f4')
        self.rng_unit = np.array(raw[16:20], dtype='uint8').view('<f4')
        self.snr_unit = np.array(raw[20:24], dtype='uint8').view('<f4')
        
        self.angle = []
        self.dopp = []
        self.rng = []
        self.snr = []
        for i in range(self.num_obj):
            self.angle.append(np.int8(raw[24 + 6*i]) * self.angle_unit)
            self.dopp.append(np.int8(raw[25 + 6*i]) * self.dopp_unit)
            self.rng.append(np.uint8(raw[(26+6*i):(28+6*i)]).view(np.uint16) * self.rng_unit)
            self.snr.append(np.uint8(raw[(28+6*i):(30+6*i)]).view(np.uint16) * self.snr_unit)
        
        self.X = self.rng * np.sin(np.deg2rad(self.angle))
        self.Y = self.rng * np.cos(np.deg2rad(self.angle))

class point_cloud_3D_new:
    """Point cloud 3D TLV, parsed based on firmware version."""
    def __init__(self,raw,radar_version='R3D001B'):
        # Version check: is SNR in TLV
        if radar_version == 'R3D002A':
            flag_snr = True
        else:
            flag_snr = False

        if len(raw) == 0:
            self.num_obj = 0
        else:
            if flag_snr:
                self.num_obj = int((np.uint8(raw[4:8]).view(np.uint32) - 8 - 20)/8)
            else:
                self.num_obj = int((np.uint8(raw[4:8]).view(np.uint32) - 8 - 16)/6)

        self.elev_unit = np.array(raw[8:12], dtype='uint8').view('<f4')
        self.azim_unit = np.array(raw[12:16], dtype='uint8').view('<f4')
        self.dopp_unit = np.array(raw[16:20], dtype='uint8').view('<f4')
        self.rng_unit = np.array(raw[20:24], dtype='uint8').view('<f4')
        
        self.elev = []
        self.azim = []
        self.dopp = []
        self.rng = []

        if flag_snr == True:
            self.snr_unit = np.array(raw[24:28], dtype='uint8').view('<f4')
            self.snr = []
            j = 28
            J = 8
        else:
            j = 24
            J = 6

        
        for i in range(self.num_obj):
            self.elev.append(np.int8(raw[j+J*i]) * self.elev_unit)
            self.azim.append(np.int8(raw[j+1+J*i]) * self.azim_unit)
            self.dopp.append(np.uint8(raw[(j+2+J*i):(j+4+J*i)]).view(np.int16) * self.dopp_unit)
            self.rng.append(np.uint8(raw[(j+4+J*i):(j+6+J*i)]).view(np.uint16) * self.rng_unit)
            if flag_snr == True:
                self.snr.append(np.uint8(raw[(j+6+J*i):(j+8+J*i)]).view(np.uint16) * self.snr_unit)
        
        self.X = self.rng * np.sin((self.azim)) * np.cos((self.elev))
        self.Y = self.rng * np.cos((self.azim)) * np.cos((self.elev))
        self.Z = self.rng * np.sin((self.elev))

        self.energy = np.sqrt(sum([val**2 for val in self.dopp]))

        
    

class PointCloudHistory:
    """This class stores the point cloud history over the last num_hist_frames frames.
    Each frame is composed of arrays of X,Y,Z spatial coordinates, and an array of Doppler values."""

    # TODO: define number of frames to store (currently set as 3)
    def __init__(self,num_hist_frames=10):
        """Initialises the point cloud histories."""
        self.X = np.array(np.empty((num_hist_frames,),dtype=object), ndmin=1)
        self.Y = np.array(np.empty((num_hist_frames,),dtype=object), ndmin=1)
        self.Z = np.array(np.empty((num_hist_frames,),dtype=object), ndmin=1)
        self.dopp = np.array(np.empty((num_hist_frames,),dtype=object), ndmin=1)
        self.num_pnts = np.array(np.empty((num_hist_frames,),dtype=object), ndmin=1)

    def update_history(self,pc):
        """Updates the point cloud history with the latest point cloud measurements."""
        # circular buffer
        self.X = np.roll(self.X, 1)
        self.Y = np.roll(self.Y, 1)
        self.Z = np.roll(self.Z, 1)
        self.dopp = np.roll(self.dopp, 1)
        self.num_pnts = np.roll(self.num_pnts, 1)

        # Update most recent frame
        self.X[0] = pc.X
        self.Y[0] = pc.Y
        self.Z[0] = pc.Z
        self.dopp[0] = pc.dopp
        self.num_pnts[0] = pc.num_obj
        
class track:
    """Track data. Tracks are typically room occupants."""
    def __init__(self, raw, version=3.112):
        self.tid = []
        self.X = []
        self.Y = []

        if np.floor(version) == 3:
            self.Z = []
        if len(raw) == 0:
            self.num_tracks = 0
        else:
            if np.floor(version) == 2:
                tlv_len = 68
            elif version == 3.40:
                tlv_len = 40
            elif version == 3.112:
                tlv_len = 112
            self.num_tracks = int((np.uint8(raw[4:8]).view(np.uint32) - 8)/tlv_len)

            for i in range(self.num_tracks):
                self.tid.append(np.uint8(raw[(8+tlv_len*i):(12+tlv_len*i)]).view(np.uint32)[0])
                self.X.append(np.uint8(raw[(12+tlv_len*i):(16+tlv_len*i)]).view('<f4')[0])
                self.Y.append(np.array(raw[(16+tlv_len*i):(20+tlv_len*i)], dtype='uint8').view('<f4')[0])
                if np.floor(version) == 3:
                    self.Z.append(np.uint8(raw[(20+tlv_len*i):(24+tlv_len*i)]).view('<f4')[0])

class PresenceDetect:
    """Processes radar TLV related to presence detction"""
    def __init__(self) -> None:
        self.present = 0
        self.tlv_len = []

    def process(self, raw):
        self.tlv_len = np.uint8(raw[4:8]).view(np.uint32)[0]
        self.present = raw[8]

class sensorTimeSeries:
    def __init__(self):
        self.frame = []
        self.packet_len = []
        self.num_tlv = []
        self.num_pnts = []
        self.num_tracks = []

        # Some stats
        self.count = 0
        self.total_frame_drop = 0
        self.min_frame_drop = 100000
        self.max_frame_drop = 0
        self.avg_frame_drop = 0

    def update(self, sensor_data, max_time_samples = 0):
        self.frame.append(sensor_data.frame)
        self.packet_len.append(sensor_data.packet_len)
        self.num_tlv.append(sensor_data.num_tlv)
        self.num_pnts.append(sensor_data.pc.num_obj)
        self.num_tracks.append(sensor_data.track.num_tracks)

        self.count += 1
        if self.count > 1:
            try:
                if isinstance(self.frame[-1], (float, int)) and isinstance(self.frame[-2], (float, int)):
                    if self.frame[-1] > self.frame[-2]:
                        frame_drop = self.frame[-1] - self.frame[-2]
                        self.total_frame_drop += frame_drop

                        if frame_drop > self.max_frame_drop:
                            self.max_frame_drop = frame_drop
                        
                        if frame_drop < self.min_frame_drop:
                            self.min_frame_drop = frame_drop

                        self.avg_frame_drop = self.total_frame_drop / self.count

                    else:
                        print(f"Frames no sequential. frame -1: {self.frame[-1]}. frame -2: {self.frame[-2]}")
                else:
                    print(f"Frames not a number. frame -1: {self.frame[-1]}. frame -2: {self.frame[-2]}")
            except:
                print(f"Frame count error {self.frame[-1]} {self.frame[-2]} {isinstance(self.frame[-1], (float, int))}")


        if max_time_samples < 0:
            print("WARNING: max_time_samples (= {}) must be greater than 0. Setting to 0.")
        elif max_time_samples > 0:
            if len(self.frame) > max_time_samples:
                self.frame = self.frame[1:]
                self.packet_len = self.packet_len[1:]
                self.num_tlv = self.num_tlv[1:]
                self.num_pnts = self.num_pnts[1:]
                self.num_tracks = self.num_tracks[1:]


class VitalSigns:
    """Storage of vital signs data."""
    def __init__(self, num_hist_samples = 100):
        self.heart_rate_raw = [None] * num_hist_samples
        self.breathing_rate_raw = [None] * num_hist_samples
        self.breathing_deviation = [None] * num_hist_samples
        self.heart_vote = [None] * num_hist_samples
        self.breathing_vote = [None] * num_hist_samples
        self.X = []
        self.Y = []
        self.heart_waveform = [None] * 95
        self.breathing_waveform = [None] * 95
        self.heart_rate = []
        self.breathing_rate = []
        self.heart_msg = ''
        self.breathing_msg = ''

    def update(self, raw):
        # Calculate target position
        r_res = 0.06
        a_res = 0.001
        r_idx = np.uint8(raw[(28):(30)]).view(np.uint16)[0]
        a_idx = np.uint8(raw[(30):(32)]).view(np.uint16)[0]
        X = r_idx*r_res * np.sin(a_idx*a_res)
        Y = r_idx*r_res * np.cos(a_idx*a_res)

        # Check (via proximity) if it's the previous target. If not, re-initialise
        # TODO: record tid on sensor
        if self.X != []:
            if (np.sqrt((X-self.X)**2 + (Y-self.Y)**2)) > 1:
                nodens.logger.debug("RESET VS: {}".format((np.sqrt((X-self.X)**2 + (Y-self.Y)**2))))
                self.__init__()
        
        # Roll history data through circular buffer
        self.heart_rate_raw = np.roll(self.heart_rate_raw, 1)
        self.breathing_rate_raw = np.roll(self.breathing_rate_raw, 1)
        self.breathing_deviation = np.roll(self.breathing_deviation, 1)
        self.heart_vote = np.roll(self.heart_vote, 1)
        self.breathing_vote = np.roll(self.breathing_vote, 1)

        # Get values
        self.X = X
        self.Y = Y
        self.heart_rate_raw[0] = np.uint8(raw[(8):(12)]).view('<f4')[0]
        self.breathing_rate_raw[0] = np.uint8(raw[(12):(16)]).view('<f4')[0]
        self.breathing_deviation[0] = np.uint8(raw[(16):(20)]).view('<f4')[0]
        self.heart_vote[0] = np.uint8(raw[20:24]).view('<f4')[0]
        self.breathing_vote[0] = np.uint8(raw[24:28]).view('<f4')[0]
        for i in range(95):
            temp = np.uint8(raw[(32+4*i):(36+4*i)]).view('<f4')[0]
            self.heart_waveform[i] = temp
            temp = np.uint8(raw[(412+4*i):(416+4*i)]).view('<f4')[0]
            self.breathing_waveform[i] = temp

        # Calculate values and Set messages
        if self.heart_rate_raw[0] != None:
            self.heart_rate = np.median([i for i in self.heart_rate_raw[0:10] if i != None])
            nodens.logger.debug(self.heart_rate, self.heart_rate_raw[0])
            if self.heart_rate_raw[0] - self.heart_rate > 8:
                self.heart_rate = self.heart_rate_raw[0]
            self.heart_msg = "Heart rate: {:.1f}".format(self.heart_rate)
            nodens.logger.info(self.heart_msg)
        else:
            self.heart_msg = "No heart rate detected"

        if self.breathing_rate_raw[0] != None:
            self.breathing_rate = np.median([i for i in self.breathing_rate_raw[0:10] if i != None])
            if self.breathing_rate_raw[0] - self.breathing_rate > 5:
                self.breathing_rate = self.breathing_rate_raw[0]

            if self.breathing_deviation[0] == 0:
                self.breathing_msg = "No presence detected"
            elif self.breathing_deviation[0] < 0.02:
                self.breathing_msg = "Holding breath!"
            else:
                self.breathing_msg = "Breathing rate: {:.1f}".format(self.breathing_rate)
        else:
            self.breathing_msg = "No breathing rate detected"


class MicroDoppler:
    """Micro-Doppler (UD) parameters and signatures."""
    def __init__(self):
        self.tid = []
        self.num_pnts = []
        self.azim = self.udFrameParam()
        self.elev = self.udFrameParam()
        self.range = self.udFrameParam()
        self.dopp = self.udFrameParam()
        self.z = self.udFrameParam()
        self.signature_energy = 0

    def signature(self, raw, Nud, spec_length, Nchirps):
        #TODO: add number of targets
        # check number of chirps compared to fft length
        if Nchirps > spec_length:
            Nchirps = spec_length
            nodens.logger.warning("Nchirps should be <= spec_length")

        # Check number of points
        
        # Save signature
        output = np.zeros([Nchirps,Nud])
        for i in range(Nchirps):
            for j in range(Nud):
                output[i,j] = raw[i + j*spec_length + 24]
        for j in range(Nud):
            if sum(output[:,j]) == 255*Nchirps:
                output[:,j] = 0*output[:,j]
        output = np.fft.fftshift(output, axes=0)
        #print(output)

        return output

    def calculate_sig_energy(self,ud_sig):
        self.signature_energy = np.sum(ud_sig)

    def parameters(self,raw):
        # General
        self.num_pnts = convert_4_to_1(raw[12:14])

        # Azimuth
        self.azim.mean = 0.01*180/np.pi*convert_uint_to_int(raw[14])
        self.azim.high_freq_env = self.azim.mean+0.01*180/np.pi*(raw[15])
        self.azim.low_freq_env = self.azim.mean-0.01*180/np.pi*(raw[16])
        #self.azim.maxmin()

        # Elevation
        self.elev.mean = 0.01*180/np.pi*convert_uint_to_int(raw[17])
        self.elev.high_freq_env = self.elev.mean+0.01*180/np.pi*(raw[18])
        self.elev.low_freq_env = self.elev.mean-0.01*180/np.pi*(raw[19])
        #self.elev.maxmin()

        # Range
        self.range.mean = 0.00025*convert_4_to_1(raw[20:22])
        self.range.high_freq_env = self.range.mean+0.00025*convert_4_to_1(raw[22:24])
        self.range.low_freq_env = self.range.mean-0.00025*convert_4_to_1(raw[24:26])
        #self.range.maxmin()

        # Doppler
        self.dopp.mean = 0.00028*convert_uint_to_int(raw[26:28])
        self.dopp.high_freq_env = self.dopp.mean+0.00028*convert_4_to_1(raw[28:30])
        self.dopp.low_freq_env = self.dopp.mean-0.00028*convert_4_to_1(raw[30:32])
        #self.dopp.maxmin()

        # Z
        self.z.mean = self.range.mean * np.sin(np.deg2rad(self.elev.mean))
        self.z.high_freq_env = self.range.high_freq_env * np.sin(np.deg2rad(self.elev.high_freq_env))
        self.z.low_freq_env = self.range.low_freq_env * np.sin(np.deg2rad(self.elev.low_freq_env))


    class udFrameParam:
        def __init__(self):
            self.mean = []
            self.high_freq_env = []
            self.low_freq_env = []


class udFrameParam:
    def __init__(self):
        self.mean = []
        self.hf = []
        self.lf = []

    #def maxmin(self):
    #    self.max = self.mean + self.high_freq_env
    #    self.min = self.mean + self.low_freq_env

class paramMaxMin:
    def __init__(self):
        self.max = 0
        self.min = 10000
        self.sum = 0
        

class paramHfLf:
    def __init__(self):
        self.hf = []
        self.lf = []

        x = [p for p in vars(self)]
        for i in range(len(x)):
            setattr(self,x[i],paramMaxMin())

class udHistParam:
    """Micro-Doppler parameters processed over a defined number of frames (previous are single-frame)."""
    def __init__(self, num_frames):
        self.count = 0
        self.num_pnts = 0
        self.azim = udFrameParam()
        self.elev = udFrameParam()
        self.range = udFrameParam()
        self.dopp = udFrameParam()

        # Initialise each measured object (azim,elev,range,dopp)
        x = [p for p in vars(self)]
        for i in range(2,len(x)):
            setattr(self,x[i],paramHfLf())

    def update(self,udParam, num_frames):
        # azim, elev, range, dopp
        x = [p for p in vars(self)]
        print("********\n",x)
        for i in range(2,len(x)):
            # mean, hf, lf
            y = [p for p in vars(getattr(self,x[i]))]
            for j in range(len(y)):
                temp = [-10000, 10000, 0, 0] # [max, min, sum, frame value]
                for k in range(num_frames):
                    temp[3] = getattr(getattr(udParam,x[i]),y[j])
                    temp[0] = max(temp[0], temp[3])
                    temp[1] = min(temp[1], temp[3])
                    temp[2] += temp[3]

                #TODO: next step is to populate the values

                # max, min, sum
                z = [p for p in vars(getattr(getattr(self,x[i]),y[j]))]
                for k in range(len(z)):
                    
                    setattr(
                        getattr(
                            getattr(
                                self,
                                x[i]
                            ),
                            y[j]
                        ),
                        z[k],
                        a2
                    )

        
    class paramMaxMin:
        def __init__(self):
            self.max = 0
            self.min = 10000
            self.sum = 0

## ~~~ CLASSIFICATION ~~~ ##

class classifierEngine:
    """Classifier engine. Currently a placeholder with a simple test."""
    def __init__(self, num_segments, class_frames_check, activity_wait_frames, energy_threshold):
        # Class buffer : class must have all positive hits to cause alert
        self.class_buffer = np.zeros(shape=[class_frames_check,1])

        # Data buffers: used for calculating
        self.ud_sig_buffer = np.zeros(shape=[num_segments,1])
        self.z_lf_buffer = np.zeros(shape=[num_segments,1])
        self.z_track_buffer = np.zeros(shape=[num_segments,1])

        self.ud_sig_energy = 0
        self.zt_bw = 0
        self.zt_grad_mean = 0
        self.z_lf = 0
        
        self.fall_score = 0
        self.jump_score = 0
        self.sit_score = 0
        
        self.activity_flag = 0
        self.classification = 0
        self.frames_since_activity = 0
        self.activity_wait_frames = activity_wait_frames

        self.energy_threshold = energy_threshold

        self.activity_alert = 0

    def framewise_calculation(self, sensor_data, t_idx):
        # Roll to remove oldest datapoint
        self.ud_sig_buffer = np.roll(self.ud_sig_buffer, 1)
        self.z_lf_buffer = np.roll(self.z_lf_buffer, 1)
        self.z_track_buffer = np.roll(self.z_track_buffer, 1)

        # Update with newest datapoint
        self.ud_sig_buffer[0] = sensor_data.ud.signature_energy
        try:
            self.z_lf_buffer[0] = sensor_data.ud.z.low_freq_env
        except:
            self.z_lf_buffer[0] = None
        try:
           self.z_track_buffer[0] = sensor_data.track.Z[t_idx]
        except:
            self.z_track_buffer[0] = None

        # Calculations
        self.ud_sig_energy = np.sum(self.ud_sig_buffer)
        try:
            self.zt_bw = np.nanmax(self.z_track_buffer) - np.nanmin(self.z_track_buffer)
        except:
            self.zt_bw = 0
        self.zt_grad_mean = (self.z_track_buffer[-1] - self.z_track_buffer[0])/len(self.z_track_buffer)
        try:
            self.z_lf = np.nanmin(self.z_lf_buffer)
        except: 
            self.z_lf = 0
        self.frames_since_activity += 1

    def activity_check(self):
        if self.ud_sig_energy > self.energy_threshold:
            self.activity_flag = 1
        else:
            self.activity_flag = 0

    def find_score(self, val, min_bnd, max_bnd):
        mid = (max_bnd + min_bnd)/2
        sig = (max_bnd - min_bnd)/2
        score = np.exp(-0.5*(val-mid)**2/(sig**2))

        return score

    def classify(self):
        self.fall_score_bw = self.find_score(self.zt_bw,0.85,1.2)
        self.fall_score_grad = self.find_score(self.zt_grad_mean,-0.12,-0.08)
        self.fall_score_lf = self.find_score(self.z_lf,-0.6,-0.4)
        self.fall_score_energy = self.find_score(self.ud_sig_energy,6600,17000)
        self.fall_score = 0.25*100*(self.fall_score_bw + self.fall_score_grad + 
                                   self.fall_score_lf + self.fall_score_energy)
        
        self.jump_score_bw = self.find_score(self.zt_bw,0.3,0.7)
        self.jump_score_grad = self.find_score(self.zt_grad_mean,-0.06,0.04)
        self.jump_score_lf = self.find_score(self.z_lf,-0.52,-0.43)
        self.jump_score_energy = self.find_score(self.ud_sig_energy,8700,17000)
        self.jump_score = 0.25*100*(self.jump_score_bw + self.jump_score_grad + 
                                   self.jump_score_lf + self.jump_score_energy)
        
        self.sit_score_bw = self.find_score(self.zt_bw,0.3,0.55)
        self.sit_score_grad = self.find_score(self.zt_grad_mean,-0.05,-0.01)
        self.sit_score_lf = self.find_score(self.z_lf,-0.85,-0.5)
        self.sit_score_energy = self.find_score(self.ud_sig_energy,2800,6000)
        self.sit_score = 0.25*100*(self.sit_score_bw + self.sit_score_grad + 
                                   self.sit_score_lf + self.sit_score_energy)

        self.activity_check()
        
        classes = ['None', 'Fall', 'Jump', 'Sit']
        if self.activity_flag == 1:
            scores = [0, self.fall_score, self.jump_score, self.sit_score]
            self.class_buffer = np.roll(self.class_buffer, 1)
            self.class_buffer[0] = scores.index(max(scores))
            if np.min(self.class_buffer) == np.max(self.class_buffer) and self.frames_since_activity >= self.activity_wait_frames:
                self.classification = self.class_buffer[0][0]
                self.frames_since_activity = 0
                self.activity_alert = 1
                print("ACTIVITY DETECTED: {}".format(self.classification))
                print("Scores: {}, {}, {}".format(self.fall_score, self.jump_score, self.sit_score))

        else:
            self.class_buffer = np.roll(self.class_buffer, 1)
            self.class_buffer[0] = 0

## ~~~~~~~~~~~~~~~~~~~~~~ ##

def convert_4_to_1(arg1, *argv):
    if  isinstance(arg1, (np.ndarray,)):
        arg1 = np.ndarray.tolist(arg1)
    if  isinstance(arg1, (list,)):   
        try:
            output = arg1[0]
            #if len(arg1) > 1:
            for x in range(1, len(arg1)):
                output += arg1[x]*256**x
        except:
            nodens.logger.error("convert_4_to_1 error. arg1: {}".format(arg1))
            output = 65536
    else:
        output = arg1
        x = 1
        for arg in argv:
            output += arg*256**x
            x += 1
            
    return output

def convert_uint_to_int(arg1):
    if isinstance(arg1, list):
        num_bits = 8*len(arg1)
    else:
        num_bits = 8
    x = convert_4_to_1(arg1)

    return x if x < 2**(num_bits-1) else x - 2**num_bits



class parseTLV:
    """Parse TLVs coming from the radar chip."""
    def __init__(self, version):
        if (version == 3):
            hl = 48
        self.packet_len = 0
        self.num_tlv = 0
        self.frame = 0
        self.pc = point_cloud_3D_new([], sv.radar_version)
        self.pc_history = PointCloudHistory()
        self.track = track([],3.112)
        self.ud_sig = np.zeros([64,40])
        self.ud = MicroDoppler()
        self.vs = VitalSigns()
        self.presence = PresenceDetect()

    def update(self, version, data, Nud):
        if (version == 3):
            hl = 48
        self.packet_len = data[12] + 256*data[13]
        if len(data) < self.packet_len:
            print("WARNING: Rx data size is smaller than expected. Expected: {}. Received: {}.".format(self.packet_len, len(data)))
            self.packet_len = len(data)
        self.num_tlv = data[44]
        self.frame = convert_4_to_1(data[20:24])
        j = hl
        flag_track = False
        flag_pc = False
        while (j < self.packet_len):
            if (data[j:j+4] == [6,0,0,0]):
                flag_pc = True
                j,self.len6,self.data6 = self.tlvN(data,j)
                if (j <= self.packet_len):
                    self.pc = point_cloud_3D_new(self.data6, sv.radar_version)
                    self.pc_history.update_history(self.pc)

                # Enter the rest of the TLVs
            elif (data[j:j+4] == [7,0,0,0]): 
                flag_track = True
                j,self.len7,self.data7 = self.tlvN(data,j)
                if (j <= self.packet_len):
                    self.track = track(self.data7,3.112)
            elif (data[j:j+4] == [10,0,0,0]):
                j,self.len10,self.data10 = self.tlvN(data,j)
                print(f"TLV10. len:{self.len10}. data:{self.data10[0:12]} ")
                if (j <= self.packet_len):
                    self.vs.update(self.data10)
                    nodens.logger.debug("(X,Y): ({:.1f},{:.1f}). HR:{:.1f}. BR: {:.1f}.".format(self.vs.X, self.vs.Y,  self.vs.heart_rate, self.vs.breathing_rate))
                    nodens.logger.debug(" B dev: {}".format(self.vs.breathing_deviation[0:3]))
                    nodens.logger.debug(" B vote: {}".format(self.vs.breathing_vote[0:3]))
            elif (data[j:j+4] == [11,0,0,0]):
                j,self.len11,self.data11 = self.tlvN(data,j)
                self.presence.process(self.data11)
            elif (data[j:j+4] == [12,0,0,0]):   # UD signature 12
                j,self.len12,self.data12 = self.tlvN(data,j)
                print(f"TLV12. len:{self.len12}. data:{self.data12[0:12]} ")
                if (j <= self.packet_len):
                    ud_sig_out = self.ud.signature(self.data12, Nud, 128, 64)
                    self.ud.calculate_sig_energy(ud_sig_out)
                    self.ud_sig = np.roll(self.ud_sig, -Nud, axis=1)
                    for i in range(64):
                        for k in range(Nud):
                            self.ud_sig[i,k+40-Nud] = ud_sig_out[i,k]
            elif (data[j:j+4] == [13,0,0,0]):   # UD parameters 13
                j,self.len13,self.data13 = self.tlvN(data,j)
                print(f"TLV13. len:{self.len13}. data:{self.data13[0:12]} ")
                if (j <= self.packet_len):
                    #UD = ud()
                    self.ud.parameters(self.data13)
                #    self.elev = np.roll(self.elev,-1)
                #    self.elev[49] = UD.elev.mean
            else:
                j,lenN,dataN = self.tlvN(data,j)
        if flag_track is False:
            self.track = track([])
        if flag_pc is False:
            self.pc = point_cloud_3D_new([], sv.radar_version)
            self.pc_history.update_history(self.pc)

    def tlvN(self, data, j):
        lenN = convert_4_to_1(data[j+4:j+8])
        if (lenN == 65536):
            nodens.logger.warning("Data packet TLV length error. j: {}. len: {}.".format(j,len(data)))
        dataN = data[j:j+lenN]
        j += lenN
        
        return j,lenN,dataN

class sendCMDtoSensor(object):
    """Send a command (e.g. a new configuration) to the sensor via MQTT."""
    def full_data_off(rcp,cp):
        config_full_data = "CMD: FULL DATA OFF."

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_full_data + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

    def full_data_on(rcp,cp):
        config_full_data = "CMD: FULL DATA OFF."
        # Parse Publish rates to payload #
        rate_unit = 2 # Baseline data transmission rate
        config_pub_rate = "CMD: PUBLISH RATE: " + str(round(2/rate_unit))
        payload_msg = [{ "addr" : [rcp.SENSOR_TARGET],
                            "type" : "json",
                            "data" : config_pub_rate + "\n"}]

        config_full_data = "CMD: FULL DATA ON. RATE: " + str(max(1,2/2))

        payload_msg.append({ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_full_data + "\n"})

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

    def request_version(rcp,cp,sv):
        config_req = "CMD: REQUEST VERSION"

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_req + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

        nodens.logger.info("Published sensor version request to {}".format(rcp.SENSOR_TOPIC))
        temp = 0
        while (1):
            if sv.string != []:
                nodens.logger.info("Version received. Version = {}. Dimensions = {}.".format(sv.string, sv.radar_dim))
                break
            elif temp < 20:
                nodens.logger.info("Waiting... {}".format(sv.string))
                temp += 1
                time.sleep(0.2)
            else:
                nodens.logger.info("No response to version request. Continue...")
                break

    def request_config(rcp,cp):
        config_req = "CMD: REQUEST CONFIG"

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_req + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        rcp.cfg_idx = 0
        rcp.cfg_sensorStart = 0
        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)
       

    def start_config_proc(rcp,cp):
        config_req = "CMD: CONFIG STATE"

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_req + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

    def end_config_proc(rcp,cp):
        config_req = "CMD: CONFIG FINISHED"

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_req + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

    def ping_back(rcp, cp):
        config_req = "CMD: REQUEST PING"

        payload_msg =[{ "addr" : [rcp.SENSOR_TARGET],
                        "type" : "json",
                        "data" : config_req + "\n"}]

        rcp.SENSOR_TOPIC = 'mesh/' + rcp.SENSOR_ROOT + '/toDevice'

        ndns_mesh.MESH.multiline_payload(cp.SENSOR_IP,cp.SENSOR_PORT,60, rcp.SENSOR_TOPIC,"", payload_msg)

## ~~~~~~~~~~ MESSAGE SENDING BETWEEN PROCESSES (THREADS) ~~~~~~~~~~~~~~ ##

class MessagePipeline:
    def __init__(self):
        self.sensor_id = []
        self.flag_send = []
        self.message = []

    def update(self, message):
        if message['addr'] in self.sensor_id:
            sens_idx = self.sensor_id.index(message['addr'])
            self.flag_send[sens_idx] = 1
            self.message[sens_idx] = message
        else:
            self.sensor_id.append(message['addr'])
            self.flag_send.append(1)
            self.message.append(message)

    def clear(self, index):
        if index < len(self.sensor_id):
            self.flag_send[index] = 0
            self.message[index] = ""
        else:
            nodens.logger.warning("Sensor index %d does not exist", index)


# # Create a custom nodens.logger
# nodens.logger = logging.getnodens.logger(__name__)
# nodens.logger.setLevel(logging.DEBUG)

# # Create handlers
# log_file = user_log_dir(APPNAME, APPAUTHOR)+'/nodens_gateway.log'
# Path(user_log_dir(APPNAME, APPAUTHOR)).mkdir(parents=True, exist_ok=True)
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler(log_file)

# c_handler.setLevel(logging.INFO)
# f_handler.setLevel(logging.DEBUG)

# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)

# # Add handlers to the nodens.logger
# nodens.logger.addHandler(c_handler)
# nodens.logger.addHandler(f_handler)

## ~~~~~~~~~~ INITIALISE FUNCTIONS ~~~~~~~~~~~~~~ ## 
si = SensorInfo()               # Sensor info
ew = EntryWays()         # Entryway monitors
oh = OccupantHist(num_hist_frames=250)      # Occupant history
sm = SensorMesh()        # Sensor Mesh state
message_pipeline = MessagePipeline()
#cp = nodens.cp
rcp = radar_config_params()
sv = sensor_version()
class_eng = classifierEngine(11,5,100,3200)
sd = parseTLV(3)
sts = sensorTimeSeries()