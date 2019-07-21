# File: btleclassifier.py
# Original Author:  Johannes K Becker <jkbecker@bu.edu>, 2019-01-29 through 2019-07-18
# Revised by: Simson Garfinkel <simsong@acm.org> 2019-07-19-

import codecs
import json

"""
Advertising Data Type (AD Type) Definitions here:
https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile
See btleclassifer.txt for more information

iBeacon format:
https://support.kontakt.io/hc/en-gb/articles/201492492-iBeacon-advertising-packet-structure
"""

def hexdump(s):
    return " ".join([hex(ch)[2:] for ch in s])

class BTLEAdvIDToken(object):
    """This isn't being used. Not sure what it's for."""
    def __init__(self, token_key):
        self.type    = str(token_key)
        self.parser  = BTLEAdvIDToken.tokens[self.type]['parser']
        self.pattern = BTLEAdvIDToken.tokens[self.type]['pattern']
        self.tokens  = BTLEAdvIDToken.tokens[self.type]['tokens']

    @classmethod 
    def get_matched_tokens(cls, data):
        for vendor in BTLEAdvIDToken.tokens.keys():
            token = BTLEAdvIDToken(vendor)
            if token.pattern in data['raw']:
                return token
        return None

    TOKENS = {
        'Apple': { 'parser': 'parse_token_apple',      
                   'pattern': "ff4c00",
                   'tokens': ["handoff", "nearby"] },
        'Microsoft': { 'parser': 'parse_token_microsoft',  
                       'pattern': "ff0600",
                       'tokens': ["msdata"] }
    }

#    @classmethod
#    def parse_token_apple(cls, data):
#        result = {}
#        id_tokens = ['handoff', 'nearby']
#        if 'manufacturer-specific' in data.keys() \
#            and isinstance(data['manufacturer-specific'], dict):
#            for t in id_tokens:
#                if t in data['manufacturer-specific'].keys() \
#                    and isinstance(data['manufacturer-specific'][t], str):
#                    result[t] = data['manufacturer-specific'][t]
#                else:
#                    result[t] = None
#        return result

#    @classmethod
#    def parse_token_microsoft(cls, data):
#        print "Parsing Microsoft", data
#        return [] 

#    @classmethod
#    def get_token_type(cls, data):
#        return


RAW = 'raw'
HEX = 'hex'
FLAGS = 'flags'
SEC_MG_OOB_FLAGS = 'sec-mg-oob-flags'
SERVICE_DATA = 'service-data'
MANUFACTURER_SPECIFIC = 'manufacturer-specific'
UNKNOWN = 'unknown'
COMPANY_ID = 'company_id'
COMPANY_NAME = 'company_name'
COMPANY_HEX  = 'company_raw'
IBEACON='ibeacon'

FLAG_LEL = 'LE Limited Discoverable Mode'
FLAG_LEG = 'LE General Discoverable Mode'
FLAG_BR  = 'BR/EDR Not Supported (i.e. bit 37 of LMP Extended Feature bits Page 0)'
FLAG_SLEBR = 'Simultaneous LE and BR/EDR to Same Device Capable (Controller) (i.e. bit 49 of LMP Extended Feature bits Page 0)'
FLAG_LEBRS = 'Simultaneous LE and BR/EDR to Same Device Capable (Host) (i.e. bit 66 of LMP Extended Feature bits Page 1)'

FLAG_OOB = "OOB data present"
FLAG_NO_OOB = "OOB data not present"
FLAG_LE  = "LE supported (Host) (i.e. bit 65 of LMP Extended Feature bits Page 1"
FLAG_LE_BR = "Simultaneous LE and BR/EDR to Same Device Capable (Host) (i.e. bit 66 of LMP Extended Fea- ture bits Page 1"
FLAG_RANDOM_ADDRESS = "Address Type: Random Address"
FLAG_PUBLIC_ADDRESS = "Address Type: Public Address"

def word16be(data):
    """return data[0] and data[1] as a 16-bit Big Ended Word"""
    return (data[1] << 8) | data[0]

class AbstractContextManager():
    def __init__(self, buf):
        assert type(buf)==bytes
        self.buf = buf
        self.pos = 0
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return

class LengthRuns(AbstractContextManager):
    """Given a buffer, return a series of (dtaa) fields. Assumes
    that data contains a set of (length,data) fields. Used by BLE header."""
    def get_data(self, lensize=1):
        while self.pos < len(self.buf):
            try:
                ad_len  = self.buf[self.pos]
                ad_data = self.buf[self.pos+1:self.pos+ad_len+1]
                self.pos += 1 + ad_len
                yield ad_data
            except IndexError as e:
                pass
    

class AppleTypeLengthRuns(AbstractContextManager):
    """Returns a context manager. Given a buffer, return a series of
    (type,data) fields. Assumes that data contains a set of
    (type,length,data) fields used by Apple, where (type) and (length)
    are both unsigned 8-bit values.

    """
    def get_type_data(self, lensize=1):
        while self.pos < len(self.buf):
            try:
                ad_type = self.buf[self.pos]
                ad_len  = self.buf[self.pos+1]
                ad_data = self.buf[self.pos+2:self.pos+ad_len+2]
                self.pos += 2 + ad_len
                yield (ad_type,ad_data)
            except IndexError as e:
                pass

class BTLEAdvClassifier():
    def __init__(self, adv_data = bytes(), manuf_data=bytes()):
        self.d      = {}
        self.d[HEX] =  adv_data.hex()

        with LengthRuns(adv_data) as lr:
            for data in lr.get_data():
                self.parse_ad_structure( data)

        if manuf_data:
            self.parse_ad_type_0xff(manuf_data)

    def __repr__(self):
        return f"BTLEAdvClassifier<{self.d}>"

    def json(self,indent=None):
        return json.dumps(self.d,indent=indent)

    def dict(self):
        return self.d

    def parse_ad_structure(self, data):
        AD_TYPE_PARSERS = {
            0x01: self.parse_ad_type_0x01,
            0x11: self.parse_ad_type_0x11,
            0x16: self.parse_ad_type_0x16,
            0xff: self.parse_ad_type_0xff}


        ad_type = data[0]
        ad_data = data[1:]
        if ad_type in AD_TYPE_PARSERS:
            AD_TYPE_PARSERS[ad_type](ad_data)
        else:
            self.d[UNKNOWN] = {'type':ad_type, 'hex':ad_data.hex()}

    def parse_ad_type_0x01(self, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] Table 18.1: Flags
        """
        ad_flags = []
        val = data[0]
        if val & 0x01<<0:
            ad_flags.append(FLAG_LEL)
        if val & 0x01<<1:
            ad_flags.append(FLAG_LEG)
        if val & 0x01<<2:
            ad_flags.append(FLAG_BR)
        if val & 0x01<<3:
            ad_flags.append(FLAG_SLEBR)
        if val & 0x01<<4:
            ad_flags.append(FLAG_LEBRS)
        self.d[FLAGS] = ad_flags

    def parse_ad_type_0x11(self, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] 
        Table 18.7: Security Manager OOB Flags
        """
        val = data[0]
        ad_flags = []
        if val & 0x01<<0:
            ad_flags.append( FLAG_OOB )
        else:
            ad_flags.append( FLAG_NO_OOB )
        if val & 0x01<<1:
            ad_flags.append( FLAG_LE )
        if val & 0x01<<2:
            ad_flags.append( FLAG_LE_BR)
        if val & 0x01<<3:
            ad_flags.append( FLAG_RANDOM_ADDRESS )
        else:
            ad_flags.append( FLAG_PUBLIC_ADDRESS )
        self.d[SEC_MG_OOB_FLAGS] = ad_flags

    def parse_ad_type_0x16(self, data):
        """Implementation of Bluetooth Specification Version 4.0 [Vol 3]
            Table 18.10: Service Data and GATT Services list
            https://www.bluetooth.com/specifications/gatt/services
        """
        service_uuid = word16be(data[0:2])
        service_data = data[2:] 
        self.d[SERVICE_DATA] = {'uuid':service_uuid, 'data':service_data}

    COMPANY_ID_MAP = {
        0x0006: 'Microsoft',
        0x004c: 'Apple'
    }

    APPLE_DATA_TYPES = {
        0x02: 'ibeacon',
        0x05: 'airdrop',
        0x07: 'airpods',
        0x08: '(unknown)',
        0x09: 'airplay_dest',
        0x0a: 'airplay_src',
        0x0c: 'handoff',
        0x10: 'nearby',
    }

    def parse_ad_type_0xff(self, data):
        """Implementation of Bluetooth Specification Version 4.0 [Vol 3]
            Table 18.11: Manufacturer Specific Data and Company
            Identifier List:
            https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers
        """
        # First 2 octets contain the 16 bit service UUID, flip bytes around
        company_id = word16be(data[0:2])

        man_data = data[2:] 

        d = {}
        d[COMPANY_ID]   = company_id
        d[COMPANY_HEX]  = man_data.hex()
        d[COMPANY_NAME] = self.COMPANY_ID_MAP.get(company_id,'??')
        if d[COMPANY_NAME]=='Apple':
            d['records'] = []
            with AppleTypeLengthRuns(man_data) as tr:
                for (apple_type,apple_data) in tr.get_type_data():
                    if apple_type==0x0c:
                        record = {'type':'Handoff Message',
                                  'Clipboard Status':apple_data[0],
                                  'Sequence Number':word16be(apple_data[1:3])
                                  }
                    elif apple_type==0x0d:
                        record = {'type':'Wi-Fi Settings',
                                  'iCloud ID':apple_data[2:].hex()
                                  }
                    elif apple_type==0x0e:
                        record = {'type':'Instant Hotspot',
                                  'Battery Life': apple_data[4],
                                  'Cell Service': apple_data[6],
                                  'Cell Bars': apple_data[7]}
                    elif apple_type==0x0f:
                        record = {'type':'Wi-Fi Join Network',
                                  'data':apple_data.hex()}
                    elif apple_type==0x10:
                        actionCode  = apple_data[0]& 0x0f
                        actionCodeText = {1:"iOS recently updated",
                               3:"Locked Screen",
                               7:"Transition Phase",
                               10:"Locked Screen, Inform Apple Watch",
                               11:"Active User",
                               13:"Unknown",
                               14:"Phone Call or Facetime"}.get(actionCode,'??')
                        record = {'type': 'Nearby Message',
                                  'Location Sharing' : apple_data[0]>>4,
                                  'Action Code' : actionCode,
                                  'Action Code Text' : actionCodeText}
                    else:
                        record = {'type' : hex(apple_type)}
                    d['records'].append(record)
        self.d[MANUFACTURER_SPECIFIC] = d

if __name__ == "__main__":
    HEX_EXAMPLES = ["02011a0aff4c0010050b1c6d9072", 
                    "02011a1aff4c000c0e00750f812422021c3e213d190f3310050b1c6d9072"]
    for hexstr in HEX_EXAMPLES:
        print(hexstr)
        obj = BTLEAdvClassifier( codecs.decode(hexstr,"hex") )
        print(obj.json(indent=5))
        print("-"*64)
