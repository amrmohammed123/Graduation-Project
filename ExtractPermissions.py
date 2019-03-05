def extractPermissions(methodsDictionary, mappingFileName, androidManifestPath):
    mapping = open(mappingFileName,'r')
    permissionDictionary = {key:set() for key in methodsDictionary.keys()}
    #extract requested permissions from uses-permission tag
    androidManifest = open(androidManifestPath, 'r')

    for line in androidManifest:
        line = line.lstrip()
        if(line.startswith('<uses-permission')):
            quoteFound = False
            permission = ''
            for i in range(line.find('android:name')+12,len(line)):
                if(line[i] == '"'):
                    if(quoteFound):
                        # add the permission to dummyMain
                        permissionDictionary['dummyMain'].add(permission.strip())
                        break
                    else:
                        quoteFound = True
                        continue
                if(quoteFound):
                    permission += line[i]
    androidManifest.close()
    #map permissions to methods
    currentPermission = ''
    for line in mapping:
        if(line.startswith('Permission:')):
            currentPermission = line[11:-1]
            continue
        if(line[0] == '<'): # a method
            methodName = line[:line.rfind('>')+1]
            if(methodName in permissionDictionary and currentPermission in permissionDictionary['dummyMain']):
                permissionDictionary[methodName].add(currentPermission)
    mapping.close()
    f = open('checkPermissions.txt','w')
    for key in permissionDictionary:
        value = str(permissionDictionary[key])
        if(value == 'set()'):
            f.write(key + '\n')
        else:
            f.write(key + ' : ' + value + '\n')


