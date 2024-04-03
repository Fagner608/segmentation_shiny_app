import pandas as pd
import datetime
import os
import re

# classe para conciliar contratos



class conciliation_contracts():

    def __init__(self, date_work: datetime.date):
        self.date_work = date_work
        self.path_to_read = f"../Comissão/{date_work.year}/{'{:02d}'.format(date_work.month)}-{date_work.year}/"
        self.conciliation()



    # metodo para ler arquivo de comissao consolidada
    def __read_consolidate_comission(self):
        files  = os.listdir(self.path_to_read)
        consolidate_comission = pd.DataFrame()
        for file in files:
            consolidate_comission = pd.concat([consolidate_comission, pd.read_excel(self.path_to_read + file, sheet_name=1, header=0)])
        return consolidate_comission


    # metdo para ler arquivos de pagamentos antecipados
    def __read_comission_antecipated(self):
        current_monh = date_work.month
        last_month = current_monh -  1
        months = [current_monh, last_month]
        reports_antecipated = pd.DataFrame()
        for month in months:
            path_to_read_tables = f"../Importados Storm/02 - COMISSÃO/{self.date_work.year}/{month}-{self.date_work.year}/"
            for file in os.listdir(path_to_read_tables):
                if not re.search(r'Copia|Cópia|copia|cópia', file):
                    new_data = pd.read_csv(path_to_read_tables + file, sep  =';')
                    new_data['meta_data'] = file
                    reports_antecipated = pd.concat([reports_antecipated, new_data])
        return reports_antecipated

    # metodo para conferir comissoes
    def conciliation(self):
        path_to_save_no_paymet_comission = f'../Comissoes_nao_pagas/{self.date_work.year}/{self.date_work.month}/'
        os.makedirs(path_to_save_no_paymet_comission, exist_ok=True)
        consolidate = self.__read_consolidate_comission()
        antecipated = self.__read_comission_antecipated()
        if not consolidate.empty and not antecipated.empty:
            antecipated.drop_duplicates(inplace=True)
            antecipated[antecipated['#ADE#'].duplicated(keep=False)].sort_values('#ADE#')
            antecipated[antecipated['#ADE#'].isin(consolidate['Nº PROP/ADE'])]
            not_payment_comission = consolidate[~consolidate['Nº PROP/ADE'].isin(antecipated['#ADE#'])]
            if not not_payment_comission.empty:
                print("Foram encontradas comissões não pagas!")
                not_payment_comission.to_csv(path_to_save_no_paymet_comission + f'comissoes_nao_pagas_{self.date_work}')
            else: print("Todas as comissões foram pagas!")
        else: print("Arquivos de comissão consolidada ou comissões antecipadas não foram lidos. Verifique se o arquivo está vazio, e se foram carregados corretamente neste procedimento.")


if __name__ == "__main__":
    date_work = datetime.date.today()
    print("PRocessando conciliação!")
    conciliation_contracts(date_work = date_work)