import sys
import time

def bfs(nrNodes, edges, start, end):   
    #Start with: no nodes visited, no nodes in found, startNode in QUE, and an empty path and minimal capacity of -1.
    visited = [False] * nrNodes
    found = [[0,0]] * nrNodes
    QUE = [start]
    path = [[],-1]

    #Set visited to True for start, because we start here
    visited[start] = True

    #For every node in the QUE we now do the classic BFS from that node
    while len(QUE)>0:
        #set startNode (from which node we apply BFS) to the first element of QUE, and pop it from the QUE
        startNode = QUE[0]
        QUE.pop(0)
        
        #For all edges adjacent to startNode in the adjacency-list
        for adjacent in edges[startNode]:
            #get the end of the edge, and get the value
            node, value = adjacent

            #If we have not visited the end yet, and the value of the edge is > 0 (otherwise that edge is at capacity)
            if (not visited[node]) and (value > 0):

                #If we have reached the end, construct the path
                if node == end:

                    #While we are not at start yet
                    while(startNode!=start):
                        #append each node we visit to the path
                        path[0].append( [startNode, node, value] )

                        #Creat appropriate minimal capacity, by testing if newCap>oldCap || oldCap < 0 (we chose this oldCap<0, such that we can always use it, otherwise
                        #We would have to set the original value equal to the maximum possible, but this would be harder.
                        if (value < path[1] or path[1]<0) and (startNode!=start and node!=end):
                            path[1] = value
                            
                        #Shift startNode to node, and get new startNode from found
                        node = startNode
                        startNode = found[startNode][0]

                        #get new value, for minimum capacity
                        value = found[node][1]

                    #Append last node to the path
                    path[0].append( [start, node, value] )
                    #Reverse path, as we created it backwards
                    path[0].reverse()
                    return path

                #If we have not reached the end, append this node to the QUE, set visited to True and set found to [startNode, value]
                #This such that we can use this to traverse through our steps backwards when constructing the path
                else:
                    QUE.append(node)
                    found[node]=[startNode,value]
                    visited[node]=True
                    
    return []

def getDgraph(edges, NR_CITIES, D, start, end):
    #Initialize empty return edges list
    edges_ret = [[] for x in range(NR_CITIES)]
    #For every edge, add it if value>=D
    for startNode in range(NR_CITIES):
        for endNode, value in edges[startNode]:
            if value >= D or startNode == start or endNode == end:
                edges_ret[startNode].append([endNode,value])
    return edges_ret

def fordFulkerson(NR_CITIES, start, end, edges_orig):
    #Initialize D with a negative number, such that any val will be larger
    D = -1

    #Set D to the maximum capacity
    for startNode in range(NR_CITIES):
        for endNode, val in edges_orig[startNode]:
            if val>D:
                D=val
    
    #As long as D is larger than 1, we apply fordFulkerson with capacity scaling
    while D>=1:

        #Get the new dGraph, for capacity scaling. Meaning only edges with capacity>=D are included.
        edges = getDgraph(edges_orig, NR_CITIES, D, start, end)

        #Apply bfs to find a path and minimum value
        res = bfs(NR_CITIES,edges,start,end)

        #repeat finding paths and updating the flow, as long as there is a path from start->end
        while(res != []):
            #get that path and minimum value from the result of bfs
            path, m = res
            keep_m = m

            #Add a new edge from end -> last node in path
            edges_orig[end].append( [path[len(path)-1][0],m] )

            #For everything in path, except for start and end
            for index in range(1,len(path)-1):
                #reset m (We do this such that we are sure that if we have 2 edges from a->b they will both be used, rather than only 1!)
                m=keep_m

                #get information from path
                startNode, endNode, value = path[index]

                #Update path and set m=0, such that we only update 1 path!
                for edge in edges_orig[startNode]:
                    if edge[0]== endNode and edge[1] == value:
                        edge[1] -= m
                        edges_orig[endNode].append( [startNode,m] )
                        m=0

            #Get the new dGraph, for capacity scaling. Meaning only edges with capacity>=D are included.
            edges = getDgraph(edges_orig, NR_CITIES, D, start, end)

            #Apply bfs to find a path and minimum value
            res = bfs(NR_CITIES,edges,start,end)

        #Update D for capacity scaling
        D/=2

    #return all edges from end -> some city
    ret = 0
    for edge in edges[end]:
        ret+=edge[1]
        
    return ret

def getInput():   
    #Getting the problem from the server
    NR_CITIES, NR_ROADS = [int(x) for x in input().split(' ')]
    print(f"NR_CITIES:{NR_CITIES} ", file=sys.stderr)
    print(f"NR_ROADS:{NR_ROADS} ", file=sys.stderr)

    #Basic case: If we have no cities, just one city or no roads then we can cleary not evacuate any people. So return 0.
    if(NR_CITIES == 0 or NR_CITIES == 1 or NR_ROADS == 0):
        print(0)
        return
    
    E, D = [int(x) for x in input().split(' ')]
    print(f"E:{E} ", file=sys.stderr)
    print(f"D:{D} ", file=sys.stderr)

    #Basic case: If we have no endagered cities or no destination cities, we cannot evacuate anyone. So return 0.
    if(E == 0 or D == 0):
        print(0)
        return
    
    END = [int(x) for x in input().split(' ')]
    print(f"END:{END} ", file=sys.stderr)
    DES = [int(x) for x in input().split(' ')]
    print(f"DES:{DES} ", file=sys.stderr)

    #Create a start-node and an end-node.
    #All endangered cities e_i will have an edge from start->e_i, such that we can apply ford-fulkerson
    #The same goes from destionation cities d_i, with edge d_i -> end.
    #These edges will have capacity of 1, and will not be updated by the algorithm
    
    start = NR_CITIES
    end = NR_CITIES+1
    
    #Increase nrOfCities to include these two abstract cities
    NR_CITIES+=2
    
    #Initialize ROADS array, with space for each of the cities and start and end.
    ROADS = [[[0,0]] for x in range(NR_CITIES)]

    #read all edges, and append them
    for x in range(NR_ROADS):
        startNode, endNode, value = [int(x) for x in input().split(' ')]
        ROADS[startNode].append( [endNode,value] )

    #As stated above, edges from start -> e_i and d_i -> end
    for x in END:
        ROADS[start].append( [x,1] )

    for x in DES:
        ROADS[x].append( [end,1] )

    #Print the result of our fordFulkerson function, aka the max-flow
    print( fordFulkerson(NR_CITIES, start, end, ROADS) )
        

def main():
    #Load and solve the problem
    getInput()

if __name__ == "__main__":
    main()
