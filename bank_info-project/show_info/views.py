from django.shortcuts import render
import mysql.connector


class MainDb:
    
    def __init__(self, dbname:str) -> None:
        self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="amma@@1953",
                    database=dbname
                    )


    def display_dat(self, tablename: str)->list:
        main = self.mydb.cursor()
        main.execute(F'SeLeCt * FrOm {tablename}')
        ans = list(main)
        main.close()
        return ans

    
    def insert_dat(self, *contents, tablename)->bool:
        try:
            main = self.mydb.cursor()
            main.execute(F'InSeRt InTo {tablename} VaLuEs {contents}')
            self.mydb.commit()
            main.close()
        except: 
            self.mydb.rollback()
            prcs = False
        else: prcs = True
        finally: pass

        return prcs


    def del_data(self, tablename,unique_id)->bool:
        try:
            main = self.mydb.cursor()
            main.execute(F'DeLeTe FrOm {tablename} WhErE UnIqUe_Id="{unique_id}"')
            self.mydb.commit()
            main.close()
        except:
            self.mydb.rollback()
            prcs = False
        else: prcs = True
        finally: pass
        
        return prcs


    def upd_data(self, tablename, newvalname, newval, newvaltype, unique_id)->bool:
        '''n means number for newvaltype'''
        try:
            main = self.mydb.cursor()
            if newvaltype=='n':
                main.execute(F'UPDATE {tablename} set {newvalname}={newval} where unique_id = \'{unique_id}\'')
            else:
                main.execute(F'UPDATE {tablename} set {newvalname}=\'{newval}\' where unique_id = \'{unique_id}\'')
            self.mydb.commit()
            main.close()
        except: 
            self.mydb.rollback()
            prcs = False
        else: prcs = True
        finally: pass
        
        return prcs


    def close_db(self)->None:
        self.mydb.close()
#---------------------------------------------------------------------------------------------------------------------->


# Create your views here.
def home(request):
    return render(request, 'generator/home.html')

def display(request):
    main_vals = dict()
    usr_id = MainDb('Mainstructure')
    vals = list(filter(lambda x: True if x[4]==request.GET.get('usr_cde') else False,usr_id.display_dat('user_main')))
    if vals:  
        main_vals['values'] = True
        main_vals['name'] = vals[0][0]
        main_vals['Gender'] = 'Male' if vals[0][1]=='M' else 'Female'
        main_vals['dob'] = vals[0][2]
        main_vals['nationality'] = vals[0][3]
        main_vals['id'] = vals[0][4]
        main_vals['phone_no'] = vals[0][5]
        main_vals['email'] = vals[0][6]
        main_vals['crtion_date'] = vals[0][7]
        main_vals['balance'] = vals[0][8]
        
    else: main_vals['values'] = False
    usr_id.close_db()
    
    
    return render(request, 'generator/display.html', main_vals)