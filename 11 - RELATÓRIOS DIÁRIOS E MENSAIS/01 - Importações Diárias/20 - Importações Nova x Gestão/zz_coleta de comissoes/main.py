import datetime
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
# import my classes

from modules import get_tables, openBrowserNova, workTablesToStorm
from task_modules import create_task


class main():
    
    def __init__(self):
        self.datawork =  date.today() - timedelta(days=30)
        self.execute_classes()
        
    def execute_classes(self):
        try:
            
            get_tables(openBrowserNova().driver, self.datawork)
            date = self.datawork
            while date <  date.today():
                print("Iniciando processamento do dados para a data: ", date)
                workTablesToStorm(date)
                date = date + timedelta(days = 1)    
                print("Processamento dos dados para a data: ", date, " finalizado!")
        except Exception as exc:
            # create_task("Nova - Erro ao executar o script de download e envio de relatórios", str(exc))
            print("Error in main.py")
            raise(exc)



if __name__ == "__main__":
    main()
    os.system("cls")
    print("Process complet!")
    