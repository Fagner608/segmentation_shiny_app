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

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import Keys, ActionChains

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
            calendario = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)')))
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

    def __download_integradas(self):

        driver = self.acess_integradas()
        
        date_work = self.date

        while date_work < date.today():
            
            path_to_save = f"./Integradas/{date_work.year}/{date_work.month}"
            if not os.path.exists(f'{path_to_save}/relatorio_{date_work.day}_{date_work.month}_{date_work.year}.xlsx'):
                print(f'{path_to_save}/relatorio_{date_work.day}_{date_work.month}_{date_work.year}.xlsx')

                self.__scroll(driver)

                if self.__calendar_manipulate(date_work = date_work, driver = driver):
                    
                    while not os.path.exists(f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx"):
                        print("path ",f"{path_to_save}/relatorio_{'{:02d}'.format(date_work.day)}_{date_work.month}_{date_work.year}.xlsx" )
                        self.__move(date_work)
                sleep(3)
                driver.refresh()

            else:
                print("Data já baixada: ", date_work)
            date_work = date_work + timedelta(days = 1)
        driver.close()

            


## Conciliação
    # classe para retornar dados conciliados
# classe para retornar dados conciliados
class conciliation():
    
    def __init__(self, datework: date):
        self.load_ZZ = False
        self.load = False
        self.intersect = False
        self.datework = datework
        self.bank = 'BANCO MERCANTIL DO BRASIL'
        self.loadzz()
        self._jsonLoad()
        self.concilation()
        self.save()
        


    # métdo para carregar propostas no zz, e, escrever no json
            # se o arquivo já existir, ele incrementa o json
    def loadzz(self):
        '''
        Função para carregar os dados do banco, casa haja dados para a data trabalhada.
        '''
        path = "../"
        date_start = self.datework - timedelta(days = 4)
        for zz in listdir(path):
            if search(self.bank, zz):
                dados = pd.read_excel(path + zz)
                data = self.datework.strftime("%d/%m/%Y")
                
                
                # if data in dados['DAT_CREDITO'].to_list():
                if data in dados['DAT_CREDITO'].to_list():
                
                    dados = dados[dados.DAT_CREDITO == data]
                    # dados = dados[(dados.DAT_CREDITO >= date_start) & (dados.DAT_CREDITO >= data)]
                    
                    propostas = dados['NUM_PROPOSTA'].to_list()
                    #escrever o arquiivo, e ler em outro método

                    try:
                        with open("./conciliando.json", mode = 'r') as fp:
                            dados_lidos = json.load(fp)
                            # propostas.append(dados_lidos['propostas']) 
                            propostas.extend(dados_lidos['propostas']) 
                            
                    except FileNotFoundError:
                        pass

                    to_save = {"propostas": propostas}
                    try:
                        with open("./conciliando.json", mode = 'w') as fp:
                            json.dump(to_save, fp)
                    except:
                        print("Erro ao escrever .json")
                    self.load_ZZ = True
                        
                else:
                    print("Data não encontrada no ZZ: ", self.datework)
                break

    #método lê json
    def _jsonLoad(self):
            if self.load_ZZ:
                with open("./conciliando.json", mode = 'r') as fp:
                    # for line in fp:
                    dados_lidos = json.load(fp)
                propostas = dados_lidos['propostas']
                setattr(self, 'propostas', propostas)
                self.load = True
        


    # carrega relatório do marcantil, baixado
    def loadMercantil(self, date: date):
        '''
        função para carregar os dados do mercantil, casa haja dados para a data trabalhada.
        '''

        if self.load:
            # path_to_read = f"./Integradas/{self.datework.year}/{self.datework.month}/relatorio_{self.datework.strftime('%d')}_{self.datework.month}_{self.datework.year}.xlsx"
            date_search = date - timedelta(days = 10)
            dados_mercantil = pd.DataFrame()
            while date_search <= date:
                path_to_read = f"./Integradas/{date_search.year}/{date_search.month}/relatorio_{date_search.strftime('%d')}_{date_search.month}_{date_search.year}.xlsx"
                
                if os.path.exists(path_to_read):
                    
                    data_read = pd.read_excel(path_to_read, parse_dates=['DataCadastro'])

                    dados_mercantil = pd.concat([dados_mercantil, data_read])
                    
                else:
                    None   

                date_search = date_search + timedelta(days = 1)        
            if dados_mercantil.shape[0] > 0:
                return dados_mercantil
            else:
                print(f"Data não encontrado nos relatórios")
                return None
        

    def concilation(self):
        '''
        função para conciliar os dados do banco com os dados do mercantil.
        '''

        if self.load:
            # recebe as propoasta do json
            propostas = getattr(self, 'propostas')
            # define a data pesquisada no loop
            datework = self.datework
            #define data limite para pequisa nos arquivos de propostas baixadas
            dateLimit = datework - timedelta(days = 20)

            dados_mercantil = None
            
            
            while datework > dateLimit:
                #carrega os dados do mercantil, para data pesquisada
                dados_mercantil = self.loadMercantil(date = datework)
                
                # if dados_mercantil is not None: break
                
                
                
                if dados_mercantil is not None:
                    # captura propstas dos dados do mercantil
                    conciliado = set(dados_mercantil['NumeroProposta'])

                    # capotura interseção das propostas
                    instersection = set(propostas).intersection(conciliado)
                    # nem todas as propostas são conciliadas no mesmo dia
                        # pensar em uma soluição para pesquisar todas as propostas d+0, d-1 e d-2 que não foram concilkioadaconciliadas
                        # solução: 1 -  criar uma variável no zz para marcar concilkiadas e não conciliadas
                        #          2 - ao informar a data  de pesquisa, pedar dados d-3 a d-1 - obs: os mesmos dados aparecem em todos os relatorios
                    #              3 - fazer um arquivo comente com as propostas a setem conciliadas - atualizar este arquivo
                    
            
                    if len(instersection) != 0:
                         
                        print("Interseção encontrada!")
                        
                        dados_mercantil = dados_mercantil[dados_mercantil.NumeroProposta.isin(instersection)]
                        
                        dados_mercantil = dados_mercantil.drop_duplicates(subset=['NumeroProposta'])
                        self.intersect = True

                        setattr(self, 'intersetction', dados_mercantil)
                        
                        resisuo = set(propostas) - instersection

                        resisuo = {'propostas': list(resisuo)}
                        #subcreve arquivo somente com propostas não encontradas
                        with open("./conciliando.json", 'w') as fp:
                            json.dump(resisuo, fp)
                        break
                    else:
                        print("Interseção zerada!")

                datework -= timedelta(days = 1)
            else:
                print("Dados do dia: ", self.datework, " não encontrado nos downloads.")
 
    def save(self):

        if self.intersect:
            print("Salvando dados")
            makedirs('conciliados', exist_ok=True)
            path = "./conciliados/"
            makedirs(path + f"/{self.datework.year}/{self.datework.month}", exist_ok= True)
            path_to_save = path + f"/{self.datework.year}/{self.datework.month}"
            dados_to_save = getattr(self, 'intersetction')
            dados_to_save.to_excel(excel_writer = path_to_save + f'/Conciliado_{self.datework.strftime("%d-%m-%Y")}.xlsx', index = False)
            print("Process complit!")


class work_tables():

    def __init__(self, date_work: datetime.date):
        self.work_tables = False
        self.date = date_work
        self.read_reports()
        self.comission_to_storm()
        self.production_reports()
        self.zz()


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
            comission_storm['comissao'] = [round((float(x) * 1.80 / 100), 2) for  x in dados['ValorEmprestimo']]
            comission_storm['#VALOR_BASE_BRUTO#'] = dados['ValorEmprestimo']
            comission_storm['QuantidadeParcelas']  = comission_storm['QuantidadeParcelas'] * 12
            comission_storm['DataCadastro'] = comission_storm['DataCadastro'].apply(lambda x: x.split(" ")[0])
            comission_storm = comission_storm[['NumeroProposta', 'ValorEmprestimo', 	'#VALOR_BASE_BRUTO#', 	'comissao', 	'QuantidadeParcelas', 	'CodigoProduto', 	'DataCadastro']]
            comission_storm.columns = columns_to_rename
            comission_storm['#VALOR_BASE#'] = comission_storm['#VALOR_BASE#'].apply(lambda x: str(x).replace(".", ","))
            comission_storm['#VALOR_BASE_BRUTO#'] = comission_storm['#VALOR_BASE_BRUTO#'].apply(lambda x: str(x).replace(".", ","))
            comission_storm.to_excel(path_to_save + f"/Comissao_{self.date}.xlsx", index = False)
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
            
            production['NUMERO PARCELAS'] = production['NUMERO PARCELAS'] * 12
            production['VALOR PARCELAS'] = ""
            production['VALOR QUITAR'] = ""
            production['ORGAO'] = "FGTS"
            production['TIPO DE OPERACAO'] = "MARGEM LIVRE (NOVO)"


            production.to_excel(path_to_save + f"/Producao_{self.date}.xlsx", index = False ) 
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