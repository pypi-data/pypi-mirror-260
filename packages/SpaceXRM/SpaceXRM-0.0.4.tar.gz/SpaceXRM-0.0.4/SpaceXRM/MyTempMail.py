from time import sleep
from bs4 import BeautifulSoup

class SpaceXTempMail:
    def getEmailFromTempmail(self,session):
        while True:
            try:
                response = session.post('https://web2.temp-mail.org/mailbox')
                text = response.text       
                if not '","mailbox":"' in text:
                    jsonn = response.json()
                    errorMessage = jsonn['errorMessage']
                    print(errorMessage)
                    continue
                else:
                    jsonn = response.json()
                    tokenmailbox = jsonn['token']
                    mailbox = jsonn['mailbox']
                    break
            except Exception as e:
                print(e)
                pass
        return mailbox , tokenmailbox
            
    def getCodeFromTempmail(self,session,token,Keyword):
        headers = {'authorization': f'Bearer {token}'}    
        soup = None
        for i in range(30):
            sleep(1)
            req = session.get('https://web2.temp-mail.org/messages', headers=headers)
            if Keyword in req.text:
                json = req.json()
                messages = json['messages'][0]
                _id = messages['_id']
                response = session.get(f'https://web2.temp-mail.org/messages/{_id}', headers=headers)
                json = response.json()
                bodyHtml = json['bodyHtml']
                soup = BeautifulSoup(bodyHtml, 'html.parser')
                break
        return soup