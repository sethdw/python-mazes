from Tkinter import *
import tkMessageBox, tkFileDialog, tkColorChooser
try: from mazeObject import Maze
except: print "error importing mazeObject.py"
import sys

class Main(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent

        # initialise maze variables
        self.maze = Maze(20,20)
        self.maze.Generate()
        self.maze.SetStart("U",1,1)
        self.maze.SetEnd("U",20,20)

        # initialise GUI variables
        self.SColour = (0,128,0)
        self.EColour = (255,0,0)
        self.RColour = (128,128,255)
        self.SolutionShown = True
        self.WaitForStart = False
        self.WaitForEnd = False
        self.ShowEditableSquares = False

        # set window minimum size
        self.parent.minsize(500,500)

        # make menu
        self.MakeMenu()

        # generate key frame
        self.key = KeyFrame(self)
        self.key.pack()
        self.UpdateKey()

        # generate maze frame
        self.mazeGrid = MazeFrame(self,self.maze)
        self.mazeGrid.pack()
        self.UpdateMaze()

    def MakeMenu(self):
        # Toolbar
        menubar = Menu(self)

        # File menu
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Save maze",command= self.SaveBin)
        fileMenu.add_command(label="Load maze",command = self.LoadBin)
        fileMenu.add_command(label="Save as picture",command = self.SavePic)
        menubar.add_cascade(label="File",menu=fileMenu)

        # Options menu
        optionsMenu = Menu(menubar)
        optionsMenu.add_command(label="Set start",command=self.SetStart)
        optionsMenu.add_command(label="Set end",command=self.SetEnd)
        optionsMenu.add_command(label="Set start colour",command=self.SetSColour)
        optionsMenu.add_command(label="Set end colour",command=self.SetEColour)
        optionsMenu.add_command(label="Set route colour",command=self.SetRColour)
        optionsMenu.add_command(label="Show editable squares",command=self.ShowEditable)
        menubar.add_cascade(label="Options",menu=optionsMenu)

        # Generate button
        menubar.add_command(label="Generate",command=self.GenerateMaze)

        # Solution button
        menubar.add_command(label="Show/Hide solution",command=self.ShowSolution)

        self.parent.config(menu=menubar)

    def stub(self):
        print "stub"

    def SaveBin(self):
        try:
            filename = tkFileDialog.asksaveasfilename(initialdir = "/",
                                                    initialfile="maze.mz",
                                                    defaultextension = ".mz",
                                                    title = "Select file",
                                                    filetypes = (("maze file","*.mz"),("all files","*.*")))

            if filename[-4:] != "/.mz":
                self.maze.ExportBinary(filename)
            else:
                tkMessageBox.showerror("Error","Please give a filename!")

        except IOError:
             tkMessageBox.showerror("Error","Error saving maze! Please try again\n"+str(sys.exc_info()[0]))
        except:
            tkMessageBox.showerror("Error","Error! Make sure you've generated a maze before saving it.\n"+str(sys.exc_info()[0]))

    def LoadBin(self):
        try:
            filename = tkFileDialog.askopenfilename(initialdir = "/",
                                                    defaultextension = ".mz",
                                                    title = "Select file",
                                                    filetypes = (("maze file","*.mz"),("all files","*.*")))

            self.maze.ImportBinary(filename)
            self.UpdateMaze()
        except:
            tkMessageBox.showerror("Error","Error loading maze! Please try again\n"+str(sys.exc_info()[0]))

    def SavePic(self):
        # Begins new SaveOptionsWindow
        OptionsWindow = SaveOptionsWindow(self)

    # callback routine for SaveOptionsWindow
    def SPicOptionsGot(self,solved,size):

        try:

            size = int(size)

            # validate size
            if size < 2 or size > 50:
                raise ValueError

            # get filename
            filename = tkFileDialog.asksaveasfilename(initialdir = "/",
                                                    title = "Select file",
                                                    defaultextension = ".jpg",
                                                    filetypes = (("jpeg file","*.jpg"),("bmp file","*.bmp"),("all files","*.*")))

            # convert OptionsWindow's values to usable values
            if solved == 1: solved = True
            else: solved = False

            # if maze hasn't been solved but should be, solve it
            if solved and not self.maze.GetSolved():
                self.maze.Solve()

            # call save function
            self.maze.ExportPicture(solved=solved,size=size,name=filename,
                                    SColour = self.SColour, EColour = self.EColour, RColour = self.RColour)

            # tell user it's been saved
            tkMessageBox.showinfo("Exported successfully","Maze has been saved!")

        # maze couldnt be saved
        except IOError:
             tkMessageBox.showerror("Error","Error saving maze! Please try again.\n"+str(sys.exc_info()[0]))

        # converting size to int didn't work
        except ValueError:
            tkMessageBox.showerror("Error","Error with maze size! Ensure you entered numbers in the correct range\n"+str(sys.exc_info()[0]))

        # user pressed cancel
        except KeyError:
            None

        except:
            tkMessageBox.showerror("Error","Error! Make sure you've generated a maze before saving it.\n"+str(sys.exc_info()[0]))

    def GenerateMaze(self):
        GenMazeOptions = GenerateOptionsWindow(self)

    # callback routine for GenerateOptionsWindow
    def GenMazeOptionsGot(self,x,y,generate):

        try:
            # try to convert x and y to integers
            MazeX = int(x)
            MazeY = int(y)

            # validate
            if MazeX < 1 or MazeY < 1 or MazeX > 500 or MazeY > 500: raise ValueError

            # make new maze
            del self.maze
            self.maze = Maze(MazeX,MazeY)
            if generate: self.maze.Generate()
            else: self.maze.GenerateBlank()

            self.UpdateMaze()

        # not integers
        except ValueError:
            tkMessageBox.showerror("Error","Invalid value for x or y!\n"+str(sys.exc_info()[0]))

        except:
             tkMessageBox.showerror("Error","An error occured!\n"+str(sys.exc_info()[0]))

    def ShowSolution(self):
        self.SolutionShown = not self.SolutionShown
        self.UpdateMaze()

    def SetStart(self):
        PosOptions = PosOptionsWindow(self, "S")

    def SetEnd(self):
        PosOptions = PosOptionsWindow(self,"E")

    def StartOptionsGot(self,method):
        # SETCOORDS IN MAZE OBJECT ONLY USES MAZE WIDTH
        # SETEDGE DOESN'T WORK WITH RECTANGLE MAZES
        try:
            # if not user defined
            if method != "U":
                self.maze.SetStart(method)
            else:
                # wait for canvas click
                self.WaitForStart = True
                # notify user how to place start
                self.UpdateKey("Click a point on the maze to set as start")

            self.UpdateMaze()

        # x or y outside maze
        except IndexError:
            tkMessageBox.showerror("Error","Your coordinates are outside the maze!\n"+str(sys.exc_info()[0]))

        # invalid x or y
        except TypeError:
            tkMessageBox.showerror("Error","Invalid value for x or y!\n"+str(sys.exc_info()[0]))

        except:
            tkMessageBox.showerror("Error","An error occured!\n"+str(sys.exc_info()[0]))

    def EndOptionsGot(self,method):
        try:
            # if there are no values for x or y
            if method != "U":
                self.maze.SetEnd(method)
            else:
                # wait for canvas click
                self.WaitForEnd = True
                # notify user how to place end
                self.UpdateKey("Click a point on the maze to set as end")

        # x or y outside maze
        except IndexError:
            tkMessageBox.showerror("Error","Your coordinates are outside the maze!\n"+str(sys.exc_info()[0]))

        # invalid x or y
        except TypeError:
            tkMessageBox.showerror("Error","Invalid value for x or y!\n"+str(sys.exc_info()[0]))

        except:
            tkMessageBox.showerror("Error","An error occured!\n"+str(sys.exc_info()[0]))

        self.UpdateMaze()

    def SetSColour(self):
        temp = self.SColour
        self.SColour = tkColorChooser.askcolor()[0]
        if self.SColour == None: self.SColour = temp
        self.UpdateMaze()
        self.UpdateKey()

    def SetEColour(self):
        temp = self.EColour
        self.EColour = tkColorChooser.askcolor()[0]
        if self.EColour == None: self.EColour = temp
        self.UpdateMaze()
        self.UpdateKey()

    def SetRColour(self):
        temp = self.RColour
        self.RColour = tkColorChooser.askcolor()[0]
        if self.RColour == None: self.RColour = temp
        self.UpdateMaze()
        self.UpdateKey()

    def UpdateMaze(self):
        if not self.maze.GetSolved() and self.maze.Start != (0,0):
            sol = self.maze.Solve()
            if sol == []:
                tkMessageBox.showerror("ERROR","Maze has no solution!")

        grid = self.maze.GetGUI()

        self.mazeGrid.Update(grid,
                             self.SColour,
                             self.EColour,
                             self.RColour,
                             self.maze.Start,
                             self.maze.End,
                             self.maze.solution,
                             self.SolutionShown)

        if self.ShowEditableSquares:
            self.mazeGrid.ShowEditabaleSquares(grid)
            self.UpdateKey("Walls or paths with gray squares on can be edited")

    def UpdateKey(self,text="Use Options -> Show Editable Squares to see where you can edit"):
        self.key.Update(self.SColour,self.EColour,self.RColour,text)

    def ShowEditable(self):
        self.ShowEditableSquares = not self.ShowEditableSquares
        self.UpdateMaze()

    def CanvasClicked(self,event):
        # gets event coordinates
        x,y = event.x, event.y

        # 20 = (maze pixel width) * 2
        areaX = (x / 20) + 1
        areaY = (y / 20) + 1

        if self.WaitForStart:
            self.maze.SetStart("U",areaX,areaY)
            self.WaitForStart = False

        elif self.WaitForEnd:
            self.maze.SetEnd("U",areaX,areaY)
            self.WaitForEnd = False

        else:
            try:
                relativeX = x % 20
                relativeY = y % 20

                if relativeX < 10 and relativeY > 10:
                    self.maze.SetWalls(areaX,areaY, W = not self.maze.GetCellW(areaX,areaY))
                if relativeX > 10 and relativeY < 10:
                    self.maze.SetWalls(areaX,areaY, N = not self.maze.GetCellN(areaX,areaY))
            except:
                None

        self.UpdateMaze()
        self.UpdateKey()

class KeyFrame(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent

        # initialise KeyBox as blank frame to avoid deleting nothing in Update()
        self.KeyBox = Frame(self)

    def Update(self,SCol,ECol,RCol,Text):
        # convert to hex values
        SCol = '#%02x%02x%02x' % SCol
        ECol = '#%02x%02x%02x' % ECol
        RCol = '#%02x%02x%02x' % RCol

        # delete and remake frame
        self.KeyBox.pack_forget()
        del self.KeyBox
        self.KeyBox = Frame(self)
        self.KeyBox.config(relief=RAISED,borderwidth = 10,padx = 5, pady = 5)
        Colours = Frame(self.KeyBox)

        # put everything in the frame
        KeyText = Label(Colours,text="KEY")
        KeyText.pack(side = LEFT, padx = 0)

        # buttons call parent's colour setters
        SFrame = Frame(Colours)
        SText = Label(SFrame,text="Start colour").pack(side=LEFT)
        SBox = Button(SFrame,bg=SCol,height=1,width=2,command = self.parent.SetSColour).pack(side=LEFT)
        SFrame.pack(side=LEFT,padx = 20)

        EFrame = Frame(Colours)
        EText = Label(EFrame,text="End colour").pack(side=LEFT)
        EBox = Button(EFrame,bg=ECol,height=1,width=2,command = self.parent.SetEColour).pack(side=LEFT)
        EFrame.pack(side=LEFT,padx = 20)

        RFrame = Frame(Colours)
        RText = Label(RFrame,text="Route colour").pack(side=LEFT)
        RBox = Button(RFrame,bg=RCol,height=1,width=2,command = self.parent.SetRColour).pack(side=LEFT)
        RFrame.pack(side=LEFT,padx = 20)

        Colours.pack()
        message = Label(self.KeyBox,text=Text)
        message.pack()

        self.KeyBox.pack(fill=X)

class MazeFrame(Frame):
    def __init__(self,parent,maze):
        Frame.__init__(self,parent)
        self.parent = parent

        self.WallWidth = 10

        self.f = Frame(self,padx = 20, pady = 20)
        self.drawboard = Canvas(self.f,width=100,height=100,bg="black")
        self.drawboard.pack()
        self.f.pack()

    def Update(self,grid,SCol,ECol,RCol,S,E,Sol,ShowSol):

        size = self.WallWidth
        width = len(grid)
        height = len(grid[0])

        SCol = '#%02x%02x%02x' % SCol
        ECol = '#%02x%02x%02x' % ECol
        RCol = '#%02x%02x%02x' % RCol

        self.drawboard.pack_forget()
        del self.drawboard

        self.drawboard = Canvas(self.f,width=width*size,
                                height=height*size,
                                bg="white")

        solutionPoints = [((S[0]*2-1) * size + (size/2),
                         (S[1]*2-1) * size + (size/2)),
                         ((S[0]*2-1) * size + (size/2),
                         (S[1]*2-1) * size + (size/2))]
        # Draw solution
        for i in Sol:
            solutionPoints += [((i[0]*2-1) * size + (size/2),
                                (i[1]*2-1) * size + (size/2))]

        # Draw solution
        if ShowSol: self.drawboard.create_line(solutionPoints,fill=RCol,width=size/2)

        # Draw start
        self.drawboard.create_rectangle(((S[0]*2-1)*size,
                                         (S[1]*2-1)*size,
                                         (S[0]*2-1)*size+size,
                                         (S[1]*2-1)*size+size),
                                         fill=SCol,outline=SCol)

        # Draw end
        self.drawboard.create_rectangle(((E[0]*2-1)*size,
                                         (E[1]*2-1)*size,
                                         (E[0]*2-1)*size+size,
                                         (E[1]*2-1)*size+size),
                                         fill=ECol,outline=ECol)

        for x in range(0,width):
            for y in range(0,height):

                if grid[x][y]:
                    self.drawboard.create_rectangle((x*size,y*size,x*size+size,y*size+size),fill="black")

        self.drawboard.bind("<Button-1>",self.parent.CanvasClicked)
        self.drawboard.pack()

    def ShowEditabaleSquares(self,grid):
        width, height = len(grid), len(grid[0])
        size = self.WallWidth

        for x in range(0,width):
            for y in range(0,height):
                if (x % 2 != y % 2) and (x != 0 and y != 0) and (x != width - 1 and y != height - 1):
                    self.drawboard.create_rectangle((x*size + 2,y*size + 2,x*size+size - 2,y*size+size - 2),outline="#aaaaaa",fill="#aaaaaa")


class GenerateOptionsWindow(Toplevel):
    def __init__(self,parent):
        Toplevel.__init__(self)
        self.parent = parent

         # set up entry boxes and set default values
        self.xBox = Entry(self,width=10)
        self.yBox = Entry(self,width=10)
        self.xBox.insert(END,10)
        self.yBox.insert(END,10)

        # set up checkbutton
        self.Blank = BooleanVar()
        self.BlankText = Label(self,text="Blank:")
        self.BlankTick = Checkbutton(self,onvalue = False,offvalue=True,variable = self.Blank)
        self.BlankTick.deselect()

        # set up button and text
        OK = Button(self,text="OK",command=self.OKButton)
        xText = Label(self,text="Width:")
        yText = Label(self,text="Height:")

        # grid everything
        xText.grid(column=1,row=2)
        yText.grid(column=1,row=3)
        self.xBox.grid(column=2,row=2)
        self.yBox.grid(column=2,row=3)
        self.BlankText.grid(column=1,row=4)
        self.BlankTick.grid(column=2,row=4)
        OK.grid(column=2,row=5)

    # button command
    def OKButton(self):
        self.parent.GenMazeOptionsGot(self.xBox.get(),self.yBox.get(),self.Blank.get())
        self.destroy()

class SaveOptionsWindow(Toplevel):
    def __init__(self,parent):
        Toplevel.__init__(self)

        self.parent = parent
        self.tick = BooleanVar()
        Options = Frame(self)

        self.solvedTick = Checkbutton(Options,text="Show solution",variable = self.tick, onvalue = True, offvalue = False)
        self.wallSize = Entry(Options,width=10)
        self.wallSize.insert(END,10)
        sizeText = Label(Options,text="Wall pixel width")
        okButton = Button(Options,text="OK",command=self.OKButton)

        # set up range text
        Range = Label(self,text="Wall width must be between 2 and 50 pixels\n")

        # grid everything
        Range.pack()
        sizeText.grid(row=2,column=1)
        self.solvedTick.grid(row=3,column=1)
        self.wallSize.grid(row=2,column=2)
        okButton.grid(row=3,column=2)
        Options.pack()

    def OKButton(self):
        self.parent.SPicOptionsGot(self.tick.get(),self.wallSize.get())
        self.destroy()

class PosOptionsWindow(Toplevel):
    def __init__(self,parent,type):
        Toplevel.__init__(self)

        # type is "E" or "S" and defines which callback to use
        self.parent = parent
        self.type = type

        self.option = StringVar()
        self.option.set("R")

        # radio buttons
        randomButton = Radiobutton(self,text="Random position",variable = self.option, value = "R")
        edgeButton = Radiobutton(self,text="Random edge",variable = self.option, value = "E")
        userButton = Radiobutton(self,text="User defined",variable = self.option, value = "U")

        # OK button
        okButton = Button(self,text="OK",command = self.OKButton)

        # pack everything
        randomButton.pack()
        edgeButton.pack()
        userButton.pack()
        okButton.pack()

    def OKButton(self):
        if self.type == "S":
            self.parent.StartOptionsGot(self.option.get())
        else:
            self.parent.EndOptionsGot(self.option.get())

        self.destroy()


root = Tk()
main = Main(root)
main.pack()
root.mainloop()

