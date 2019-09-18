from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import  json
import os.path

"""modulo para validar cpf/cnpj"""
from pycpfcnpj import cpfcnpj


class List():
    #width - largura do widget
    #height - altura do widget
    #text - texto a ser exibido
    #font - família da fonte do texto
    #Fg - cor do texto do widget
    #Bg - cor do fundo do widget
    #Side - que lado o widget se posicionará(LEFT, RIGHT, TOP, BOTTOM)

    def __init__(self, root, model):
        self.fontPadrao = ("Arial", "10")
        self.fontEntry = ("Vendana", "8")
        self.model = model()

        self.toplevel = root
        self.operacao = "BROWSER" #BROWSER EDIT INSERT
        self.id = StringVar()

        self.searchFrame = Frame(self.toplevel)
        self.searchFrame['padx'] = 10
        self.searchFrame['pady'] = 10
        self.searchFrame.pack(side="top")

        self.frame = Frame(self.toplevel)
        self.frame.pack(side="top")

        self.form = Frame(self.toplevel)
        self.form.pack(side="top")

        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        """Estilo para os label e botões"""

        style = ttk.Style()
        style.configure("BW.TLabel", padding=6, foreground="white" , background="brown", font=('helvetica', 9, 'bold'))
        style.configure("BW.TEntry", padding=6, background="#ccc", relief="flat")
        style.configure("BW.TButton", padding=6, relief="flat", background="#ccc")

        """Imagens para os botões"""
        self.btnNewImage = PhotoImage(file=r'C:\Users\eliba\PycharmProjects\SolosInter\venv\bin\images\new.png').subsample(3, 3)
        self.btnDelImage = PhotoImage(file=r'C:\Users\eliba\PycharmProjects\SolosInter\venv\bin\images\del.png').subsample(3,3)
        self.btnSaveImage = PhotoImage(file=r'C:\Users\eliba\PycharmProjects\SolosInter\venv\bin\images\disk_save.png').subsample(3,3)
        self.btnCancelImage = PhotoImage(file=r'C:\Users\eliba\PycharmProjects\SolosInter\venv\bin\images\cancel.png').subsample(3, 3)

        self.CreateSearch()
        self.CreateTable()
        self.CreateForm()
        self.LoadTable(tipoLeitura='all')#all byname
        self.initBotoes()

    """Validação dos campos"""
    def validate_text(self, texto):
        if len(texto) == 0:
            return False
        else:
            return True



    def error(self,tipo, msg):
        messagebox.showwarning(tipo,msg)

    def mensagem(self, tipo, msg):
        messagebox.showinfo(tipo, msg)

    def CreateSearch(self):
        self.labelS = ttk.Label(self.searchFrame, text="Localizar: ", style="BW.TLabel", compound=LEFT)
        self.labelS.grid(row=0, column=0)

        self.txtSearch  = ttk.Entry(self.searchFrame, style="BW.TEntry")
        self.txtSearch.grid(row=0, column=2, columnspan=5, sticky=W, ipadx=100, padx=(10,5))

        self.btnSearch = ttk.Button(self.searchFrame, style="BW.TButton", compound=LEFT)
        self.btnSearch['text'] = 'Localizar'
        self.btnSearch['width'] = 12
        self.btnSearch['command'] = self.localizarPropriedade
        #self.btnSearch['image'] = self.btnDelImage
        self.btnSearch.grid(row=0, column=7, padx=(10,5))



    def CreateForm(self):
        """Label para mensagens de erro ou sucesso"""
        self.container1 = Frame(self.form)
        self.container1['pady'] = 10
        self.container1.grid(row=0, column=0, columnspan=3)
        self.titulo1 = ttk.Label(self.container1, text="Formulário")
        self.titulo1["font"] = ("Verdana","9", "italic")
        self.titulo1.pack(fill=X)

        """Caixas de texto"""
        """Informa o nome da propriedade"""
        self.container2 = Frame(self.form)
        self.container2['pady'] = 10
        self.container2.grid(row=1, column=0)
        self.lblNomePropriedade = Label(self.container2, text="Propriedade:", font=self.fontPadrao, width=10)
        self.lblNomePropriedade.pack(side=LEFT)
        #vcmd = self.container2.register(self.validate_text) #registra a validação do texto
        #self.txtNomePropriedade = Entry(self.container2, validate='key', validatecommand=(vcmd, '%P'))
        self.txtNomePropriedade = Entry(self.container2)
        self.txtNomePropriedade.focus_set()
        self.txtNomePropriedade['width'] = 65
        self.txtNomePropriedade['font'] =self.fontEntry
        self.txtNomePropriedade.pack(side=LEFT)

        """Informa o nome do proprietario"""
        self.container3 = Frame(self.form)
        self.container3['pady'] = 10
        self.container3.grid(row=2, column=0)
        self.lblNomePropritario = Label(self.container3, text="Proprietário:", font=self.fontPadrao, width=10)
        self.lblNomePropritario.pack(side=LEFT)
        self.txtNomeProprietario = Entry(self.container3)
        self.txtNomeProprietario['width'] = 30
        self.txtNomeProprietario['font'] = self.fontEntry
        self.txtNomeProprietario.pack(side=LEFT)

        """Informa o cpf do proprietário"""
        self.lblCPF = Label(self.container3, text="CPF:", font=self.fontPadrao, width=10)
        self.lblCPF.pack(side=LEFT)
        self.txtCpfProprietario = Entry(self.container3)
        self.txtCpfProprietario['width'] = 20
        self.txtCpfProprietario['font'] = self.fontEntry
        self.txtCpfProprietario.pack(side=LEFT)

        """Informa o Localidade do proprietário"""
        self.container4 = Frame(self.form)
        self.container4['pady'] = 10
        self.container4.grid(row=3, column=0, columnspan=4)
        self.lblLocalidade= Label(self.container4, text="Endereço:", font=self.fontPadrao, width=10)
        self.lblLocalidade.pack(side=LEFT)
        self.txtLocalidade = Entry(self.container4)
        self.txtLocalidade['width'] = 65
        self.txtLocalidade['font'] = self.fontEntry
        self.txtLocalidade.pack(side=LEFT)

        """Informa o Localidade do proprietário"""
        self.container5 = Frame(self.form)
        self.container5['pady'] = 10
        self.container5.grid(row=4, column=0)
        self.lblCidade = Label(self.container5, text="Cidade:", font=self.fontPadrao, width=10)
        self.lblCidade.pack(side=LEFT)
        self.txtCidade = Entry(self.container5)
        self.txtCidade['width'] = 65
        self.txtCidade['font'] = self.fontEntry
        self.txtCidade.pack(side=LEFT)

        """Botões para as ações"""
        self.container6 = Frame(self.form)
        self.container6['pady'] = 10
        self.container6.grid(row=5, column=0)

        self.btnNew = ttk.Button(self.container6, style="BW.TButton", compound=LEFT)
        self.btnNew['text'] = 'New'
        self.btnNew['width'] = 12
        self.btnNew['command'] = self.newPropriedade
        self.btnNew['image'] = self.btnNewImage
        self.btnNew.pack(side=LEFT, padx=10, pady=10)

        self.btnSave = ttk.Button(self.container6, style="BW.TButton", compound=LEFT)
        self.btnSave['text'] = 'Save'
        self.btnSave['width'] = 12
        self.btnSave['command'] = self.savePropriedade
        self.btnSave['image'] = self.btnSaveImage
        self.btnSave.pack(side=LEFT, padx=10, pady=10)

        self.btnCancel = ttk.Button(self.container6, style="BW.TButton", compound=LEFT)
        self.btnCancel['text'] = 'Cancel'
        self.btnCancel['width'] = 12
        self.btnCancel['command'] = self.cancelActions
        self.btnCancel['image'] = self.btnCancelImage
        self.btnCancel.pack(side=LEFT, padx=10, pady=10)

        self.btnDelete = ttk.Button(self.container6, style="BW.TButton", compound=LEFT)
        self.btnDelete['text'] = 'Delete'
        self.btnDelete['width'] = 12
        self.btnDelete['command'] = self.deletePropriedade
        self.btnDelete['image'] = self.btnDelImage
        self.btnDelete.pack(side=LEFT, padx=10, pady=10)
        #https://www.devmedia.com.br/tkinter-interfaces-graficas-em-python/33956

    def initBotoes(self):
        if self.operacao == 'BROWSER':
            self.btnNew['state'] = NORMAL
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = DISABLED
            self.btnDelete['state'] = NORMAL
            self.txtNomeProprietario['state'] = DISABLED
            self.txtNomePropriedade['state'] = DISABLED
            self.txtLocalidade['state'] = DISABLED
            self.txtCidade['state'] = DISABLED
            self.txtCpfProprietario['state'] = DISABLED
        elif self.operacao == 'EDIT':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = DISABLED
            self.txtNomeProprietario['state'] = NORMAL
            self.txtNomePropriedade['state'] = NORMAL
            self.txtLocalidade['state'] = NORMAL
            self.txtCidade['state'] = NORMAL
            self.txtCpfProprietario['state'] = NORMAL
        elif self.operacao == 'INSERT':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = NORMAL
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = DISABLED
            self.txtNomeProprietario['state'] = NORMAL
            self.txtNomePropriedade['state'] = NORMAL
            self.txtLocalidade['state'] = NORMAL
            self.txtCidade['state'] = NORMAL
            self.txtCpfProprietario['state'] = NORMAL
        elif self.operacao == 'DELETE':
            self.btnNew['state'] = DISABLED
            self.btnSave['state'] = DISABLED
            self.btnCancel['state'] = NORMAL
            self.btnDelete['state'] = NORMAL
            self.txtNomeProprietario['state'] = DISABLED
            self.txtNomePropriedade['state'] = DISABLED
            self.txtLocalidade['state'] = DISABLED
            self.txtCidade['state'] = DISABLED
            self.txtCpfProprietario['state'] = DISABLED

    def limpaCampos(self):
        """Limpa todos os campos"""
        self.txtNomeProprietario.delete(0, END)
        self.txtNomePropriedade.delete(0, END)
        self.txtLocalidade.delete(0, END)
        self.txtCidade.delete(0, END)
        self.txtCpfProprietario.delete(0, END)
        self.id = ''

    def cancelActions(self):
        self.operacao = 'BROWSER'
        self.initBotoes()
        self.limpaCampos()


    def newPropriedade(self):
        self.operacao = 'INSERT'
        self.initBotoes()
        self.limpaCampos()


    def savePropriedade(self):
        if self.operacao == 'INSERT':
            lista = self.model
            """Captura o conteúdo dos campos"""
            proprietario = self.txtNomeProprietario.get()
            propriedade = self.txtNomePropriedade.get();
            localidade = self.txtLocalidade.get()
            cidade = self.txtCidade.get()
            cpf = self.txtCpfProprietario.get()

            """Valida todos os campos"""
            pr, pp, local, city, doc = True, True, True, True, True
            valida = [
                pr == self.validate_text(proprietario),
                pp == self.validate_text(propriedade),
                local == self.validate_text(localidade),
                city == self.validate_text(cidade),
                doc == self.validate_text(cpf)
            ]

            if all(valida):
                """Válida cpf/cnpj"""
                if (cpfcnpj.validate(cpf) == True):
                    lista.proprietario = self.txtNomeProprietario.get()
                    lista.propriedade = self.txtNomePropriedade.get()
                    lista.localidade = self.txtLocalidade.get()
                    lista.cidade = self.txtCidade.get()
                    lista.cpf = self.txtCpfProprietario.get()

                    """Informa se ocorreu sucesso ou erro"""
                    self.mensagem('Insert', lista.insert())

                    self.CreateTable()
                    self.LoadTable(tipoLeitura='all')
                    """Configura os botões"""
                    self.operacao = 'BROWSER'
                    self.limpaCampos()
                    self.initBotoes()
                else:
                    self.error('Aviso', 'O CPF/CNPJ é inválido.\nEntre com um CPF/CNPJ válido.')
            else:
                self.error('Aviso', 'Todos os campos devem ser preenchidos')
        elif self.operacao == 'EDIT':
            lista = self.model
            """Captura o conteúdo dos campos"""
            proprietario = self.txtNomeProprietario.get()
            propriedade = self.txtNomePropriedade.get();
            localidade = self.txtLocalidade.get()
            cidade = self.txtCidade.get()
            cpf = self.txtCpfProprietario.get()

            """Valida todos os campos"""
            pr, pp, local, city, doc = True, True, True, True, True
            valida = [
                pr == self.validate_text(proprietario),
                pp == self.validate_text(propriedade),
                local == self.validate_text(localidade),
                city == self.validate_text(cidade),
                doc == self.validate_text(cpf)
            ]
            if all(valida):
                """Válida cpf/cnpj"""
                if (cpfcnpj.validate(cpf) == True):
                    lista.id = self.id
                    lista.proprietario = self.txtNomeProprietario.get()
                    lista.propriedade = self.txtNomePropriedade.get()
                    lista.localidade = self.txtLocalidade.get()
                    lista.cidade = self.txtCidade.get()
                    lista.cpf = self.txtCpfProprietario.get()

                    """Informa se ocorreu sucesso ou erro"""
                    self.mensagem('Edit', lista.save())
                    self.CreateTable()
                    self.LoadTable(tipoLeitura='all')
                    self.operacao = 'BROWSER'
                    self.limpaCampos()
                    """Configura os botões"""
                    self.initBotoes()
                else:
                    self.error('Aviso', 'O CPF/CNPJ é inválido.\nEntre com um CPF/CNPJ válido.')
            else:
                self.error('Aviso', 'Todos os campos devem ser preenchidos')


    def deletePropriedade(self):
        selection = self.tree.selection()
        for selection in self.tree.selection():
            curItem = self.tree.set(selection, "#1")
            if curItem:
                lista = self.model.deleteItem(curItem)
                self.mensagem('Delete', lista)
                self.CreateTable()
                self.LoadTable(tipoLeitura='all')
                self.operacao = 'BROWSER'
                self.initBotoes()
            else:
                self.error('Aviso', 'Você deve selecionar um item primeiro.')

        #https://gist.github.com/dobesv/57aa185fbdca7d99559ae91cfbadcb24

    def localizarPropriedade(self):
        self.LoadTable(tipoLeitura='byname')
        self.txtSearch.delete(0, END)

    def CreateTable(self):
        style = ttk.Style()
        style.configure('Custom.Treeview', highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("Custom.Treeview.Heading", background="blue", foreground="brown", relief="flat" )

        self.titulo2 = Label(self.frame, text="Listagem de Propriedades")
        self.titulo2['font'] = ("Arial", "10", "bold")
        #self.titulo.pack()
        self.titulo2.grid(row=0, column=0, columnspan=8)

        self.tree = ttk.Treeview(self.frame, columns=(1, 2, 3), show="headings", selectmode = "browse")
        self.tree['style'] = "Custom.Treeview"
        #self.tree.pack(side='left')
        self.tree.grid(row=1, column=0, columnspan=8, sticky='nsew')

        self.tree.heading(1, text="ID")
        self.tree.heading(2, text="Proprietário")
        self.tree.heading(3, text="CPF")

        self.tree.column(1, width=50)
        self.tree.column(2, width=350)
        self.tree.column(3, width=100)

        self.tree.bind('<Double-Button-1>', self.selectItem) #clique duplo
        self.tree.bind('<Button-1>', self.navega)

        self.scroll = ttk.Scrollbar(self.frame, orient=VERTICAL)
        #self.scroll.pack(side='right', fill='y')
        self.scroll.grid(row=1, column=9, sticky='ns')

        self.tree.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.tree.yview)

    def navega(self,a):
        self.operacao = 'DELETE'
        self.initBotoes()

    def selectItem(self,a):
        self.operacao = 'EDIT'
        self.initBotoes()
        selection = self.tree.selection()
        for selection in self.tree.selection():
            curItem = self.tree.set(selection, "#1")
            if curItem:
                lista = self.model.getItem(curItem)
                lista = json.loads(lista)
                for i in range(0, len(lista.get('items'))):
                    #self.titulo['text'] = 'ID da Propriedade: {}'.format(lista['items'][i]['idpropriedade'])
                    self.id = lista['items'][i]['idpropriedade']
                    self.txtNomeProprietario.delete(0, END)
                    self.txtNomeProprietario.insert(0, lista['items'][i]['nomeproprietario'])
                    self.txtNomePropriedade.delete(0, END)
                    self.txtNomePropriedade.insert(0, lista['items'][i]['nomepropriedade'])
                    self.txtLocalidade.delete(0, END)
                    self.txtLocalidade.insert(0, lista['items'][i]['localidadepropriedade'])
                    self.txtCidade.delete(0, END)
                    self.txtCidade.insert(0, lista['items'][i]['cidadepropriedade'])
                    self.txtCpfProprietario.delete(0, END)
                    self.txtCpfProprietario.insert(0, lista['items'][i]['cpfproprietario'])
        return

    def LoadTable(self, tipoLeitura):
        if tipoLeitura=='all':
            lista = self.model.getAll()
        elif tipoLeitura=='byname':
            lista = self.model.getByName(self.txtSearch.get().upper())

        lista = json.loads(lista)
        records = self.tree.get_children()
        for element in records: #se houver elementos em records delete todos
            self.tree.delete(element)
        for i in range(0, len(lista.get('items'))): #e depois preencha a tabela
            #insert(parent, index, iid=None, **kw)
            #index = end -> inserir no final
            #idd = values -> lista de valores associado ao item
            self.tree.insert('', 'end', values = (lista['items'][i]['idpropriedade'], lista['items'][i]['nomeproprietario'], lista['items'][i]['cpfproprietario']))
