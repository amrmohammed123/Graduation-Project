import os
#for multiple apk folders use constructAllGraphs
#for one apk folder user constructGraph
import time
def constructAllGraphs(path):
    for filename in os.listdir(path):
        methodsDictionary = {'dummyMain':0}
        methodsArray = []
        f = open(filename+'_dictionary.txt','w')
        global adjacencyIndex
        adjacencyIndex = 1
        constructGraph(os.path.join(path,filename), methodsDictionary, True, methodsArray)
        for key, value in methodsDictionary.items():
            f.write(key + ':'+str(value) + '\n')
        adj = []
        #handle dummy main row (all ones)
        firstRow = []
        for j in range(0,adjacencyIndex):
            firstRow.append(1)
        adj.append(firstRow)
        #handle remained methods
        for i in range(1,adjacencyIndex):
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
                formatedMethod = changeFormat((currentClass + '->' + currentMethod))
                methodsArray.append(formatedMethod)
                if (not (formatedMethod in methodsDictionary)):
                    methodsDictionary[formatedMethod] = adjacencyIndex
                    adjacencyIndex += 1
            # check for current invoke method
            elif (line.lstrip().startswith('invoke')):
                for j in range(0, len(line)):
                    if line[j] == 'L':
                        currentInvokeMethod = line[j:]
                        formatedMethod = changeFormat(currentInvokeMethod)
                        methodsArray.append(('\t'+formatedMethod))
                        if(not (formatedMethod in methodsDictionary)):
                            methodsDictionary[formatedMethod] = adjacencyIndex
                            adjacencyIndex += 1
                        break

        file.close()
    except FileNotFoundError:
        return

def changeFormat(method):
    method = method[:-1]
    className = ''
    returnType = ''
    methodName = ''
    i = 1
    currentClass = ''
    startMethodName = False
    startReturnType = False
    arrayFoundReturnType = False
    arrayFoundmethodName = False
    arrayFoundClassName = False
    while i < len(method):
        #check for [] (array)
        if(startMethodName and method[i] == ')'):
            if (arrayFoundmethodName):
                methodName += '[])'
                arrayFoundReturnType = False
                i += 1
                continue
        if (method[i] == '['):
            i += 1
            continue
        if(startReturnType and method[i] == 'L' and method[i-1] == '['):
            arrayFoundReturnType = True
            i += 1
            continue
        if(startMethodName and method[i] == 'L' and method[i - 1] == '['):
            arrayFoundmethodName = True
            i += 1
            continue
        if(method[i] == 'L' and (method[i-1] == ';' or method[i-1] == '(' or method[i-1] == ')')): #chjeck for L
            i += 1
            continue
        if(method[i] == '/'): #check for /
            if (startReturnType):
                returnType += '.'
            elif (startMethodName):
                methodName += '.'
            else:
                className += '.'
            i += 1
            continue
        if(method[i] == ';'): #check for ;->
            if(i+1 < len(method) and method[i+1] == '-' and i+2 < len(method) and method[i+2] == '>'):
                currentClass = className[className.rfind('.')+1:]
                startMethodName = True
                i += 3
                continue
        if(method[i] == '<'):#check for <clinit> and <init>
            if(method.find('<init>',i) != -1): # check for <init>
                i += 6
                methodName += currentClass #replace it with class name
                continue
            elif(method.find('<clinit>',i) != -1):
                i += 8
                methodName += 'static' #replace it with static
                continue
        if(method[i] == ')'): #check for the start of return type
            startReturnType = True
            methodName += method[i]
            i += 1
            continue
        if(method[i-1] == ')'): #check for prmitive types
            # V - void, B - byte, S - short, C - char, I - int
            # J - long (uses two registers), F - float, D - double
            if(method[i] == 'V'):
                returnType += 'void'
                i += 1
                continue
            elif(method[i] == 'B'):
                returnType += 'byte'
                i += 1
                continue
            elif(method[i] == 'S'):
                returnType += 'short'
                i += 1
                continue
            elif(method[i] == 'C'):
                returnType += 'char'
                i += 1
                continue
            elif(method[i] == 'I'):
                returnType += 'int'
                i += 1
                continue
            elif(method[i] == 'J'):
                returnType += 'long'
                i += 1
                continue
            elif(method[i] == 'F'):
                returnType += 'float'
                i += 1
                continue
            elif(method[i] == 'D'):
                returnType += 'double'
                i += 1
                continue
            elif(method[i] == 'Z'):
                returnType += 'boolean'
                i += 1
                continue
        #check for ;
        if(method[i] == ';'):
            if (startMethodName and i+1 < len(method) and method[i+1] != ')'):
                if (arrayFoundReturnType):
                    returnType += '[],'
                    arrayFoundReturnType = False
                    i += 1
                    continue
                elif (arrayFoundmethodName):
                    methodName += '[],'
                    arrayFoundmethodName = False
                    i += 1
                    continue
                methodName += ','
            i += 1
            continue
        if(startReturnType):
            returnType += method[i]
        elif(startMethodName):
            methodName += method[i]
        else:
            className += method[i]
        i += 1
    if (arrayFoundReturnType):
        returnType += '[]'
        arrayFoundReturnType = False
        i += 1
    return '<' + className + ': '+ returnType + ' '+ methodName + '>'

#pass folder name to constructAllGraphs
t0 = time.time()
adjacencyIndex = 1

constructAllGraphs("c")
print(time.time() - t0)
print(adjacencyIndex)
