from modules.modules import openBrowserCrefisa, get_tables, work_tables, contracts_conference
import datetime

def main():


    date_work_old = datetime.date.today() - datetime.timedelta(days = 10)
    print("Baixando relatórios antigos.")
    get_tables(driver = openBrowserCrefisa().loguinSendKeys(), date = date_work_old, get_old_tables=True).download()

    date_work = datetime.date.today() - datetime.timedelta(days = 4)
    get_tables(driver = openBrowserCrefisa().loguinSendKeys(), date = date_work).download()
    while date_work < datetime.date.today():
        contracts_conference(date_work= date_work)
        work_tables(data = date_work)
        date_work += datetime.timedelta(days=  1)


if __name__  == "__main__":

    main()
    print("Processo concluído!")
 