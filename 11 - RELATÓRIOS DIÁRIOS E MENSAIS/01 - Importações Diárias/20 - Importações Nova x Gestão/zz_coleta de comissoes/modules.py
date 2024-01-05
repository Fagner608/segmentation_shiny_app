import requests
import pandas as pd
import os
import json
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver import Keys, ActionChains
import calendar
from re import search
import pandas.io.common



   

class openBrowserNova():
    
    def __init__(self, user_credencials: dict = dotenv_values("./data/.env")) -> WebDriver:
        
        self.user_credencials_login = user_credencials['LOGIN_USER']
        self.user_credencials_password = user_credencials['LOGIN_PASSWORD']
        self.mkDirDownload = self.__mkDirDownload()
        self.driver = self.__loguinSendKeys()
        
        
    
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
        
        
    def __loguinSendKeys(self):
        driver = self.__initialize_driver()
        
        driver.get("https://sistema.novafinanceira.com/consignado/CorretorExterno/inicio")
        
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Olá, MAIS AGIL FRANQUIAS S/A!']")))
            return driver
    
        except TimeoutException as exc:
                print("Logando no sistema.")
                WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID, "usuario")))
                    
                driver.find_element(By.ID, "usuario").send_keys(self.user_credencials_login)
                    
                driver.find_element(By.ID, "senha").send_keys(self.user_credencials_password)
                    
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "logar"))).click()
                    
                    # try:
                    #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located(By.XPATH, "//div[text() = 'Usuário ou senha invalidos']"))
                    # except:
                    #     pass
                    # try:
                    #     WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()='Pendências']")))
                    # except:
                    #     os.system("cls")
                    #     print("Erro ao carregar a página logada.")
                    
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Olá, MAIS AGIL FRANQUIAS S/A!']")))
                os.system("cls")
                print("Sistema logado")
                return driver
        except Exception as exc:
            raise exc
        
class get_tables():
    
    def __init__(self,driver: WebDriver, date: date):
        self.driver = driver
        self.date = date
        self.select_dates()
        self.download_reports()
    
    def select_dates(self):
        driver = self.driver
        WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'st-icon bi bi-currency-dollar')]"))).click()
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Exportação de Comissão') and .//i[@class='bi bi-file-arrow-down-fill']]"))).click()
        WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]"))).click()
        WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
        except TimeoutException as exc:
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]"))).click()
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
        except TimeoutException:
            pass    
        driver.find_element(By.ID, 'contra_senha').send_keys('nova')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'btn-yes'))).click()
        self.driver = driver
        
        
        
    def download_reports(self):
            date = self.date
            today = date.today()
            datework = date
            driver = self.driver
            while datework < today:
                for input_camp in ['data_inicio', 'data_fim']:
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_inicio')]")))
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_fim')]")))    
                    for _ in range(0, 10):
                        try:
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                        except NoSuchElementException:
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                    driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(datetime.strftime(datework, "%d/%m/%Y"))
                
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ed-download-arquivo-contratos-digitados"))).click()
                
                datework = datework + timedelta(days=1)
            driver.close()
    
    
# classe para importar tabelas para o storm
    ## está tudo certo, só preciso ver porque as fuções mazzpaths e makeTempPaths estão zerando os arquivos
class workTablesToStorm():
    
    def __init__(self, datework: date):
        self.storm = False
        self.datework = datework
        self.istable()
        self.toStorm()
        self.save()
        self.makezzpaths()
        self.makeTempPaths()
        self.concatZZ()
    
    def istable(self):
        '''
        Função que libera as demais, se o arquivo com a data for encontrado.
        Define o arquivo encontrado como atributo "dados"
        '''
        path = f'./download/'
        listdir = os.listdir(path)
        for dir in listdir:
            if search(str(self.datework), dir):
                if os.path.getsize(path + dir) > 0:
                    dados = pd.read_csv(path + dir,
                            delimiter=";",
                            encoding="ISO-8859-1", decimal=".")
                    setattr(self, 'dados', dados)
                    self.storm = True
                
                            
    def toStorm(self):
        '''
        Se o arquivo for encontrado, os relatórios para o storm serão gerados.
        Os atributos banks e columns serão definidos
        '''
        
        if self.storm:
            dados = self.dados
            banks = dados.NOM_BANCO.unique()
            columns = dados.columns
            setattr(self, 'banks', banks)
            setattr(self, 'columns', columns)
            dados = dados[['NOM_BANCO', 'NUM_PROPOSTA', 'VAL_BASE_COMISSAO', 'VAL_COMISSAO_TOTAL', 'QTD_PARCELA', 'DAT_EMPRESTIMO']]
            dados.insert(4, "#VALOR_BASE_BRUTO#", dados['VAL_BASE_COMISSAO'])
            dados.columns = ['NOM_BANCO', '#ADE#', '#VALOR_BASE#', '#VALOR_CMS#', '#PRAZO#', '#VALOR_BASE_BRUTO#', '#DATA_DIGITACAO#']
            for bank in banks:
                path_to_save = f'../Importados_storm/Comissao/{self.datework.year}/{self.datework.month}/{bank}'
                os.makedirs(path_to_save, exist_ok=True)
                report = dados[dados.NOM_BANCO == bank]
                report.to_excel(excel_writer = path_to_save + f'/Comissao_{self.datework.strftime("%d-%m-%Y")}.xlsx', index = False)
                
    def save(self):
        '''
        Depois de encontrar o arquivo, definir os atributos, está função aplica filtro por banco.
        Salva um atributo de DF com o nome do banco
        '''
        if self.storm:
            dados = self.dados
            banks = self.banks
            for bank in banks:
                dados = dados[dados.NOM_BANCO == bank]
                setattr(self, f'{bank}', dados)
                
    
    def makezzpaths(self):
        '''
        Função para criar zz_geral para cada banco, uma única vez.
        '''
        if self.storm:
            for bank in self.banks: 
                path = f'zz_geral_{bank}.xlsx'
                if path not in os.listdir("../"):
                        zz = pd.DataFrame(columns=self.columns)
                        zz.to_excel("../"+path, index=False, sheet_name = f'Producao_ate{self.datework.strftime("%Y-%m-%d")}')
                        
        
                        
    def makeTempPaths(self):
        '''
        Função faz uma cópia do zz_geral para o tmp
        '''
        if self.storm:
            os.makedirs("tmp", exist_ok=True)
            for bank in self.banks: 
                path = f'../zz_geral_{bank}.xlsx'
                tempPath = f'tmp/zz_geral_{bank}_temp.xlsx'
                shutil.copy(path, tempPath)
                
                
    def concatZZ(self):
        '''
        função lê o arquivo temporáriio, captura os dados filtrados pelo NOM_BANK da função save
        se tiver arquivo para a data, depois de ser copiado para o temp
        - lê o temp
        - filtra por data
        - concatena novos dados do banco
        - sobscreve o temp com os novos dados
        - faz o novo zz geral
        
        '''
        
        if self.storm:
            dados = self.dados
            
            for bank in self.banks:
                
                zzpath = pd.read_excel(f'tmp/zz_geral_{bank}_temp.xlsx')
                if self.datework not in zzpath['DAT_EMPRESTIMO']:
                    dados_to_save = dados[dados.NOM_BANCO == bank]
                    concatenado = pd.concat([zzpath, dados_to_save])
                    concatenado.drop_duplicates(inplace=True)
                    concatenado.to_excel(excel_writer = f'tmp/zx_geral_{bank}_temp.xlsx', 
                                        index = False, 
                                        sheet_name = f'Producao_ate{self.datework.strftime("%Y-%m-%d")}')
                    shutil.move(f'tmp/zx_geral_{bank}_temp.xlsx', f'../zz_geral_{bank}.xlsx')
                
                