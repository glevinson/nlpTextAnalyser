from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from ChooseCsvHeaders import ChooseCsvHeaders
from InstructionPage import InstructionPage
#from ModelPage import ModelPage
    
class HomePage:

    def __init__(self,root,frame,app):

        self.root = root
        self.frame = frame
        self.app = app

        # Instantiated on loadCSV click
        self.header_page = None
        self.csv_file_string = None

        
        # self.model_page = ModelPage(self.root,self.app.addPageFrame("model frame",self.root),self.app)
        self.configurePage()

        self.full_screen = False
    
    def configurePage(self):
        """        

        Configures the homepage frame/page layout    
        
        """        
        self.frame.grid(column=0, row=0, sticky="NSEW")
        self.frame.columnconfigure(1,weight=2)
        self.frame.rowconfigure(1,weight=1)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)
        self.frame.columnconfigure(2,weight=1)

        
        title = ttk.Label(self.frame, justify=CENTER, text = "Patient\n\nFree Text\n\nExplorer", font=("bold",25,"underline"))
        title.grid(column=1, columnspan=1,row=0,rowspan=1)
        self.csv_file_string = StringVar()
        self.csv_file_string.set("The name of your CSV file will appear here")
        csv_name_box = Label(self.frame, textvariable = self.csv_file_string)
        csv_name_box.grid(column = 1, row = 2, sticky="NSEW")
        load_csv_button = Button(self.frame, text="Open CSV", command = self.loadCSVClick,
                                     bg = "light blue", borderwidth=2, font=("bold", 12))
        load_csv_button.grid(column=1, row=3,sticky=(N,S,E,W),padx=10,pady=10)
        instruction_button = Button(self.frame, text="Instructions (opens new window)", command=self.instructionsClick,
                                        bg = "light blue", borderwidth=2, font=("bold", 12))
        instruction_button.grid(column=1,row=6,sticky=(N,S,E,W),padx=10,pady=10)

        # Disabled by default
        # Set to normal by ChooseCsvHeaders.chooseCsvHeaders() function
        self.main_menu_button = Button(self.frame, bg = "light blue", borderwidth=2, font=("bold", 12), 
                                           text = "Main Menu", 
                                           state = DISABLED, 
                                           command = lambda: self.app.displayFrame("main frame"))
        self.main_menu_button.grid(column = 1, row = 4, sticky = NSEW,padx=10,pady=10)


    
    def loadCSVClick(self):       
        
        """
        Opens a file dialog window that only allows the user to choose a csv file
        
        After a file is selected, set up the relevant data and open the chooseCSVHeaders page

        """

        # Only permit CSV files, returns the full file path        
        csv_file = filedialog.askopenfilename(title = "Select a CSV file", 
                                              filetypes=(("csv files", "*.csv"),
                                                         ))
        if csv_file == "":
            return
        else:
            self.csv_file_string.set(csv_file.rsplit('/', 1)[1])
        # initialise class for csv page frame
        self.header_page = ChooseCsvHeaders(self.root, 
                                            self.app, 
                                            self.app.addPageFrame("choose headers", 
                                                                  self.root), 
                                            csv_file)
        # set up data for csv page and display the page
        self.header_page.chooseCSVHeaders()
        

    def instructionsClick(self):
        InstructionPage()
    

        