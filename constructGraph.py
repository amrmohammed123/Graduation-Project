import os
#for multiple apk folders use constructAllGraphs
#for one apk folder user constructGraph
import time
def constructAllGraphs(path):
    for filename in os.listdir(path):
        constructGraph(os.path.join(path,filename),open(filename+'.txt','a'))

def constructGraph(path, file):
    for filename in os.listdir(path):
        nextPath = os.path.join(path,filename)
        if os.path.isdir(nextPath):
            #it's a directory call constructGraph again (recursively)
            constructGraph(nextPath, file)
        else:
            #check extension
            if(filename.endswith('.smali')):
                constructGraphFromSmali(nextPath,file)

def constructGraphFromSmali(path, output):
    currentClass = ''
    currentMethod = ''
    currentInvokeMethod = ''
    file = open(path, 'r', errors='ignore')
    for line in file:
        #check for current class
        if(line.startswith('.class')):
            for i in range(0,len(line)):
                if line[i] == 'L':
                    currentClass = line[i:-1]
                    break
        #check for current method
        elif(line.startswith('.method')):
            currentMethod = line[line.rfind(' ')+1:]
            output.write(currentClass + '->' + currentMethod)
        #check for current invoke method
        elif(line.lstrip().startswith('invoke')):
            for j in range(0,len(line)):
                if line[j] == 'L':
                    currentInvokeMethod = line[j:]
                    output.write('\t'+currentInvokeMethod)
                    break
    file.close()

#pass folder name to constructAllGraphs
constructAllGraphs("c")



