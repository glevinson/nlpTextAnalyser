import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from matplotlib.figure import Figure



import enum
import pandas as pd

from Interfaces import ISentimentGraphAdapter

class SentimentScoreType(enum.Enum) :
    COMPOUND = 0
    NEGATIVE = 1
    NEUTRAL = 2
    POSITIVE = 3

class SentimentGrapher_tk (ISentimentGraphAdapter):
    """Graphs sentiments with matplotlib for Tkinter.

    Args:
        ISentimentGraphAdapter (_type_): _description_
    """
    def __init__(self) -> None:
        pass
    
    
    @staticmethod
    def plotUserGraphs( tk_frame, sent_on, disabl_on, combine_on,
                       sentimentHistory = None, edssHistory = None,
                       height = 0
                        ):
        count = 0
        if sent_on:
            count+=1
        if disabl_on:
            count +=1
        if combine_on:
            count +=1
            
        figure = Figure(figsize=(6,3*count), dpi=100)
        
        idx = 1
        if sent_on:
            ax_sent = figure.add_subplot(int(f"{count}1{idx}"))
            ax_sent.set_ylabel("Sentiment")
            ax_sent.set_ylim(-1, 1)
            sortedPts = sentimentHistory.sort_values(by="CompletedDate")
            ax_sent.plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
            idx += 1
        if disabl_on:
            ax_disa = figure.add_subplot(int(f"{count}1{idx}"))
            ax_disa.set_ylabel("EDSS")
            ax_disa.set_ylim(0, 10)
            sortedPts = edssHistory.sort_values(by="CompletedDate")
            ax_disa.plot(sortedPts["CompletedDate"], sortedPts["EDSS"])
            idx += 1
        if combine_on:
            sorted_edss = edssHistory.sort_values(by="CompletedDate")
            sorted_sent = sentimentHistory.sort_values(by="CompletedDate")
            
            ax_comb1 = figure.add_subplot(int(f"{count}1{idx}"))
            ax_comb1.set_xlabel("Date")
            ax_comb1.set_ylabel("EDSS", color = "blue")
            ax_comb1.set_ylim(-1, 1)
            ax_comb1.tick_params(axis="y", labelcolor = "blue")
            ax_comb1.plot(sorted_edss["CompletedDate"], sorted_edss["EDSS"], color="blue")
            
            ax_comb2 = ax_comb1.twinx()
            ax_comb2.set_ylabel("Sentiment", color = "red")
            ax_comb2.tick_params(axis="y", labelcolor = "red")
            ax_comb2.set_ylim(0, 10)
            ax_comb2.plot(sorted_sent["CompletedDate"], sorted_sent["Sent_Comp"], color="red")
        
        #add to tkinter canvas
        canvas = FigureCanvasTkAgg(figure, tk_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column = 0, sticky=(tk.E,tk.W))

        toolbar = NavigationToolbar2Tk(canvas, tk_frame)
        toolbar.update()
        canvas._tkcanvas.grid(row=1, column = 0, sticky=(tk.E,tk.W))
        return
    
    @staticmethod
    def plotTrendGraphs(tk_frame, sent_on, disabl_on, 
                        sentimentHistory = pd.DataFrame, 
                        edssHistory = pd.DataFrame):
        count = 0
        if sent_on:
            count+=1
        if disabl_on:
            count +=1
            
        figure = Figure(figsize=(6,3*count), dpi=100)
        idx = 1
        if sent_on:            
            subplotArrangement = int(f"{count}1{idx}")
            SentimentGrapher_tk.plotSentimentHistory(figure, subplotArrangement, sentimentHistory)
            idx += 1
            
        if disabl_on:
            subplotArrangement = int(f"{count}1{idx}")
            SentimentGrapher_tk.plotEdssHistory(figure, subplotArrangement, edssHistory)
        
        #add to tkinter canvas
        canvas = FigureCanvasTkAgg(figure, tk_frame)
        canvas.get_tk_widget().grid(row=0, column = 0)
        
        canvas._tkcanvas.grid(row=0, column = 0)
        return
    
    
    @staticmethod
    def plotSentimentDistribution(tk_frame, sentiments, 
                                  distroNeg_on, distroNeu_on, 
                                  distroPos_on, distroComp_on, 
                                  scatter_on):
        count = 0
        if distroNeg_on:
            count+=1
        if distroNeu_on:
            count +=1
        if distroPos_on:
            count +=1
        if distroComp_on:
            count +=1
        if scatter_on:
            count +=1
            
        sliceNum = 100 
        figure = Figure(figsize=(6,3*count), dpi=100)
        
        idx = 1
        if distroNeg_on:
            ax_neg = figure.add_subplot(int(f"{count}1{idx}"))
            ax_neg.hist(sentiments["Sent_Neg"], sliceNum)
            ax_neg.set_title("Negative Sentiment")
            idx+=1
        if distroNeu_on:
            ax_neu = figure.add_subplot(int(f"{count}1{idx}"))
            ax_neu.hist(sentiments["Sent_Neu"], sliceNum)
            ax_neu.set_title("Neutral Sentiment")
            idx+=1
        if distroPos_on:
            ax_pos = figure.add_subplot(int(f"{count}1{idx}"))
            ax_pos.hist(sentiments["Sent_Pos"], sliceNum)
            ax_pos.set_title("Positive Sentiment")
            idx+=1
        if distroComp_on:
            ax_comp = figure.add_subplot(int(f"{count}1{idx}"))
            ax_comp.hist(sentiments["Sent_Comp"], sliceNum)
            ax_comp.set_title("Compound Sentiment")
            idx+=1
        if scatter_on:
            ax_scatter = figure.add_subplot(int(f"{count}1{idx}"))
            ax_scatter.scatter(sentiments["Sent_Neg"], sentiments["Sent_Pos"])
            ax_scatter.set_title("Neg/Pos Scatter")
            
        #add to tkinter canvas
        canvas = FigureCanvasTkAgg(figure, tk_frame)
        canvas.get_tk_widget().grid(row=1, column = 0)
        
        canvas._tkcanvas.grid(row=1, column = 0)
        return
    
    
    @staticmethod
    def plotScoreDistribution(sentimentScores, type, numSlices = 100) :
        """_summary_
            Plots a histogram showing the distribution of one sentiment score type.
        Args:
            sentimentScores ( ndarray ( ,4) ): 0 = compound, 1 = neg, 2 = neu, 3 = pos.
            type (int): select which type to plot.
            numSlices (int, optional): Define resolution of histogram. Defaults to 100.
        """
        if type < 0 or type > 3:
            raise ValueError("Sentiment Type must be value 0-3.")
#
        numSlices = 100
        #filter out 0
        sc = sentimentScores[sentimentScores[:, type] != 0]
        
        plt.hist(sc[:,0], numSlices)
        plt.title("Compound Sentiment Distribution")
        plt.ylabel("count")
        plt.xlabel("score")
        plt.show()
        
        
    @staticmethod
    def plotNegPosScatter(sentimentScores) : 
        """_summary_
            Plots a scatter graph. x-axis for negative sentiment, y-axis for 
            positive sentiment
        Args:
            sentimentScores (ndarray ( , 4 )): 0 = compound, 1 = neg, 2 = neu, 3 = pos.
        """
        #scatter positive to negative sentiment
        plt.figure()
        plt.scatter(sentimentScores[:, 1], sentimentScores[:, 3])
        plt.title("Positive to Negative Sentiment")
        plt.xlabel("negative sentiment")
        plt.ylabel("positive sentiment")
        plt.show()
        return
        
        
        
    ############### SENTIMENT ANALYSIS  ##########################
    @staticmethod
    def plotSentimentHistory_single(sentimentHistory, tk_frame):
        """Plot sentiment history of a single user. 
        Args:
            sentimentHistory (pd.DataFrame): 
                ["UserId", "CompletedDate", 
                "Sent_Neg", "Sent_Neu", "Sent_Pos", "Sent_Comp"]
                
        """
        
        #build matplotlib figure
        f = Figure(figsize=(6,3), dpi=100)
        ax = f.add_subplot(111)
        sortedPts = sentimentHistory.sort_values(by="CompletedDate")
        ax.plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])
        
        #add to tkinter canvas
        canvas = FigureCanvasTkAgg(f, tk_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column = 0)

        canvas._tkcanvas.grid(row=1, column = 0)
        return
    
    @staticmethod
    def plotSentimentHistory(figure, subplotArrangement, sentimentHistory = pd.DataFrame):
        """
        Plot sentiment history of a collection of users. 
        
        Args:
            sentimentHistory (pd.DataFrame): preprocessed dataframe
            figure: matplotlib figure
            subplotArrangement: int specifying position of subplot. 
                                ex: (312) second subplot in a layout with 3 rows, 1 column
            
                
        """
        uniqueId = pd.unique(sentimentHistory.loc[:,"UserId"])
        ax_sent = figure.add_subplot(subplotArrangement)
        for i in range(len(uniqueId)):
            dataPts = sentimentHistory.loc[sentimentHistory["UserId"] == uniqueId[i]]
            
            sortedPts = dataPts.sort_values(by="CompletedDate")
            ax_sent.plot(sortedPts["CompletedDate"], sortedPts["Sent_Comp"])

        ax_sent.set_title("Sentiment Trend")
        ax_sent.set_ylim(-1, 1)
        ax_sent.set_ylabel("Sentiment Score")
        ax_sent.set_xlabel("Date")
        return
    
    
    
    ############################## EDSS  ####################################
    @staticmethod
    def plotEDSSHistory_single(inputData, tk_frame):
        #build matplotlib fifure
        f = Figure(figsize=(6,3), dpi=100)
        ax = f.add_subplot(111)
        sortedPts = inputData.sort_values(by="CompletedDate")
        ax.plot(sortedPts["CompletedDate"], sortedPts["EDSS"])
        
        #add to tkinter canvas
        canvas = FigureCanvasTkAgg(f, tk_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column = 0)
        
        canvas._tkcanvas.grid(row=1, column = 0)
        return
    
    
    @staticmethod
    def plotEdssHistory(figure, subplotArrangement, edssHistory = pd.DataFrame):
        uniqueId = pd.unique(edssHistory.loc[:,"UserId"])
        ax_disa = figure.add_subplot(subplotArrangement)

        for i in range(len(uniqueId)):
            dataPts = edssHistory.loc[edssHistory["UserId"] == uniqueId[i]]
            
            sortedPts = dataPts.sort_values(by="CompletedDate")
            ax_disa.plot(sortedPts["CompletedDate"], sortedPts["EDSS"])
            
        ax_disa.set_title("EDSS Trend")
        ax_disa.set_ylim(0, 10)
        ax_disa.set_ylabel("EDSS")
        ax_disa.set_xlabel("Date")
        return
    
    
    @staticmethod
    def plot_EDSS_sentiment(userId, edss_history, sentiment_history):
        
        data_edss = edss_history.loc[edss_history["UserId"] == userId]
        data_sent = sentiment_history.loc[sentiment_history["UserId"] == userId]
        
        #if no matching user, ignore
        if len(data_sent) == 0 or len(data_edss) == 0:
            print("No matches found.")
            return
        
        sorted_edss = data_edss.sort_values(by="CompletedDate")
        sorted_sent = data_sent.sort_values(by="CompletedDate")
        plt.figure()
        
        plt.plot(sorted_edss["CompletedDate"], sorted_edss["EDSS"])
        plt.plot(sorted_sent["CompletedDate"], sorted_sent["Sent_Comp"])
        
        plt.show()
        return
    
    
            