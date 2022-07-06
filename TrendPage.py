from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk

import os


from SentimentController import SentimentController

class TrendPage:

    def __init__(self,root,frame,app):
        self.root = root
        self.frame = frame
        self.app = app
        self.searchBox = None   #search box that contains user input
        self.displayFrame = None #frame where generated profile is displayed
        self.controller = SentimentController()
        self.totalWidth = 900
        self.totalHeight = 640
        self.optionsWidth = 200
        self.scrollbarWidth = 10
        self.headerHeight = 30
        self.NhsBlue = '#005EB8'
        
        self.configureTrendPage()
        return

        
    def configureTrendPage(self):
        totalWidth = self.totalWidth
        totalHeight = self.totalHeight
        optionsWidth = self.optionsWidth
        scrollbarWidth = self.scrollbarWidth
        displayWidth = totalWidth - optionsWidth - scrollbarWidth
        mainHeight = totalHeight - self.headerHeight
        
        NhsBlue = self.NhsBlue
         # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame')

        # style for debugging
        s.configure('Frame1.TFrame', background='red')
        s.configure('HeaderFrame.TFrame', background = NhsBlue)
        s.configure('Label1.TLabel', background = NhsBlue)
        ########################################################################
        #Header Frame
        ########################################################################
        f_header = ttk.Frame(self.frame, style = "HeaderFrame.TFrame", height = self.headerHeight)
        f_header.place(x= 0, y = 0, relwidth=1.0, height= self.headerHeight)
        
        l_pageTitle = ttk.Label(f_header, text ="TREND ANALYSIS", foreground='white', style = 'Label1.TLabel')
        l_pageTitle.grid(column=0,row=0)
        
        #########################################################################
        #Control frame
        ########################################################################
        f_controls = ttk.Frame(self.frame)
        f_controls.place(x = 0, y = self.headerHeight, width = optionsWidth, height= mainHeight)
        
        ##  options frame
        f2_options = ttk.Frame(f_controls)
        f2_options.place(x = 0, rely=0.0, width=optionsWidth, relheight=0.8)
        
        ### input
        f3_input = ttk.Frame(f2_options)
        f3_input.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        
        l_options = ttk.Label(f3_input, text = "Options")
        l_options.grid(row = 0, sticky="W", padx=10)
        
        l_numUsers = ttk.Label(f3_input, text = "Number of Users\n(0 for all, min 20):")
        l_numUsers.grid(row = 1, column= 0, sticky="W", padx=10)
        
        numUsers = StringVar()
        self.e_numUsers = ttk.Entry(f3_input, textvariable=numUsers)
        self.e_numUsers.grid(row=2, column = 0, sticky="EW")
        
        
        ### trend graphs
        f3_trends = ttk.Frame(f2_options)
        f3_trends.place(relx=0, rely=1/3, relwidth=1, relheight=1/3)

        l_trends = ttk.Label(f3_trends, text = "Trend Graphs")
        l_trends.grid(row = 0,sticky="W", padx=10)
        self.sa_on = IntVar()
        self.check_sa = ttk.Checkbutton(f3_trends, text = "Sentiment Trend", 
                                   variable=self.sa_on)
        self.check_sa.grid(row = 1, sticky="W", padx=10)
        
        self.disabl_on = IntVar()
        self.check_disabl = ttk.Checkbutton(f3_trends,text = "EDSS Trend", 
                                       variable=self.disabl_on)
        self.check_disabl.grid(row = 2, sticky="W", padx=10)
        
    
        ### distribution graphs
        f3_distro = ttk.Frame(f2_options)
        f3_distro.place(relx=0, rely=2/3, relwidth=1, relheight=1/3)
        
        l_distribution = ttk.Label(f3_distro, text = "Distribution Graphs")
        l_distribution.grid(row = 0, sticky="W", padx=10)
        
        self.distroNeg_on = IntVar()
        self.check_distroNeg = ttk.Checkbutton(f3_distro, text="Negative", 
                                          variable=self.distroNeg_on)
        self.check_distroNeg.grid(row = 1, sticky="W", padx=10)
        
        self.distroNeu_on = IntVar()
        self.check_distroNeu = ttk.Checkbutton(f3_distro, text="Neutral", 
                                          variable=self.distroNeu_on)
        self.check_distroNeu.grid(row = 2, sticky="W", padx=10)
        
        self.distroPos_on = IntVar()
        self.check_distroPos = ttk.Checkbutton(f3_distro, text="Positive", 
                                          variable=self.distroPos_on)
        self.check_distroPos.grid(row = 3, sticky="W", padx=10)
        
        self.distroComp_on = IntVar()
        self.check_distroComp = ttk.Checkbutton(f3_distro, text="Compound", 
                                          variable=self.distroComp_on)
        self.check_distroComp.grid(row = 4, sticky="W", padx=10)
        
        self.scatter_on = IntVar()
        self.check_scatter = ttk.Checkbutton(f3_distro, text="Scatter", 
                                          variable=self.scatter_on)
        self.check_scatter.grid(row = 5, sticky="W", padx=10)
        
        
        ##control footer frame
        f2_footer = ttk.Frame(f_controls)
        f2_footer.place(x = 0, rely=0.8, relwidth=1.0, relheight=0.2)
        
        b_generate = Button(f2_footer, text = "Generate", bg = "light blue", borderwidth=2, font=("bold", 12),
                                command = lambda: self.generate_click())
        b_generate.place(x = 5, y= 0, width=optionsWidth-10, relheight=1/2*0.95)
        
        
        b_back = Button(f2_footer, text="Back", bg = "light blue", borderwidth=2, font=("bold", 12),
                            command= lambda: self.app.displayFrame("main frame"))
        b_back.place(x = 5, rely=1/2*0.97, width=optionsWidth-10, relheight=1/2*0.95)
        
        
        ########################################################################
        #Display frame
        ########################################################################
        f_display = ttk.Frame(self.frame)
        f_display.place(x=optionsWidth, y = self.headerHeight, width=displayWidth, height=mainHeight)
        self.displayFrame = f_display
        
        
        canvas = Canvas(f_display)
        canvas.place(relx=0, rely=0, relheight=1, relwidth=0.95)
        
        scrollbar = ttk.Scrollbar(f_display, orient=VERTICAL, command=canvas.yview)
        scrollbar.place(relx=0.95, rely=0, relheight = 1, relwidth = 0.05)
        
        canvas.configure(yscrollcommand=scrollbar.set)

        self.f2_container = ttk.Frame(canvas)
        self.f2_container.place(relx= 0, rely=0,relheight=1, relwidth=1)
        self.f2_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.f2_container, anchor="nw")

        results = Text(self.f2_container, width=95)
        results.grid(row=0, column = 0, sticky=(N,S,E,W))
        results.insert("1.0","Result will appear here")
        results.configure(font="16")
        results.configure(state="disabled")
        return
    
    def validateAndInit(self):
        """
        validate imported csv file and feed into 
        sentiment model with standardized headers
        
        """ 
        h = self.app.csv_header_combo_boxes
        #userId
        if h[0].get() == "NONE":
            messagebox.showerror("Input Error", "Error: User ID required")
            return
        #value
        if h[2].get() == "NONE":
            self.check_sa.configure(state="disabled")
            self.check_distroNeg.configure(state="disabled")
            self.check_distroNeu.configure(state="disabled")
            self.check_distroPos.configure(state="disabled")
            self.check_distroComp.configure(state="disabled")
            self.check_scatter.configure(state="disabled")
        #edss
        if h[6].get() == "NONE":
            self.check_disabl.configure(state="disabled")
        #date
        if h[3].get() == "NONE":
            messagebox.showerror("Input Error", 
                                 "Error: Completed Date required")
            return
        
        #import and standardize headers
        self.controller.validateCSV(self.app.df, self.app.csv_header_combo_boxes)
        
        #display this page
        self.app.displayFrame("trend frame")
        return
    
    def loadFile_click(self):
        """
        OBSOLETE
        
        """
        file = filedialog.askopenfile(mode="r", 
                                      filetypes=[("CSV Files", "*.csv")])
        if file:
            filepath = os.path.abspath(file.name)
            self.controller.loadCSV(filepath)
        return
        
    
    def generate_click(self) :
        #store entered user number
        try:
            num = int(self.e_numUsers.get())
            print(f"entered number: {num}")
        except:
            messagebox.showerror("Input Error", "Error: Only Integers Allowed!")
            return
        self.e_numUsers.delete(0, "end")
        
        
        #clear display frame
        for widget in self.f2_container.winfo_children():
            widget.destroy()

        #build graphs
        
        if (self.sa_on.get() or self.distroNeg_on.get() or 
            self.distroNeu_on.get() or self.distroPos_on.get() or 
            self.distroComp_on.get() or self.scatter_on.get()):
                self.controller.calcSentiments()
        if self.disabl_on.get():
            self.controller.calcEDSS()
            
        self.controller.buildTrendGraphs(num, self.f2_container, 
                                        self.sa_on, 
                                        self.disabl_on)
        self.controller.buildSentDistribution(self.f2_container,
                                              self.distroNeg_on,
                                              self.distroNeu_on, 
                                              self.distroPos_on,
                                              self.distroComp_on,
                                              self.scatter_on)
            
        return
    
    def isInt(S):
        if S in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True
        return False