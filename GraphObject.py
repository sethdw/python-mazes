# File for node and graph objects
import math

# Node object

class Node():
    def __init__(self,pos,key = "0"):
        #print "node made at",pos
        # physical location of the node
        self.location = pos
        # Connections and weights to other nodes
        self.Connections = []
        # Distance to end node
        self.Distance = 0
        # Node's key, optional
        self.key = key

    # Adds a one-way connection
    def AddConnection(self,Node,Weight):
        self.Connections += [[Node,Weight]]

    # Adds a two-way connection
    def AddArc(self,Node,Weight):
        self.AddConnection(Node,Weight)
        Node.AddConnection(self,Weight)

    # Gets connections in an array
    def GetConnections(self):
        return self.Connections

    # Gets the weight of the connection to a node, if it's got a connection
    def GetWeightTo(self,Node):
        for i in self.Connections:
            if i[0] == Node:
                return i[1]
        return -1

    # Uses pythagoras to find the physical distance to a given point
    # Point will usually be end point, but can work with any
    def SetDistance(self,pos):
        xDist = self.location[0] - pos[0]
        yDist = self.location[1] - pos[1]
        self.Distance = math.sqrt(xDist**2 + yDist**2)

    # Gets distance
    def GetDistance(self):
        return self.Distance

    # Gets position
    def GetPos(self):
        return self.location

    # Gets key
    def GetKey(self):
        return self.key

class Graph():
    def __init__(self,x,y,s,e):
        self.xsize = len(str(x))
        self.ysize = len(str(x))
        self.width = x
        self.height = y
        self.nodes = {}
        self.start = s
        self.end = e

    # generates a key from x and y coordinates
    def GetKey(self,x,y):
        # converts x and y to strings
        x = str(x)
        y = str(y)

        # gets difference in length between
        # what the length should be and what it is
        xDif = self.xsize - len(x)
        yDif = self.ysize - len(y)

        # Adds the appropriate amount of 0's to the front
        x = "0"*xDif + x
        y = "0"*yDif + y

        return x + y

    # Adds a Node to the graph
    def AddNode(self,x,y):
        key = self.GetKey(x,y)
        self.nodes[key] = Node((x,y),key)
        self.nodes[key].SetDistance(self.end)

    # Connects two nodes for given x and y coords
    def Connect(self,x1,y1,x2,y2,weight):
        # Get keys of positions
        key1 = self.GetKey(x1,y1)
        key2 = self.GetKey(x2,y2)

        # Tries to connect the two
        try:
            self.nodes[key1].AddArc( self.nodes[key2],
                                     weight )

        # If one of the keys doesn't point to anything, the dictionary will raise an error
        except:
            print "One of",(x1,y1),(x2,y2),"doesn't exist so cannot be connected!"

    # Connects two nodes for given keys
    def ConnectK(self,k1,k2,weight):
        # tries to connect the two
        try:
            self.nodes[k1].AddArc( self.nodes[k2],
                                   weight )

        # if one of the keys doesn't point to anything, an error is raised
        except:
            print "One of",k1,k2,"doesn't exist so can't be connected!"

    # Returns true if there's a node at x,y and false if not
    def IsNode(self,x,y):
        # Generate key
        key = self.GetKey(x,y)

        # Try to access node at key, if it works node exists so return true
        try:
            self.nodes[key]
            return True

        # if it doesn't work node doesn't exist so return false
        except:
            return False

    # converts maze grid to a graph
    def GridToGraph(self,grid,d=False):
        # d = true for debugging mode

        # Connects to left
        def ConnectL(self,x,y,left):
            if d: print (x,y),"connected to",left.GetPos(),"with connectC"
            # absolute of horizontal difference
            weight = abs((left.GetPos()[0] - x))

            # connect to left
            self.ConnectK(self.GetKey(x,y),
                         left.GetKey(),
                         weight)

        # Connects to above
        def ConnectA(self,x,y,above):
            if d: print (x,y),"connected to",above.GetPos(),"with connectA"
            # absolute of vertical difference
            weight = abs((above.GetPos()[1] - y))

            # connect nodes
            self.ConnectK(self.GetKey(x,y),
                         above.GetKey(),
                         weight)

        # initialise local variables
        width = len(grid)
        height = len(grid[0])
        left = [None for i in range(self.height)]
        above = None

        # debug variables
        nodesMade = []

        for x in range(1,width):
            for y in range(1,height):
                walls = [grid[x][y].GetN(),
                         grid[x][y].GetE(),
                         grid[x][y].GetS(),
                         grid[x][y].GetW()]

                if d:
                    print (x,y)
                    print walls

                """      C      """
                if walls[1] == walls[3] == False:

                    if d: print 1

                    # Wall above but not below
                    if walls[0] == True != walls[2]:
                        self.AddNode(x,y)
                        nodesMade += [(x,y)]
                        above = self.nodes[self.GetKey(x,y)]

                        ConnectL(self,x,y,left[y])
                        left[y] = self.nodes[self.GetKey(x,y)]

                    # Wall below but not above
                    if walls[2] == True != walls[0]:
                        self.AddNode(x,y)
                        nodesMade += [(x,y)]
                        ConnectA(self,x,y,above)
                        above = None

                        ConnectL(self,x,y,left[y])
                        left[y] = self.nodes[self.GetKey(x,y)]


                """    # C      """
                if walls[1] != walls[3]:

                    if d:  print 2

                    self.AddNode(x,y)
                    nodesMade += [(x,y)]

                    # Wall above but not below
                    if walls[0] == True and walls[2] == False:
                        above = self.nodes[self.GetKey(x,y)]

                    # Wall right
                    if walls[1] == True:
                        ConnectL(self,x,y,left[y])
                        left[y] = None

                    # Wall below but not above
                    if walls[2] == True and walls[0] == False:
                        ConnectA(self,x,y,above)
                        above = None

                    # wall left
                    if walls[3] == True:
                        if left[y] != None:
                            print "Left wasn't none when a new one was set!"

                        left[y] = self.nodes[self.GetKey(x,y)]

                    # wall above and below
                    if walls[0] == walls[2] == False:
                        ConnectA(self,x,y,above)
                        # change above node to this node
                        above = self.nodes[self.GetKey(x,y)]

                """    # C #    """
                if walls[1] == walls[3] == True:

                    if d: print 3

                    # above and below walls are the same
                    if walls[0] == walls[2]:
                        # do nothing
                        None

                    # Wall above but not below
                    elif walls[0] == True:
                        self.AddNode(x,y)
                        nodesMade += [(x,y)]
                        above = self.nodes[self.GetKey(x,y)]

                    # Wall below but not above
                    elif walls[2] == True:
                        self.AddNode(x,y)
                        nodesMade += [(x,y)]
                        ConnectA(self,x,y,above)
                        above = None

                try:
                    self.nodes[self.GetKey(x,y)]
                except:
                    """    # C #    where C is start or end"""
                    if (x,y) == self.start or (x,y) == self.end:

                        if d: print "made s/e"

                        # must make a node at start or end
                        self.AddNode(x,y)
                        nodesMade += [(x,y)]

                        # no wall above
                        if walls[0] == False:
                            ConnectA(self,x,y,above)
                            above = None

                        # no wall left
                        # before checking right wall so it won't link to itself
                        if walls[3] == False:
                            ConnectL(self,x,y,left[y])
                            left[y] = None

                        # no wall right
                        if walls[1] == False:
                            left[y] = self.nodes[self.GetKey(x,y)]

                        # no wall below
                        if walls[2] == False:
                            above = self.nodes[self.GetKey(x,y)]

                if d: print

        return nodesMade


    # performs A*
    def AStar(self):
        # A* produces a dictionary, CameFrom, that contains values for
        # every key of every node. Each key contains the node to come
        # from for the optimal distance to the start node

        # local bubble sort routine
        def Sort(op):
            swaps = 1

            while swaps != 0:
                swaps = 0

                for i in range(len(op) - 1):

                    if op[i][0] > op[i+1][0]:
                        swaps += 1

                        temp = op[i]
                        op[i] = op[i+1]
                        op[i+1] = temp
            return op

        # checks if key is in options array
        # can't use "if key in Options" as need to know where too
        # linear search
        def InOptions(key,op):

            for i in range(len(op)):
                if key in op[i]:
                    return True,i

            return False,-1

        # gets start and end keys
        SKey = self.GetKey(self.start[0],self.start[1])
        EKey = self.GetKey(self.end[0],self.end[1])

        # initialise variables
        Options = []
        Visited = []
        CurrentKey = "0"
        CameFrom = {}
        CameFrom[SKey] = [SKey,0]

        # Heuristic, Weight, Key, Previous Node
        Options += [[0,0,SKey,0]]

        # While options array isn't empty
        while len(Options) != 0:

            # Set CurrentKey to key in Options[0]
            CurrentKey = Options[0][2]
            index = 0

            # Keeps index as 0 if it isn't the end key
            # Changes index to 1 if it is
            # as long as the end key isn't the only one left
            if CurrentKey != EKey or len(Options) == 1:
                CurrentKey = Options[0][2]
                index = 0
            else:
                try:
                    CurrentKey = Options[1][2]
                    index = 1
                except:
                    print Options, index

            # Get connections
            Connections = self.nodes[CurrentKey].GetConnections()

            # For each connection
            for i in Connections:

                # connection key
                ConKey = i[0].GetKey()

                # calculate weight and heuristic
                weight = Options[index][1] + i[1]
                heuristic = weight + self.nodes[ConKey].GetDistance()

                # get if it's in options
                inOptions,indexInOptions = InOptions(ConKey,Options)

                # previously unvisited
                if not inOptions and ConKey not in Visited:
                    # add to Options
                    Options += [[heuristic,weight,ConKey,CurrentKey]]

                # previously visited
                elif inOptions and ConKey not in Visited:
                    # if new heuristic is better than old one
                    if heuristic < Options[indexInOptions][0]:
                        # add to Options
                        Options[indexInOptions] = [heuristic,weight,ConKey,CurrentKey]

            # Add options[0]'s key to visited
            Visited += [Options[index][2]]

            # Add where it came from and its weight to CameFrom
            CameFrom[CurrentKey] = [Options[index][3],Options[index][1]]

            # Remove current index from options
            if index == 0:
                Options = Options[1:]
            else:
                Options = Options[:1] + Options[2:]

            # Sort Options
            Options = Sort(Options)

        # traces back through
        try:
            # Initialise Key and path, path with end node's cooordinates
            Key = CameFrom[EKey]
            path = [self.end]

            # while Key isn't the start node
            while Key[0] != SKey:

                # append key's position to the start of path
                path = [self.nodes[Key[0]].GetPos()] + path

                # get next key
                Key = CameFrom[Key[0]]

            # append start node to front of path
            path = [self.start] + path

        except:
            path = []

        return path



### create graph
##graph = Graph(10,(0,0),(2,2))
##
### add nodes
##graph.AddNode(0,0)
##graph.AddNode(0,1)
##graph.AddNode(0,2)
##graph.AddNode(1,0)
##graph.AddNode(1,1)
##graph.AddNode(1,2)
##graph.AddNode(2,0)
##graph.AddNode(2,1)
##graph.AddNode(2,2)
##
### connect nodes
##graph.Connect(0,0,1,0,2)
##graph.Connect(1,0,1,1,3)
##graph.Connect(2,0,2,1,1)
##graph.Connect(0,1,1,1,1)
##graph.Connect(1,1,2,1,4)
##graph.Connect(0,1,0,2,1)
##graph.Connect(2,1,2,2,2)
##graph.Connect(0,2,1,2,1)
##graph.Connect(1,2,2,2,2)
##
### testing code
##print graph.AStar()
