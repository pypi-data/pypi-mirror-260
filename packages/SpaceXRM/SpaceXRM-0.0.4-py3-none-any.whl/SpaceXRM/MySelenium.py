try:
    import os,random
    from colorama import Fore
    from selenium.webdriver.common.by import By
    from selenium.webdriver import ActionChains
    from selenium.webdriver.support import expected_conditions as EC
    from selenium_profiles.webdriver import Chrome
    from selenium_profiles.profiles import profiles
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    import ua_generator
    
    import codecs
    import json
    from selenium.common.exceptions import (ElementClickInterceptedException as ECI_Exception,ElementNotInteractableException as ENI_Exception,InvalidArgumentException,MoveTargetOutOfBoundsException,NoSuchElementException,NoSuchWindowException,StaleElementReferenceException as Stale_Exception,TimeoutException,WebDriverException)
    from SpaceXRM.MyFileHandling import SpaceXFile
except Exception as e:
    print('------------------------------------------------------------------------------------------------')
    print(e)
    print('------------------------------------------------------------------------------------------------')
    input("Press ENTER to exit: ")
    quit()

class SpaceXSelenium(SpaceXFile):
    def __init__(self):
        self.driver     = None
        self.playwright = None
        #pass
        

    def ClickElement(self,selector,timeout):
        if 'text=' in selector:
            text = str(selector).split('="')[1].split('"')[0].strip()
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.XPATH,f"//*[contains(text(), '{text}')]"))).click()
        else:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR,selector))).click()
        
    def SendKeysElement(self,selector,text,timeout):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector))).send_keys(str(text))
        
    def CreateActionChains(self,selector,timeout):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        actions = ActionChains(self.driver)
        return actions.move_to_element(element)


    def quit_all_driver(self):
        for driver in self.drivers_list:
            try:
                if (hasattr(driver, "service") and driver.service.process):
                    driver.quit()
            except AttributeError:
                pass
            except Exception:
                pass
    def save_page_source(self,name, folder=None):
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
        page_source = self.driver.page_source
        html_file = codecs.open(html_file_path, "w+", "utf-8")
        html_file.write(page_source)
        html_file.close()
    
    def save_cookies(self, name="cookies.txt"):
        """Saves the page cookies to the "saved_cookies" folder."""
        #self.wait_for_ready_state_complete()
        cookies = self.driver.get_cookies()
        json_cookies = json.dumps(cookies)
        if name.endswith("/"):
            raise Exception("Invalid filename for Cookies!")
        if "/" in name:
            name = name.split("/")[-1]
        if "\\" in name:
            name = name.split("\\")[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = 'Cookie'
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        cookies_file_path = os.path.join(file_path, name)
        cookies_file = codecs.open(cookies_file_path, "w+", encoding="utf-8")
        cookies_file.writelines(json_cookies)
        cookies_file.close()
    
    def load_cookies(self, name="cookies.txt"):
        """Loads the page cookies from the "saved_cookies" folder."""
        if name.endswith("/"):
            raise Exception("Invalid filename for Cookies!")
        if "/" in name:
            name = name.split("/")[-1]
        if "\\" in name:
            name = name.split("\\")[-1]
        if len(name) < 1:
            raise Exception("Filename for Cookies is too short!")
        if not name.endswith(".txt"):
            name = name + ".txt"
        folder = 'Cookie'
        abs_path = os.path.abspath(".")
        file_path = os.path.join(abs_path, folder)
        cookies_file_path = os.path.join(file_path, name)
        json_cookies = None
        with open(cookies_file_path, "r") as f:
            json_cookies = f.read().strip()
        cookies = json.loads(json_cookies)
        for cookie in cookies:
            if "expiry" in cookie:
                del cookie["expiry"]
            self.driver.add_cookie(cookie)
    
    def check_browser(self):
        """This method raises an exception if the active window is closed.
        (This provides a much cleaner exception message in this situation.)"""
        active_window = None
        try:
            active_window = self.driver.current_window_handle  # Fails if None
        except Exception:
            pass
        if not active_window:
            raise NoSuchWindowException("Active window was already closed!")
            
    def print_msg(self,namecolor,messege):
        print(f"{namecolor}{messege}")
    def GetChromeOptions(self,type_disply,Use_Proxy):     
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--lang=en-US")
        options.add_argument("--log-level=3")
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=400,800")
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-blink-features=AutomationControlled') 
        #theuseragent = UserAgent(random.choice(['firefox','edge','ios'])).Random()
        theuseragent = ua_generator.generate(device='desktop', browser='firefox').text
        options.add_argument(f'--user-agent={theuseragent}')
        if type_disply == 'y' or type_disply == 'Y' or type_disply == 'غ':
            options.add_argument("--headless=new")
        if Use_Proxy == 'y' or Use_Proxy == 'Y' or Use_Proxy == 'غ':
            proxy  = self.Usetextfile_Update(file_name='Proxies',file_name_Update='ProxiesUpdate')
            proxy_type = 'http'
            options.add_argument(f'--proxy-server={proxy_type}://{proxy}')
            self.print_msg(Fore.GREEN,f'[-] Proxy Used  :: [{proxy}]')
        return options
        
    def GetDriverNormal(self,type_disply,Use_Proxy):
        options = self.GetChromeOptions(type_disply,Use_Proxy)
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
        self.driver = webdriver.Chrome(service=Service(executable_path='chromedriver.exe'),options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",})
        self.driver.set_page_load_timeout(100)
        return self.driver
    
    def GetDriverFromProfiles(self,Typeprofiles,uc_driver,type_disply,Use_Proxy):
        if Typeprofiles == 1:
            profile = profiles.Android()
        else:
            profile = profiles.Windows()
        options = self.GetChromeOptions(type_disply,Use_Proxy)
        if uc_driver == False:
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        try:
            self.driver  = Chrome(profile,options=options,executable_path='chromedriver.exe',uc_driver=uc_driver)
        except:
            self.driver  = Chrome(profile,options=options,executable_path='chromedriver.exe',chrome_binary='chromedriver.exe',uc_driver=uc_driver)
        if uc_driver == True:
            self.driver.set_window_position(random.randint(111,999),random.randint(000,600))
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",})
        self.driver.set_page_load_timeout(100)
        return self.driver
    
    def GetDriverFromBlaywright(self,headless_disply,Use_Proxy):
        proxy = None
        currentproxy = None
        if Use_Proxy == 'y' or Use_Proxy == 'Y' or Use_Proxy == 'غ':
            prox = self.Usetextfile_Update(file_name='Proxies',file_name_Update='ProxiesUpdate')
            currentproxy = {'http': f'http://{prox}','https': f'http://{prox}'}
            proxy = {"server": f"http://{prox}"}
            self.print_color(Fore.GREEN,f'[-] Proxy Used  :: [{proxy}]')
        #playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless_disply,proxy=proxy)
        useragent = ua_generator.generate(device='mobile').text
        self.driver = self.browser.new_page(viewport={"width":600,"height":800},locale='en-US',user_agent=useragent)
        return self.driver