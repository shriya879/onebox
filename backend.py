import imapclient 
import time
from email.header import decode_header
def connectingimap(username,password,server):
    email=imapclient.IMAPClient(server,ssl=True)
    email.login(username,password)
    email.select_folder('inbox')
    return email
def fetch_emails(email,since_day=30):
    since_date=time.strftime("%d-%b-%y",time.gmtime(time.time()-since_day*86400))
    ids=email.search(['SINCE',since_date])
    mails=[]
    for id in ids:
        raw_message=email.fetch([id],['RFC822'])[id][b'RFC822']
        msg=emails.message_form_bytes(raw_message)
        subjects,encoding=decode_header(msg["subjects"])[0]
        subjects=subjects.decode(encoding)if encoding else subjects
        mails.append({"subjects":msg["Subjects"],"from":msg["From"],"to":msg["To"],"date":msg["Date"],"body":msg.get_payload(decode=True)})
    return mails
        
        
if __name__=="__main__":
    username="your-email@example.com"
    password="your-passwoard"
    server="imap.gmail.com"
    mail=connectingimap(username,password,server)
    email=fetch_emails(email,since_day=30)
    for mail in mails:
        print(f"subjects:{mail['subjects']}")
        print(f"from:{mail['from']}")
        print(f"to:{mail['to']}")
        print(f"date:{mail['date']}")
        print(f"body:{mail['body']}")
        print("-"*50)
    email.logout()








