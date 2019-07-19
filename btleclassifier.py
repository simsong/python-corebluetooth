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

class LengthRuns():
    """Returns a context manager"""
    def __init__(self, buf):
        assert type(buf)==bytes
        self.buf = buf
        self.pos = 0
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return
    def get_data(self, lensize=1):
        while self.pos < len(self.buf):
            try:
                if lensize==1:
                    ad_len  = self.buf[self.pos]
                elif lensize==2:
                    ad_len  = (self.buf[self.pos]<<8) | self.buf[self.pos+1]
                elif lensize==-2:
                    ad_len  = (self.buf[self.pos+1]<<8) | (self.buf[self.pos])
                else:
                    raise ValueError("Unknown length size (%d)" % lensize)
                ad_data = self.buf[self.pos+1:ad_len+1]
                self.pos += ad_len + 1
                yield ad_data
            except IndexError as e:
                pass

class BTLEAdvClassifier():
    def __init__(self, adv_data):
        self.d      = {}
        self.d[HEX] =  adv_data.hex()
        with LengthRuns(adv_data) as tr:
            for data in tr.get_data():
                self.parse_ad_structure(data)

    def __repr__(self):
        return f"BTLEAdvClassifier<{self.d}>"

    def json(self,indent=None):
        return json.dumps(self.d,indent=indent)

    def parse_ad_structure(self, data):
        try:
            ad_type = data[0]
            ad_data = data[1:]
            if ad_type == 0x01:
                self.d[FLAGS] = self.parse_ad_type_0x01(ad_data)
            elif ad_type == 0x11:
                self.d[SEC_MG_OOB_FLAGS] = self.parse_ad_type_0x11(ad_data)
            elif ad_type == 0x16:
                self.d[SERVICE_DATA] = self.parse_ad_type_0x16(ad_data)
            elif ad_type == 0xff:
                self.d[MANUFACTURER_SPECIFIC] = self.parse_ad_type_0xff(ad_data)
            else:
                self.d[UNKNOWN] = (ad_type, ad_data)
        except ValueError:
            pass

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
        return ad_flags

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
        return ad_flags

    def parse_ad_type_0x16(self, data):
        """Implementation of Bluetooth Specification Version 4.0 [Vol 3]
            Table 18.10: Service Data and GATT Services list
            https://www.bluetooth.com/specifications/gatt/services
        """
        service_uuid = word16be(data[0:2])
        service_data = data[2:] 
        return (service_uuid, service_data)

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
        man_specific_data = data[2:] # additional service data

        d = {}
        d[COMPANY_ID] = company_id
        d[COMPANY_HEX] = man_specific_data.hex()
        if company_id == 0x0006:
            d[COMPANY_NAME] = "Microsoft"
        elif company_id == 0x004c:
            d[COMPANY_NAME] = "Apple"
            d[IBEACON] = (0x1502 == word16be(man_specific_data[0:2]))
            with LengthRuns(man_specific_data) as tr:
                for data in tr.get_data():
                    apple_type = self.APPLE_DATA_TYPES.get(data[0],"(unknown)")
                    apple_data = data[1:]
        else:
            d[COMPANY_NAME] = '??'
        return d

if __name__ == "__main__":
    HEX_EXAMPLES = ["02011a0aff4c0010050b1c6d9072", 
                    "02011a1aff4c000c0e00750f812422021c3e213d190f3310050b1c6d9072"]
    for hexstr in HEX_EXAMPLES:
        print(hexstr)
        data = codecs.decode(hexstr,"hex")
        obj = BTLEAdvClassifier(data)
        print(obj.json(indent=5))
