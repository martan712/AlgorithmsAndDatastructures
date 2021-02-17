#For client side debugging, not relevant to solution
import sys

#For client side graphing, not relevant to solution
import numpy as np   
import networkx as nx  
import matplotlib.pyplot as plt

#Open debuf file
f = open('debug.txt', 'w')

#GLOBALS
counter = 0
originalGroupSize = 0
NR_OF_TESTS = 0
points = 0

#####
def graph(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    labelmap = dict(zip(G.nodes(), list(range(nrNodes))))
    nx.draw(G, labels=labelmap, with_labels=True) 
    plt.show()

def graphCases(nodes, infected, edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    labelmap = dict(zip(G.nodes(), nodes))
    labelmap2 = dict(zip(G.nodes(), nodes))
    colors = ["Blue"]*len(nodes)
    for i in infected:
        colors[i] = "Red"
    try:
        nx.draw(G, labels=labelmap, with_labels=True, node_color = colors) 
        plt.show()
    except:
        nx.draw(G, labels=labelmap, with_labels=True)
#####

def sendTest(string, upperBound):
    global counter
    global NR_OF_TESTS
    global originalGroupSize
    global points

    #If we have not yet found max number of tests, go here
    if counter<upperBound:
        points -= int(1000000/originalGroupSize)
        #Send string to server
        print(string)
        #print(string, file=sys.stderr)
        response = input()
        print(f"Node(s)  {string} tested: {response}", file=f)
        NR_OF_TESTS+=1
        return response
    
    #Skip test if we already found all
    return "false"

def testGroup(group, upperBound):
    global counter
    group.sort()
    #Create test string
    string = ""
    for i in group:
        string += " "+str(i)
    
    #Catch response
    response =sendTest(f"test{string}", upperBound)

    #Return response as boolean
    return response=="true"
    
def test(nodes, upperB, splitNr):
    global counter
    #Initialization of return
    result = []
    #Base case
    if(len(nodes)<=3):
        for i in nodes:
            response = sendTest(f"test {i}", upperB)
            if(response == "true"):
                result.append(i)
                counter+=1
                
    #Recursive cases       
    elif (len(nodes)<16):
        splitNr = 2
        #Split into splitNr groups
        groupSize = int(len(nodes)/splitNr)
        finalGroupSize = len(nodes) - groupSize*(splitNr-1)

        #recursive call for each group
        for i in range(splitNr-1):
            group = nodes[i*groupSize : (i+1)*groupSize]
            #print(group, file=sys.stderr)
            result += testWithCheck(group, upperB, splitNr, False)
        
        group = nodes[len(nodes)-finalGroupSize:]
        result += testWithCheck(group, upperB, splitNr, False)


    else:
        #Split into splitNr groups
        groupSize = int(len(nodes)/splitNr)
        finalGroupSize = len(nodes) - groupSize*(splitNr-1)

        #recursive call for each group
        for i in range(splitNr-1):
            group = nodes[i*groupSize : (i+1)*groupSize]
            #print(group, file=sys.stderr)
            result += testWithCheck(group, upperB, splitNr, False)
        
        group = nodes[len(nodes)-finalGroupSize:]
        result += testWithCheck(group, upperB, splitNr, False)

        
    #Return value 
    return result

def testWithCheck(group, upperB, splitNr, alwaysCheck):
    #Initialize array
    result = []

    #Test if someone in group has Corona if metric is met
    if(len(group)< int(originalGroupSize/upperB) and len(group)!=2) or alwaysCheck:
        if(testGroup(group,upperB)):
            #Test groups, will start recursion
            result = test(group, upperB, splitNr)
            
    #If metric fails, then split without testing the group
    else:
        result = test(group, upperB, splitNr)
    return result

def bfs(nodes, startNode, edges, alreadyDone):
    #Start with no nodes found, and with startNode in QUE
    found = []
    QUE = [startNode]

    #For every node in the QUE
    for start in QUE:
        #For all nodes
        for node in nodes:
            #If node can be reached, add it to found and alreadyDone
            if not node in alreadyDone:
                if (edges[start][node] == 1 or edges[node][start] == 1):
                    found.append(node)
                    alreadyDone.append(node)
                    QUE.append(node)
    return found
            

def getGroups(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges):
    #Initialize lists
    groups = []
    alreadyDone = []
    nodes = list(range(nrNodes))

    #For every node
    for n1 in nodes:
        #If it wasn't put in a group already
        if not n1 in alreadyDone:
            #Create new group
            group = [n1]
            #Add current node to the list of nodes that are done
            alreadyDone.append(n1)
            #BFS from n1, add all those to the group and alreadyDone
            group+=bfs(nodes, n1, edges, alreadyDone)
            #Add group to groups
            groups.append(group)

    #Print grouped list
    s = sum(groups,[])
    s.sort()
    #print(s,file=sys.stderr)
    return groups

def formatGroups(groups, minLength):
    #Groups tiny groups together
    ret = []
    groupsSorted = sorted(groups, key=len)
    for index in range(len(groupsSorted)):
        if(len(groupsSorted[index]) < minLength and index < len(groupsSorted)-1):
            groupsSorted[index+1]+=groupsSorted[index] 
        else:
            ret.append(groupsSorted[index])
    return ret


def filterClusters(clusters, nodes):
    clusters = sorted(clusters, key=len, reverse=True)
    alreadyFound = []
    ret = []
    
    for cluster in clusters:
        addCluster = True
        for node in cluster:
            if node in alreadyFound:
                addCluster = False
        if addCluster:
            ret.append(cluster)
            alreadyFound+=cluster

    rest = []
    s = sum(ret,[])
    for x in nodes:
        if x not in s:
            rest.append(x)

    ret.append(rest)
    
    return ret
    
def getCluster(nodes, edgesMatrix, startNode, alreadyFound):
    cluster = [startNode]
    for node in nodes:
        if not node in cluster:
            add = True
            for node2 in cluster:
                if not (edgesMatrix[node2][node] == 1 or edgesMatrix[node][node2] == 1):
                    add = False

            if add:
                cluster.append(node)
    return cluster

def getClusters(nodes, edgesMatrix):
    #Initialization
    alreadyFound = []
    clusters = []

    #For each node, find all clusters
    for node in nodes:
        clusters.append(getCluster(nodes,edgesMatrix,node, alreadyFound))

    #Return clusters
    return filterClusters(clusters, nodes)



def testGroups(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges):
    #Initialization
    print("started testing", file=sys.stderr)
    tested = []
    splitNr = 4
    minGroupSize= 4
    
    #If we have edges, search for subgraphs
    if(nrEdges>0):
        groups = getGroups(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges)
        print(groups,file=f)
        print("", file=f)

        #If we already split the graph we are done
        if len(groups) > 1:
            groups = formatGroups(groups,minGroupSize)
            print("Seperate groups are present",file=f)
            print("Seperate groups are present",file=sys.stderr)
            #print(groups, file=sys.stderr)
            for group in groups:
                print(group,file=f)
                tested += testWithCheck(group, upperB, splitNr, True)

        #Otherwise, try to find clusters
        else:
            print("Clusters created",file=f)
            groups = getClusters(groups[0], edges)
            print(groups,file=f)
            for group in groups:
                print(group,file=f)
                tested += testWithCheck(group, upperB, splitNr, True)
    
    #No edges, so we use binary search as we cannot exploit the relations in the graph since there are none
    else:
        tested+=testWithCheck(list(range(nrNodes)), upperB, splitNr, False)

    #Signal that testing is finished to console
    print("done testing", file=sys.stderr)
    #Return test results
    return tested

def answer(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges, edges_graph):
    #Get global total nr of tests, and set it to 0
    global points
    global NR_OF_TESTS
    
    NR_OF_TESTS = 0
    
    #Get infected nodes
    result = testGroups(nrNodes,nrEdges,initInf,probInf,lowerB,upperB,edges)
    #Sort infected nodes
    result.sort()

    #Show the result
    #print(result, file=sys.stderr)

    #Get answer string from results
    string = str(result[0])
    for i in range(1,len(result)):
        string+= " "+str(result[i])

    #Send answer to server    
    print(f"answer {string}")
    #Getting result from server
    response = input()

    #Increase point estimate if correct
    if(response == "succes"):
        points+=1000000
        
    #Graph results
    #graphCases(list(range(nrNodes)), result, edges_graph) #Corona marked red
    #graph(NR_NODES,NR_EDGES,INIT_INF,PROB_INF,LOWER_B,UPPER_B,EDGES) #Corona not marked
        
    #Output feedback on problem
    print(f"tests: {response} with {NR_OF_TESTS} tests for {nrNodes} nodes", file=sys.stderr)
    print(f"tests: {response} with {NR_OF_TESTS} tests for {nrNodes} nodes", file=f)

    #Current points estimates
    print(f"points: {points}",file=sys.stderr)
        
def single_problem():
    global counter, originalGroupSize
    counter = 0
    
    #Getting the problem from the server
    NR_NODES = int(input())
    print(f"NO_NODES: {NR_NODES}", file=f)
    NR_EDGES = int(input())
    print(f"NR_EDGES: {NR_EDGES}", file=f)
    INIT_INF = int(input())
    print(f"INIT_INF: {INIT_INF}", file=f)
    PROB_INF = float(input())
    print(f"PROB_INF: {PROB_INF}", file=f)
    
    LOWER_B, UPPER_B = [int(x) for x in input().split(' ')]
    print(f"LOWER_B: {LOWER_B}, UPPER_B: {UPPER_B}", file=f)
    EDGES = []
    EDGES_MATRIX = [ [ 0 for y in range( NR_EDGES) ] 
                 for x in range( NR_EDGES ) ]
    
    for edges in range(NR_EDGES):
        edge = [int(x) for x in input().split(' ')]
        EDGES.append(edge)
        EDGES_MATRIX[edge[0]][edge[1]]=1
        #print(f"edge: {edge}", file=f)

    originalGroupSize = NR_NODES
    
    answer(NR_NODES,NR_EDGES,INIT_INF,PROB_INF,LOWER_B,UPPER_B,EDGES_MATRIX, EDGES)   
    print("", file=f)

def main():
    #Get number of problems
    global points
    
    NR_PROBLEMS = int(input())

    #Load every problem
    for i in range(NR_PROBLEMS):
        print(f"Current problem: {i+1}/19",file=sys.stderr)
        print(f"Current problem: {i+1}", file=f)
        single_problem()
        
    print(points,file=f)

if __name__ == "__main__":
    main()
