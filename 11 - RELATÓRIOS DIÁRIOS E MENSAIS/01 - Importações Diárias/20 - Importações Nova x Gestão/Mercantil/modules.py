import requests
import pandas as pd
import json
import datetime

from datetime import datetime
from datetime import timedelta
from datetime import date
from time import strptime

from pathlib import Path
import shutil
import time
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from re import search
from tqdm import tqdm
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import Keys, ActionChains
import sys
import calendar
from re import search
import pandas.io.common
import locale

import os
import pickle
from requests.cookies import RequestsCookieJar

from datetime import datetime, date
from datetime import timedelta
from datetime import time
from time import sleep
import os
from os import listdir, makedirs
from re import search
import warnings
warnings.filterwarnings("ignore")






## downloads reports method
class openBrowser():
    
    def __init__(self, user_credencials: dict = dotenv_values("./data/.env")):
        
        self.user_credencials_login = user_credencials['LOGIN_USER']
        self.user_credencials_password = user_credencials['LOGIN_PASSWORD']
        self.__mkDirDownload()
        
        
        
   

    def __mkDirDownload(self) -> None:
        os.makedirs("download", exist_ok=True)
        for file in os.listdir('download'):
            os.remove(f"download\\{file}")
            
    def __initialize_driver(self):
        
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", fr"{str(Path().absolute())}\\download")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        driver = webdriver.Firefox(options=options)
        
        
        driver.maximize_window()
        return driver
    

    def loguinSendKeys(self):
        driver = self.__initialize_driver()
        


       
        driver.get("https://meumb.mercantil.com.br/propostas")
       
        try:
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,200 ).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='mat-input-0']"))).send_keys(self.user_credencials_login)
            WebDriverWait(driver,200 ).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='mat-input-1']"))).send_keys(self.user_credencials_password)
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='reCAPTCHA']")))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()

            input("Prenchar o captcha, Pressione 'ENTRAR', após, pressione qualquer tecla")
            
            mainWin = driver.current_window_handle
            driver.switch_to.window(mainWin)

            
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'X409847')]")))
            
            return driver

        except TimeoutException as exc:
                raise exc

class downaload_reports():


    def __init__(self, driver: webdriver, date: date):
        self.driver = driver
        self.date = date
        self.__download_integradas()

    def __scroll(self, driver: WebDriver):
        
        driver.execute_script("window.scrollBy(0, 3000)")
        sleep(1)
        driver.execute_script("window.scrollBy(3000, 0)")

    def acess_integradas(self):
        driver = self.driver

        driver.get('https://meumb.mercantil.com.br/propostas')
        
        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
        try:
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()
        except ElementClickInterceptedException:
            driver.refresh()
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()

        return driver
    

    
    def __move(self, date_move: datetime.date):
        
        date_work = date_move
        print("Movendo arquivo do dia: ", date_work)
        file_search = 'download/'
        
        path_to_save = f"./Integradas/{date_work.year}/{date_work.month}"
        
        os.makedirs(path_to_save, exist_ok = True)
        
        while not os.path.exists(file_search + "relatorio.xlsx") and not os.path.exists(file_search + "relatorio(1).xlsx"):
            sleep(1)
            print("Aguardando arquivo")

        if os.path.exists(file_search + "relatorio(1).xlsx"):
            while os.path.getsize(file_search + "relatorio(1).xlsx") == 0:
                continue
            shutil.move(file_search + f"relatorio(1).xlsx", f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx")
        else:
            while os.path.getsize(file_search + "relatorio.xlsx") == 0:
                continue
            shutil.move(file_search + f"relatorio.xlsx", f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx")

        if os.listdir(file_search) != 0:
            for path in os.listdir(file_search):
                os.remove(file_search + path)

        dados = pd.read_excel(f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx")
        dados.DataCadastro = dados['DataCadastro'].apply(lambda x: x.split(" ")[0])
        print(f"{'{:02d}'.format(date_work.day)}/{'{:02d}'.format(date_work.month)}/{date_work.year}")
        dados = dados[dados.DataCadastro == f"{'{:02d}'.format(date_work.day)}/{'{:02d}'.format(date_work.month)}/{date_work.year}"]
        dados.to_excel(f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx", index = False)


    def __calendar_manipulate(self, date_work: date, driver: WebDriver):
        locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
        WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
        try:
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ngx-pagination")))
        except ElementClickInterceptedException:
            driver.refresh()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ngx-pagination")))

        calendar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#mat-date-range-input-0')))
        driver.execute_script("arguments[0].click();", calendar)
        date_1 = date_work
        date_2 = date_1 + timedelta(days = 1)
        if date_1.strftime("%b %Y").upper() == driver.find_element(By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)').text :
        
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            
            for i in result:
                if i.text == '{:d}'.format(date_1.day):
                    driver.execute_script("arguments[0].click();", i)
                    break
        else:
            calendario = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)')))
            driver.execute_script("arguments[0].click();", calendario)
            result = driver.find_elements(By.CSS_SELECTOR, ".mat-calendar-body > tr")
            
            for i in result:
                datas = i.find_elements(By.CSS_SELECTOR, 'td')
                datas = i.find_elements(By.TAG_NAME, 'td')
                click = False
                for j in datas:
                    sleep(.50)
                    if j.text == str(date_1.strftime("%Y")):
                        driver.execute_script("arguments[0].click();", j)
                        click = True
                        break
                if click:
                    break
                
                        
            resulta_month = driver.find_elements(By.CLASS_NAME, "mat-calendar-body")
            for month in resulta_month:
                result_month = month.find_elements(By.TAG_NAME, 'td')
                click = False
                for i in result_month:
                    if search(date_1.strftime("%b").upper(), i.text):
                        driver.execute_script("arguments[0].click();", i)
                        click = True
                        break
                if click:
                    break
            # iteração nos dias
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')))    
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')

            for i in result:
                if i.text == '{:d}'.format(date_1.day):
                    driver.execute_script("arguments[0].click();", i)
                    break



        sleep(2)
        if date_2.strftime("%b %Y").upper() == driver.find_element(By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)').text :
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            for i in result:
                if date_2 == date.today():
                    today = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-calendar-body-today')))
                    driver.execute_script('arguments[0].click();', today)
                    break
                else:
                    if i.text == '{:d}'.format(date_2.day):
                        driver.execute_script("arguments[0].click();", i)
                        break
        
        else:
            
            button_pass = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.mat-focus-indicator:nth-child(4)")))
            driver.execute_script("arguments[0].click();", button_pass)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')))
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            for i in result:
                if i.text == '{:d}'.format(date_2.day):
                    sleep(.50)
                    driver.execute_script("arguments[0].click();", i)
                    break

        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Sem dados')]")))
            date_work += timedelta(days = 1)
            print("Sem dados para a datra: ", date_work)
            return False
        except TimeoutException:
            exportar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Exportar')]")))
            driver.execute_script("arguments[0].click();", exportar)
            xlsx_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mat-menu-item')))
            driver.execute_script("arguments[0].click();", xlsx_button)
            return True


    def inter_download_reports(self, date_work: date, driver: WebDriver):

        while date_work < date.today():
            
            path_to_save = f"./Integradas/{date_work.year}/{date_work.month}"
            if not os.path.exists(f'{path_to_save}/relatorio_{date_work.day}_{date_work.month}_{date_work.year}.xlsx'):
                print(f'{path_to_save}/relatorio_{date_work.day}_{date_work.month}_{date_work.year}.xlsx')

                self.__scroll(driver)

                if self.__calendar_manipulate(date_work = date_work, driver = driver):
                    
                    while not os.path.exists(f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx"):
                        
                        self.__move(date_work)
                sleep(3)
                driver.refresh()

            else:
                print("Data já baixada: ", date_work)
            date_work = date_work + timedelta(days = 1)

    def inter_download_concilaition_tmp(self, date_work: date, driver: WebDriver):

            path_to_save = f"./tmp/report_tmp_conciliation_{date_work.year}/{date_work.month}"
            self.__scroll(driver)
            if self.__calendar_manipulate(date_work = date_work, driver = driver):
                while not os.path.exists(f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx"):
                    self.__move(date_work)
            sleep(3)
            driver.refresh()

            
    def __download_integradas(self):

        driver = self.acess_integradas()
        date_work = self.date
        self.inter_download_reports(date_work=date_work, driver=driver)
        driver.close()

    def _download_concoliation_report_tmp(self):

        driver = self.acess_integradas()
        date_work = self.date
        self.inter_download_reports(date_work=date_work, driver=driver)
        driver.close()


            


## Conciliação
    # classe para retornar dados conciliados

# Falhas na classe conciliation
class conciliation():
    
    def __init__(self, datework: date):
        self.start_app = False
        self.load_mc = False
        self.load = False
        self.difference = False
        # A data de referência é de d-2
        self.datework = datework - timedelta(days = 10)
        self.bank = 'BANCO MERCANTIL DO BRASIL'
        self.path = f"./comissoes_nao_pagas/{self.datework.year}/{self.datework.month}/{self.datework.day}"  
        self.concilation()
        self.search_payment(date=self.datework)
        self.__mkdir()
         

    def start_app(self):
        if os.path.exists(self.path):
            pass
        else:
            self.start_app = True

    def __mkdir(self):
        os.makedirs(self.path, exist_ok = True)


    def loadzz(self):
        '''
        Função para carregar os dados da nova d-n.
        '''
        if self.start_app:
            path = "../"
            for zz in listdir(path):
                if search(self.bank, zz):
                    dados = pd.read_excel(path + zz, parse_dates=['DAT_CREDITO'])
                    range_date = pd.date_range(start = self.datework - timedelta(days = 50),
                                            end = date.today())

                    if dados['DAT_CREDITO'].isin(range_date).any():
                        
                        dados = dados[dados['DAT_CREDITO'].isin(range_date)]
                        

                        return dados
                            
                    else:
                        print("Data não encontrada no ZZ: ", self.datework)
                        return

 
    def loadMercantil(self):
        '''
        função para carregar os dados de novos pagamentos do mercantil (do próprio banco) em D-, este é o atraso tolerado
        '''
        if self.start_app:
            date_search = self.datework
            path_to_read = f"./Integradas/{date_search.year}/{date_search.month}/relatorio_{date_search.strftime('%d')}_{date_search.month}_{date_search.year}.xlsx"
            if os.path.exists(path_to_read):
                dados_mercantil = pd.read_excel(path_to_read, parse_dates=['DataCadastro'])
                # vai salvar as propostas pagas pelo mercantil
                return dados_mercantil
            else:
                None   
                        

    def concilation(self):
        '''
        Método receve os dados de d-3 do Mewrcantil, e D-n da Nova, para conciliar o primeiro no segundo. 
        '''
        # se houverem dados no json
        if self.start_app:
            propostas_mercantil = self.loadMercantil()
            propostas_nova = self.loadzz()
            
            if propostas_nova is not None and propostas_mercantil is not None:
                    diffferemce_proposal = propostas_mercantil[~propostas_mercantil['NumeroProposta'].isin(propostas_nova['NUM_PROPOSTA'])]
                    if not diffferemce_proposal.empty:
                        print("Propostas não pagas encontradas.")
                        print(diffferemce_proposal.tail())
                        diffferemce_proposal.to_csv(self.path + f"/nao_pagas_{self.datework}.csv", index=False)
                        #subcreve arquivo somente com propostas não encontradas
                    

    def search_payment(self, date: date):

        path = f"./comissoes_nao_pagas/{date.year}/{date.month}/"
        paths = tqdm(os.listdir(path))
        for char in paths:
            sleep(0.25)
            paths.set_description("Processing dia %s/%s " % (char, date.month))
            diretorio = path + char
            if len(os.listdir(diretorio)) > 0: 
                    os.system('cls')
                    raise Exception(
                        '''
                        #####################################################################################################################################################################################

                        ATENÇÂO! Pagamentos em atraso encontrados no diretório: %s, Avalie a proposta, e, após resolver o problema, exclua o arquivo da pasta e execute o programa novamente.
                        
                        #####################################################################################################################################################################################

                                                '''% diretorio)


class work_tables():

    def __init__(self, date_work: datetime.date):
        self.work_tables = False
        self.date = date_work
        self.read_reports()
        self.comission_to_storm()
        self.production_reports()
        # self.zz()


    def read_reports(self):
        path_to_read = f"./Integradas/{self.date.year}/{self.date.month}/relatorio_{self.date.strftime('%d')}_{self.date.month}_{self.date.year}.xlsx"
        if os.path.exists(path_to_read):
            dados = pd.read_excel(path_to_read)
            return dados
        else:
            return


    def comission_to_storm(self):
        dados = self.read_reports()
        path_to_save = f"./Importados_storm/Comissao/{self.date.year}/{self.date.month}/BANCO MERCANTIL DO BRASIL"
        if dados is not None:
            os.makedirs(path_to_save, exist_ok= True)
            columns_to_rename = ['#ADE#',	'#VALOR_BASE#',	'#VALOR_BASE_BRUTO#',	'#VALOR_CMS#',	'#PRAZO#',	'#CODIGO_TABELA#',	'#DATA_DIGITACAO#']
            dados['ValorEmprestimo'] = dados['ValorEmprestimo'].apply(lambda x:  x.replace(".", "").replace(",", "."))
            comission_storm = dados[['NumeroProposta', 'ValorEmprestimo',  'QuantidadeParcelas', 'CodigoProduto', 'DataCadastro']]
            
            dados['ValorEmprestimo'] = dados['ValorEmprestimo'].astype(dtype = float)
            comission_storm['comissao'] = dados['ValorEmprestimo']
            
            comission_storm['#VALOR_BASE_BRUTO#'] = dados['ValorEmprestimo']
            comission_storm['DataCadastro'] = comission_storm['DataCadastro'].apply(lambda x: x.split(" ")[0])
            comission_storm = comission_storm[['NumeroProposta', 'ValorEmprestimo', 	'#VALOR_BASE_BRUTO#', 	'comissao', 	'QuantidadeParcelas', 	'CodigoProduto', 	'DataCadastro']]
            comission_storm['comissao'] = [(round(x * 16.50 / 100, 2) if j in [13728077, 13728127, 13728128]  else round(x * 6 / 100, 2)) for x, j in zip(comission_storm['comissao'], comission_storm['CodigoProduto'])]
            # comission_storm['comissao'] = [(round(x * 15 / 100, 2) if j == 13728077  else round(x * 6 / 100, 2)) for x, j in zip(comission_storm['comissao'], comission_storm['CodigoProduto'])]
            print(comission_storm['comissao'])
            
            comission_storm.columns = columns_to_rename
            comission_storm['#VALOR_BASE#'] = comission_storm['#VALOR_BASE#'].apply(lambda x: str(x).replace(".", ","))
            comission_storm['#VALOR_BASE_BRUTO#'] = comission_storm['#VALOR_BASE_BRUTO#'].apply(lambda x: str(x).replace(".", ","))
            comission_storm['#VALOR_CMS#'] = comission_storm['#VALOR_CMS#'].apply(lambda x: str(x).replace(".", ","))
            
            comission_storm.to_csv(path_to_save + f"/Comissao_{self.date}.csv", index = False, sep = ';')
            setattr(self, 'comission_storm', comission_storm)



    def production_reports(self):
        dados = self.read_reports()
        path_to_save = f"./Importados_storm/Producao/{self.date.year}/{self.date.month}/BANCO MERCANTIL DO BRASIL"
        os.makedirs(path_to_save, exist_ok = True)
        if dados is not None:
            production = dados[['NumeroProposta',
                                'DataCadastro',
                                'QuantidadeParcelas',
                                'ValorEmprestimo',
                                'Cpf',
                                'Nome',
                                'ValorFinanciado',
                                
                                'CodigoConvenio',
                                'CodigoProduto',
                                
                                
                                'ValorFinanciado',
                                'ValorEmprestimo',
                                'DataPagamentoCliente',
                                'UsuarioDigitador'

                             ]]

            production['banco'] = "BANCO MERCANTIL DO BRASIL"
            production['tipo de operacao'] = "FGTS"
            production['situacao'] = "PAGO"
            production['formalizacao digital'] = "SIM"
            
            production = production [['NumeroProposta',  
                                    'DataCadastro',
                                    'banco',
                                    'CodigoConvenio',
                                    'CodigoProduto',
                                    'tipo de operacao',
                                    'QuantidadeParcelas',
                                        
                                    'ValorFinanciado',
                                    'ValorEmprestimo',
                                
                                    'UsuarioDigitador',
                                    'situacao',
                                    'DataPagamentoCliente',
                                    'Cpf',
                                    'Nome',
                                    'formalizacao digital'
                                    
                                ]]  
            
    
            
            production.columns =   ['PROPOSTA',	
                                    'DATA CADASTRO',
                                    'BANCO',
                                    'ORGAO',
                                    'CODIGO TABELA',
                                    'TIPO DE OPERACAO',	
                                    'NUMERO PARCELAS',
                                    'VALOR PARCELAS',
                                    'VALOR OPERACAO',	
                                    'VALOR LIBERADO',	
                                    'VALOR QUITAR'	,
                                    'USUARIO BANCO'	,
                                    'SITUACAO',
                                    'DATA DE PAGAMENTO',	
                                    'CPF'	,
                                    'NOME'	,
                                    'FORMALIZACAO DIGITAL'
                                    ]
            
            # production['NUMERO PARCELAS'] = production['NUMERO PARCELAS'] * 12
            production['VALOR PARCELAS'] = ""
            production['VALOR QUITAR'] = ""
            production['ORGAO'] = "FGTS"
            production['TIPO DE OPERACAO'] = "MARGEM LIVRE (NOVO)"

            production.to_csv(path_to_save + f"/Producao_{self.date}.csv", index = False , sep = ';') 
            setattr(self, 'production_storm', production)
            self.work_tables = True


    def zz(self):
        if self.work_tables:
            comission_storm = getattr(self, 'comission_storm')
            production_storm = getattr(self, 'production_storm')
            production_storm.insert(0, 'data_processamento', self.date)    
            comission_storm.insert(0, 'data_processamento', self.date)    
            if os.path.exists("zz_geral_MERCANTIL.xlsx"):
                comission_storm = pd.concat([comission_storm, pd.read_excel("zz_geral_MERCANTIL.xlsx", sheet_name = 'comissao')])
                production_storm = pd.concat([pd.read_excel("zz_geral_MERCANTIL.xlsx", sheet_name = 'producao'), production_storm])
                

            writer = pd.ExcelWriter('zz_geral_MERCANTIL.xlsx', engine = 'xlsxwriter')
            comission_storm.to_excel(writer, sheet_name = 'comissao', index = False)
            production_storm.to_excel(writer, sheet_name = 'producao', index = False)
            writer.close()
            print("Complet!")