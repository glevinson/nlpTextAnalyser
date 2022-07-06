
#import nltk
#nltk.data.path.append("S:\ICLMScProject - Imperial MSc project/nltk_data")
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from VaderSentimentAdapter import VaderSentimentAdapter
from DataProcessing import DataQueryBuilder as builder


########################################################################
class SentimentModel():
    
    def __init__(self):
        self.rawData = pd.DataFrame()
        self.sentimentHistory = None
        self.sentimentSet = pd.DataFrame()
        self.comboTable = pd.DataFrame()
        self.EDSS = pd.DataFrame()
        self.EDSS_history = None
        self.HADS = pd.DataFrame()
        #adapter must return single sentiment as a dict with keys
        #["neg", "neu", "pos", "compound"].
        self.adapter = VaderSentimentAdapter()
        self.DATEFORMAT = "%d/%m/%Y"
        self.STANDARD_HEADERS = ["UserId", "DOB", "Value", 
                                 "CompletedDate", "MS_Type", 
                                 "OnsetDate", "EDSS", 
                                 "DiagnosisDate", "Gender"]
        
        
    def importFile(self, csvPath, 
                   userId = "UserId", date = "CompletedDate", 
                   value = "Value", edss = "webEDSS",
                   anx ="Anxiety", depr = "Depression", 
                   dob = "DOB", gender = "Gender", 
                   mstype = "MS_Type", onsetDate ="OnsetDate", 
                   diagnosisdate = "DiagnosisDate") :
        qb = builder.query(csvPath).add(userId).add(date).add(value)
        qb.add(edss).add(anx).add(depr).add(dob).add(gender)
        qb.add(mstype).add(onsetDate).add(diagnosisdate)
        df = qb.build().execute()
        standardizedHeaders = { userId : "UserId",
                                date : "CompletedDate",
                                value: "Value",
                                edss : "webEDSS",
                                anx :"Anxiety", 
                                depr : "Depression", 
                                dob : "DOB", 
                                gender : "Gender", 
                                mstype : "MS_Type", 
                                onsetDate :"OnsetDate", 
                                diagnosisdate : "DiagnosisDate"}
        df.rename(columns = standardizedHeaders, inplace=True)
        
        self.rawData = df
        return
    
    def validateUserId(self, userId):
        print("\nUSER INPUT: " + str(userId) + "\n\n")
        try:
            user = self.rawData.loc[self.rawData["UserId"] == userId].iloc[0]
        except:
            raise ValueError()
        return
    
    def getUserInfo(self, userId) -> str:
        #generate user info header
        user = self.rawData.loc[self.rawData["UserId"] == userId].iloc[0]
        userInfo = ""
        userInfo += f"User ID: {userId}\n"
        if "DOB" in self.rawData.columns:
            dob = user.loc["DOB"]
            userInfo += f"Date of Birth: {dob}\n"
        if "Gender" in self.rawData.columns:
            gen = user.loc["Gender"]
            userInfo += f"Gender: {gen}\n"
        if "MS_Type" in self.rawData.columns:
            typ = user.loc["MS_Type"]
            userInfo += f"MS Type: {typ}\n"
        if "OnsetDate" in self.rawData.columns:
            on = user.loc["OnsetDate"]
            userInfo += f"MS Onset Date: {on}\n"
        if "DiagnosisDate" in self.rawData.columns:
            dia = user.loc["DiagnosisDate"]
            userInfo += f"MS Diagnosis Date: {dia}"
        
        return userInfo
        
    
    def getUserFreetxt(self, userId) -> list:
        user = self.rawData.loc[self.rawData["UserId"] == userId]
        return user["Value"].values.tolist()
        
        
    #region Sentiment
    
    #################################################################################
    #                                   SENTIMENT
    #################################################################################    
    
    def calcSentiments(self, inputData = None, numPts = 0) -> pd.DataFrame:
        """Calculate sentiments by entry. Will process all data points
        in set if numPts is set to 0. Warning: If data set is large, 
        will have a high time cost.
        
        Args:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -numPts     --  Number of data pts to be calculated.
                            if 0, will calculate all pts in set.
        Returns:
            -pd.DataFrame with structure:
             ["UserId", "CompletedDate", 
             "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        """
        if (inputData == None):
            inputData = self.rawData
            
        data = inputData.sample(frac=1).reset_index(drop=True)
        
        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiments = pd.DataFrame(columns = col)

        setLength = len(data) if numPts == 0 else numPts
 
        i = 0
        for idx, row in data.iterrows():
            modulo = int(setLength/10)
            if modulo != 0 and idx % modulo == 0:
                    print(f"Processing sentiments {idx/setLength * 100}% ...")
            if numPts != 0 and i == numPts:
                break
            
            res = self.adapter.calculateSentiment(str(row['Value']))
            processedDate = datetime.strptime(str(row["CompletedDate"]), self.DATEFORMAT)
            content = [row["UserId"], processedDate, res["neg"], res["neu"], res["pos"], res["compound"]]
            sentiments.loc[i] = content
            i+=1
            
        self.sentimentSet = sentiments
        return sentiments
            

    def buildSentimentHistory(self, inputData = None, minN = 3, cap = 0) -> pd.DataFrame:
        """Build sentiment table sorted by UserId with cap specifying number of users. 
        User must have a minimum of minN data points to be added to the table.

        Args:
            inputData (DataFrame):  UserId and Value (string) required.
            minN (int, optional):   Minimum number of data points to be considered. 
                                    Defaults to 3.
            cap (int, optional):    Function is stopped when number 
                                    of found users reaches cap. Defaults to 0.
        Returns:
            pd.DataFrame: ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
             sorted by UserId
        """
        if (inputData == None):
            inputData = self.rawData
        uniqueUserId = pd.unique(inputData.loc[:,"UserId"])

        
        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiments = pd.DataFrame(columns = col)
        userCount = 0
        idx = 0
        for i in range(len(uniqueUserId)):
            dataPts = inputData.loc[inputData["UserId"] == uniqueUserId[i]]
            if len(dataPts) < minN:
                continue
            if cap != 0 and userCount > cap:
                break
            if cap !=0 and userCount % int(cap/20) == 0:
                    print(f"Calculating Sentiments {int((userCount/cap) * 100)}%")
            for index, row in dataPts.iterrows():
                
                s = self.adapter.calculateSentiment(str(row['Value']))
                
                date = str(row["CompletedDate"])            
                dateProcessed = datetime.strptime(date , self.DATEFORMAT)
                
                content = [uniqueUserId[i], dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
                sentiments.loc[idx] = content
                idx += 1
            userCount += 1
        print("Finished Calculating Sentiments")
        self.sentimentHistory = sentiments
        return sentiments
    

    def buildSentimentHistory_single(self, userId = int, inputData = None, minN = 3) -> pd.DataFrame:
        """
        Build sentiment history of one user. 
        Parameters:
            -inputData  --  pd.DataFrame: UserId and Value (string) 
                            required.
            -userId     --  self explanatory.
            -minN       --  minimum number of data points to be considered.
        Returns:
            -pd.DataFrame with structure:
             ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
             sorted by UserId
        """
        
        if inputData == None:
            inputData = self.rawData
            
        dataPts = inputData.loc[inputData["UserId"] == userId]
        if len(dataPts) < minN:
            raise ValueError("Insufficient data points!")

        col = ["UserId", "CompletedDate", "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        sentiments = pd.DataFrame(columns = col)
        idx = 0
        for index, row in dataPts.iterrows():
            s = VaderSentimentAdapter.calculateSentiment(str(row["Value"]))
            #process date format. some are just strings.
            date = str(row["CompletedDate"])            
            dateProcessed = datetime.strptime(date , self.DATEFORMAT)
            content = [userId, dateProcessed, s["neg"], s["neu"], s["pos"], s["compound"]]
            sentiments.loc[idx] = content
            idx += 1
        
        return sentiments
    #endregion
    
    
    #region EDSS
    
    #################################################################################
    #                                   EDSS
    #################################################################################
    def processEDSS(self, csvPath= None, inputData = None, userId = "UserId", date = "CompletedDate",
                    score = "EDSS") :
        """Import CSV file for EDSS scoring, assign standardized header names and 
        store in class member self.EDSS.

        Args:
            csvPath (str): Full file path to CSV file.
            userId (str, optional): Defaults to "UserId".
            date (str, optional): Defaults to "CompletedDate_webEDSS".
            score (str, optional): Defaults to "webEDSS".
        """
        standardizedHeaders = {userId : "UserId",
                                date : "CompletedDate",
                                score: "EDSS"}
        if (csvPath != None):
            qb = builder.query(csvPath).add(userId).add(date).add(score)
            df = qb.build().execute()
            
            df.rename(columns = standardizedHeaders, inplace=True)
            self.EDSS = df
            return
        
        if (inputData == None):
            inputData = self.rawData
            
        df = inputData[[userId, date, score]]
        df.rename(columns = standardizedHeaders, inplace = True)
        self.EDSS = df
        return
            
    
    def buildEDSSHistory_single(self, userId, minN = 3) -> pd.DataFrame:
        """_summary_

        Args:
            inputData (pd.DataFrame): _description_
            dateFormat (str): example "%Y-%m-%d"
            minN (int, optional): Minimum number of data pts per user. Defaults to 3.
            cap (int, optional): Function finishes when cap is reached. Defaults to 0.

        Returns:
            _type_: _description_
        """

        col = ["UserId", "CompletedDate", "EDSS"]
        EDSS = pd.DataFrame(columns = col)
        dataPts = self.rawData.loc[self.rawData["UserId"] == userId]
        
        if len(dataPts) < minN:
            print("Insufficient data points!")
            return
        
        idx = 0
        for index, row in dataPts.iterrows():
            date = str(row["CompletedDate"])
            dateProcessed = datetime.strptime(date, self.DATEFORMAT)
            
            content = [userId, dateProcessed, row["EDSS"]]
            EDSS.loc[idx] = content
            idx+=1
        return EDSS
        
    def buildEDSSHistory(self, inputData = None, minN = 3, cap = 0):
        """Build EDSS history by unique user. if cap is 0, will process all data points.

        Args:
            inputData (pd.DataFrame): _description_
            dateFormat (str): example "%Y-%m-%d"
            minN (int, optional): Minimum number of data pts per user. Defaults to 3.
            cap (int, optional): Function finishes when cap is reached. Defaults to 0.

        Returns:
            _type_: _description_
        """
        
        if (inputData == None):
            inputData = self.EDSS
            
        uniqueUserId = pd.unique(inputData.loc[:,"UserId"])

        col = ["UserId", "CompletedDate", "EDSS"]
        EDSS = pd.DataFrame(columns = col)
        userCount = 0
        idx = 0
        for i in range(len(uniqueUserId)):
            dataPts = inputData.loc[inputData["UserId"] == uniqueUserId[i]]
            
            if len(dataPts) < minN:
                continue
            if cap != 0 and userCount > cap:
                break
            
            
            if cap !=0 and userCount % int(cap/20) == 0:
                    print(f"Calculating EDSS {int((userCount/cap) * 100)}%")
                    
            for index, row in dataPts.iterrows():
                date = str(row["CompletedDate"])
                dateProcessed = datetime.strptime(date , self.DATEFORMAT)
                
                content = [uniqueUserId[i], dateProcessed, row["EDSS"]]
                EDSS.loc[idx] = content
                idx+=1
            userCount += 1
            
        print("Finished building EDSS")
        self.EDSS_history = EDSS
        return EDSS
    #endregion
    
    
    """Note: HADS functionallity not implemented in current app."""
    #region HADS
    
    #################################################################################
    #                                   HADS
    #################################################################################
    def processHADS(self, csvPath, userId = "UserId", date = "CompletedDate",
                    anxietySums = "anxiety_sums", 
                    depressionSums = "depression_sums") :
        """Import CSV file for HADS scoring, assign standardized header names and 
        store in class member self.HADS.

        Args:
            csvPath (str): Full file path to CSV file.
            userId (str, optional): Defaults to "UserId".
            date (str, optional): Defaults to "CompletedDate".
            anxietySums (str, optional): Defaults to "anxiety_sums".
            depressionSums (str, optional): Defaults to "depression_sums".
        """
        qb = builder.query(csvPath)
        qb = qb.add(userId).add(date)
        qb = qb.add(anxietySums)
        qb = qb.add(depressionSums)
        df = qb.build().execute()
        
        standardizedHeaders = {userId : "UserId",
                              date : "Date",
                              anxietySums: "Anxiety",
                              depressionSums: "Depression"}
        df.rename(columns = standardizedHeaders, inplace=True)
        self.HADS = df
        return
    #endregion
            
    
    #################################################################################
    #                                   UTILITY
    #################################################################################
    def _collapseSameDateEntries(userId, dataPts) :
        """ Checks if there are several entries for the same date. If there are,
            entries will be collapsed into one with mean taken for the sentiments.

        Args:
            userId (int): Unique user ID belonging to the data points.
            dataPts (pd.DataFrame): 
                ["UserId", "CompletedDate", 
                "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
        """
        uniqueDates = pd.unique(dataPts.loc[:, "CompletedDate"])
        for date in range(len(uniqueDates)):
            sameDate = dataPts.loc[dataPts["CompletedDate"] == uniqueDates[date]]
            if len(sameDate) > 1:
                avgScore = [userId, uniqueDates[date], 
                            sameDate["Sent_Neg"].mean(), sameDate["Sent_Neu"].mean(),
                            sameDate["Sent_Pos"].mean(), sameDate["Sent_Comp"].mean()]
                dataPts = dataPts.loc[dataPts["CompletedDate"] != uniqueDates[date]]
                dataPts.loc[len(dataPts)] = avgScore
        return