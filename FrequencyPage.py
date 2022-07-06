# FrequencyPage.py
# configures the UI for the Word Frequency Analysis page/frame

# Dicts are created on page load - searches can then be performed instantly

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import pandas as pd

from FrequencyAnalyser import FrequencyAnalyser

class FrequencyPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.analyser = None

        self.configureFreqPage()
    
    # configuration (called on initialisation)
    def configureFreqPage(self):
        

        # RESULTS BOX #
        
        
        # Configure the area where frequency results will be displayed
        results = Text(self.frame, width=95, height=10)
        results.grid(row=0,column=0,rowspan=3,columnspan=3,sticky=(N,S,E,W))
        results.insert("1.0","Frequency results will appear here")
        results.configure(font="16")
        results.configure(state="disabled")

        self.display_results = results    
        
        # Configure the results scrollbar - *for 'list most freq' only?*
        results_scroll = ttk.Scrollbar(self.frame, orient=VERTICAL, command=results.yview)
        results_scroll.grid(row=0,column=3,rowspan=3,sticky=(N,S))
        results["yscrollcommand"] = results_scroll.set
        
        # SEARCH #

        search_frame = Frame(self.frame,relief=RIDGE,bd=5)
        search_frame.grid(column=0,row=3,columnspan=3,rowspan=2)
        
        search_header = Label(search_frame, anchor = W, text = "Find phrase frequency in data (max 4 words)",font=("bold",12, "underline"))
        search_header.grid(column = 0, row = 3, columnspan = 2, pady = 8, padx=263, sticky = NSEW)

        # Search box
        freq_phrase = StringVar()
        freq_box = ttk.Entry(search_frame, textvariable = freq_phrase)
        freq_box.grid(column = 0, row = 4, sticky = (N,S,E,W),pady=10)

        self.freq_phrase = freq_phrase
        self.freq_box = freq_box

        # 'Get phrase frequency' button
        freq_search_button = Button(search_frame, bg = "light blue", borderwidth=2, font=("bold", 12), 
                                        text = "Get phrase frequency", 
                                        command = lambda: self.freqSearchButtonClick())
        freq_search_button.grid(column=1,row=4,sticky=(N,S,E,W),pady=10)


        # MOST FREQUENT N-GRAMS #

        ngram_frame = Frame(self.frame,relief=RIDGE,bd=5)
        ngram_frame.grid(column=0, row=5, columnspan=3, rowspan=3)
        
        most_freq_header = Label(ngram_frame, anchor = CENTER, text = "Most frequent n-grams in data",font=("bold",12, "underline"))
        most_freq_header.grid(column = 0, row = 5, columnspan = 2, pady = 8,padx=314,sticky = NSEW)
        
        # n-gram list ('n' in 'n-gram)
        ngram_list_label = ttk.Label(ngram_frame, anchor = CENTER, text = "Number of words in the n-gram:")
        ngram_list_label.grid(column = 0, row = 6, sticky = NSEW)
        
        ngram_list = ttk.Combobox(ngram_frame, textvariable=None)
        ngrams = [1,2,3,4]
        ngram_list["values"] = ngrams
        ngram_list.current(0)
        ngram_list.state(["readonly"])
        ngram_list.grid(column=1, row=6, sticky=(N,S,E,W))
        
        self.ngram_list = ngram_list
        
        # most frequent number list (length of list displayed)
        
        most_frequent_list_label = ttk.Label(ngram_frame, anchor = CENTER, text = "Length of list:")
        most_frequent_list_label.grid(column = 0, row = 7, sticky = NSEW,pady=10)
        
        most_frequent_list = ttk.Combobox(ngram_frame, textvariable=None)
        sizes = [5,10,15,20,25,30]
        most_frequent_list["values"] = sizes
        most_frequent_list.current(3)
        most_frequent_list.state(["readonly"])
        most_frequent_list.grid(column = 1, row = 7, sticky = (N,S,E,W),pady=10)

        self.most_frequent_list = most_frequent_list


        # graph/plot freq button
        graph_freq_button = Button(ngram_frame, bg = "light blue", borderwidth=2, font=("bold", 12), 
                                       text = "Plot most frequent n-grams", 
                                       command = lambda: self.graphMostFreqNgramsClick())
        graph_freq_button.grid(column = 0, columnspan=2, row = 8, sticky = (N,S,E,W))
        
        # SETTINGS #
        settings_frame = Frame(self.frame,relief=RIDGE,bd=5)
        settings_frame.grid(column=0,columnspan=3,row=9,rowspan=5)
        
        settings_header = Label(settings_frame, anchor = CENTER, text = "Settings for plotting n-grams",font=("bold",12, "underline"))
        settings_header.grid(column = 0, row = 9, columnspan = 2, pady = 10, sticky = NSEW,padx=320)

        # Configure the ms type list
        ms_type_list_label = ttk.Label(settings_frame, anchor = CENTER, text = "MS Type:")
        ms_type_list_label.grid(column = 0, row = 10, pady=10, sticky = NSEW)
        
        ms_type_list = ttk.Combobox(settings_frame, textvariable=None)
        types = ["All","Benign","PPMS","SPMS","RRMS"]
        ms_type_list["values"] = types
        ms_type_list.current(0)
        ms_type_list.state(["readonly"])
        ms_type_list.grid(column = 1, row = 10, sticky = (N,S,E,W))

        self.ms_type_list = ms_type_list

        # SETTINGS - CHECKBOXES #
        # stopwords
        self.remove_stopwords = IntVar()
        remove_stopwords = ttk.Checkbutton(settings_frame, 
                                           text = "Remove Stopwords", 
                                           variable = self.remove_stopwords)
        remove_stopwords.grid(column=0,row=11, sticky = (N,S,E,W))

        # only medical words
        self.medical_only = IntVar()
        medical_only = ttk.Checkbutton(settings_frame, 
                                       text = "Search Medical Terms Only", 
                                       variable = self.medical_only)
        medical_only.grid(column = 0, row = 12, sticky = (N,S,E,W))
        self.medical_box = medical_only
        # unique users
        self.unique_only = IntVar()
        unique_only = ttk.Checkbutton(settings_frame, 
                                      text = "Only Count A Word Once Per User", 
                                      variable = self.unique_only)
        unique_only.grid(column = 0, row = 13, sticky = (N,S,E,W))

        # count word once per text entry
        self.different_entries_only = IntVar()
        different_entries_only = ttk.Checkbutton(settings_frame, 
                                                 text = "Only Count A Word Once Per User Entry", 
                                                 variable = self.different_entries_only)
        different_entries_only.grid(column = 0, row = 14, sticky = (N,S,E,W))
        
        self.plot_by_type_var = IntVar()
        plot_by_type = ttk.Checkbutton(settings_frame, 
                                           text = "Plot by MS type", 
                                           variable = self.plot_by_type_var)
        plot_by_type.grid(column=1,row=11, sticky = (N,S,E,W))

        self.plot_by_type = plot_by_type

        
        # BACK BUTTON #

        back_b = Button(self.frame, bg = "light blue", borderwidth=2, font=("bold", 12), 
                            text = "Back", 
                            command = lambda: self.backButtonClick())
        back_b.grid(column = 0, row = 15, columnspan=2, pady = 20, sticky=(N,S,E,W))


    def backButtonClick(self):
        self.app.resizeWindow("900x640")
        self.app.displayFrame("main frame")

    def clearAnalyser(self):
        self.analyser = None

    # Loads the Word Frequency Analysis page frame (from Main Menu)
    # Heavy function - creates dictionaries from csv
    def validateAndInit(self):
        # validate
        # user ID
        if self.app.csv_header_combo_boxes[0].get() == "NONE":
            messagebox.showerror("Input Error", "Error: User ID required")
            return
        # free text
        if self.app.csv_header_combo_boxes[2].get() == "NONE":
            messagebox.showerror("Input Error", "Error: Free Text required")
            return
        # init

        self.ms_type = self.app.csv_header_combo_boxes[4].get()

        if self.ms_type == "NONE":
            self.ms_type_list.configure(state="disabled")
            self.plot_by_type.configure(state="disabled")
        else:
            self.ms_type_list.configure(state="normal")
            self.plot_by_type.configure(state="normal")

          

        self.app.resizeWindow("900x750")
        if self.analyser == None:
            loading_window,loading_bar = self.setupLoadingWindow()



            if self.ms_type == "NONE":
                self.ms_type=None
            self.analyser = FrequencyAnalyser(self.app.df, 
                                            self.app.csv_header_combo_boxes[2].get(), 
                                            self.app.csv_header_combo_boxes[0].get(), 
                                            self.ms_type,
                                            processed= False, loading_bar= loading_bar,
                                            loading_window = loading_window)
            loading_window.destroy()
        if self.analyser.medical_file == False:
            self.medical_box.configure(state="disabled")
        self.app.displayFrame("freq frame")
        
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

    # 'Get phrase frequency' button (search button) : behaviour
    def freqSearchButtonClick(self):

        freq_search_phrase = self.freq_box.get().strip()
        # change to read in number entered
        # prevent from moving forward with more than 4 words in a phrase
        ngrams = count_words_in_string(self.freq_phrase.get())
        if ngrams <= 0 or ngrams > 4:
            self.display_results.configure(state = "normal")
            self.display_results.delete('1.0', 'end')
            self.display_results.insert('1.0', "Please enter a phrase containing 4 words or fewer")
            self.display_results.configure(state = "disabled")
            return
        ms_type = str(self.ms_type_list.get())      

        # Build Boolean variables
        remove_stopwords = False
        medical_only = False
        allow_duplicates = True
        allow_duplicates_across_entries = False
            

        frequency_count = self.analyser.getFrequencyOfNgram(freq_search_phrase, 
                                                            ngrams, 
                                                            remove_stopwords, 
                                                            medical_only, 
                                                            allow_duplicates, 
                                                            allow_duplicates_across_entries, 
                                                            ms_type)

        entry_count = self.analyser.getFrequencyOfNgram(freq_search_phrase, 
                                                            ngrams, 
                                                            remove_stopwords, 
                                                            medical_only, 
                                                            allow_duplicates=False, 
                                                            allow_duplicates_across_entries=True, 
                                                            ms_type=ms_type)
        
        total_entries = self.analyser.getTotalEntries()

        proportion_of_entries = entry_count/total_entries * 100

        proportion_of_entries = "{:.2f}".format(proportion_of_entries)


        

        result = "Frequency of the phrase: '"
        result += freq_search_phrase
        result += "' is: "
        result += str(frequency_count)
        result += "\n\nAppearing in "
        result += proportion_of_entries
        result += "% of entries, out of a total of "
        result += str(total_entries)
        result += " entries\n\n"


        self.display_results.configure(state="normal")
        self.display_results.delete('1.0','end')
        self.display_results.insert('1.0',result)
        self.display_results.configure(state="disabled")

   
    # Button of 'same' name ('plot _')
    def graphMostFreqNgramsClick(self):

        ngrams = int(self.ngram_list.get())
        size = int(self.most_frequent_list.get())
        if self.ms_type != None:
            ms_type = str(self.ms_type_list.get()) 
        else:
            ms_type = "All"

        # Build Boolean variables
        remove_stopwords = False
        medical_only = False
        allow_duplicates = True
        allow_duplicates_across_entries = False

        if self.remove_stopwords.get():
            remove_stopwords = True
        if self.medical_only.get():
            medical_only = True
        if self.unique_only.get():
            allow_duplicates = False
        if self.different_entries_only.get():
            allow_duplicates_across_entries = True

        if allow_duplicates == False:
            allow_duplicates_across_entries = False

        plt_by_type = False

        if self.ms_type != None:
            if self.plot_by_type_var.get():
                plt_by_type = True

        self.analyser.graphMostFrequentNgrams(ngrams,size,remove_stopwords,medical_only,allow_duplicates,
                                              allow_duplicates_across_entries,ms_type,plot_by_type=plt_by_type)
        
        #
        #
        
# HELPER FUNCTIONS #

def count_words_in_string(string):
    return len(string.split())


#
#
#