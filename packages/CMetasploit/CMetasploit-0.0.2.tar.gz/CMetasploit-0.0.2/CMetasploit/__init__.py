'''                         Created By : Ankit Chandok                       '''
#####################################################################################
if __name__ == '__main__':
    print()
    print('==================== Welcome to CMetasploit Module v1.0 ====================')
    print('Type "help()", "classes()", "credits()" or "functions()" for more information.')
    print()
#####################################################################################
class BruteForce:
#####################################################################################
    def DictionaryCreator():
        try:
            import string,time
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print('                                                                          ')
            print('  ____   ____ ___  ____  _____  __  __ ____                               ')
            print(' / / /  / ___/ _ \|  _ \| ____| \ \/ / \ \ \                              ')
            print('/ / /  | |  | | | | | | |  _|    \  /   \ \ \                             ')
            print('\ \ \  | |__| |_| | |_| | |___   /  \   / / /                             ')
            print(' \_\_\  \____\___/|____/|_____| /_/\_\ /_/_/                              ')
            print('                                                                          ')
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print('                                                                          ')
            print('  ____  ____  ____  _   _ _____ _____                                     ')
            print(' / / / | __ )|  _ \| | | |_   _| ____|                                    ')
            print('/ / /  |  _ \| |_) | | | | | | |  _|                                      ')
            print('\ \ \  | |_) |  _ <| |_| | | | | |___                                     ')
            print(' \_\_\ |____/|_| \_\\\___/  |_| |_____|                                   ')
            print('                                                                          ')
            print(' ____   _    ____ ______        _____  ____  ____    _     ___ ____ _____ ')
            print('|  _ \ / \  / ___/ ___\ \      / / _ \|  _ \|  _ \  | |   |_ _/ ___|_   _|')
            print('| |_) / _ \ \___ \___ \\ \ /\ / / | | | |_) | | | | | |    | |\___ \  | | ')
            print('|  __/ ___ \ ___) |__) |\ V  V /| |_| |  _ <| |_| | | |___ | | ___) || |  ')
            print('|_| /_/   \_\____/____/  \_/\_/  \___/|_| \_\____/  |_____|___|____/ |_|  ')
            print('                                                                          ')
            print('____                                                                      ')
            print('\ \ \                                                                     ')
            print(' \ \ \                                                 Created by ANKIT   ')
            print(' / / /                                                 ^^^^^^^^^^^^^^^^   ')
            print('/_/_/                                                                     ')
            print('                                                                          ')
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print()
            print('WHAT TYPE PASSWORD LIST DO YOU WANT')
            print()
            print('[1] NUMBERS')
            print('[2] ALPHABETS')
            print('[3] SPECIAL CHARACTERS')
            print('[4] NUMBERS + ALPHABETS')
            print('[5] NUMBERS + SPECIAL CHARACTERS')
            print('[6] ALPHABETS + SPECIAL CHARACTERS')
            print('[7] NUMBERS + ALPHABETS + SPECIAL CHARACTERS')
            print()
            r = int(input('ENTER YOUR OPTION : '))        
            a=string.ascii_lowercase
            b=string.ascii_uppercase
            c=string.punctuation
            d=string.digits
            while r < 1 or r > 7:
                r = int(input('PLEASE ENTER THE VALID OPTION ( [8] TO CHOOSE DEFAULT COMBINATION[] ): '))
                if r == 8:
                    print('YOU CHOOSEN DEFAULT COMBINATION !!')
                    e = a+b+c+d
                    break
            if r == 1:
                e = d
            elif r == 2:
                e = a+b
            elif r == 3:
                e = c
            elif r == 4:
                e = d+a+b
            elif r == 5:
                e = d+c
            elif r == 6:
                e = a+b+c
            elif r == 7:
                e = a+b+c+d           
            x = []
            n = int(input("ENTER THE LENGTH OF PASS : "))
            print()
            start = time.time()
            for i in e:
                if n >= 2:
                    for j in e:
                        if n >= 3:
                            for k in e:
                                if n == 4:
                                    for l in e:
                                        x.append(i+j+k+l)
                                        end = time.time()
                                        print(i+j+k+l,'    ~ ',end - start,' ~ sec')
                                elif n == 3:               
                                    x.append(i+j+k)
                                    end = time.time()
                                    print(i+j+k,'    ~ ',end - start,' ~ sec')
                        elif n == 2:
                            x.append(i+j)
                            end = time.time()
                            print(i+j,'    ~ ',end - start,' ~ sec')
                elif n == 1:
                    x.append(i)
                    end = time.time()
                    print(i,'    ~ ',end - start,' ~ sec')
            print()
            print(x)
            print()
            end = time.time()
            print('    ~ ',end - start,' ~ sec')
            print()
            q = int(input('THANKS FOR USING OUR TOOL : (ENTER [0] TO EXIT) : '))
            while q != 0:
                print()
                print('PLEASE TRY AGAIN')
                q = int(input('THANKS FOR USING OUR TOOL : (ENTER [0] TO EXIT) : '))
            if q == 0:
                print()
                print('__________________________________________________________________________')
                print('__________________________________________________________________________')
                print('                                                                          ')
                print('  ____   ____ ___  ____  _____  __  __ ____                               ')
                print(' / / /  / ___/ _ \|  _ \| ____| \ \/ / \ \ \                              ')
                print('/ / /  | |  | | | | | | |  _|    \  /   \ \ \      THINK BEYOND THE RANGE ')
                print('\ \ \  | |__| |_| | |_| | |___   /  \   / / /        ANONYMOUS CODE X ??  ')
                print(' \_\_\  \____\___/|____/|_____| /_/\_\ /_/_/                              ')
                print('                                                                          ')
                print('                https://codex-studios.renderforestsites.com               ')
                print('__________________________________________________________________________')
                print('__________________________________________________________________________')
                print()
            q = input('PRESS ANY KEY TO CLOSE THE TOOL ')
        except:
            print("Sorry , Some Unexpected Error Occured Please Try Again !!")
#####################################################################################
    def ZipCracker():
        try:
            from tqdm import tqdm
            import zipfile
            from termcolor import colored
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print('                                                                          ')
            print('  ____   ____ ___  ____  _____  __  __ ____                               ')
            print(' / / /  / ___/ _ \|  _ \| ____| \ \/ / \ \ \                              ')
            print('/ / /  | |  | | | | | | |  _|    \  /   \ \ \                             ')
            print('\ \ \  | |__| |_| | |_| | |___   /  \   / / /                             ')
            print(' \_\_\  \____\___/|____/|_____| /_/\_\ /_/_/                              ')
            print('                                                                          ')
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print('                                                                          ')
            print('  ____  ____  ____  _   _ _____ _____                                     ')
            print(' / / / | __ )|  _ \| | | |_   _| ____|                                    ')
            print('/ / /  |  _ \| |_) | | | | | | |  _|                                      ')
            print('\ \ \  | |_) |  _ <| |_| | | | | |___                                     ')
            print(' \_\_\ |____/|_| \_\\\___/  |_| |_____|                                   ')
            print('                                                                          ')
            print(' ____   _    ____ ______        _____  ____  ____    _     ___ ____ _____ ')
            print('|  _ \ / \  / ___/ ___\ \      / / _ \|  _ \|  _ \  | |   |_ _/ ___|_   _|')
            print('| |_) / _ \ \___ \___ \\ \ /\ / / | | | |_) | | | | | |    | |\___ \  | | ')
            print('|  __/ ___ \ ___) |__) |\ V  V /| |_| |  _ <| |_| | | |___ | | ___) || |  ')
            print('|_| /_/   \_\____/____/  \_/\_/  \___/|_| \_\____/  |_____|___|____/ |_|  ')
            print('                                                                          ')
            print('____                                                                      ')
            print('\ \ \                                                                     ')
            print(' \ \ \                                                 Created by ANKIT   ')
            print(' / / /                                                 ^^^^^^^^^^^^^^^^   ')
            print('/_/_/                                                                     ')
            print('                                                                          ')
            print('__________________________________________________________________________')
            print('__________________________________________________________________________')
            print()
            var=''
            file=input(colored('Enter Your Zip Folder Name : ','yellow'))
            text=input(colored('Enter Word List File Name : ','yellow'))
            wordlist=[password.strip() for password in open(text,'r')]
            print(wordlist)
            #wordlist=['a','ankit','A','Ankit']
            zip_file=zipfile.ZipFile(file+'.zip')
            for i in tqdm(wordlist,desc="Checked "):
                try:
                    print()
                    zip_file.extractall(pwd=i.encode())
                    var=i
                    break
                except:
                    print(colored('Checking Password : '+str(i),'blue'))
            print()
            if var == '':
                print('Password Not Found')
            else:
                print(colored("Password Found :"+var,'green'))
            print()
            print(var)
            print()
            q = int(input('THANKS FOR USING OUR TOOL : (ENTER [0] TO EXIT) : '))
            while q != 0:
                print()
                print('PLEASE TRY AGAIN')
                q = int(input('THANKS FOR USING OUR TOOL : (ENTER [0] TO EXIT) : '))
            if q == 0:
                print()
                print('__________________________________________________________________________')
                print('__________________________________________________________________________')
                print('                                                                          ')
                print('  ____   ____ ___  ____  _____  __  __ ____                               ')
                print(' / / /  / ___/ _ \|  _ \| ____| \ \/ / \ \ \                              ')
                print('/ / /  | |  | | | | | | |  _|    \  /   \ \ \      THINK BEYOND THE RANGE ')
                print('\ \ \  | |__| |_| | |_| | |___   /  \   / / /        ANONYMOUS CODE X ??  ')
                print(' \_\_\  \____\___/|____/|_____| /_/\_\ /_/_/                              ')
                print('                                                                          ')
                print('                https://codex-studios.renderforestsites.com               ')
                print('__________________________________________________________________________')
                print('__________________________________________________________________________')
                print()
            q = input('PRESS ANY KEY TO CLOSE THE TOOL ')
        except:
            print("Sorry , Some Unexpected Error Occured Please Try Again !!")
#####################################################################################
class Socket:
#####################################################################################
    def connect():
        pass
#####################################################################################
    def server():
        pass
#####################################################################################
class Ping:
#####################################################################################
    def about():
        return print("Ping Tester")
#####################################################################################
    def basefunc():
        from subprocess import call as ping
        end=False
        while not end:
            a = input('~$ ')
            exec(a)
#####################################################################################
    def get():
        import subprocess
        while True :
            print()
            print('Starting....')
            print("ENTER AN IP OR WEBSITE NAME")
            i = input(">>>>")
            if i=='exit()':
                print('Exiting....')
                break
            print()
            subprocess.call("ping "+ i ,shell=True)
#####################################################################################
'''                          More Tools Coming Soon                               '''