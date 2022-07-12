from tkinter import *
from chat import get_response, nomBoot


TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

alphabet_min = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet_maj = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self.config_main_window()
        
    def display(self):
        self.window.mainloop()
        
    def config_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600,height=500, bg="#2F1F2B")
        
        # Séparateur
        line = Label(self.window, width=450, bg="#FCB677")
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # Affichage de la conversation
        self.chat_affichage = Text(self.window, width=20, height=2, bg="#2F1F2B", fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.chat_affichage.place(relheight=0.745, relwidth=1, rely=0.08)
        self.chat_affichage.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.chat_affichage)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.chat_affichage.yview)
        
        # label du bas
        label_bas = Label(self.window, bg="#FCB677", height=80)
        label_bas.place(relwidth=1, rely=0.825)
        
        # Champs de saisie
        self.saisie = Entry(label_bas, bg="#2F1F2B", fg=TEXT_COLOR, font=FONT)
        self.saisie.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.saisie.focus()
        self.saisie.bind("<Return>", self.button_presse)
        
        # Button d'envoie
        button_envoie = Button(label_bas,fg=TEXT_COLOR, text="Send", font=FONT_BOLD, width=20, bg="#034C65",
                             command=lambda: self.button_presse(None))
        button_envoie.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
    
    def button_presse(self, event):
        msg = self.saisie.get()
        self.inserrer_msg(msg, "You")
        
    def inserrer_msg(self, msg, sender):
        count = 0
        if not msg:
            return

        self.saisie.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        
        self.chat_affichage.configure(state=NORMAL)
        self.chat_affichage.insert(END, msg1)
        self.chat_affichage.configure(state=DISABLED)
        
        msg2 = f"{nomBoot}: {get_response(msg)}\n\n"
        msg2_modif = ""
        for lettre in msg2 :
            msg2_modif += lettre 
            count += 1
            if count >= 60 and lettre not in alphabet_min and lettre not in alphabet_maj:
                count = 0
                msg2_modif += "\n"
        self.chat_affichage.configure(state=NORMAL)
        self.chat_affichage.insert(END, msg2_modif)
        self.chat_affichage.configure(state=DISABLED)
        self.chat_affichage.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.display()