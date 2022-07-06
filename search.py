import pandas as pd
import string
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import wordpunct_tokenize
import os

class TextSearcher:

    def __init__(self,df,csv_header_combo_boxes,loading_bar=None,loading_window=None):

        self.df=df
        self.current_txt = None
        self.row_number = 0
        self.searched = False
        self.finished = False
        self.occurence_found = False
        self.csv_headers = csv_header_combo_boxes
        self.loading_bar = loading_bar
        self.loading_window = loading_window

        

        # Sets the nltk data path depending on where this application is saved on the users' machine
        cwd = os.getcwd()
        nltk_data_directory = cwd
        nltk_data_directory += "//nltk_data"
        nltk.data.path.append(nltk_data_directory)
        nltk_data_directory = cwd
        nltk_data_directory += "\\nltk_data"
        nltk.data.path.append(nltk_data_directory)
        self.number_of_rows = len(df.index)

    def removePunctuation(self,text):
        
        """
        Input: text (string)

        Returns: string with no punctuation
        """

        no_punct_list = [char for char in text if char not in string.punctuation]
        no_punct_string = ''.join(no_punct_list)
        return no_punct_string

    def clean(self,text):

        """
        Input: text (string)

        Removes punctuation from string
        and converts it to lower case

        Returns cleaned text (string)

        """
        if isinstance(text,str):
            text = self.removePunctuation(text)
            text = text.lower()
            text = wordpunct_tokenize(text)
            return ' '.join(text)
        

    def preProcessText(self,text_col_name):

        """
        Input: pandas dataframe containing the read in CSV file (df)
            the name of the column containing the raw free text (text_col_name)
        
        For each entry in the data frame, it cleans the text in the free_text cell.
        The full list of cleaned text is then added as a new column of the dataframe
        as "cleaned_txt"        

        """

        proccesed_list = []
        count = 0

        if self.loading_bar != None:
            total_rows = len(self.df.index)
            increment_amount = total_rows//5
            increment = increment_amount

        for _,row in self.df.iterrows():
            count += 1
            if self.loading_bar != None:
                if count == increment:
                    self.loading_bar["value"] += 25
                    self.loading_window.update_idletasks()
                    increment += increment_amount
            proccesed_list.append(self.clean(row[text_col_name]))

        self.df["cleaned_txt"] = proccesed_list
        
    def reset(self):
        self.row_number = 0
        self.current_txt = None
        self.searched = False
        self.finished = False
        self.occurence_found = False

    def findPhraseInText(self,phrase, window, query_list=None):

        """
        Input phrase (string): the phrase to be searched in text 
            window (int): how many words either side of the phrase to display
            df (pd dataframe): contains the dataframe with the free text
            query_list (list): contains the additional information to be returned along with the text

        Searches the cleaned_text for the phrase (exact matches only)

        Returns the found text plus additional queries about that user (if any)

        """    


        df_to_search = self.df.iloc[self.row_number:,:]
        print_str = ""

        for index,row in df_to_search.iterrows():

            if self.searched == False:
                current_txt = row["cleaned_txt"]
                new_str, self.new_txt = self.getPhraseInString(current_txt,phrase,window)
            else:
                new_str,self.new_txt = self.getPhraseInString(self.new_txt,phrase,window)

            if new_str == "":
                self.searched = False
                continue
            
            self.occurence_found = True
            self.searched = True
            self.row_number=index

            # Combo boxes: [user_id, dob, free_txt, completed_date, ms_type, ms_onset_year] 
            # Build the query based on additional parameters
            query = ""
            if "user_id" in query_list:
                query += "User ID: " + str(row[str(self.csv_headers[0].get())]) + "\n"
            if "dob" in query_list:
                query += "User Date of Birth: " + str(row[str(self.csv_headers[1].get())]) + "\n"
            if "survey date" in query_list:
                query += "Survey completed on: " + str(row[str(self.csv_headers[3].get())]) + "\n"
            if "ms type" in query_list:
                query += "User MS Type: " + str(row[str(self.csv_headers[4].get())]) + "\n"
            if "ms year" in query_list:
                query += "Onset year of MS: " + str(row[str(self.csv_headers[5].get())]) + "\n"
            
            if query != "":
                query += "\n\n"
                new_str = query + new_str

            print_str += new_str
            print_str += "\n\n"
            print_str += "-------------------------------------------------------------------------------------"
            print_str += "-------------------------------------------------------------------------------------"
            print_str += "\n\n"

                   

        self.finished = True
        if self.occurence_found == False:
            return "No matches in any text"

        return print_str  
           



    def getPhraseInString(self,text,phrase,window):
        
        if not isinstance(text,str):
            return "","finish"
        
        start_pos = text.find(phrase)

        if start_pos == -1:
            return "","finish"
        
        if window == "All":
            window = len(text)
        else:
            window = int(window)
        
        start,_,end_str = text.partition(phrase)
        f1 = False
        f2 = False

        if start == "":
            f1 = True
            start=[""]
        else:
            start = wordpunct_tokenize(start)

        if end_str == "":
            f2 = True
            end = [""]
        else:
            end = wordpunct_tokenize(end_str)
        
        phrase = wordpunct_tokenize(phrase)

        start_len = len(start)
        end_len = len(end)

        if start_len <= window:
            f1 = True
        if end_len <= window:
            f2 = True
        
        if f1 and f2:
            start += phrase+end
        elif f1:
            end = end[:window]
            start += phrase+end
        elif f2:
            start = start[-window:]
            start += phrase+end
        else:
            start = start[-window:]
            end = end[:window]
            start += phrase+end
        
        print_str = " ".join(start)

        return print_str,end_str
    

    



        
    





