import pandas as pd
from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


#================================================================
class DataQuery:
    """Generic data extractor for csv file. any header name 
    can be added to query, will return empty if name doesnt match."""



    def __init__(self, path, filterVals):
        self.path = path;
        self.filterValues = filterVals
    
    def execute(self) -> pd.DataFrame:
        """Execute query and return a pd.DataFrame;
        # """
        dat_raw = pd.read_csv(self.path)
        dat = dat_raw.filter(self.filterValues)
        return dat
    
#================================================================
class DataQueryBuilder:

    """
    syntax: query(path).withAttr1().withAttr2().build().execute()
    will return a pd.DataFrame. Without execute() will return 
    a DataQuery object.
    """
    
    def __init__(self):
        self.filterValues = list()
        self.path = None
        
    @staticmethod
    def query(path):
        qb = DataQueryBuilder()
        qb.path = path
        return qb
        
    def build(self):
        return DataQuery(self.path, self.filterValues)
        
    def add(self, customHeader) :
        """Append a custom header to the query string.
        Args:
            customHeader (string): Match with header in CSV file.

        """
        self.filterValues.append(customHeader)
        return self
    
    def withUserId(self):
        self.filterValues.append("UserId")
        return self
    
    def withBirthDate(self):
        self.filterValues.append("DOB")
        return self    
    
    def withOnsetDate(self):
        self.filterValues.append("OnsetDate")
        return self
    
    def withValue(self):
        self.filterValues.append("Value")
        return self
    
    def withDiagnosisDate(self):
        self.filterValues.append("DiagnosisDate")
        return self
    
    def withQuestionnaireId(self):
        self.filterValues.append("QuestionnaireId")
        return self
    
    def withCompletedDate(self):
        self.filterValues.append("CompletedDate")
        return self
    
    def withGroupdD(self):
        self.filterValues.append("GroupId")
        return self
    
    def withGender(self):
        self.filterValues.append("Gender")
        return self
    
    def withMSAtDiagnosis(self):
        self.filterValues.append("MSAtDiagnosis")
        return self
    
    def withMSTypeNow(self):
        self.filterValues.append("MSTypeNow")
        return self
    
    def withQuestionnaireKey(self):
        self.filterValues.append("QuestionnaireKey")
        return self
    
    def withWebEDSS(self):
        self.filterValues.append("webEDSS")
        return self
    
    def withCompletedDate_webEDSS(self):
        self.filterValues.append("CompletedDate_webEDSS")
        return self

#================================================================

class DataDisplayer:
 
    """
    Display/Download Graphs in App Feature
    """
 
    #Embeds MatplotLib Chart into a Window.
    def display(plot, title, window):
        fig = Figure(figsize = (5,5), dpi = 100)
        canvas = FigureCanvasTkAgg(fig, master = window)
        canvas.draw()
        canvas.get_tik_widget().pack()
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()
        canvas.get_tik_widget().pack()
 
        window.title(title)
        window.geometry("750x750")
        plot_button = Button(master = window, 
                     command = plot,
                     height = 2, 
                     width = 10,
                     text = "Plot")
        plot_button.pack()
 

 #===============================================================
 #Utility functions
def min_max_scaling(self, data, minV, maxV):
    return (data - minV) / (maxV - minV)

