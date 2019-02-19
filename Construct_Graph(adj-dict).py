import os
#for multiple apk folders use constructAllGraphs
#for one apk folder user constructGraph
import time
def constructAllGraphs(path):
    for filename in os.listdir(path):
        methodsDictionary = {}
        methodsArray = []
        f = open(filename+'_dictionary.txt','w')
        global adjacencyIndex
        adjacencyIndex = 0
        constructGraph(os.path.join(path,filename), methodsDictionary, True, methodsArray)
        for key, value in methodsDictionary.items():
            f.write(key[:-1]+':'+str(value)+'\n')
        adj = []
        for i in range(0,adjacencyIndex):
            temp = []
            for j in range(0,adjacencyIndex):
                temp.append(0)
            adj.append(temp)
        for line in methodsArray:
            if(line.startswith('\t')):
                line2 = line[1:]
                adj[currentNode][methodsDictionary[line2]] += 1
            else:
                currentNode = methodsDictionary[line]
        f5 = open(filename+'_adjacency.txt','w')
        for z in adj:
            f5.write(str(z)+'\n')
        f5.close()





def constructGraph(path, methodsDictionary, firstTime, methodsArray):
    global adjacencyIndex
    for filename in os.listdir(path):
        nextPath = os.path.join(path,filename)
        if os.path.isdir(nextPath):
            if(firstTime):
                if(not filename.startswith('smali')):
                    continue
            #it's a directory call constructGraph again (recursively)
            constructGraph(nextPath, methodsDictionary, False, methodsArray)
        else:
            #check extension
            if(filename.endswith('.smali')):
                constructGraphFromSmali(nextPath, methodsDictionary, methodsArray)

def constructGraphFromSmali(path, methodsDictionary, methodsArray):
    global adjacencyIndex
    currentClass = ''
    currentMethod = ''
    currentInvokeMethod = ''
    try:
        file = open(path, 'r', errors='ignore')
        for line in file:
            # check for current class
            if (line.startswith('.class')):
                for i in range(0, len(line)):
                    if line[i] == 'L':
                        currentClass = line[i:-1]
                        break
            # check for current method
            elif (line.startswith('.method')):
                currentMethod = line[line.rfind(' ') + 1:]
                methodsArray.append((currentClass + '->' + currentMethod))
                if (not ((currentClass + '->' + currentMethod) in methodsDictionary)):
                    methodsDictionary[(currentClass + '->' + currentMethod)] = adjacencyIndex
                    adjacencyIndex += 1
            # check for current invoke method
            elif (line.lstrip().startswith('invoke')):
                for j in range(0, len(line)):
                    if line[j] == 'L':
                        currentInvokeMethod = line[j:]
                        methodsArray.append('\t'+currentInvokeMethod)
                        if(not (currentInvokeMethod in methodsDictionary)):
                            methodsDictionary[currentInvokeMethod] = adjacencyIndex
                            adjacencyIndex += 1
                        break

        file.close()
    except FileNotFoundError:
        return

#pass folder name to constructAllGraphs
t0 = time.time()
adjacencyIndex = 0

constructAllGraphs("c")
print(time.time() - t0)
print(adjacencyIndex)
