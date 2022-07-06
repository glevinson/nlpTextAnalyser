from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd

from search import TextSearcher


class SearchPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searcher = None

        self.configureSearchPage()


    def configureSearchPage(self):

        """
        Configures the layout of the search page, which allows the user to search the free text
        
        The user can select a phrase to search, along with how many additional words either side
        of that phrase they wish to display

        Search results are displayed in the Text box, and the user must press clear before they
        can edit their search phrase or window, once they have pressed search for a first time

        The user can also select additional information to extract and display in their search results
        depending on the headers that they have selected from their CSV file

        """        

        # Configure search box for query
        search_phrase = StringVar()
        search_box = ttk.Entry(self.frame,textvariable=search_phrase)
        search_box.grid(column=0,row=4,sticky=(N,S,E,W))

        self.search_box = search_box

        # Configure search button
        self.search_button = Button(self.frame,text="Search",command= lambda: self.searchButtonClick_sf(),
                                    bg = "light blue", borderwidth=2, font=("bold", 12))
        self.search_button.grid(column=0,row=5,sticky=(N,S,E,W),pady=5)

        # Configure download button
        download_b = Button(self.frame, text="Download results", command= lambda: self.downloadButtonClick_sf(),
                            bg = "light blue", borderwidth=2, font=("bold", 12))
        download_b.grid(column=0, row=6, sticky=(N,S,E,W),pady=5)

        # Configure clear button
        clear_b = Button(self.frame, text="Clear", command=lambda: self.clearButtonClick_sf(),
                        bg = "light blue", borderwidth=2, font=("bold", 12))
        clear_b.grid(column=0,row=7,sticky=(N,S,E,W),pady=5)
        
        # Configure back button
        back_b = Button(self.frame, text="Back", command= lambda: self.app.displayFrame("main frame"),
                        bg = "light blue", borderwidth=2, font=("bold", 12))
        back_b.grid(column=0, row=8, sticky=(N,S,E,W),pady=5)

        # Configure search window list
        window_list = ttk.Combobox(self.frame, textvariable=None)
        windows = [5,10,15,20,25,30,"All"]
        window_list["values"] = windows
        window_list.current(3)
        window_list.state(["readonly"])
        window_list.grid(column=1,row=4,sticky=(N,S,E,W))

        self.window_list = window_list

        # Configure the area where query results will be displayed
        results = Text(self.frame, width=95, height=20,wrap=WORD)
        results.grid(row=0,column=0,rowspan=3,columnspan=3,sticky=(N,S,E,W))
        results.insert("1.0","Search results will appear here")
        results.configure(font="16")
        results.configure(state="disabled")

        self.display_search_results = results

        # Configure the text scrollbar
        txt_scroll = ttk.Scrollbar(self.frame, orient=VERTICAL, command=results.yview)
        txt_scroll.grid(row=0,column=3,rowspan=3,sticky=(N,S))
        results["yscrollcommand"] = txt_scroll.set

        # Configure check button grid
        check_frame = Frame(self.frame,relief=RIDGE,bd=10)
        check_frame.grid(column=1,row=5,columnspan=1,rowspan=5,pady=20) 
        

        # Configure checkbuttons to allow the user to display additional information from their query
        self.user_id_c_sv = IntVar()
        user_id_c = ttk.Checkbutton(check_frame,text="User ID",variable=self.user_id_c_sv,)
        user_id_c.grid(column=1,row=6,sticky=W,padx=40)

        self.dob_c_sv = IntVar()
        dob_c = ttk.Checkbutton(check_frame,text="Date of Birth",variable=self.dob_c_sv)
        dob_c.grid(column=1,row=7,sticky=W,padx=40)

        self.survey_date_c_sv = IntVar()
        survey_date_c = ttk.Checkbutton(check_frame,text="Survey Date",variable=self.survey_date_c_sv)
        survey_date_c.grid(column=1,row=8,sticky=W,padx=40)

        self.ms_type_c_sv = IntVar()
        ms_type_c = ttk.Checkbutton(check_frame,text="MS Type",variable=self.ms_type_c_sv)
        ms_type_c.grid(column=1,row=9,sticky=W,padx=40)

        self.ms_onset_year_c_sv = IntVar()
        ms_onset_year_c = ttk.Checkbutton(check_frame,text="MS Onset Year",variable=self.ms_onset_year_c_sv)
        ms_onset_year_c.grid(column=1,row=10,sticky=W,padx=40,pady=5)       
        
        # Configure labels
        search_box_l = ttk.Label(self.frame,text="Enter your search term below:")
        search_box_l.grid(column=0,row=3)

        window_l = ttk.Label(self.frame,text="Choose how many words either side of your term you wish to extract:")
        window_l.grid(column=1,row=3)

        checkbutton_l = ttk.Label(check_frame, text="Select additional information to display. If a box is greyed out it means the information\n was not provided when the CSV was loaded in")
        checkbutton_l.grid(column=1,row=5)

        # Store the combo boxes as data members to use in other member functions
        self.user_id_c_s = user_id_c
        self.dob_c_s = dob_c
        self.survey_date_c_s = survey_date_c
        self.ms_type_c_s = ms_type_c
        self.ms_onset_year_c_s = ms_onset_year_c
    
    def validateAndInit(self):

        """
        Defines the behaviour for when the text search button on the main menu is clicked

        Instatiates an instance of the TextSearcher class as a data member, runs the preprocessing
        of the CSV, dynamically disables the combo boxes according to the choose header combobox values
        and displays the search page 

        """
        
        # Disable the combo boxes for those that the user has not told us are in the CSV file
        # Combo boxes: [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year] 
        
        csv_header_combo_boxes = self.app.csv_header_combo_boxes
        
        if self.app.csv_header_combo_boxes[2].get() == "NONE":
            messagebox.showerror("Input Error", "Error: Free Text required")
            return
        
        if csv_header_combo_boxes[0].get() == "NONE":
            self.user_id_c_s.configure(state="disabled")
        if csv_header_combo_boxes[1].get() == "NONE":
            self.dob_c_s.configure(state="disabled")
        if csv_header_combo_boxes[3].get() == "NONE":
            self.survey_date_c_s.configure(state="disabled")
        if csv_header_combo_boxes[4].get() == "NONE":
            self.ms_type_c_s.configure(state="disabled")
        if csv_header_combo_boxes[5].get() == "NONE":
            self.ms_onset_year_c_s.configure(state="disabled")

        if self.searcher == None:
            loading_window,loading_bar = self.setupLoadingWindow()
            self.searcher = TextSearcher(self.app.df,csv_header_combo_boxes,loading_bar=loading_bar,loading_window=loading_window)
            text_header = csv_header_combo_boxes[2].get()
            self.searcher.preProcessText(text_header)
            self.clearButtonClick_sf()
            loading_window.destroy()


        self.app.resizeWindow("900x750")
        self.app.displayFrame("search frame")  

    def clearSearcher(self):
        self.searcher = None    

    def setupLoadingWindow(self):
        loading_window = Toplevel(self.root)
        loading_window.geometry("300x60+750+500")
        loading_window.transient()
        loading_window.update_idletasks()
        loading_label = Label(loading_window,text="Loading... this may take a while for large datasets")
        loading_label.grid(column=0, row=0, sticky=(N,S,E,W))
        loading_bar = ttk.Progressbar(loading_window,orient=HORIZONTAL,mode="determinate",length=200)
        loading_bar.grid(column=0,row=1)
        loading_window.update_idletasks()

        return loading_window,loading_bar



    def clearButtonClick_sf(self):

        """
        Defines the behaviour for when the clear button is clicked

        Clears all relevant information and allows the user to search for
        a different phrase and window

        """
            
        # Reset search information stored in the searcher
        self.searcher.reset()

        # Allow user to enter text in the search box again
        self.search_box.config(state="normal")

        # Delete entry in the search box
        self.search_box.delete(0,"end")  

        # Allow the user to alter the window again
        self.window_list.config(state="normal")

        # Reset the window list to 20
        self.window_list.current(3)        

        # Reset the text displayed in the text box
        self.display_search_results.configure(state="normal")
        self.display_search_results.delete('1.0','end')
        self.display_search_results.insert("1.0","Search results will appear here")
        self.display_search_results.configure(state="disabled")
        self.search_button.configure(state="normal")

     
    def downloadButtonClick_sf(self):
        """
        """
        # Returns a file object in write mode
        save_file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")

        # The above returns none if the user exits the dialog without pressing save
        if save_file == None:
            return
        
        # Get the search results to write to the file
        search_results = self.display_search_results.get("1.0","end")
        save_file.write(search_results)
        

    
    def searchButtonClick_sf(self):

        """
        Defines the behaviour for when the search button is clicked

        Gets the search results from the TextSearcher class, and outputs
        this result to the Text box on the page

        """
        
        search_phrase = self.search_box.get()
        window = self.window_list.get()

        # Prevent the user from altering text, unless the clear button is pressed
        self.search_box.config(state="disabled")

        # Prevent the user from altering the window, unless the clear button is pressed
        self.window_list.config(state="disabled")

        # Define the additional queries to display
        query_l = []
        if self.user_id_c_sv.get():
            query_l.append("user_id")
        if self.dob_c_sv.get():
            query_l.append("dob")
        if self.survey_date_c_sv.get():
            query_l.append("survey date")
        if self.ms_type_c_sv.get():
            query_l.append("ms type")
        if self.ms_onset_year_c_sv.get():
            query_l.append("ms year")

        result = self.searcher.findPhraseInText(search_phrase,window,query_list=query_l)
        self.display_search_results.configure(state="normal")
        self.display_search_results.delete('1.0','end')
        self.display_search_results.insert('1.0',result)

        # Highlight all occurnces of the search phrase
        phrase_len = len(search_phrase)
        start_pos = self.display_search_results.search(search_phrase,"1.0","end")

        
        while start_pos != "":
            tag_end = start_pos + "+" + str(phrase_len) + "c"
            self.display_search_results.tag_add("highlight",start_pos,tag_end)
            self.display_search_results.tag_config("highlight", background= "yellow", foreground= "black")           

            start_pos = self.display_search_results.search(search_phrase,tag_end,"end")


        self.search_button.configure(state="disabled")
        self.display_search_results.configure(state="disabled")
