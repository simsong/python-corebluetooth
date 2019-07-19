#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Originally from https://github.com/masato-ka/python-corebluetooth-sample.git

import struct

from Foundation import CBCentralManager,CBUUID
from PyObjCTools import AppHelper

from btleclassifier import BTLEAdvClassifier

from constants import C
print(C.kCBAdvDataIsConnectable)

wx2_service = CBUUID.UUIDWithString_(u'0C4C3000-7700-46F4-AA96-D5E974E32A54')
wx2_characteristic_data = CBUUID.UUIDWithString_(u'0C4C3001-7700-46F4-AA96-D5E974E32A54')

class MyBLE(object):
    def __init__(self,debug=False):
        self.seen = set()
        self.debug = debug

    def centralManagerDidUpdateState_(self, manager):
        if self.debug:
            print("centralManagerDidUpdateState_")
        self.manager = manager
        manager.scanForPeripheralsWithServices_options_(None,None)

    def centralManager_didDiscoverPeripheral_advertisementData_RSSI_(self, manager, peripheral, data, rssi):
        if self.debug:
            print('centralManager_didDiscoverPeripheral_advertisementData_RSSI_')
        seen = set(data.keys())
        if C.kCBAdvDataChannel in data:
            print("Channel: ",data[C.kCBAdvDataChannel], "RSSI:",rssi)
            seen.remove(C.kCBAdvDataChannel)
        if C.kCBAdvDataIsConnectable in data:
            print("kCBAdvDataIsConnectable: ",data[C.kCBAdvDataIsConnectable])
            seen.remove(C.kCBAdvDataIsConnectable)
        if C.kCBAdvDataManufacturerData in data:
            mdata = data[C.kCBAdvDataManufacturerData]
            print("mdata:",mdata)
            #print(BTLEAdvClassifier.parse_data(mdata))
            #seen.remove(C.kCBAdvDataManufacturerData)
        for prop in seen:
            print(f"data[{prop}] = {data[prop]}")
        print("")

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
    AppHelper.runConsoleEventLoop()