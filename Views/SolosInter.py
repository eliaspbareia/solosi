from tkinter import *
from Views.List import List as formList
from Models.Propriedade import Propriedade as modelProp

class Sistema:
    def __init__(self):
        self.root = Tk();

        self.frame = Frame(self.root)
        self.frame.pack()
        """Cria o menu"""
        self.menu = Menu(self.root)
        self.menuArquivo = Menu(self.menu, tearoff=0)
        self.menuArquivo.add_command(label="Análise")
        self.menuArquivo.add_command(label="Propriedades", command=self.showPropriedade)
        self.menuArquivo.add_command(label="Produtos")
        self.menuArquivo.add_command(label="Laudos")
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label="Sair", command=self.root.quit)
        self.menu.add_cascade(label="Sistema", menu=self.menuArquivo)

        self.root.config(menu=self.menu)

    def showPropriedade(self):
        #self.top = Toplevel(self.root)
       # self.top.geometry("550x500")
       # self.center(self.top)
        #list = formList(self.top, modelProp)

            self.top = Toplevel(self.root)
            self.top.geometry("550x650")
            self.center(self.top)
            self.top.transient(self.root)
            self.top.focus_force()
            self.top.grab_set()
            list = formList(self.top, modelProp)




    def center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() -  win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height //2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def start(self):
        self.root.title("Lista de Propriedades")
        self.root.geometry("600x400")
        self.root.attributes('-alpha',0.0)
        self.center(self.root)
        self.root.attributes('-alpha',1.0)
        self.root.mainloop()
