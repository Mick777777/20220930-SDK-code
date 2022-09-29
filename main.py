import datetime
import time
import string
import random
import threading
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer
global _edgeAgent

def on_connected(edgeAgent, isConnected):
    print("connected !")
    config = __generateConfig()
    _edgeAgent.uploadConfig(action = constant.ActionType['Update'], edgeConfig = config)

def on_disconnected(edgeAgent, isDisconnected):
    print("disconnected !")

def __sendData():
    _edgeAgent.sendData(__generateData())

def __generateData():
    edgeData = EdgeData()

    value=[random.randrange(1,10,1),random.randrange(1,10,1)]  

    deviceId = '{Device ID}' #需對應剛剛取名的Device
    tagName = '{Tag1 name}'     #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[1])
    edgeData.tagList.append(tag)
    deviceId = '{Device ID}' #需對應剛剛取名的Device
    tagName = '{Tag2 name}' #需對應剛剛取名的Tag
    tag = EdgeTag(deviceId, tagName, value[0])
    edgeData.tagList.append(tag)

    return edgeData

def __generateConfig():
    config = EdgeConfig()
    deviceConfig = DeviceConfig(id = '{Device ID}',#需對應剛剛取名的Device
    name = '{Device name}',                        #需對應剛剛取名的name
    description = '{Device description}',                 #需對應剛剛取名的description
    deviceType = '{Device type}',            #需對應剛剛取名的deviceType
    retentionPolicyName = '')

    analog = AnalogTagConfig(name = '{Tag1 name}',    #需對應剛剛取名的Tag
    description = '{Tag1 name}',                    #需對應剛剛取名的Tag 
    readOnly = False,
    arraySize = 0,
    spanHigh = 10000,
    spanLow = 0,
    engineerUnit = '',
    integerDisplayFormat = 4,
    fractionDisplayFormat = 2)
    deviceConfig.analogTagList.append(analog)

    analog = AnalogTagConfig(name = '{Tag2 name}',#需對應剛剛取名的Tag
    description = '{Tag2 name}',                #需對應剛剛取名的Tag
    readOnly = False,
    arraySize = 0,
    spanHigh = 1000,
    spanLow = 0,
    engineerUnit = '',
    integerDisplayFormat = 4,
    fractionDisplayFormat = 2)
    deviceConfig.analogTagList.append(analog)

    config.node.deviceList.append(deviceConfig)

    return config

def Auth():
    options = EdgeAgentOptions(
    nodeId = '{Your Node ID}',
    type = constant.EdgeType['Gateway'],                    # 節點類型 (Gateway, Device), 預設是 Gateway
    deviceId = 'deviceId',                                  # 若 type 為 Device, 則必填
    heartbeat = 60,                                         # 預設是 60 seconds
    dataRecover = True,                                     # 是否需要斷點續傳, 預設為 true
    connectType = constant.ConnectType['DCCS'],             # 連線類型 (DCCS, MQTT), 預設是 DCCS
    DCCS = DCCSOptions(
    apiUrl = '{Your DCCS API URL}',
    credentialKey = '{Your Credential Key}'
    )
)
    return options
           
if __name__ == '__main__':    
    _edgeAgent = EdgeAgent( options = Auth() );
    _edgeAgent.on_connected = on_connected
    _edgeAgent.on_disconnected = on_disconnected
    _edgeAgent.connect()
    time.sleep(2)
    while True:
        __sendData()
        time.sleep(5)
    _edgeAgent.disconnect()