# objective: parse through gmail messages and determine which are spam by blacklisting certain colleges
# write functions(done)
# create GUI(tkinter), gonna take some time
# accept full user input from GUI
# streamline and style finished program

import imaplib # imports the IMAP libraries for access to gmail
import email # allows me to parse emails by their subjects, bodies, attachments, etc.
from email.header import decode_header # need to decode headers from bin
import webbrowser 
import os
from tkinter import * # necessary for G.U.I.

lst = ['Directions:', 'Choose from options to delete or move emails in mass', 'Begin by logging in, then enter the necessary info']

def clean(text):
    #clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")

user, passcode = " ", " "
global isLoggedIn
isLoggedIn = 'false'

def end():
    if(isLoggedIn=="true"):
        imap.close()
        imap.logout()
    root.destroy()

def output():
    print(username.get())
    print(password.get())
    user = username.get()
    passcode = password.get()
    try:
        imap.login(user, passcode)
        isLoggedIn='true'
        #status, messages = imap.select('"[Gmail]/All Mail"')
        status, messages = imap.select("INBOX")
        N=3
        #total number of emails
        messages = int(messages[0])
        print(imap.list()) # lists given directories within an email
    except:
        t.delete("1.0", "end")
        t.insert(END, "Invalid Credentials \n", "center")
        isLoggedIn="false"

def deleteEmails():
    try:
         mailer = target.get() # trying to make user input decide the target email
         status, messages = imap.search(None, 'FROM', '"%s"' % mailer)
         messages = messages[0].split(b' ')
         for mail in messages:
            _, msg = imap.fetch(mail, '(RFC822)')
            # you can delete the for loop for performance if you have a long list of emails
            # because it is only for printing the SUBJECT of target email to delete
            for response in msg:
                if isinstance(response, tuple):
                    # decode the email subject
                        msg = email.message_from_bytes(response[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes type, decode to str
                            subject = subject.decode()
                        print("Deleting", subject)
                # mark the mail as deleted
                imap.store(mail, "+FLAGS", "\\Deleted")
         t.delete("1.0", "end")
         t.insert(END, "Emails deleted \n", "center")
         imap.expunge()
    except:
         t.delete("1.0", "end")
         t.insert(END, "Invalid Target Email \n", "center")

def moveEmails():
    try:
        mailer = target.get() # trying to make user input decide the target email
        folder = fold.get()

        status, messages = imap.search(None, 'FROM', '"%s"' % mailer)
        messages = messages[0].split(b' ')
        for mail in messages:
                _, msg = imap.fetch(mail, '(RFC822)')
                # you can delete the for loop for performance if you have a long list of emails
                # because it is only for printing the SUBJECT of target email to delete
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            # if it's a bytes type, decode to str
                            subject = subject.decode()
                        print("Copying:", subject)
                        imap.copy(mail, folder)
                        imap.store(mail, "+FLAGS", "\\Deleted")
                        #mark mail as deleted
        t.delete("1.0", "end")
        t.insert(END, "Emails moved \n", "center")
        imap.expunge()
    except:
        t.delete("1.0", "end")
        t.insert(END, "Invalid Folder/Target Email \n", "center")

def printThreeMostRecentEmails():
    for i in range(messages, messages-N, -1):
        #fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
               # parse a bytes email into a message object
               msg = email.message_from_bytes(response[1])
               #decode the email subject
               subject, encoding = decode_header(msg["Subject"])[0]
               if isinstance(subject,bytes):
                  #if it's in bytes, made it a string
                  subject = subject.decode(encoding)
              #decode who the sender is
               From, encoding = decode_header(msg.get("From"))[0]
               if isinstance(From, bytes):
                   From = From.decode(encoding)
               print("Subject:", subject)
               print("From:", From)
               #if the email message is multipart
               if msg.is_multipart():
                  #iterate over the email's parts
                  for part in msg.walk():
                    #extract content
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        #get email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        #print plain emails and skip attachments
                        print(body)
                    elif "attachment" in content_disposition:
                        pass
                        # i am not downloading attachments that a computer can't tell if its a virus or not :/
               else:
                 #extract content type
                 content_type = msg.get_content_type()
                 #get the body
                 body = msg.get_payload(decode=True).decode()
                 if content_type == "text/plain":
                    #print only the text in the email
                    print(body)
               if content_type == "text/html":
                  pass
                #html files give me pain with char mapping ugh
                #html emails get opened as a new file in a browser
                #folder_name = clean(subject)
                #if not os.path.isdir(folder_name):
                    #make a folder for this email(named after the subject)
                #    os.mkdir(folder_name)
                #filename = "index.html"
                #filepath = os.path.join(folder_name, filename)
                #write the file
                #open(filepath, "w").write(body)
                #open in a browser
                #webbrowser.open(filepath)
               print("="*100) # need to move and include this function

root = Tk()
height = 400
width = 700.00
widthbutLie = 600
buttonXShift = 90
yBuffer = 80
root.geometry("600x%s" % height)
window = Canvas(root, bg="light grey", height = "%s" % height, width="600").place(x=0,y=0)
frame = Frame(root)
textLabel = Label(window, text='Email Manager', bg="light grey", fg="black").place(x=(width*0.5)-90, y=50)
t = Text(window, bg="white", fg="black", font = "Herculanum 12", highlightthickness = 0, bd = 0, height=3, width=55)
t.tag_configure("center", justify='center')


for x in lst:
    t.insert(END, x + '\n', "center")

t.tag_add("center", "1.0", "end")
t.place(x=45,y=50)
# set window size

#the buttons
loginButton = Button(window, text="Click to Login", fg="black", bg="white", font = "Herculanum 12", highlightthickness = 0, bd = 0, command=output).place(x=(0.1*widthbutLie)-80+buttonXShift,y=10)
moveButton = Button(window, text="Click to Move Emails", fg="black", bg="white", font = "Herculanum 12", highlightthickness = 0, bd = 0, command=moveEmails).place(x=(widthbutLie*0.5)-20+buttonXShift,y=10)
deleteButton = Button(window, text="Click to Delete Emails", fg="black", bg="white", font = "Herculanum 12", highlightthickness = 0, bd = 0, command=deleteEmails).place(x=(widthbutLie*0.2)-40+buttonXShift,y=10)
quitButton = Button(window, text="QUIT", fg="red", bg="white", font = "Herculanum 12", highlightthickness = 0, bd = 0, command=end).place(x=(0.5*widthbutLie)-60+buttonXShift,y=10)

userLabel = Label(window, text='Enter Email: ', bg="light grey", fg="black", font = "Herculanum 12",).place(x=(width*0.5)-100, y=(height*0.1)+yBuffer) # block for entering email

username = StringVar(window, value='Enter your email here...')
userTf = Entry(window, textvariable=username, width=40, justify='center').place(x=(width*0.5)-180, y=(height*0.1)+20+yBuffer)

passLabel = Label(window, text='Enter Password: ', font = "Herculanum 12", bg="light grey", fg="black").place(x=(width*0.5)-120, y=(height*0.1)+50+yBuffer) # block for entering password

password = StringVar(window, value='Enter your password here...')
passTf = Entry(window, textvariable=password, width=40, justify='center').place(x=(width*0.5)-180, y=(height*0.1)+70+yBuffer)

targetLabel = Label(window, text='Enter Target Mailing Address: ', font = "Herculanum 12", bg="light grey", fg="black").place(x=(width*0.5)-160, y=(height*0.1)+100+yBuffer) # block for entering target email

target = StringVar(window, value='Enter the target email here...')
targetTf = Entry(window, textvariable=target, width=40, justify='center').place(x=(width*0.5)-180, y=(height*0.1)+120+yBuffer)

foldLabel = Label(window, text='Enter Mailbox Folder to Move to(Optional): ', font = "Herculanum 12", bg="light grey", fg="black").place(x=(width*0.5)-200,y=(height*0.1)+150+yBuffer) # block for entering target folder

fold = StringVar(window, value='Enter the target mailbox here...')
foldTf = Entry(window, textvariable=fold, width=40, justify='center').place(x=(width*0.5)-180,y=(height*0.1)+170+yBuffer)

#start the g.u.i, and effectively the program
root.mainloop() 

