f = open('b327c0bbb16c9adcd566877ac29dc0b0edcff9e654dad66c514b19877a45b6c8_dictionary.txt','r') #dictionary file
f2 = open('allmappings.txt','r').read().split('\n') #permissions file

i = 0
permissions = set()
currentPermissions = ''
for line in f:
    line = line[:line.rfind(':')]
    for line2 in f2:
        if(line2.startswith('Permission:')):
            currentPermission = line2[11:]
        if(line in line2):
            permissions.add(currentPermission)

for permission in permissions:
    print(permission)
