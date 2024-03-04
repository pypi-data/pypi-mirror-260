from phone_iso3166.country import phone_country,country_prefix
import pycountry , phonenumbers
from threading import  Semaphore
from time import sleep
from colorama import Fore
import getpass
import os
from glob import glob
import shutil
from pathlib import Path

screenlock = Semaphore(value=1)

class SpaceXFile:
    def __init__(self):
        pass
    def create_folder(self, folder):
        """Creates a folder of the given name if it doesn't already exist."""
        if folder.endswith("/"):
            folder = folder[:-1]
        if len(folder) < 1:
            raise Exception("Minimum folder name length = 1.")
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception:
                pass
                
    def create_file(self,filename):
        if Path(f'{filename}.txt').is_file():
            f = 0
        else:
            open(f'{filename}.txt' , 'w+')
                
    def clear_temp(self):
        usernamePath = getpass.getuser()
        Temp = f'C:/Users/{usernamePath}/AppData/Local/Temp/'
        lists = glob(f"{Temp}*")
        for l in lists:
            try:
                shutil.rmtree(l, ignore_errors=True)
            except:
                pass
            try:
                os.unlink(l)
            except:
                pass

    def SaveLineInFile(self,filename,line):
        sleep(0.1)
        if Path(f'{filename}.txt').is_file():
            f = 0
        else:
            open(f'{filename}.txt' , 'w+')
        print(line,file=open(f'{filename}.txt','a+'))

    def Usetextfile_Update(self,file_name,file_name_Update):
        screenlock.acquire()
        with open(f'{file_name}.txt','r+') as fin:
            lines = fin.readlines()
            fin.close()
        if len(lines) == 0 or lines[0] == '\n':
            with open(f'{file_name_Update}.txt','r') as fin:
                lines = fin.readlines()
                if len(lines) == 0 or lines[0] == '\n':
                    print(f'{Fore.RED}[!] Check The File {Fore.GREEN}"{file_name}.txt"{Fore.RED} Because It Is Empty ')
                    screenlock.release()
                    while 1 == 1:
                        sleep(99999)
                line_value = lines[0].strip()
                del lines[0]
                print(''.join(lines).strip(), file=open(f'{file_name}.txt', "w+"))
                fin.close()
            screenlock.release()
        else:
            line_value = lines[0].strip()
            del lines[0]
            print(''.join(lines).strip(), file=open(f'{file_name}.txt', "w+"))
            screenlock.release()
        return line_value
    def getNumber(self,file_name,file_name_Update):
        while True:
            phonenume  = self.Usetextfile_Update(file_name=file_name,file_name_Update=file_name_Update)
            readnumber = f"+{phonenume}"
            try:
                phone = phonenumbers.parse(readnumber).national_number
                region_code = phone_country(readnumber)
                prefix = country_prefix(region_code)
                name = pycountry.countries.get(alpha_2=region_code).name
                break
            except Exception as e:
                pass
        return phone , region_code , prefix , name , readnumber , phonenume