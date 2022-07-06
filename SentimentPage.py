import os

from tkinter import *
from tkinter import ttk, filedialog, messagebox

from numpy import place

from SentimentController import SentimentController



class SentimentPage:

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
        self.configureSentimentPage()
        

    def configureSentimentPage(self):
        totalWidth = self.totalWidth
        totalHeight = self.totalHeight
        optionsWidth = self.optionsWidth
        scrollbarWidth = self.scrollbarWidth
        headerHeight = self.headerHeight
        displayWidth = totalWidth - optionsWidth - scrollbarWidth
        mainHeight = totalHeight - headerHeight
        ########################################################################
        #Style
        ########################################################################
        NhsBlue = self.NhsBlue
         # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame')
        s.configure('Custom.TButton', borderwidth=10, bd=10) #doesnt work

        # style for debugging
        s.configure('Frame1.TFrame', background='red')
        s.configure('HeaderFrame.TFrame', background = NhsBlue)

        ########################################################################
        #Header Frame
        ########################################################################
        
        
        f_header = ttk.Frame(self.frame, style='HeaderFrame.TFrame')
        # f_header.grid(column =0, row = 0)
        f_header.place(x= 0, y = 0, relwidth=1.0, height= headerHeight)
        s.configure('Label1.TLabel', background = NhsBlue)
        l_pageTitle = ttk.Label(f_header, text ="USER ANALYSIS", style='Label1.TLabel', 
                                foreground='white')
        l_pageTitle.grid(column=0,row=0)
        
        ########################################################################
        #Control frame
        ########################################################################
        f_controls = ttk.Frame(self.frame)
        f_controls.grid(column=0, row = 1)
        f_controls.place(x = 0, y = headerHeight, width = optionsWidth, height= mainHeight)
        
        ##search area
        f2_search = ttk.Frame(f_controls, width=optionsWidth)
        #f2_search.grid(row = 1)
        f2_search.place(x = 0, y = 0, width = optionsWidth, relheight=0.2)
        
        l_searchInstructions = ttk.Label(f2_search, text= "Enter User ID", width=optionsWidth-10)
        l_searchInstructions.grid(row=0, column = 0, sticky=(E,W)) 
        # l_searchInstructions.place(x = 5, y= 0)
        
        search_phrase = StringVar()
        search_box = ttk.Entry(f2_search,textvariable=search_phrase, width=optionsWidth-10)
        # search_box.grid(row=1, column = 0, padx = 10, pady=10)
        search_box.place(x = 5, y = 30, width=optionsWidth-10, height=24)
        self.searchBox = search_box
        
        
        ##options frame
        f2_options = ttk.Frame(f_controls)
        f2_options.grid(row =2, column = 0)
        f2_options.place(x = 0, rely=0.2, width=optionsWidth, relheight=0.6)
        
        l_options = ttk.Label(f2_options, text = "Options")
        l_options.grid(row = 0, column = 0, sticky="W", padx=10)
        
        self.sa_on = IntVar()
        self.check_sa = ttk.Checkbutton(f2_options, text = "Sentiment Analysis", 
                                   variable=self.sa_on)
        self.check_sa.grid(row = 1, column = 0, sticky="W", padx=10)

        
        self.disabl_on = IntVar()
        self.check_disabl = ttk.Checkbutton(f2_options,text = "Disability Score (EDSS)", 
                                       variable=self.disabl_on)
        self.check_disabl.grid(row = 2, column = 0, sticky="W", padx=10)
        
        self.combine_on = IntVar()
        self.check_combine = ttk.Checkbutton(f2_options, text = "Combine", 
                                        variable=self.combine_on)
        self.check_combine.grid(row = 4, column = 0, sticky="W", padx=10)
        
        
        
        self.freetxt_on = IntVar()
        ch_freetxt = ttk.Checkbutton(f2_options, text = "List Free Text", 
                                     variable= self.freetxt_on)
        ch_freetxt.grid(row = 5, sticky="W", padx=10)
        
        
        ##control footer frame
        f2_footer = ttk.Frame(f_controls)
        #f2_footer.grid(row = 4, column = 0)
        f2_footer.place(x = 0, rely=0.8, relwidth=1.0, relheight=0.2)
        
        b_generate = Button(f2_footer, text = "Generate", bg = "light blue", borderwidth=2, font=("bold", 12),
                                command = lambda: self.generate_click())
        b_generate.place(x = 5, y= 0, width=optionsWidth-10, relheight=1/2*0.95)
        
        b_back = Button(f2_footer, text="Back", bg = "light blue", borderwidth=2, font=("bold", 12),
                            command= lambda: self.app.displayFrame("main frame"))
        #b_back.grid(row=2, column = 0, sticky=(N,S,E,W))
        b_back.place(x = 5, rely=1/2*0.97, width=optionsWidth-10, relheight=1/2*0.95)
        
        
        ########################################################################
        #Display frame
        ########################################################################
        
        f_display = ttk.Frame(self.frame, borderwidth=0, width= displayWidth, height = mainHeight)
        #f_display.grid(column = 1, row = 1, sticky=(N,S,E,W))
        f_display.place(x=optionsWidth, y = headerHeight, width=displayWidth, height=mainHeight)
            
        canvas = Canvas(f_display, width = displayWidth, height = mainHeight)
        #canvas.grid(row = 0, column = 0, sticky=(N,S,E, W))
        canvas.place(relx=0, rely=0, relheight=1, relwidth=0.95)
        
        scrollbar = ttk.Scrollbar(f_display, orient=VERTICAL, command=canvas.yview)
        # scrollbar.grid(row=0, column = 1, sticky=(N,S))
        scrollbar.place(relx=0.95, rely=0, relheight = 1, relwidth = 0.05)
        
        canvas.configure(yscrollcommand=scrollbar.set)

        self.f2_container = ttk.Frame(canvas)
        #self.f2_container.grid(sticky=(N,S,E,W))
        self.f2_container.place(relx= 0, rely=0,relheight=1, relwidth=1)
        self.f2_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=self.f2_container, anchor="nw")
        
        results = Text(self.f2_container, width=95)
        results.grid(row=0, column = 0, sticky=(E,W))
        results.insert("1.0","Result will appear here")
        results.configure(font="16")
        results.configure(state="disabled")
        
        
        return
    
    def validateAndInit(self):       
        h = self.app.csv_header_combo_boxes
        #userId
        if h[0].get() == "NONE":
            messagebox.showerror("Input Error", "Error: User ID required")
            return
        #value
        if h[2].get() == "NONE":
            self.check_sa.configure(state="disabled")
            self.check_combine.configure(state="disabled")
        #edss
        if h[6].get() == "NONE":
            self.check_disabl.configure(state="disabled")
            self.check_combine.configure(state="disabled")
        #date
        if h[3].get() == "NONE":
            messagebox.showerror("Input Error", "Error: Completed Date required")
            return
        
        #import and standardize headers
        self.controller.validateCSV(self.app.df, self.app.csv_header_combo_boxes)
        
        #display this page
        self.app.displayFrame("sent frame")
        return
        
        
    def generate_click(self) :
        #store entered user id
        try:
            userId = int(self.searchBox.get())
        except:
            messagebox.showerror("Input Error", "Error: Only Integers Allowed!")
            return
        self.searchBox.delete(0, "end")
        
        #check if user id val
        try:
            self.controller.validateUserId(userId)
        except:
            messagebox.showerror("Input Error", "Error: User ID not found!")
            return
        
        #clear display frame
        for widget in self.f2_container.winfo_children():
            widget.destroy()


        #Build textual component of output
        padx = 10
        tWidth = 60 #width at which wrapping occurs
        #create user info header
        outputText = self.controller.buildUserInfo(userId)
        
        #list free text
        if self.freetxt_on.get():
            outputText += self.controller.getFreeTxt(userId, tWidth)
            
            
        h = outputText.count('\n') + 2
        r = Text(self.f2_container, width = tWidth, height = h ,padx= 20)
        r.insert("end", outputText)
        
        r.configure(font="10")
        r.configure(state= "disabled")
        r.grid(row=0, column = 0, sticky=(E,W))
        #r.place(relx= 0.5, rely = 0.0, relwidth=1.0, anchor="center")
        
        # build graphs   
        try:
            self.controller.buildUserGraphs(userId, self.f2_container, 
                                            self.sa_on, self.disabl_on,
                                            self.combine_on, h)
        except ValueError as e:
            print(e)
            messagebox.showerror("Insufficient Data", "User does not have enough data points to generate graph.")
            
        
        return
    
    
 