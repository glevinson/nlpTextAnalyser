from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from HomePage import HomePage
from MainMenu import MainMenu

import os
import nltk

class App:

    def __init__(self,root):

        """
        Initalisation for the App class

        Configures all the pages of the app (in terms of their user interface)

        Sets up a dictionary to store all of the App's pages

        """                

        root.title("Patient free text explorer")
        root.geometry("900x640+500+150")  
        root.resizable(False,False)             
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)    
        
        # This will store a list of combo boxes that the user enters the CSV header information in
        # Need to store this in the App class so any other class has access to the user input
        self.csv_header_combo_boxes = None
        self.df = None

        # Dictionary to store all of our frames -- frames are essentially a "new page" for our application
        # making it so that we do not need to have multiple windows, rather it can be done all in one window.
        # Widgets (buttons, labels, etc.) can all be added to a frame such that only the top-most frame's widgets
        # are displayed
            
        self.frames_dict = {}
        self.root = root     

        # Set up the two direct child pages
        self.homepage = HomePage(self.root, 
                            self.addPageFrame("home frame", self.root), 
                            self) 
        self.main_menu = MainMenu(self.root, 
                             self.addPageFrame("main frame", self.root), 
                             self)     
       
       
        # Display the home page
        self.displayFrame("home frame")  
        style = ttk.Style()
        style.configure("TFrame", background="white") 

        # Set the nltk data directory
        self.setNltkDirectory() 

    def setNltkDirectory(self):
         # Sets the nltk data path depending on where this application is saved on the users' machine
        cwd = os.getcwd()
        nltk_data_directory = cwd
        nltk_data_directory += "//nltk_data"
        nltk.data.path.append(nltk_data_directory)
        nltk_data_directory = cwd
        nltk_data_directory += "\\nltk_data"
        nltk.data.path.append(nltk_data_directory)
   
    def addPageFrame(self, frame_name,root):
        
        """
        Inputs (self, frame_name, root), where root is the parent window of the Tk application
        and frame_name is a string containing the name of the frame

        Creates a new page frame and adds it so the class dictionary that contains all of the frame pages

        Returns the newly created frame

        """

        new_frame = ttk.Frame(root, padding=(3,3,12,12))
        new_frame.grid(column=0,row=0,sticky=(N,S,E,W))

        self.frames_dict[frame_name] = new_frame
        return new_frame

    
    def displayFrame(self,frame_name):
        self.frames_dict[frame_name].tkraise()      


    def resizeWindow(self, size):
        self.root.geometry(size)

def runApp():
    root = Tk()
    setTheme(root)
    App(root)
    root.mainloop()
    
def setTheme(root):
    """
    Theme from https://github.com/rdbende/Azure-ttk-theme 
    MIT License

    Copyright (c) 2021 rdbende

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    try:
        root.tk.call("source","Azure-ttk-theme-main/azure.tcl")
    except:
            try:
                root.tk.call("source","Azure-ttk-theme-main\\azure.tcl")
            except:
                print("Error loading theme")
        
    root.tk.call("set_theme","light") 





if  __name__ == "__main__":
    runApp()




