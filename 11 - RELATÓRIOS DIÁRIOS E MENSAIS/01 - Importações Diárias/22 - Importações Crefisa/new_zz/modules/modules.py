from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import Keys, ActionChains
from shutil import move
import os
from pathlib import Path
import datetime
import time

import pandas as pd
import datetime
import os
import json
import warnings
import sys
warnings.filterwarnings("ignore")

# Autenticação no site
class openBrowserCrefisa():
    
    # def __init__(self, user_credencials: dict = dotenv_values("./data/.env")) -> WebDriver:
    def __init__(self, user_credencials: dict = dotenv_values("./data/.env")) -> WebDriver:
        self.user_credencials_login = user_credencials['LOGIN_USER']
        self.user_credencials_password = user_credencials['LOGIN_PASSWORD']
        self.mkDirDownload = self.__mkDirDownload()
        
        
        
    
    def __mkDirDownload(self) -> None:
        os.makedirs("download", exist_ok=True)
        for file in os.listdir('download'):
            os.remove(f"download\\{file}")
            
    def __initialize_driver(self):
        
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        # options.add_argument('-headless')
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", fr"{str(Path().absolute())}\\download")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver
    
    def loguinSendKeys(self):
        driver = self.__initialize_driver()
        driver.get('https://app1.gerencialcredito.com.br/CREFISA/')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtUsuario'))).send_keys(self.user_credencials_login)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtSenha'))).send_keys(self.user_credencials_password)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnLogin'))).click()
        return driver
        

# Download das tabelas    
class get_tables():


    def __init__(self, driver: WebDriver, date: datetime.date, user_credencials= dotenv_values("./data/.env"), get_old_tables = False):
        self.driver = driver
        self.get_old_tables = get_old_tables
        self.user_autentiction = user_credencials['USER_AUTHENTICATION']
        self.date = date
        


    def __move_file(self, date: datetime.date):

        path_download = f"./download/"
        path_to_move = f'./relatorios/{date.year}/{date.month}'
        if self.get_old_tables:
            path_to_move = f'./relatorios_novos/{date.year}/{date.month}'
        
        
        os.makedirs(path_to_move, exist_ok = True)
        if os.path.exists(path_download):
            while os.listdir(path_download) == 0:
                continue
            time.sleep(3)
            if self.get_old_tables:
                move(path_download + os.listdir(path_download)[0], path_to_move + f"/relatorio_pagamentos{date.day}_{date.month}_{date.year}.xls")
            else:
                move(path_download + os.listdir(path_download)[0], path_to_move + f"/relatorio_{date.day}_{date.month}_{date.year}.xls")
            


    def download(self):
        date_work = self.date
        while date_work  < datetime.date.today():


            WebDriverWait(self.driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu4'))).click()
            
            
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu4 > li:nth-child(2) > a:nth-child(1)'))).click()

            try:
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtAutenticacaoSenhaFinanceira'))).send_keys(self.user_autentiction)
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn:nth-child(2)'))).click()
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.swal2-confirm'))).click()
            except TimeoutException:
                pass            
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).clear()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).send_keys(date_work.strftime("%d/%m/%Y"))
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).clear()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).send_keys(date_work.strftime("%d/%m/%Y"))
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado'))).click()

            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(2)'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(2)'))).click()

            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btn'))).click()
            
            try:
                allert = self.driver.switch_to.alert
                self.driver_alert = allert.text

                if self.driver_alert == 'NENHUM RESULTADO FOI ENCONTRADO.':
                    print("Sem dados para: ", date_work)
                    allert.dismiss()
                    date_work = date_work + datetime.timedelta(days = 1)
                    continue

                else:
                    allert = self.driver.switch_to.alert
                    allert.accept()
                    p = self.driver.current_window_handle
                    chwd = self.driver.window_handles
                    for w in chwd:

                        if(w!=p):
                            self.driver.switch_to.window(w)
                            break

            except NoAlertPresentException:
                pass

            self.__move_file(date =date_work)
            date_work
            date_work = date_work + datetime.timedelta(days = 1)

        self.driver.quit()
        

        

# Trabalha nas tabelas
class work_tables():

    def __init__(self, data: datetime.date):
        self.process = False
        self.date = data
        self.load_table()
        self.production_to_storm()
        self.comission_to_storm()
        self.zz()



    def load_json(self):
        
        with open("./data/production_code.json", mode ='r', encoding = 'utf-8') as fp:
            json_data = json.load(fp)
            return json_data

    def load_table(self):
        path_to_read = f"./relatorios/{self.date.year}/{self.date.month}/relatorio_{self.date.day}_{self.date.month}_{self.date.year}.xls" 
        # path_to_read_late_payment = f"../Pagamentos_atrasados/{self.date.year}/{'{:02d}'.format(self.date.month)}/pagamento_atrasado_{self.date.year}_{self.date.month}_{self.date.day}.csv" 
        # path_to_read_late_payment = f"../Pagamentos_atrasados/{self.date.year}/{'{:02d}'.format(self.date.month)}/pagamento_atrasado_{self.date.year}_{self.date.month}_{self.date.day}.csv" 
        path_to_read_late_payment = f"../Pagamentos_atrasados/{self.date.year}/{self.date.month}/pagamento_atrasado_{self.date}.csv" 
        if os.path.exists(path_to_read):
            dados = pd.read_html(path_to_read, header = 0, thousands='.')
            dados_lidos = pd.DataFrame(dados[0])
            if os.path.exists(path_to_read_late_payment):
                print("Lendo pagamentos atrasados!")
                late_payment = pd.read_csv(path_to_read_late_payment)
                print(late_payment.head())
                dados_lidos = pd.concat([dados_lidos, late_payment])


            self.process = True
            setattr(self, 'dados', dados_lidos)


    def production_to_storm(self):
        columns_to_rename = ['PROPOSTA',	
                              'DATA CADASTRO',	
                              'BANCO',	
                              'ORGAO',	
                              'CODIGO TABELA',	
                              'TIPO DE OPERACAO',	
                              'NUMERO PARCELAS',	
                              'VALOR PARCELAS',	
                              'VALOR OPERACAO',	
                              'USUARIO BANCO',
                              'SITUACAO',	
                              'DATA DE PAGAMENTO',
                              'CPF',	
                              'NOME',	
                              'FORMALIZACAO DIGITAL']
        
        columns_to_filter = ['NUMERO_ADE',
                            'DATA_DIGIT_BANCO',
                            'PRAZO',	
                            'VLR_PARC',	
                            'VALOR_BRUTO',	
                            'LOGIN_SUB_USUARIO',
                            'DATA_SUB_STATUS',
                            'CPF',
                            'CLIENTE']
        path_to_save = f'../Importados Storm/01 - PRODUÇÃO/{self.date.year}/{self.date.month}-{self.date.year}'
        os.makedirs(path_to_save, exist_ok = True)
        if self.process:
            dados = getattr(self, 'dados')
            dados_storm = dados[columns_to_filter]
            print(dados_storm)
            dados_storm.insert(2, 'BANCO', 'BANCO CREFISA')
            dados_storm.insert(3, 'ORGAO', '')
            dados_storm.insert(4, 'CODIGO TABELA', '')
            dados_storm.insert(5, 'TABELA', '')
            dados_storm.insert(10, 'SITUACAO', 'PAGO')
            dados_storm.insert(14, 'FORMALIZACAO DIGITAL', 'SIM')
            dados_storm.columns = columns_to_rename
            # dados_storm.head()
            # dados_storm.PROPOSTA.head()

            dados_storm['PROPOSTA'] = dados_storm['PROPOSTA'].apply(lambda x: x[1:] if len(str(x)) > 12 else x)
            dados_storm['USUARIO BANCO'] = dados_storm['USUARIO BANCO'].apply(lambda x: x[1:])
            dados_storm['CODIGO TABELA'] = dados['CONVENIO'].map(self.load_json()['tables_code'])
            dados_storm['ORGAO'] = dados['CONVENIO'].map(self.load_json()['Orgao_code'])
            dados_storm['TIPO DE OPERACAO'] = dados['TIPO CONTRATO'].map(self.load_json()['Operations_code'])
            dados_storm.drop_duplicates(inplace =True)
            dados_storm.to_csv(path_to_save + f"/PRODUÇÃO CREFISA {self.date.day}-{self.date.month}-{self.date.year}.csv", sep = ';', index = False) 

    def comission_to_storm(self):
            columns_to_filter = ["NUMERO_ADE",
                                 'VALOR_BRUTO',
                                 'VLR_COMISSAO_REPASSE',
                                 'VLR_BONUS_REPASSE',
                                 'PRAZO',
                                 'DATA_DIGIT_BANCO'

                                 ]
            columns_to_rename = ['#ADE#',	
                                '#VALOR_BASE#',
                                '#VALOR_CMS#',
                                '#VALOR_BONUS#',	
                                '#PRAZO#',
                                '#DATA_DIGITACAO#',	
                                '#CODIGO_TABELA#',	
                                '#VALOR_BASE_BRUTO#']
            path_to_save = f'../Importados Storm/02 - COMISSÃO/{self.date.year}/{self.date.month}-{self.date.year}'
            os.makedirs(path_to_save, exist_ok = True)
            if self.process:
                dados = getattr(self, 'dados')
                dados_storm = dados[columns_to_filter]
                dados_storm['CODIGO TABELA'] = dados['CONVENIO'].map(self.load_json()['tables_code'])
                dados_storm['#VALOR_BASE_BRUTO#'] = dados_storm['VALOR_BRUTO']
                dados_storm[['NUMERO_ADE',	
                             'VALOR_BRUTO', 
                             'VLR_COMISSAO_REPASSE',	
                             'VLR_BONUS_REPASSE',	
                             'PRAZO',
                             'CODIGO TABELA', 
                             'DATA_DIGIT_BANCO', 
                             '#VALOR_BASE_BRUTO#']]
                dados_storm.columns = columns_to_rename
                dados_storm['#ADE#'] = dados_storm['#ADE#'].map(lambda x: str(x).replace("'", ""))
                dados_storm.drop_duplicates(inplace =True)
                setattr(self, 'comissao', dados_storm)
                dados_storm.to_csv(path_to_save + f"/COMISSÃO CREFISA {self.date.day}-{self.date.month}-{self.date.year}.csv", sep = ';', index = False)



    def zz(self):
        path_zz = f'../zz_geral_Crefisa_novo.xlsx'
        if self.process:
            producao = getattr(self, 'dados')
            comissao = getattr(self, 'comissao')
            if os.path.exists(path_zz):
                producao_zz = pd.read_excel(path_zz, sheet_name = 'Producao')
                comissao_zz = pd.read_excel(path_zz, sheet_name = 'Comissao')
                producao = pd.concat([producao, producao_zz])
                comissao = pd.concat([comissao , comissao_zz])
                producao.drop_duplicates(inplace= True)
                comissao.drop_duplicates(inplace= True)
            
            writer = pd.ExcelWriter(path_zz, engine='xlsxwriter')
            producao.to_excel(writer, sheet_name = 'Producao', index = False)
            comissao.to_excel(writer, sheet_name = 'Comissao', index = False)
            writer.close()



#Classe para pesquisar contratos pagos em ataso# classe para conferir a quantidade de contratos da mesma data
class contracts_conference():

    def __init__(self, date_work = datetime.date):
        self.process = False
        self.date= date_work 
        self.load_new_table()
        self.load_table()
        
        
    # Carrega os novos relatórios
    def load_new_table(self):
        path_new_reports =  f"./relatorios_novos/{self.date.year}/{self.date.month}"
        path_to_read = path_new_reports + f"/relatorio_pagamentos{self.date.day}_{self.date.month}_{self.date.year}.xls" 
        os.makedirs(path_new_reports, exist_ok = True)
        if os.path.exists(path_to_read):
            dados = pd.read_html(path_to_read, header = 0, thousands='.')
            dados_lidos = pd.DataFrame(dados[0])
            self.process = True
            setattr(self, 'dados_novos', dados_lidos)
    
    # Carrega os relatórios usados no storm
    def load_table(self):
        path_new_reports =  f"./relatorios/{self.date.year}/{self.date.month}"
        path_to_read = path_new_reports + f"/relatorio_{self.date.day}_{self.date.month}_{self.date.year}.xls" 
        if self.process:
            if os.path.exists(path_to_read):
                dados = pd.read_html(path_to_read, header = 0, thousands='.')
                dados_lidos = pd.DataFrame(dados[0])
                setattr(self, 'dados', dados_lidos)


    # Verifica se são as mesmas propostas
    def retorna_dimensao(self):
        path_to_save = f'../Pagamentos_atrasados/{self.date.year}/{self.date.month}'
        save_date = datetime.date.today() - datetime.timedelta(days = 1)
        path_to_save_file = path_to_save + f"/pagamento_atrasado_{save_date}.csv"
        os.makedirs(path_to_save, exist_ok = True)
        if self.process:
            dados_novos = getattr(self, 'dados_novos')
            dados = getattr(self, 'dados')
            propostas_novas = dados_novos.NUMERO_ADE.map(lambda x: x.replace("'", ""))
            propostas = dados.NUMERO_ADE.map(lambda x: x.replace("'", ""))
            result = list(set(propostas_novas) - set(propostas))
            dados_novos['NUMERO_ADE'] = dados_novos['NUMERO_ADE'].map(lambda x: x.replace("'", ""))
            filtrados = dados_novos[dados_novos['NUMERO_ADE'].isin(result)]
            print("Propostas pagas em atraso foram encontradas!")
            if os.path.exists(path_to_save_file):
                filtrados = pd.concat([filtrados, pd.read_csv(path_to_save_file)])
            filtrados.to_csv(path_to_save_file, index = False)
# lendo_dados = contracts_conference(date_work = datetime.date(2024, 3, 25)).retorna_dimensao()
    