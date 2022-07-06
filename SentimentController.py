import pandas as pd
from SentimentModel import SentimentModel
from SentimentGrapher import SentimentGrapher_tk as sg

import textwrap

class SentimentController:
    def __init__(self) :
        self.model = SentimentModel()

    
    def loadCSV(self, filepath):
        self.model.importFile(filepath)
    
    
    def validateCSV(self, input = pd.DataFrame, csv_headers = list()):
        #process input csv into standardized dataframe
        #[user_id, dob, free_txt, 
        # completed_date, ms_type, 
        # ms_onset_year, edss, 
        # diagnosisDate, gender]
        data = pd.DataFrame()
        headers = self.model.STANDARD_HEADERS
        idx = 0
        #userid
        if csv_headers[0].get() != "NONE":
            column = input[csv_headers[0].get()]
            data.insert(idx, headers[0], column)
            idx+=1
        #dob
        if csv_headers[1].get() != "NONE":
            column = input[csv_headers[1].get()]
            data.insert(idx, headers[1], column)
            idx+=1
        #value
        if csv_headers[2].get() != "NONE":
            column = input[csv_headers[2].get()]
            data.insert(idx, headers[2], column)
            idx+=1
        #date
        if csv_headers[3].get() != "NONE":
            column = input[csv_headers[3].get()]
            data.insert(idx, headers[3], column)
            idx+=1
        #ms type
        if csv_headers[4].get() != "NONE":
            column = input[csv_headers[4].get()]
            data.insert(idx, headers[4], column)
            idx+=1
        #ms onset yr
        if csv_headers[5].get() != "NONE":
            column = input[csv_headers[5].get()]
            data.insert(idx, headers[5], column)
            idx+=1
        #edss
        if csv_headers[6].get() != "NONE":
            column = input[csv_headers[6].get()]
            data.insert(idx, headers[6], column)
            idx+=1
        #diagnosis date
        if csv_headers[7].get() != "NONE":
            column = input[csv_headers[7].get()]
            data.insert(idx, headers[7], column)
        #gender
        if csv_headers[8].get() != "NONE":
            column = input[csv_headers[8].get()]
            data.insert(idx, headers[8], column)
        
        self.model.rawData = data
        return
       
    ####################################################################################
    #region                             USER PAGE
    
    def validateUserId(self, userId):
        self.model.validateUserId(userId)
        return
    
    def buildUserInfo(self, userId) -> str:
        return self.model.getUserInfo(userId)
    
    
    def getFreeTxt(self, userId, tWidth = 40) -> list:
        result = "\n\n\n"
        txt = self.model.getUserFreetxt(userId)
        for entry in txt:
            w = textwrap.wrap(entry, tWidth)
            w2 = '\n'.join(w)
            result += w2
            result += "\n\n"
        return result
    
    
    def buildUserGraphs(self, userId, tk_frame, sent_on, 
                        disabl_on, combine_on, height = 0):
        sHist = None
        dHist = None
        
        if sent_on.get() or combine_on.get():
            sHist = self.model.buildSentimentHistory_single(userId)
        if disabl_on.get() or combine_on.get():
            dHist = self.model.buildEDSSHistory_single(userId)
        
        sg.plotUserGraphs(  tk_frame, sent_on.get(), 
                            disabl_on.get(), combine_on.get(), 
                            sentimentHistory=sHist, edssHistory=dHist, height = height)
        return
    #endregion
    
    ####################################################################################
    #region                          TREND PAGE
    
    
    def calcSentiments(self):
        self.model.calcSentiments()
        return
    
    
    def calcEDSS(self):
        self.model.processEDSS()
        
        return
    
    
    def buildTrendGraphs(self, num, displayFrame,
                         sa_on, disabl_on):
        if sa_on.get():
            self.model.buildSentimentHistory(cap = num)
        if disabl_on.get():
            self.model.buildEDSSHistory(cap = num)
            
        sg.plotTrendGraphs(displayFrame, sa_on.get(), disabl_on.get(),
                           self.model.sentimentHistory,
                           self.model.EDSS_history)
        return
    
    
    def buildSentDistribution(self, displayFrame,
                              distroNeg_on, distroNeu_on,
                              distroPos_on, distroComp_on,
                              scatter_on):
        sg.plotSentimentDistribution(displayFrame, self.model.sentimentSet,
                              distroNeg_on.get(), distroNeu_on.get(),
                              distroPos_on.get(), distroComp_on.get(),
                              scatter_on.get())
        return
    
    #endregion