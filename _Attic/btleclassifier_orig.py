# File: btleclassifier.py
# Author:  Johannes K Becker <jkbecker@bu.edu>
# Date: 2019-01-29
# Last Modified Date: 2019-07-18
# Last Modified By: Johannes K Becker <jkbecker@bu.edu>

# Advertising Data Type (AD Type) Definitions here:
# https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile
#
# Data Type Value Data Type Name                                Reference for Definition
# 0x01 	    "Flags" 	                                        Bluetooth Core Specification:Vol. 3, Part C, section 8.1.3 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.3 and 18.1 (v4.0)Core Specification Supplement, Part A, section 1.3
# 0x02 	    "Incomplete List of 16-bit Service Class UUIDs"     Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x03 	    "Complete List of 16-bit Service Class UUIDs"       Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x04 	    "Incomplete List of 32-bit Service Class UUIDs"     Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, section 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x05 	    "Complete List of 32-bit Service Class UUIDs"       Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, section 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x06 	    "Incomplete List of 128-bit Service Class UUIDs"    Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x07 	    "Complete List of 128-bit Service Class UUIDs" 	    Bluetooth Core Specification:Vol. 3, Part C, section 8.1.1 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.1 and 18.2 (v4.0)Core Specification Supplement, Part A, section 1.1
# 0x08 	    "Shortened Local Name" 	                            Bluetooth Core Specification:Vol. 3, Part C, section 8.1.2 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.2 and 18.4 (v4.0)Core Specification Supplement, Part A, section 1.2
# 0x09 	    "Complete Local Name" 	                            Bluetooth Core Specification:Vol. 3, Part C, section 8.1.2 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.2 and 18.4 (v4.0)Core Specification Supplement, Part A, section 1.2
# 0x0A 	    "Tx Power Level" 	                                Bluetooth Core Specification:Vol. 3, Part C, section 8.1.5 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.3 (v4.0)Core Specification Supplement, Part A, section 1.5
# 0x0D 	    "Class of Device" 	                                Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)Core Specification Supplement, Part A, section 1.6
# 0x0E 	    "Simple Pairing Hash C" 	                        Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)
# 0x0E 	    "Simple Pairing Hash C-192" 	                    Core Specification Supplement, Part A, section 1.6
# 0x0F 	    "Simple Pairing Randomizer R" 	                    Bluetooth Core Specification:Vol. 3, Part C, section 8.1.6 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.5 and 18.5 (v4.0)
# 0x0F 	    "Simple Pairing Randomizer R-192" 	                Core Specification Supplement, Part A, section 1.6
# 0x10 	    "Device ID" 	                                    Device ID Profile v1.3 or later
# 0x10 	    "Security Manager TK Value" 	                    Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.7 and 18.6 (v4.0)Core Specification Supplement, Part A, section 1.8
# 0x11 	    "Security Manager Out of Band Flags" 	            Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.6 and 18.7 (v4.0)Core Specification Supplement, Part A, section 1.7
# 0x12 	    "Slave Connection Interval Range" 	                Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.8 and 18.8 (v4.0)Core Specification Supplement, Part A, section 1.9
# 0x14 	    "List of 16-bit Service Solicitation UUIDs" 	    Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.9 and 18.9 (v4.0)Core Specification Supplement, Part A, section 1.10
# 0x15 	    "List of 128-bit Service Solicitation UUIDs" 	    Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.9 and 18.9 (v4.0)Core Specification Supplement, Part A, section 1.10
# 0x16 	    "Service Data" 	                                    Bluetooth Core Specification:Vol. 3, Part C, sections 11.1.10 and 18.10 (v4.0)
# 0x16 	    "Service Data - 16-bit UUID" 	                    Core Specification Supplement, Part A, section 1.11
# 0x17 	    "Public Target Address" 	                        Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.13
# 0x18 	    "Random Target Address" 	                        Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.14
# 0x19 	    "Appearance" 	                                    Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.12
# 0x1A 	    "Advertising Interval" 	                            Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.15
# 0x1B 	    "LE Bluetooth Device Address" 	                    Core Specification Supplement, Part A, section 1.16
# 0x1C 	    "LE Role" 	                                        Core Specification Supplement, Part A, section 1.17
# 0x1D 	    "Simple Pairing Hash C-256" 	                    Core Specification Supplement, Part A, section 1.6
# 0x1E 	    "Simple Pairing Randomizer R-256" 	                Core Specification Supplement, Part A, section 1.6
# 0x1F 	    "List of 32-bit Service Solicitation UUIDs" 	    Core Specification Supplement, Part A, section 1.10
# 0x20 	    "Service Data - 32-bit UUID" 	                    Core Specification Supplement, Part A, section 1.11
# 0x21 	    "Service Data - 128-bit UUID" 	                    Core Specification Supplement, Part A, section 1.11
# 0x22 	    "LE Secure Connections Confirmation Value" 	        Core Specification Supplement Part A, Section 1.6
# 0x23 	    "LE Secure Connections Random Value" 	            Core Specification Supplement Part A, Section 1.6
# 0x24 	    "URI" 	                                            Bluetooth Core Specification:Core Specification Supplement, Part A, section 1.18
# 0x25 	    "Indoor Positioning" 	                            Indoor Posiioning Service v1.0 or later
# 0x26 	    "Transport Discovery Data" 	                        Transport Discovery Service v1.0 or later
# 0x27 	    "LE Supported Features" 	                        Core Specification Supplement, Part A, Section 1.19
# 0x28 	    "Channel Map Update Indication" 	                Core Specification Supplement, Part A, Section 1.20
# 0x29 	    "PB-ADV"                                            Mesh Profile Specification Section 5.2.1
# 0x2A 	    "Mesh Message"                                      Mesh Profile Specification Section 3.3.1
# 0x2B 	    "Mesh Beacon"                                       Mesh Profile Specification Section 3.9
# 0x3D 	    "3D Information Data" 	                            3D Synchronization Profile, v1.0 or later
# 0xFF 	    "Manufacturer Specific Data" 	                    Bluetooth Core Specification:Vol. 3, Part C, section 8.1.4 (v2.1 + EDR, 3.0 + HS and 4.0)Vol. 3, Part C, sections 11.1.4 and 18.11 (v4.0)Core Specification Supplement, Part A, section 1.4

class BTLEAdvIDToken(object):

    def __init__(self, token_key):
        self.type = str(token_key)
        self.parser = BTLEAdvIDToken.tokens[self.type]['parser']
        self.pattern = BTLEAdvIDToken.tokens[self.type]['pattern']
        self.tokens = BTLEAdvIDToken.tokens[self.type]['tokens']

    @classmethod 
    def get_matched_tokens(cls, data):
        for vendor in BTLEAdvIDToken.tokens.keys():
            token = BTLEAdvIDToken(vendor)
            if token.pattern in data['raw']:
                return token
        return None

    tokens = {
        'Apple':        { 'parser': 'parse_token_apple',      'pattern': "ff4c00",    'tokens': ["handoff", "nearby"] },
        'Microsoft':    { 'parser': 'parse_token_microsoft',  'pattern': "ff0600",    'tokens': ["msdata"] }
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

class BTLEAdvClassifier(object):

    @classmethod
    def parse_data(cls, adv_data):
        d = {}
        d["raw"] = adv_data
        while adv_data:
            ad_len = int(adv_data[:2], 16)
            ad_str = adv_data[2:2+2*ad_len]
            d = cls.parse_ad_structure(d, ad_str)
            adv_data = adv_data[2+2*ad_len:]
        return d

    @classmethod
    def parse_ad_structure(cls, d, ad_str):
        try:
            ad_type = int(ad_str[:2], 16)
            ad_data = ad_str[2:]
            if ad_type == 0x01:
                d["flags"] = cls.parse_ad_type_0x01(ad_data)
            elif ad_type == 0x11:
                d["sec-mg-oob-flags"] = cls.parse_ad_type_0x11(ad_data)
            elif ad_type == 0x16:
                d["service-data"] = cls.parse_ad_type_0x16(ad_data)
            elif ad_type == 0xff:
                d["manufacturer-specific"] = cls.parse_ad_type_0xff(ad_data)
            else:
                d["unknown"] = (ad_type, ad_data)
        except ValueError:
            return d
        return d

    @classmethod
    def parse_ad_type_0x01(cls, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] Table 18.1: Flags
        """
        ad_data = int(data, 16)
        ad_flags = []
        if ad_data & 0x01<<0:
            ad_flags.append("'LE Limited Discoverable Mode'")
        if ad_data & 0x01<<1:
            ad_flags.append("'LE General Discoverable Mode'")
        if ad_data & 0x01<<2:
            ad_flags.append("'BR/EDR Not Supported (i.e. bit 37 of LMP Extended Feature bits Page 0)'")
        if ad_data & 0x01<<3:
            ad_flags.append("'Simultaneous LE and BR/EDR to Same Device Capable (Controller) (i.e. bit 49 of LMP Extended Feature bits Page 0)'")
        if ad_data & 0x01<<4:
            ad_flags.append("'Simultaneous LE and BR/EDR to Same Device Capable (Host) (i.e. bit 66 of LMP Extended Feature bits Page 1)'")
        return ad_flags

    @classmethod
    def parse_ad_type_0x11(cls, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] Table 18.7: Security Manager OOB Flags
        """
        ad_data = int(data, 16)
        ad_flags = []
        if ad_data & 0x01<<0:
            ad_flags.append("'OOB data present'")
        else:
            ad_flags.append("'OOB data not present'")
        if ad_data & 0x01<<1:
            ad_flags.append("'LE supported (Host) (i.e. bit 65 of LMP Extended Feature bits Page 1'")
        if ad_data & 0x01<<2:
            ad_flags.append("'Simultaneous LE and BR/EDR to Same Device Capable (Host) (i.e. bit 66 of LMP Extended Fea- ture bits Page 1)'")
        if ad_data & 0x01<<3:
            ad_flags.append("'Address Type: Random Address'")
        else:
            ad_flags.append("'Address Type: Public Address'")
        return ad_flags

    @classmethod
    def parse_ad_type_0x16(cls, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] Table 18.10: Service Data
            and GATT Services list https://www.bluetooth.com/specifications/gatt/services
        """
        service_uuid = int(data[2:4]+data[:2], 16) # First 2 octets contain the 16 bit service UUID, flip bytes around
        service_data = data[4:] # additional service data
        return (service_uuid, service_data)

    apple_data_types = {
        '02': 'ibeacon',
        '05': 'airdrop',
        '07': 'airpods',
        '08': '(unknown)',
        '09': 'airplay_dest',
        '0a': 'airplay_src',
        '0c': 'handoff',
        '10': 'nearby',
    }

    @classmethod
    def parse_ad_type_0xff(cls, data):
        """ Implementation of Bluetooth Specification Version 4.0 [Vol 3] Table 18.11: Manufacturer Specific Data
            and Company Identifier List: https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers
        """
        company_id = int(data[2:4]+data[:2], 16) # First 2 octets contain the 16 bit service UUID, flip bytes around
        man_specific_data = data[4:] # additional service data
        d = {}
        d["company_id"] = company_id
        d["raw"] = man_specific_data
        if company_id == 0x0006:
            d["company_name"] = "Microsoft"
        elif company_id == 0x004c:
            d["company_name"] = "Apple"
            # iBeacon: see format @ https://support.kontakt.io/hc/en-gb/articles/201492492-iBeacon-advertising-packet-structure
            d["ibeacon"] = (0x1502 == int(man_specific_data[2:4]+man_specific_data[:2], 16))
            while man_specific_data:
                if man_specific_data[:2] in cls.apple_data_types:
                    apple_type = cls.apple_data_types[man_specific_data[:2]]
                else:
                    apple_type = '(unknown)'
                apple_len  = int(man_specific_data[2:4], 16)
                apple_data = man_specific_data[4:4+2*apple_len]
                d[apple_type] = apple_data
                man_specific_data = man_specific_data[4+2*apple_len:]
                #print "###", data, apple_type, apple_len, apple_data, man_specific_data
        return d


if __name__ == "__main__":
    def print_r(d, level=0):
        for k,v in d.items():
            if isinstance(v, dict):
                print(level*"\t" + k + ":")
                print_r(v,level+1)
            else:
                print(level*"\t" + "%s: %s" % (k, v) )

    example_data = ["02011a1aff4c000c0e00750f812422021c3e213d190f3310050b1c6d9072",
                    "02011a0aff4c0010050b1c6d9072"
    ]
    print("Hi, this is just a demo:")
    for data in example_data:
        print("Parsing %s" % data)
        print_r(BTLEAdvClassifier.parse_data(data), 1)
