import random, time, pickle
from GraphObject import Graph
try: from PIL import Image, ImageDraw
except: print "Please install PIL for full functionality, program may crash unexpectedly"

# Cell class
# Needs to be put in a grid along with EdgeCell objects
class Cell():
    def __init__(self,AboveCell,LeftCell):
        self.Above = AboveCell
        self.Left = LeftCell
        self.S = True
        self.E = True
        self.Visited = False

    def SetN(self,Val):
        if Val in [True,False]:
            self.Above.SetS(Val)
        else:
            print "invalid input for Cell.SetN"

    def SetE(self,Val):
        if Val in [True,False]:
            self.E = Val
        else:
            print "invalid input for Cell.SetE"

    def SetS(self,Val):
        if Val in [True,False]:
            self.S = Val
        else:
            print "invalid input for Cell.SetS"

    def SetW(self,Val):
        if Val in [True,False]:
            self.Left.SetE(Val)
        else:
            print "invalid input for Cell.SetW"

    # Returns walls as (N,E,S,W)
    # MUCH slower in large mazes than individual getters
    def GetWalls(self):
        NorthCell = self.Above.GetWalls()
        WestCell = self.Left.GetWalls()
        return [NorthCell[2],
                self.E,
                self.S,
                WestCell[1]]

    def SetVisited(self,Val):
        if Val in [True,False]:
            self.Visited = Val
        else:
            print "invalid input for Cell.SetVisited"

    def GetVisited(self):
        return self.Visited

    def GetN(self):
        return self.Above.GetS()

    def GetE(self):
        return self.E

    def GetS(self):
        return self.S

    def GetW(self):
        return self.Left.GetE()

# EdgeCell class
# Does nothing but provide correct values. No setters should ever be called
class EdgeCell():
    def GetVisited(self):
        return True

    def GetWalls(self):
        return [True,True,True,True]

    def SetE(self,Val):
        None

    def SetS(self,Val):
        None

    def GetN(self):
        return True

    def GetE(self):
        return True

    def GetS(self):
        return True

    def GetW(self):
        return True


# Maze class
class Maze():
    def __init__(self,width,height):

        self.Start = (0,0)
        self.End = (0,0)
        self.Solved = False

        # sets up grid
        # add one for EdgeCells
        self.w = width + 1
        self.h = height + 1
        self.grid = [[0]*self.h for i in range(self.w)]

        # Generates grid
        for x in range(0,self.w):
            for y in range(0,self.h):

                # Edgecells where either coordinate is 0
                if x == 0 or y == 0:
                    self.grid[x][y] = EdgeCell()

                # Normal cells linked properly everywhere else
                else:
                    self.grid[x][y] = Cell(self.grid[x][y-1],
                                      self.grid[x-1][y])

        self.solution = []

    def SetWalls(self,x,y,N=None,E=None,S=None,W=None,V=None):
        go = True

        # validate x and y
        if x <= 0 or x >= self.w:
            print "x value for cell setting is outside the maze"
            go = False
        if y <= 0 or y >= self.h:
            print "y value for cell setting is outside the maze"
            go = False

        # validate N,E,S,W,V
        # Note: inputting None as a value for any of these
        # will pass validation, but will not actually be set
        # in the Cell object
        for param in [N,E,S,W,V]:
            if param not in [True,False,None]:
                print param,"is not a valid input"
                go = False

        # Set the values of NESWV if they aren't None
        if go:
            if N != None:
                self.grid[x][y].SetN(N)
            if E != None:
                self.grid[x][y].SetE(E)
            if S != None:
                self.grid[x][y].SetS(S)
            if W != None:
                self.grid[x][y].SetW(W)
            if V != None:
                self.grid[x][y].SetVisited(V)

            self.Solved = False

    def SetSolved(self,value):
        self.Solved = value

    def GetSolved(self):
        return self.Solved

    def GetWalls(self,x,y):
        cell = self.grid[x][y]
        return cell.GetN(), cell.GetE(), cell.GetS(), cell.GetW()

    def GetCellN(self,x,y):
        return self.grid[x][y].GetN()

    def GetCellW(self,x,y):
        return self.grid[x][y].GetW()

    def GetSize(self):
        return self.w, self.h

    # for testing only
    def GetConsole(self,S = False,nodesMade = []):
        # print start and end positions
        print "Start:",self.Start
        print "End:",self.End

        # Set up output array
        output = [[" "]*(self.h * 2 + 1) for i in range(self.w * 2 + 1)]
        for x in range(self.w*2-1): output[x][0] = "#"
        for y in range(self.h*2-1): output[0][y] = "#"

        for x in range(1,self.w):
            for y in range(1,self.h):
                # Gets "central" point in output array
                centre = [x*2 - 1, y*2 -1]

                # get walls
                cell = self.grid[x][y]
                walls = [cell.GetN(),cell.GetE(),cell.GetS(),cell.GetW()]

                # set middle
                if x == self.Start[0] and y == self.Start[1]:
                    output[centre[0]][centre[1]] = "S"

                elif x == self.End[0] and y == self.End[1]:
                    output[centre[0]][centre[1]] = "E"

                elif (x,y) in nodesMade:
                    output[centre[0]][centre[1]] = "."

                elif (x,y) in self.solution and S:
                    output[centre[0]][centre[1]] = "o"

                # East wall
                if walls[1] == True:
                    output[centre[0] + 1][centre[1]] = "#"

                # South wall
                if walls[2] == True:
                    output[centre[0]][centre[1] + 1] = "#"

                output[centre[0] + 1][centre[1] + 1] = "#"


        # print output nicely
        out = ""
        for x in range(output[0]):
            out = ""
            for y in range(h):
                out += output[y][x] + " "
            print out

    # essentially the same as GetConsole, but doesn't print and uses Booleans
    def GetGUI(self):
        # Set up output array
        output = [[False]*(self.h * 2 - 1) for i in range(self.w * 2 - 1)]
        for x in range(self.w*2-1): output[x][0] = True
        for y in range(self.h*2-1): output[0][y] = True

        for x in range(1,self.w):
            for y in range(1,self.h):
                # Gets "central" point in output array
                centre = [x*2 - 1, y*2 -1]

                cell = self.grid[x][y]
                walls = [cell.GetN(),cell.GetE(),cell.GetS(),cell.GetW()]

                # East wall
                if walls[1] == True:
                    output[centre[0] + 1][centre[1]] = True

                # South wall
                if walls[2] == True:
                    output[centre[0]][centre[1] + 1] = True

                # also sets middle to True if all surrounding walls are
                if False not in walls:
                    output[centre[0]][centre[1]] = True

                output[centre[0] + 1][centre[1] + 1] = True

        return output

    # Iterates through whole grid to find unvisited cells
    def FindUnvisited(self):
        for x in range(1,self.w):
            for y in range(1,self.h):
                if self.grid[x][y].Visited == False:
                    return x,y
        return 0,0

    # finds cells with visited value v around x and y
    def FindAdjacent(self,x,y,v):
        offsets = [[0,-1],[1,0],[0,1],[-1,0]] # n e s w offsets
        out = []
        for o in offsets:
            # try/except so it won't search for cells outside the maze
            try:

                # if this cell's visited is true
                if self.grid[x + o[0]][y + o[1]].GetVisited() == v:

                    # if it's an edgecell, do nothing
                    if x + o[0] == 0 or y + o[1] == 0:
                        None

                    # if it isn't, add it to output array
                    else:
                        out += [(x + o[0] , y + o[1])]
            except:
                None

        # If there's no cells found return 0,0
        if len(out) == 0:
            return [(0,0)]
        else:
            return out

    # removes wall between two cells
    def Connect(self,x1,y1,x2,y2):

        # finds the offsets of the two cells
        xOffset = x1 - x2
        yOffset = y1 - y2

        # if either offset is not -1,0,1 they aren't adjacent
        if xOffset > 1 or xOffset < -1 or yOffset > 1 or yOffset < -1:
            print "Tried to connect (",x1,y1,") with (",x2,y2,")"

        # if neither are 0, they aren't adjacent
        elif 0 not in [xOffset,yOffset]:
            print "Tried to connect (",x1,y1,") with (",x2,y2,")"

        # if both are 0, they're the same cell
        elif xOffset == yOffset == 0:
            print "Tried to connect (",x1,y1,") with (",x2,y2,")"

        # otherwise valid, set walls appropriately
        elif yOffset == 1:
            self.SetWalls(x1,y1,N=False)
        elif xOffset == -1:
            self.SetWalls(x1,y1,E=False)
        elif yOffset == -1:
            self.SetWalls(x1,y1,S=False)
        elif xOffset == 1:
            self.SetWalls(x1,y1,W=False)

    # generates maze with hunt-and-kill
    def Generate(self,d=False):

        # start in top left
        Current = (1,1)

        # debug
        if d: routes = 1

        while Current != (0,0):
            # set current cell's visited to True
            self.grid[Current[0]][Current[1]].SetVisited(True)

            # get random next cell
            potentials = self.FindAdjacent(Current[0],Current[1],False)
            Next = potentials[random.randint(0,len(potentials)-1)]

            # if there were no unvisited adjacent squares
            if Next == (0,0):

                # set new current
                Current = self.FindUnvisited()

                if d: routes += 1

                # if not finished generating
                if Current != (0,0):

                    # connect current cell to adjacent visited cell and connect
                    potentials = self.FindAdjacent(Current[0],Current[1],True)
                    self.Connect(Current[0],Current[1],potentials[0][0],potentials[0][1])

            else:
                # connect
                self.Connect(Current[0],Current[1],Next[0],Next[1])
                Current = Next

        if d: print routes,"total routes made\n"

        self.Solved = False

    # generates maze with all walls set to false
    def GenerateBlank(self):
        for x in range(1,self.w):
            for y in range(1,self.h):
                self.SetWalls(x,y,False,False,False,False)

                # resets south/east walls to true if on bottom/right edge
                if x == self.w - 1: self.SetWalls(x,y,E=True)
                if y == self.h - 1: self.SetWalls(x,y,S=True)

    # gets coordinates with given method (for start/end placement)
    def GetCoords(self,Method,x,y):
        # R = Random Coordinate
        # E = Random edge coordinate
        # U = User defined, REQUIRES x AND y

        Coords = [0,0]

        # Random
        if Method == "R":
            Coords[0] = random.randint(1,self.w - 1)
            Coords[1] = random.randint(1,self.h - 1)

        # Random Edge
        if Method == "E":
            # "side" coord is the one that'll be either 1 or maze size
            # "slide" coord is the one that'll be between 1 and maze size

            maxSlide = 1
            maxSide = 1
            SideCoord = random.randint(0,1)

            if SideCoord == 0:
                maxSlide = self.h
                maxSide = self.w
                SliderCoord = 1
            else:
                maxSlide = self.w
                maxSide = self.h
                SliderCoord = 0

            Coords[SideCoord] = (maxSide - 1)**random.randint(0,1)
            Coords[SliderCoord] = random.randint(1,maxSlide - 1)

        # User defined
        if Method == "U":
            go = True

            # validate x and y
            if x <= 0 or x >= self.w:
                go = False
            if y <= 0 or y >= self.h:
                go = False
            if x == None or y == None:
                go = False

            if go: Coords = [x,y]
            else: raise IndexError

        return Coords

    # sets start with given method
    def SetStart(self,Method, x = None, y = None):
        Coords = self.GetCoords(Method,x,y)

        # repeat until coords aren't the end coords
        while Coords == self.End:
            Coords = self.GetCoords(Method,x,y)

        self.Start = (Coords[0],Coords[1])

        self.Solved = False

    # sets end with given method
    def SetEnd(self,Method, x = None, y = None):
        Coords = self.GetCoords(Method,x,y)

        # repeat until coords aren't the start coords
        while Coords == self.Start:
            Coords = self.GetCoords(Method,x,y)

        self.End = (Coords[0],Coords[1])

        self.Solved = False

    # solve using Graph object
    # d = True for debugging
    def Solve(self,d=False):

        # if there is a start and an end
        if self.Start != self.End != (0,0):

            # create graph object
            g = Graph(self.w,self.h,self.Start,self.End)

            if d: print "generating graph"

            # generate maze graph
            nodesMade = g.GridToGraph(self.grid,d)

            if d: self.oGetConsole(False,nodesMade)
            if d: print len(nodesMade),"nodes made\n"

            if d: print "solving"

            # solve graph
            self.solution = g.AStar()
            del g

            self.Solved = True

            # return solution as it may be needed
            return self.solution

    # exports maze as picture
    def ExportPicture(self,solved = False,size=10,name="maze.bmp",
                      SColour = (0,128,0),EColour = (255,0,0),RColour = (128,128,255)):

        # Initialise image + draw object
        img = Image.new("RGB",
                        ((self.w*2-1)*size,
                        (self.h*2-1)*size),
                        (255,255,255))

        draw = ImageDraw.Draw(img)

        # Calculate x and y coordinates of solution cells
        solutionPoints = []
        for i in self.solution:
            solutionPoints += [((i[0]*2-1) * size + (size/2),
                                (i[1]*2-1) * size + (size/2))]

        # Draw solution
        if solved: draw.line(solutionPoints,fill=RColour,width=size/2)

        # Draw start
        draw.rectangle([(self.Start[0]*2 - 1) * size,(self.Start[1]*2-1) * size,
                        (self.Start[0]*2) * size, (self.Start[1]*2) * size]
                        ,SColour)

        # Draw end
        draw.rectangle([(self.End[0]*2 - 1) * size,(self.End[1]*2-1) * size,
                        (self.End[0]*2) * size, (self.End[1]*2) * size]
                        ,EColour)

        # black bars from top left to top right and bottom left
        draw.line([(size/2),0,
                   (size/2),(self.h*2+1)*size + (size/2)],
                  fill=(0,0,0),width=size)

        draw.line([0,(size/2),
                   (self.w*2+1)*size + (size/2),(size/2)],
                  fill=(0,0,0),width=size)

        for x in range(1,self.w):
            for y in range(1,self.h):
                # Gets "central" point in picture
                centre = ((x*2 - 1) * size, (y*2 -1) * size)

                # gets walls
                cell = self.grid[x][y]
                walls = [cell.GetN(),cell.GetE(),cell.GetS(),cell.GetW()]

                # East wall
                if walls[1] == True:
                    draw.rectangle([centre[0] + size,centre[1],
                                centre[0] + size*2, centre[1] + size]
                                ,(0,0,0))

                # South wall
                if walls[2] == True:
                    draw.rectangle([centre[0],centre[1] + size,
                                centre[0] + size, centre[1] + size*2],
                               (0,0,0))

                # centre black if all walls are false
                if False not in walls:
                    draw.rectangle([centre[0],centre[1],
                                    centre[0] + size, centre[1] + size],
                                   (0,0,0))

                draw.rectangle([centre[0] + size,centre[1] + size,
                                centre[0] + size*2, centre[1] + size*2],
                               (0,0,0))

        # save and clean up variables
        img.save(name)
        del draw
        del img

    # export maze as binary file
    def ExportBinary(self,name="maze.mz"):

        # create pickleable object
        data = MazeData(self.grid,
                        self.Start,
                        self.End,
                        self.solution)

        # create pickle file
        pickleFile = open(name,"w")

        # pickle
        pickle.dump(data,pickleFile)

        pickleFile.close()

    # import maze from binary file
    def ImportBinary(self,name):

        # try to open file "name"
        try: dataFile = open(name,"r")
        except AttributeError: print "filename",name,"does not exist!"

        # try to read pickled object
        try: data = pickle.load(dataFile)
        except: "Error unpickling file",name

        # set data from file
        self.grid = data.getGrid()
        self.Start = data.getStart()
        self.End = data.getEnd()
        self.solution = data.getSolution()

        # set data that can be worked out
        self.w = len(self.grid)
        self.h = len(self.grid[0])

# class for pickling maze data
class MazeData():
    # takes four most important maze variables as parameters
    def __init__(self, grid, start, end, solution):
        self.grid = grid
        self.start = start
        self.end = end
        self.solution = solution

    # getters
    def getGrid(self): return self.grid
    def getStart(self): return self.start
    def getEnd(self): return self.end
    def getSolution(self): return self.solution

if __name__ == "__main__":
    None

##    ## GENERATING AND EXPORTING TESTING
##    size = 10
##    m = Maze(192,108)
##    print "generating"
##    m.Generate()
##    m.SetStart("R")
##    m.SetEnd("R")
##    m.Solve()
##    print "exporting"
##    m.ExportPicture(False,10,"maze.jpg")
##    m.ExportPicture(True,10,"mazeSolved.jpg")

##    ## TIME TESTING
##    while True:
##        size = input("\nsize: ")
##        s = time.time()
##        maze = Maze(size,size)
##        maze.Generate()
##        maze.SetStart("R")
##        maze.SetEnd("R")
##        g = time.time()
##        maze.oGetConsole()
##        e = time.time()
##        print "Generated in:",g-s,"s\nDisplayed in:",e-g,"s"
