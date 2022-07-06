# ChooseCsvHeaders.py
# Class for CSV headers select page 

# where headers are mapped by the user after selecting their CSV file

from tkinter import *
from tkinter import ttk


import pandas as pd


"""
Class for the csv header select page

"""

class ChooseCsvHeaders:

    def __init__(self, root , app, frame, csv_file):
        
        """
        Parameters:
            root Tk() instance of the app
            app class instance containing root
            own frame object
            csv file name string
            
        """
        self.root = root
        self.frame = frame
        self.app = app
        self.csv_file = csv_file
        self.combo_boxes = None
        self.configureHeaderSelectFrame()
        self.user_ids_selected = False
        self.free_text_selected = False

    def enableDoneButton(self, event):
        """
        Enables the Done button
        Only suitable for single requirement case
        
        """
        self.done_b['state'] = 'normal'

    def configureHeaderSelectFrame(self):

        """
        Inputs: (self, root) where root is the parent window of the Tk application

        Configures the choose headers frame
        This frame allows the user to select the relevant headers from their CSV file

        returns: configured homepage frame (type ttk.frame), combo boxes (type list of combo boxes)
        
        """
        # Set up the frame, in which all the widgets in this page are placed
        
        self.frame.grid(column=0,row=0,sticky=(N,S,E,W))

        ######################## Set up the Labels #######################################################################
        instructions = " Use the drop down menus below to select the header of the csv column that contains the relevant data.\n If there is no such column, select NONE"
        instruction_l = ttk.Label(self.frame, 
                                  justify=CENTER, 
                                  text=instructions, 
                                  font=("bold",14),)
        instruction_l.grid(column=0,row=0,rowspan=2, columnspan=2,padx=10,pady=10,sticky=(N,S,E,W))
        
        user_id_l = ttk.Label(self.frame, 
                              text = "Select the column that contains UserIDs")
        user_id_l.grid(column = 0, row = 3, padx = 10, pady = 10)

        dob_l = ttk.Label(self.frame, 
                          text = "Select the column that contains users' date of birth")
        dob_l.grid(column=1,row=3,padx=10,pady=10)

        free_txt_l = ttk.Label(self.frame, 
                               text = "Select the column that contains users' free text", 
                               font = "TkDefaultFont 12 bold")
        free_txt_l.grid(column=0,row=5,padx=10,pady=10)

        completed_date_l = ttk.Label(self.frame, 
                                     text = "Select the column that contains the date the users completed the survey")
        completed_date_l.grid(column=1,row=5,padx=10,pady=10)

        ms_type_l = ttk.Label(self.frame, 
                              text = "Select the column that contains users' MS type")
        ms_type_l.grid(column = 0, row = 7, padx = 10, pady = 10)

        ms_onset_l = ttk.Label(self.frame, 
                               text = "Select the column that contains users' MS onset year")
        ms_onset_l.grid(column=1,row=7,padx=10,pady=10)
        
        l_edss = ttk.Label(self.frame, 
                           text = "Select the column that contains the EDSS")
        l_edss.grid(column=0, row=9, padx=10, pady=10)
        
        l_diagnosis = ttk.Label(self.frame, 
                           text = "Select the column that contains the users' diagnosis date")
        l_diagnosis.grid(column=1, row=9, padx=10, pady=10)
        
        l_gender = ttk.Label(self.frame, 
                           text = "Select the column that contains the users' gender")
        l_gender.grid(column=0, row=11, padx=10, pady=10)

        ######################## Set up the ComboBoxes ###################################################################
       
        user_id = ttk.Combobox(self.frame, textvariable=None)
        user_id.grid(column=0,row=4)

        dob = ttk.Combobox(self.frame, textvariable=None)
        dob.grid(column=1,row=4)

        free_txt = ttk.Combobox(self.frame, textvariable=None)
        free_txt.bind('<<ComboboxSelected>>', self.enableDoneButton)
        free_txt.grid(column=0,row=6)

        completed_date = ttk.Combobox(self.frame, textvariable=None)
        completed_date.grid(column=1,row=6)

        ms_type = ttk.Combobox(self.frame, textvariable=None)
        ms_type.grid(column=0,row=8)

        ms_onset_year = ttk.Combobox(self.frame, textvariable=None)
        ms_onset_year.grid(column=1,row=8)
        
        edss = ttk.Combobox(self.frame, textvariable=None)
        edss.grid(column=0,row=10)

        diagnosisDate = ttk.Combobox(self.frame, textvariable=None)
        diagnosisDate.grid(column=1,row=10)

        gender = ttk.Combobox(self.frame, textvariable=None)
        gender.grid(column=0,row=12)
        
        # Headers data names
        self.combo_boxes = [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year, edss, diagnosisDate, gender]   

        ######################## Set up the Buttons #######################################################################

        # Insert a blank row before the button to put button at bottom of screen
        self.frame.rowconfigure(13, weight = 1)  
        
        # Back button
        back_b = Button(self.frame, bg = "light blue", borderwidth=2, font=("bold", 12),  
                            text = "Back", 
                            command = lambda: self.app.displayFrame("home frame"))
        back_b.grid(column = 0, row = 14, padx=10, sticky = (N,S,E,W))  
        
        # Done button
        self.done_b = Button(self.frame, bg = "lightblue", borderwidth=2, font=("bold", 12), 
                            text = "Done", 
                            state = DISABLED, 
                            command = self.doneButtonClick)
        self.done_b.grid(column = 1, row = 14, sticky = (N,S,E,W))  

        
    def doneButtonClick(self):
        """
        Enables Main Menu button on homepage
        Then loads the Main Menu
        
        """
        self.app.homepage.main_menu_button['state'] = 'normal'
        self.app.main_menu.freq_page.clearAnalyser()
        self.app.main_menu.search_page.clearSearcher()
        self.app.displayFrame("main frame")
    
    def chooseCSVHeaders(self):

        """
        Reads in the user CSV file as a pandas dataframe 
        and stores the CSV headers as a data variable

        Set all of the headers as options for the combo boxes for the user
        to choose 

        Finally, displays the choose headers page

        """
        self.app.homepage.main_menu_button['state'] = 'disabled'
        df = pd.read_csv(self.csv_file)

        # Store the dataframe as an object datamember
        self.df = df
        # Pass the dataframe to the App class as well
        self.app.df = df

        # Stores the column headers of the dataframe        
        self.headers = list(df.columns.values)       
        self.headers.append("NONE") 

        # Add the CSV headers as options for the combo boxes
        for combo_box in self.combo_boxes:
            combo_box["values"] = list(self.headers)
            combo_box.state(["readonly"])
            # Make the default value "NONE"
            combo_box.current(len(self.headers)-1)
        
        # Store the combo boxes in the App Class
        self.app.csv_header_combo_boxes = self.combo_boxes

        # Display the choose headers frame
        self.app.displayFrame("choose headers")  
        
        
        