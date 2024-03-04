
try:
    import os , requests
    import curl_cffi.requests as requests2 
    from colorama import Fore
    from SpaceXRM.MyFileHandling import SpaceXFile
    from SpaceXRM.MyTempMail import SpaceXTempMail
except Exception as e:
    print('------------------------------------------------------------------------------------------------')
    print(e)
    print('------------------------------------------------------------------------------------------------')
    input("Press ENTER to exit: ")
    quit()

class SpaceXRequests(SpaceXFile,SpaceXTempMail):
    def __init__(self):
        self.session = None
        #pass

    def check_connection(self) -> None:
        try:
            self.session.get("https://google.com")
        except requests.RequestException:
            self.print_msg(Fore.RED,"Error while connecting to the Internet. Make sure you are connected to the Internet!")

    def save_page_source(self,name,folder,page_source):
        if not name.endswith(".html"):
            name = name + ".html"
        if folder:
            abs_path = os.path.abspath(".")
            file_path = os.path.join(abs_path, folder)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            html_file_path = os.path.join(file_path, name)
        else:
            html_file_path = name
        with open(html_file_path, "wb") as file:
            file.write(page_source) 
    def print_msg(self,namecolor,messege):
        print(f"{namecolor}{messege}")

    def GetRequestsSessionNormal(self,Use_Proxy,socks,currentproxy):
        self.session = requests.Session()
        if Use_Proxy == 'y' or Use_Proxy == 'Y' or Use_Proxy == 'غ':
            if currentproxy == None:
                currentproxy = self.Usetextfile_Update(file_name='Proxies',file_name_Update='ProxiesUpdate')
            try:
                userp , passw , ip , port = currentproxy.split(':')
                proxy = f'{userp}:{passw}@{ip}:{port}'
            except:
                ip , port = currentproxy.split(':')
                proxy = f'{ip}:{port}'
            if socks == True:
                self.session.proxies.update({'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'})
            else:
                self.session.proxies.update({'http': f'http://{proxy}', 'https': f'http://{proxy}'})
        return self.session

    def GetRequestsSessionCurl_cffi(self,Use_Proxy,socks,currentproxy):
        self.session = requests2.Session(impersonate="chrome120",timeout=5)
        if Use_Proxy == 'y' or Use_Proxy == 'Y' or Use_Proxy == 'غ':
            if currentproxy == None:
                currentproxy = self.Usetextfile_Update(file_name='Proxies',file_name_Update='ProxiesUpdate')
            try:
                userp , passw , ip , port = currentproxy.split(':')
                currentproxy = f'{userp}:{passw}@{ip}:{port}'
            except:
                ip , port = currentproxy.split(':')
                currentproxy = f'{ip}:{port}'
            if socks == True:
                self.session.proxies.update({'http': f'socks5://{currentproxy}', 'https': f'socks5://{currentproxy}'})
            else:
                self.session.proxies.update({'http': f'http://{currentproxy}', 'https': f'http://{currentproxy}'})
        return self.session