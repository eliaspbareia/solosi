import json
import mysql.connector
from mysql.connector import Error, errorcode
#https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html
import collections

class Propriedade(object):

    def __init__(self, idpropriedade=0, nomeproprietario=None, nomepropriedade=None, localidadepropriedade=None, cidadepropriedade=None, cpfproprietario=None, ):
        self.id = idpropriedade;
        self.proprietario = nomeproprietario
        self.propriedade = nomepropriedade
        self.localidade = localidadepropriedade
        self.cidade = cidadepropriedade
        self.cpf = cpfproprietario

    def conectar(self):
        try:
            self.con = mysql.connector.connect(host="localhost",
                                               user="root",
                                               passwd="Bot9e0l1i2a1s7",
                                               db="solosvirtual")
            if self.con.is_connected():
                return True
            else:
                return False
        except Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(f'Você digitou errado o login ou a senha')
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'O banco de dados não existe')
            else:
                print(e)


    def desconectar(self):
        if self.con.is_connected():
            self.con.close()

    def getAll(self):
        """ Abre o banco de dados e busca todos os registros"""
        retorno = self.conectar()
        if retorno:
            query = "SELECT idpropriedade, nomeproprietario, nomepropriedade, cpfproprietario FROM solosvirtual.propriedades"
            rs = self.con.cursor()
            rs.execute(query)
            rows_headers = [x[0] for x in rs.description]  # retorna as colunas
            rows = rs.fetchall() #retorna os dados
            json_list = []
            for row in rows:
                json_list.append(dict(zip(rows_headers, row)))

            rs.close()
            self.desconectar()
            return json.dumps({'items':json_list},indent=4)

    def getItem(self, id):
        retorno = self.conectar()
        if retorno:
            query = "SELECT idpropriedade, nomeproprietario, nomepropriedade, localidadepropriedade, cidadepropriedade, cpfproprietario FROM solosvirtual.propriedades where idpropriedade = {}".format(id)
            rs = self.con.cursor()
            rs.execute(query)
            rows_headers = [x[0] for x in rs.description]  # retorna as colunas
            rows = rs.fetchall() #retorna os dados
            json_list = []
            for row in rows:
                json_list.append(dict(zip(rows_headers, row)))
            rs.close()
            self.desconectar()
            return json.dumps({'items':json_list},indent=4)

    def getByName(self, texto):
        retorno = self.conectar()
        if retorno:
            #cursor.execute("SELECT name FROM `table` WHERE name LIKE '%s' " % (txt))
            #cursor.execute("SELECT name FROM `table` WHERE name LIKE '%s'" % (txt_for_query))
            query = "SELECT idpropriedade, nomeproprietario, nomepropriedade, localidadepropriedade, cidadepropriedade, cpfproprietario FROM solosvirtual.propriedades where nomeproprietario LIKE '{}%'".format(texto)
            rs = self.con.cursor()
            rs.execute(query)
            rows_headers = [x[0] for x in rs.description]  # retorna as colunas
            rows = rs.fetchall() #retorna os dados
            json_list = []
            for row in rows:
                json_list.append(dict(zip(rows_headers, row)))
            rs.close()
            self.desconectar()
            return json.dumps({'items':json_list},indent=4)

    def insert(self):
        """ Insere os registros no BD"""
        retorno = self.conectar()
        try:
            #query = "INSERT INTO solosvirtual.propriedades (nomeproprietario,nomepropriedade,localidadepropriedade,cidadepropriedade,cpfproprietario) values ('"+self.proprietario+"','"+self.propriedade+"','"+self.localidade+"','"+self.cidade+"','"+self.cpf+"')"
            query = "INSERT INTO solosvirtual.propriedades (nomeproprietario,nomepropriedade,localidadepropriedade,cidadepropriedade,cpfproprietario)" \
                    "VALUES('{}','{}','{}','{}','{}')".format(self.proprietario,self.propriedade,self.localidade,self.cidade,self.cpf)
            rs = self.con.cursor()
            rs.execute(query)
            self.con.commit()
            rs.close()
            self.desconectar()
            return "Registro inserido com sucesso."
        except  Error as e:
            return "Error: {}".format(e)

    def save(self):
        """ Salva os registros no BD"""
        retorno = self.conectar()
        try:
            query = "UPDATE solosvirtual.propriedades SET nomeproprietario = '{}', nomepropriedade = '{}', localidadepropriedade = '{}',cidadepropriedade = '{}',cpfproprietario = '{}' WHERE idpropriedade = '{}'".format(self.proprietario, self.propriedade, self.localidade,
                                                              self.cidade, self.cpf, self.id)
            rs = self.con.cursor()
            rs.execute(query)
            self.con.commit()
            rs.close()
            self.desconectar()
            return "Registro atualizado com sucesso."
        except  Error as e:
            return "Error: {}".format(e)

    def deleteItem(self, id):
        retorno = self.conectar()
        try:
            query = "DELETE FROM solosvirtual.propriedades WHERE idpropriedade = '{}'".format(id)
            rs = self.con.cursor()
            rs.execute(query)
            self.con.commit()
            rs.close()
            self.desconectar()
            return "Registro excluido com sucesso."
        except Error as e:
            return "Error: {}".format(e)
