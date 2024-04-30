import customtkinter

class IP_Login(customtkinter.CTk):
    
    def __init__(self, sock):
        super().__init__()
        
        self.socket = sock
        
        self.title("IP configurration")
        self.geometry("700x450")
        
        # 4x1 grid
        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        
        text_font = customtkinter.CTkFont(family="Segoe UI", size=15)
        label_font = customtkinter.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        self.label = customtkinter.CTkLabel(master=self, width=300, justify="center", fg_color="gray80",
                                            height=50, corner_radius=30, text="Configure IP", font=label_font)
        self.label.place(relx=0.5, rely=0.15, anchor=customtkinter.CENTER)
        
        self.IP_entry = customtkinter.CTkEntry(master=self, width=300, height=50, fg_color="gray80",
                                               justify="center", corner_radius=30, 
                                               placeholder_text="Enter IP here", font=text_font)
        self.IP_entry.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)
        
        self.PORT_entry = customtkinter.CTkEntry(master=self, width=300, height=50, fg_color="gray80",
                                               justify="center", corner_radius=30, 
                                               placeholder_text="Enter PORT here", font=text_font)
        self.PORT_entry.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)
        
        self.button = customtkinter.CTkButton(master=self, width=300, height=75, fg_color="gray80",
                                              corner_radius=30, text="Enter", font=label_font,
                                              text_color="gray40", command=self.enter)
        self.button.place(relx=0.5, rely=0.65, anchor=customtkinter.CENTER)
        
    def enter(self):
        IP = self.IP_entry.get()
        PORT = self.PORT_entry.get()
        PORT = int(PORT)
        self.socket.connect((IP, PORT))
        self.destroy()
        