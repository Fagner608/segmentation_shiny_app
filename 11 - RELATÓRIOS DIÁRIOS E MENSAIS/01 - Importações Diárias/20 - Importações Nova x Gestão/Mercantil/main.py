from modules import openBrowser, downaload_reports, conciliation, work_tables
from datetime import date
from datetime import timedelta

def main():

        datework = date.today() - timedelta(days = 2)
        # downaload_reports(driver = openBrowser().loguinSendKeys(),date = datework)
        
        while datework < date.today():
            conciliation(datework = datework)

            work_tables(date_work = datework)
            
            datework += timedelta(days = 1)

        





if __name__ == '__main__':
    main()
