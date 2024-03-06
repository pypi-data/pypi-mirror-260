import string
import random
import urllib.request
from twocaptcha import TwoCaptcha
with open(f'CaptchaKey.txt', 'r') as f:
    apikey = f.readline().strip() 
solver = TwoCaptcha(apikey)
letters = string.ascii_lowercase  
class SpaceXSolver:
    def __init__(self):
        pass
    def TwoCaptchaImage(self,folder,url):
        result_str  = ''.join(random.choice(letters)for i in range(20))
        urllib.request.urlretrieve(url,f"{folder}/{result_str}.png")            
        result = solver.normal(f"{folder}/{result_str}.png")['code']
        return result 