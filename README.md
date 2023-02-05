# Installation
The project requires Python version 3.8 or later. The required libraries can be found in the requirements.txt file. 

A text file containing a list of stopwords to be removed must be placed in nltk_data/stopwords and called "english.txt". We recommend the one found on NLTK_data at: https://www.nltk.org/nltk_data/ 

For the user/trend analysis to work, we require the VADER sentiment (Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.) model zip file top be placed in nltk_data/sentiment/ This can again be found on the NTLK data website: https://www.nltk.org/nltk_data/


# CSVTextAnalyser
## About the software
This software contains several tools that are designed to analyse textual data within a CSV file. Whilst the software was originally designed to analyse unprompted free-text entries of medical patients with Multiple Sclerosis (MS), many of the analytical tools will work with any CSV file that contains a column with text entries.


## Installation
The project requires Python version 3.8 or later. The required libraries can be found in the requirements.txt file. 

## Usage
Once downloaded, navigate to the project's directory in a terminal. Then, run AppClass.py to launch the GUI application.

### About the software
This software contains several tools that are designed to analyse textual data within a CSV file. Whilst the software was originally designed to analyse unprompted free-text entries of medical patients with Multiple Sclerosis (MS), many of the analytical tools will work with any CSV file that contains a column with text entries.

The software was designed and developed by myself, Gus Levinson, and 6 other Imperial MSc Computing students. Throughout the process we kept in close contact with the [UK MS Register](ukmsregister.org), a leading UK study designed to increase understanding of living with MS, for whom this software was originally intended, to ensure that we satisfied user requirements.

### Getting started
From the initial screen, the first step is to click the “load CSV” button, which will prompt you to select the desired CSV file to be analysed. After selecting the file, you will be taken to the “ChooseCSVHeaders” page. On this page, you are required to select the headers of the loaded in CSV file, that contain the relevant, asked for, information. If no such column exists, you simply choose “NONE”. The only required column is a column that contains free text. Once this has been selected, the “Done” button will become unlocked, allowing progression to the main menu of the application. However, most features require more than just a free-text column. The search tool only requires a free text column. The frequency tool requires a free-text column and a user ID column. The user and trend analysis tools requires a free-text column, user ID column, and a completed date column. Note that these requirements are a minimum; additional analysis can be done if more columns are provided.

### Search tool
This tool allows you to search for a given phrase in all the free-text entries. Upon the first entry into this tool’s page, some pre-processing is done (such as removing punctuation and converting all words to lower case), which may take a while if the CSV file is sufficiently large. Search results are displayed in the text box at the top of the window. In addition, you can specify how many words either side of the phrase you wish to display in each entry (by entry, we mean a ‘row’ in the CSV file) where the phrase appears. If ‘all’ is selected, the entirety of all matching entries will be displayed. Along with the free text, additional information can be displayed for each entry, such as the date of birth of the user entry (assuming that you have specified a date of birth header in the “ChooseCSVHeaders” page). 
Each matching entry is separated by dashes, and the display box can be scrolled if the number of matching entries is large. Query results can be downloaded in a txt file by pressing the download button. To search another entry, the clear button must be pressed to reset the output display.   

### Frequency tool
This tool allows you to query the frequency of a specified n-grams in the free text, as well as plotting a graph of the most frequent n-grams in the text. Upon the first entry into this tool’s page, a lot of pre-processing is done, which may take a while if there are a large number of rows and text in the CSV file. An n-gram is a sequence of consecutive words. For example, “blood pressure” is a bi-gram, so if the frequency of “blood pressure” is 10, that means that there are 10 occurrences of “blood pressure” in all text entries. A maximum of four sequential words (i.e., quad-grams) can be queried. This is to save on pre-processing time and, in our experience, an n larger than four does not lead to many interesting results, as the frequency count gets very small.

For plotting the most frequent n-grams, there are a series of options you can specify, located in the “settings” section. The “remove stopwords” option will consider the frequency of n-grams in the free text with stopwords removed. Stopwords are commonly used words in language such as “the, is, this, and” that do not add much meaning. The list of stopwords we use comes from NLTK. The “medical terms only” option will consider the frequency of n-grams in the free text with all words other than those appearing in a medical lexicon removed. This option will only be enabled if there exists a file in the current working directory called medical_terms.txt. One such open source medical lexicon that we would suggest is from Aristotelis P., R. Robinson, and Rajasekharan N., published under the GPL-3.0 license, and can be found on github at: https://github.com/glutanimate/wordlist-medicalterms-en. 

The “only count a word once per user entry option” does what is says on the tin. For example, the same user has multiple entries in the free text (identified by their user ID), and if all of these entries contain the bi-gram “blood pressure”, this would only be counted as once on the frequency score. Similarly, the option “only count a word once per user entry” will only score one frequency count if a n-gram is mentioned multiple times in the same entry. If two entries by the same user mention the same n-gram, this would be counted twice under this option. If both of these options are ticked, it defaults to the “only count a word once per user” option.

The final two options require an “MS type” column to be selected, and are only relevant for CSV files directly related to MS. The MS type drop-down affects the frequency that is displayed on the graph; the frequency will simply be the frequency scores for entries where the user has the specified type of MS. If “plot by MS type” is selected, four graphs will be displayed once the “plot most frequent n-grams” is pressed, one for each type of MS. 

### User Analysis
This tool allows analysis of a specific user, identified by their user ID. The tool can generate the free text entries of that user, the sentiment score for those entries, the users’ disability score at the time of their free text entry/entries (if provided). If the user has more than two entries, graphs for sentiment and disability scores can be displayed to show how they have changed over time. The “combine” option allows sentiment and disability score to be overlayed onto a single graph, to potentially highlight any correlation over time.

### Trend Analysis
This tool plots the trend of multiple users’ sentiment and disability scores overtime. A minimum of 20 users is required to use this tool. The trend plots themselves get fairly ‘busy’ with much more than 20 users. What is perhaps more useful is the distribution plots. These plots are bar charts, where the y-axis is the number of entries, and the x-axis is the value of sentiment/disability scores. This is a useful way to gauge the overall sentiment/disability scores of entries in the free text.  


## License
Full details for the license can be seen on the license page. In essence, the toolkit is free to use for non-commercial use. 
Please kindly cite the work if used for any research purposes.
