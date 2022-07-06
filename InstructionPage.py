from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

"""
Class for the Instruction Page
"""


class InstructionPage:

    def __init__(self):
        info = Toplevel()
        info.title("Instructions Page")
        info.geometry("900x640+0+0")
        info.columnconfigure(0, weight=1)
        info.rowconfigure(0, weight=1)

        major_title = ('Calibri (Body)', 24, 'bold', 'underline')
        small_title = ('Calibri (Body', 20, 'bold')
        normal_text = ('Calibri (Body', 14)
        header = ('Calibri (Body', 16, 'bold', 'underline')

        textTitle = Label(info, anchor=CENTER, text='Instructions\n')
        textTitle.config(font=major_title)
        textTitle.grid(row=0, column=0, columnspan=3)

        self.header1 = "About the software\n"
        self.header2 = "Getting started\n"
        self.header3 = "Search tool\n"
        self.header4 = "Frequency tool\n"
        self.header5 = "User analysis\n"
        self.header6 = "Trend analysis\n"

        self.about_the_software = (
            "This software contains several tools that are designed to analyse textual data within a CSV file."
            " Whilst the software was originally designed to analyse unprompted free-text entries of medical patients with Multiple Sclerosis (MS),"
            " many of the analytical tools will work with any CSV file that contains a column with text entries.\n\n")

        self.getting_started = (
            "From the initial screen, the first step is to click the “load CSV” button, which will prompt you to select the desired CSV file to be analysed."
            " After selecting the file, you will be taken to the “ChooseCSVHeaders” page. On this page, you are required to select the headers of the loaded"
            "in CSV file that contain the relevant, asked for, information. If no such column exists, you simply choose “NONE”. The only required column is"
            " a column that contains free text. Once this has been selected, the “Done” button will become unlocked, allowing progression to the main menu"
            " of the application. However, most features require more than just a free-text column. The search tool only requires a free text column."
            " The frequency tool requires a free-text column and a user ID column. The user and trend analysis tools requires a free-text column, user ID column,"
            " and a completed date column. Note that these requirements are a minimum; additional analysis can be done if more columns are provided.\n\n")

        self.search_tool = (
            "This tool allows you to search for a given phrase in all the free-text entries."
            " Upon the first entry into this tool’s page, some pre-processing is done (such as removing punctuation"
            " and converting all words to lower case), which may take a while if the CSV file is sufficiently large."
            " Search results are displayed in the text box at the top of the window. In addition, you can specify how"
            " many words either side of the phrase you wish to display in each entry (by entry, we mean a ‘row’ in the CSV file)"
            " where the phrase appears. If ‘all’ is selected, the entirety of all matching entries will be displayed. Along with"
            " the free text, additional information can be displayed for each entry, such as the date of birth of the user entry"
            " (assuming that you have specified a date of birth header in the “ChooseCSVHeaders” page).\n\nEach matching entry is "
            "separated by dashes, and the display box can be scrolled if the number of matching entries is large. Query results"
            " can be downloaded in a txt file by pressing the download button. To search another entry, the clear button must be"
            " pressed to reset the output display.\n\n")

        self.frequency_tool = (
            "This tool allows you to query the frequency of a specified n-grams in the free text, as well as"
            " plotting a graph of the most frequent n-grams in the text. Upon the first entry into this tool’s page, a lot of pre-processing is done,"
            " which may take a while if there are a large number of rows and text in the CSV file. An n-gram is a sequence of consecutive words. For"
            " example, “blood pressure” is a bi-gram, so if the frequency of “blood pressure” is 10, that means that there are 10 occurrences of “blood pressure”"
            " in all text entries. A maximum of four sequential words (i.e., quad-grams) can be queried. This is to save on pre-processing time and, in our"
            " experience, an n larger than four does not lead to many interesting results, as the frequency count gets very small.\n\nFor plotting the most"
            " frequent n-grams, there are a series of options you can specify, located in the “settings” section. The “remove stopwords” option will consider"
            " the frequency of n-grams in the free text with stopwords removed. Stopwords are commonly used words in language such as “the, is, this, and” that"
            " do not add much meaning. The list of stopwords we use comes from NLTK. The “medical terms only” option will consider the frequency of n-grams in the"
            " free text with all words other than those appearing in a medical lexicon removed. This option is only enabled if a file in the current working directory called medical_terms.txt  One such medical lexicon is from Aristotelis P., R. Robinson,"
            " and Rajasekharan N., published under the GPL-3.0 license, and can be found on github at: https://github.com/glutanimate/wordlist-medicalterms-en.\n\n"
            "The “only count a word once per user entry option” does what is says on the tin. For example, the same user has multiple entries in the free text"
            " (identified by their user ID), and if all of these entries contain the bi-gram “blood pressure”, this would only be counted as once on the frequency"
            " score. Similarly, the option “only count a word once per user entry” will only score one frequency count if a n-gram is mentioned multiple times in the"
            " same entry. If two entries by the same user mention the same n-gram, this would be counted twice under this option. If both of these options are ticked,"
            " it defaults to the “only count a word once per user” option.\n\n"
            "The final two options require an “MS type” column to be selected, and are only relevant for CSV files directly related to MS. The MS type drop-down affects"
            " the frequency that is displayed on the graph; the frequency will simply be the frequency scores for entries where the user has the specified type of MS. "
            "If “plot by MS type” is selected, four graphs will be displayed once the “plot most frequent n-grams” is pressed, one for each type of MS.\n\n")

        self.user_analysis = (
            "This tool allows analysis of a specific user, identified by their user ID. The tool can generate the free text entries of that user,"
            " the sentiment score for those entries, the users’ disability score at the time of their free text entry/entries (if provided). If the user has more than two"
            " entries, graphs for sentiment and disability scores can be displayed to show how they have changed over time. The “combine” option allows sentiment and disability"
            " score to be overlayed onto a single graph, to potentially highlight any correlation over time.\n\n")

        self.trend_analysis = (
            "This tool plots the trend of multiple users’ sentiment and disability scores overtime. A minimum of 20 users is required to use this tool."
            " The trend plots themselves get fairly ‘busy’ with much more than 20 users. What is perhaps more useful is the distribution plots. These plots are bar charts,"
            " where the y-axis is the number of entries, and the x-axis is the value of sentiment/disability scores. This is a useful way to gauge the overall "
            "sentiment/disability scores of entries in the free text.\n\n")

        instructions = Text(info, width=1, height=22)
        instructions.grid(row=1, column=0, sticky=(N, S, E, W))
        instructions.insert(tk.END, self.header1)
        instructions.insert(tk.END, self.about_the_software)
        instructions.insert(tk.END, self.header2)
        instructions.insert(tk.END, self.getting_started)
        instructions.insert(tk.END, self.header3)
        instructions.insert(tk.END, self.search_tool)
        instructions.insert(tk.END, self.header4)
        instructions.insert(tk.END, self.frequency_tool)
        instructions.insert(tk.END, self.header5)
        instructions.insert(tk.END, self.user_analysis)
        instructions.insert(tk.END, self.header6)
        instructions.insert(tk.END, self.trend_analysis)
        instructions.configure(font=normal_text, wrap=WORD)
        instructions.configure(state="disabled")

        instructions.tag_configure("header", font=header)
        instructions.tag_add("header", "1.0", "1.end")
        instructions.tag_add("header", "4.0", "4.end")
        instructions.tag_add("header", "7.0", "7.end")
        instructions.tag_add("header", "12.0", "12.end")
        instructions.tag_add("header", "21.0", "21.end")
        instructions.tag_add("header", "24.0", "24.end")

        txt_scroll = ttk.Scrollbar(info, orient=VERTICAL, command=instructions.yview)
        txt_scroll.grid(row=1, column=1, sticky=(N, S))
        instructions["yscrollcommand"] = txt_scroll.set

        empty_space = Label(info, text=" ")
        empty_space.grid(row=2, column=0)
