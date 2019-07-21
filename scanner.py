#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Originally from https://github.com/masato-ka/python-corebluetooth-sample.git

import struct

from Foundation import CBCentralManager,CBUUID
from PyObjCTools import AppHelper

from btleclassifier import BTLEAdvClassifier

from constants import C
import btleclassifier
import datetime

wx2_service = CBUUID.UUIDWithString_(u'0C4C3000-7700-46F4-AA96-D5E974E32A54')
wx2_characteristic_data = CBUUID.UUIDWithString_(u'0C4C3001-7700-46F4-AA96-D5E974E32A54')

EXIT_COUNT = 5

class MyBLE(object):
    def __init__(self,debug=False):
        self.seen = set()
        self.debug = debug
        self.count_advertisements = 0

    def centralManagerDidUpdateState_(self, manager):
        if self.debug:
            print("centralManagerDidUpdateState_")
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(None,None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        self.count_advertisements += 1
        if self.debug:
            print('centralManager_didDiscoverPeripheral_advertisementData_RSSI_')
        print("\n======== Advertisement {} t={} len={}  rssi={} =======".format(
            self.count_advertisements,
            datetime.datetime.now().isoformat(),
            len(data),
            rssi))

        for prop in data.keys():
            if prop==C.kCBAdvDataChannel:
                print("Channel: ",data[C.kCBAdvDataChannel])
            elif prop==C.kCBAdvDataIsConnectable:
                print("kCBAdvDataIsConnectable: ",data[C.kCBAdvDataIsConnectable])
            elif prop==C.kCBAdvDataManufacturerData:
                obj = BTLEAdvClassifier( manuf_data = bytes( data[C.kCBAdvDataManufacturerData] ) )
                print(obj.json(indent=5))
            else:
                print(f"data[{prop}] = {data[prop]}")

        if EXIT_COUNT==self.count_advertisements:
            exit(0)

    def centralManager_didConnectPeripheral_(self, manager, peripheral):
        if self.debug:
            print("centralManager_didConnectPeripheral_")
            print(repr(peripheral.UUID()))
        peripheral.setDelegate_(self)
        self.peripheral.discoverServices_([wx2_service])
        
    def peripheral_didDiscoverServices_(self, peripheral, services):
        if self.debug:
            print("peripheral_didDiscoverServices_")
        self.service = self.peripheral.services()[0]
        self.peripheral.discoverCharacteristics_forService_([wx2_characteristic_data], self.service)

    def peripheral_didDiscoverCharacteristicsForService_error_(self, peripheral, service, error):
        if self.debug:
            print("peripheral_didDiscoverCharacteristicsForService_error_")
        for characteristic in self.service.characteristics():
            if characteristic.properties() == 18:
                peripheral.readValueForCharacteristic_(characteristic)
                break

    def peripheral_didWriteValueForCharacteristic_error_(self, peripheral, characteristic, error):
        if self.debug:
            print("peripheral_didWriteValueForCharacteristic_error_")
        print('In error handler')
        print('ERROR:' + repr(error))

    def peripheral_didUpdateNotificationStateForCharacteristic_error_(self, peripheral, characteristic, error):
        if self.debug:
            print("Notification handler")

    def peripheral_didUpdateValueForCharacteristic_error_(self, peripheral, characteristic, error):
        print(repr(characteristic.value().bytes().tobytes()))
        value = characteristic.value().bytes().tobytes()

        temp = decode_value(value[1:3],0.01)
        print('temprature:' + str(temp))

        humid = decode_value(value[3:5],0.01)
        print('humidity:' + str(humid))

        lum = decode_value(value[5:7])
        print('lumix:' + str(lum))

        uvi = decode_value(value[9:7], 0.01)
        print('UV index:' + str(uvi))

        atom = decode_value(value[9:11], 0.1)
        print('Atom:' + str(atom))

        noise = decode_value(value[11:13], 0.01)
        print('Noise:' + str(noise))

        disco = decode_value(value[13:15], 0.01)
        print('Disco:' + str(disco))

        heat = decode_value(value[15:17], 0.01)
        print('Heat:' + str(heat))
        
        batt = decode_value(value[17:19],0.001)
        print('Battery:' + str(batt))

if "__main__" == __name__:
    import argparse
    parser = argparse.ArgumentParser(description='Monitor BLE')
    parser.add_argument("--debug", action='store_true', help="Run in debugger mode")
    args = parser.parse_args()
    
    central_manager = CBCentralManager.alloc()
    central_manager.initWithDelegate_queue_options_(MyBLE(debug=args.debug), None, None)
    try:
        AppHelper.runConsoleEventLoop()
    except (KeyboardInterrupt, SystemExit) as e:
        print(e)
    except OC_PythonException as e:
        print(e)
        pass
