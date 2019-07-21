Sample source for CoreBlutooth via PyObjC(Python)
====

#Overview

## Description

 This sample source code is writing in how to implementation BLE application using python on OSX.
 It is using CoreBluetooth Library via [PyObjC](https://pythonhosted.org/pyobjc/).
 Target BLE device is [2JCIE-BL01 OMRON Enviroment sensor](http://www.omron.co.jp/ecb/products/sensor/special/environmentsensor/).

## Tested Version

Mac OSX 10.14.5
Python 3.6 (Anaconda Distribution)

## License

[MIT LICENCE](https://github.com/masato-ka/geo-hash-potate/blob/master/LICENSE.txt)

# Build and Run

##Install PyObjC

You must install pyobjc first. You can try to install it using pip with:

    pip install pyobjc

If that fails, you can install it from source downloaded with mecruial:

  $ hg clone https://bitbucket.org/ronaldoussoren/pyobjc
  $ python3 pyobjc/install.py

Finally, you can download and install a pre-compiled verison from:

* https://www.dropbox.com/sh/vkfzaa5m1snch8h/AABq4RTvbRl1fvVpHaGSoe0Ma?dl=0

##Run script

```
$ cd corebluetooth
$ python corebluetooth_sample.py
```

# See Also
* [Python - Human Interface Device Android Attack Framework](https://github.com/SkiddieTech/HIDAAF)
* [Creating a Simple BLE Scanner on iPhone](https://scribles.net/creating-a-simple-ble-scanner-on-iphone/)
* [Adafruit - Connecting to a Peripheral](https://learn.adafruit.com/crack-the-code/connecting)

# Authors


* Original code: [@masato-ka](https://twitter.com/masato_ka)
* Rewrite by: [simsong](https://github.com/simsong)


