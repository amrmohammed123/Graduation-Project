def extractHardwareFeatures(permissionsDictionary, androidManifestFilePath, apktoolYmlFilePath):
    #find minSdkVersion
    apktoolYml =  open(apktoolYmlFilePath, 'r')
    minSdkVersion = 1 #default value
    for line in apktoolYml :
        line = line.lstrip()
        if(line.startswith('minSdkVersion:')):
            temp = ''
            for i in range(line.find("'")+1,len(line)):
                if(line[i] == "'"):

                    break
                temp += line[i]
            try:
                minSdkVersion = int(temp)
            except ValueError:
                minSdkVersion = 1
            break
    HardwareDictionary = {key: set() for key in permissionsDictionary.keys()}
    #open android manifest file
    androidManifest = open(androidManifestFilePath, 'r')
    #get hardware feature from uses-feature, and android:screenOrientation from activies
    orientationDictionary = {} #key:method name , value:hardware feature of orientation
    packageName = ''
    manifestNotFound = True
    for line in androidManifest:
        line = line.lstrip()
        #get package name
        if(manifestNotFound):
            manifestStart = line.find('<manifest')
            if(manifestStart != -1):
                manifestStart += 10
                manifestNotFound = False
                quoteFound = False
                for i in range(line.find('package')+7,len(line)):
                    if(line[i] == '"'):
                        if(not quoteFound):
                            quoteFound = True
                            continue
                        else:
                            break
                    if(quoteFound):
                        packageName += line[i]
                packageName = packageName.strip()
                quoteFound = False
        if(line.startswith('<activity')): #get android:screenOrientation
            quoteFound = False
            key = ''
            for i in range(line.find('android:name')+12,len(line)):
                if(line[i] == '"'):
                    if(not quoteFound):
                        quoteFound = True
                        continue
                    else:
                        break
                if(quoteFound):
                    key += line[i]
            quoteFound = False
            value = ''
            for i in range(line.find('android:screenOrientation')+25,len(line)):
                if(line[i] == '"'):
                    if(not quoteFound):
                        quoteFound = True
                        continue
                    else:
                        break
                if(quoteFound):
                    value += line[i]
            #add to orientation dictionary
            key = key.strip()
            value = value.strip()
            if(key.startswith('.')):
                key = packageName + key
            if(value != '' and key != ''):
                if(value == 'portrait'):
                    orientationDictionary[key] = 'android.hardware.screen.portrait'
                elif(value == 'landscape'):
                    orientationDictionary[key] = 'android.hardware.screen.landscape'
        elif(line.startswith('<uses-feature')):
            quoteFound = False
            hardwareFeature = ''
            for i in range(line.find('android:name')+12,len(line)):
                if(line[i] == '"'):
                    if(not quoteFound):
                        quoteFound = True
                        continue
                    else:
                        HardwareDictionary['dummyMain'].add(hardwareFeature.strip())
                        break
                if(quoteFound):
                    hardwareFeature += line[i]
    #assign android.hardware.screen.landscape or protrait to corresponding methods
    for method in HardwareDictionary:
        #find className
        className = method[1:method.find(':')]
        if(className in orientationDictionary):
            HardwareDictionary[method].add(orientationDictionary[className])
    #map permissions to hardware (based on aapt code)
    for method in permissionsDictionary:
        if('android.permission.CAMERA' in permissionsDictionary[method]):
            HardwareDictionary[method].add('android.hardware.camera')
        if('android.permission.ACCESS_FINE_LOCATION' in permissionsDictionary[method]):
            HardwareDictionary[method].add('android.hardware.location')
            if(minSdkVersion < 21): # 21 for SDK_LOLLIPOP
                HardwareDictionary[method].add('android.hardware.location.gps')
        if('android.permission.ACCESS_COARSE_LOCATION' in permissionsDictionary[method]):
            HardwareDictionary[method].add('android.hardware.location')
            if(minSdkVersion < 21): # 21 for SDK_LOLLIPOP
                HardwareDictionary[method].add('android.hardware.location.network')
        if (('android.permission.ACCESS_MOCK_LOCATION' in permissionsDictionary[method])
            or ('android.permission.ACCESS_LOCATION_EXTRA_COMMANDS' in permissionsDictionary[method])
            or ('android.permission.INSTALL_LOCATION_PROVIDER' in permissionsDictionary[method])):
            HardwareDictionary[method].add('android.hardware.location')
        if(('android.permission.BLUETOOTH' in permissionsDictionary[method])
            or ('android.permission.BLUETOOTH_ADMIN' in permissionsDictionary[method])):
            if(minSdkVersion > 4 ): # 4 for SDK_DONUT
                HardwareDictionary[method].add('android.hardware.bluetooth')
        if('android.permission.RECORD_AUDIO' in permissionsDictionary[method]):
            HardwareDictionary[method].add('android.hardware.microphone')
        if(('android.permission.ACCESS_WIFI_STATE' in permissionsDictionary[method])
            or ('android.permission.CHANGE_WIFI_STATE' in permissionsDictionary[method])
            or ('android.permission.CHANGE_WIFI_MULTICAST_STATE' in permissionsDictionary[method])):
            HardwareDictionary[method].add('android.hardware.wifi')
        if(('android.permission.CALL_PHONE' in permissionsDictionary[method])
            or ('android.permission.CALL_PRIVILEGED' in permissionsDictionary[method])
            or 'android.permission.MODIFY_PHONE_STATE' in permissionsDictionary[method]
            or 'android.permission.PROCESS_OUTGOING_CALLS' in permissionsDictionary[method]
            or 'android.permission.READ_SMS' in permissionsDictionary[method]
            or 'android.permission.RECEIVE_SMS' in permissionsDictionary[method]
            or 'android.permission.RECEIVE_MMS' in permissionsDictionary[method]
            or 'android.permission.RECEIVE_WAP_PUSH' in permissionsDictionary[method]
            or 'android.permission.SEND_SMS' in permissionsDictionary[method]
            or 'android.permission.WRITE_APN_SETTINGS' in permissionsDictionary[method]
            or 'android.permission.WRITE_SMS' in permissionsDictionary[method]):
            HardwareDictionary['dummyMain'].add('android.hardware.faketouch')
    if('android.hardware.touchscreen' not in HardwareDictionary['dummyMain']):
        HardwareDictionary['dummyMain'].add('android.hardware.telephony')
    #return dictionary of methods to hardwareFeatures
    f = open('checkHardware.txt','w')
    for key in HardwareDictionary:
        value = str(HardwareDictionary[key])
        if(value == 'set()'):
            f.write(key + '\n')
        else:
            f.write(key + ' : ' + value + '\n')
    apktoolYml.close()
    androidManifest.close()
    f.close()
    return HardwareDictionary