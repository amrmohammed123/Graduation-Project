import os

#put the folders coming from zip in form drebin-0 , drebin-1, drebin-2 , drebin-3, drebin-4, drebin-5
for i in range(0,6):
    for filename in os.listdir("drebin-"+str(i)):
        os.system('apktool d ' + os.path.join("drebin-"+str(i),filename) +' -o '+ os.path.join('output',"drebin-"+str(i),filename))
