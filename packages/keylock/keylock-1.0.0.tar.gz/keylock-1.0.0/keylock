#!/use/bin/python


# MIT License

# Copyright (c) 2022 CodingSangh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os, base64, subprocess, requests
from requests import get
from subprocess import run
from os import system, popen, remove
from pprint import pformat
from time import sleep

White = '\033[37m'
Blue = '\033[34m'
Red = '\033[91m'
Green = '\033[92m'
Yellow = '\033[93m'
NoColour = "\033[00m"

ask = Green + '[' + White + '?' + Green + '] '+ Yellow
success = Yellow + '[' + White + '✓' + Yellow + '] '+Green
error = Blue + '[' + White + '!' + Blue + '] '+Red
info= Yellow + '[' + White + '+' + Yellow + '] '+ Blue
info2= Green + '[' + White + '•' + Green + '] '+ Blue

# VERSION
version = '2.0'

# INTERNET CHECKER
def internet():
    try:
        get("https://github.com/keylock")
        return True
    except Exception:
        return False

# UPDATE
def update():
    system("clear")
    print(run(["lolcat"], input=logo ,capture_output= True, text=True).stdout)
    print(f"\n{info}Checking for updates")
    fver = get("https://raw.githubusercontent.com/CodingSangh/keylock/master/.version").text.strip()
    if (fver != version and fver != "404: Not Found"):
        changelog=popen("curl -s -N https://raw.githubusercontent.com/CodingSangh/keylock/main/.changelog.log").read().strip()
        update_commands=popen("curl -s -N https://raw.githubusercontent.com/CodingSangh/keylock/main/.update").read().strip()
        system("clear")
        print(run(["lolcat"], input=logo ,capture_output= True, text=True).stdout)
        print(f"{info}keylock has a new update!\n{info2}Current Version: {Red}{version}\n{info}Available Version: {Green}{fver}\n")
        update_ask =input(ask+"Do you want to update keylock?[y/n] > "+Green)
        if update_ask =="y" or update_ask =="Y" :
            print(NoColour)
            system(update_commands)
            if (fver == version and fver!= "404: Not Found"):
                 print("\n"+success+"keylock updated successfully!! Please Start Again!\n")
                 exit()
            else :
                 update()
            if (changelog != "404: Not Found"):
                print(info2+"What's New! :\n"+Yellow+changelog)
        elif update_ask =="n" or update_ask =="N" :
            print("\n"+info+f"Updating cancelled. Using old version! \nVERSION : {version}")
            sleep(2)
            main()
        else:
            print("\n"+error+"Wrong input!\n")
            update()
    else:
        print(f"\n\n{success}keylock is up-to-date\n{success}Starting keylock")
        sleep(1)
        main()

logo =f"""
       ╔══════════════════════════════════╗
       ║  ╔╗           ╔╗         ╔╗      ║
       ║  ║║           ║║         ║║      ║
       ║  ║║╔╗╔══╗╔╗ ╔╗║║ ╔══╗╔══╗║║╔╗    ║
       ║  ║╚╝╝║║═╣║║ ║║║║ ║╔╗║║╔═╝║╚╝╝    ║
       ║  ║╔╗╗║║═╣║╚═╝║║╚╗║╚╝║║╚═╗║╔╗╗    ║
       ║  ╚╝╚╝╚══╝╚═╗╔╝╚═╝╚══╝╚══╝╚╝╚╝    ║
       ║          ╔═╝║                    ║
       ║          ╚══╝                    ║
       ║                                  ║
       ║     [VERSION = {version}]              ║
       ║     [By CodingSangh]                 ║
       ╚══════════════════════════════════╝
\n"""
options= """
     [1] Encrypt Bash         [2] Decrypt Bash
     [3] Python to Emoji      [4] Python to Var
     [5] About Tool           [0] Exit
"""

system("""command -v lolcat > /dev/null 2>&1 || { echo >&2 "...";echo "";echo "";echo "[^^] lolcat Installing...";pip install git+https://github.com/CodingSangh/lolcat.git;clear; }
command -v toilet > /dev/null 2>&1 || { echo >&2 "...";echo "";echo "";echo "[^^] Toilet Installing...";pkg install toilet -y && pkg install figlet -y;clear; }
""")

keylock = ""
keylock += "\x61\x57\x59\x67\x49\x6b\x35\x70\x63\x32"
keylock += "\x68\x68\x62\x6e\x51\x69\x49\x47\x6c\x75"
keylock += "\x49\x47\x78\x76\x5a\x32\x38\x67\x4f\x67"
keylock += "\x6f\x67\x49\x43\x41\x67\x63\x47\x46\x7a"
keylock += "\x63\x77\x70\x6c\x62\x48\x4e\x6c\x49\x44"
keylock += "\x6f\x4b\x49\x43\x41\x67\x49\x48\x42\x79"
keylock += "\x61\x57\x35\x30\x4b\x47\x56\x79\x63\x6d"
keylock += "\x39\x79\x49\x43\x73\x69\x52\x47\x38\x67"
keylock += "\x62\x6d\x39\x30\x49\x48\x4e\x30\x5a\x57"
keylock += "\x56\x73\x49\x47\x4e\x76\x5a\x47\x55\x69"
keylock += "\x4b\x51\x6f\x67\x49\x43\x41\x67\x5a\x58"
keylock += "\x68\x70\x64\x43\x67\x70"

#BASH ENCRYPT
def Encrypt():
  try:
       Script = input(ask + White + "Script " + Green + "> " + White)
       if not os.path.isfile(Script):
         print(error+'File not found')
         sleep(2)
         Encrypt()
       output = input(ask + White + "Output " + Green + "> " + White)
       system("bash-obfuscate " + Script + " -o .test.sh")
       with open(".test.sh",'r') as r, open(output,"w") as w:
         data= r.read()
         w.write("# Decrypted by keylock\n# Github- https://github.com/CodingSangh/keylock\n\n"+data)
       remove("test.sh")
       print (success+"Done..")
  except KeyboardInterrupt :
      print (error + "Stopped!")

#BASH DECRYPT
def Decrypt():
  try:
       Script = input(ask + White + "Script " + Green + "> " + White)
       if not os.path.isfile(Script):
         print(error+'File not found')
         sleep(2)
         Decrypt()
       file = open(Script,'r')
       filedata = file.read()
       file.close()
       newdata = filedata.replace("eval","echo")
       out = input(ask + White + "Output" + Green + " > " + White)
       file = open(out,'w')
       file.write(newdata)
       file.close()
       system("touch .test.sh")
       system("bash " + out + " > .test.sh")
       remove(out)
       with open(".test.sh",'r') as r, open(out,"w") as w:
         data= r.read()
         w.write("# Decrypted by keylock\n# Github- https://github.com/CodingSangh/keylock\n\n"+data)
       remove("test.sh")
       print (success + "Done..")

  except KeyboardInterrupt :
       print (error + " Stopped!")
  except IOError :
       print (error + " File Not Found!")

#ABOUT
def About ():
    print(run(["lolcat"],input = "[•] Tool Name :        Bash Encrypter & Decrypter\n[•] Coder     :        CodingSangh\n[•] Github    :        https://github.com/CodingSangh \n[•] Coded On  :        17-04-2004 \n[•] Telegram  :        t.me/codingsangh" , capture_output= True, text=True).stdout)

#PYTHON ENCRYPT EMOJI

alphabet = [
    "\U0001f600",
    "\U0001f603",
    "\U0001f604",
    "\U0001f601",
    "\U0001f605",
    "\U0001f923",
    "\U0001f602",
    "\U0001f609",
    "\U0001f60A",
    "\U0001f61b",
]
MAX_STR_LEN = 70

def wrt_emoji (code,n):
    return"\n".join("{}\\".format(code[i : i + n]) for i in range(0, len(code), n)).rstrip("\\")
    
def to_write(code,alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    return (
        'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
        '"{}"\n.split("  ")])))\n'.format(
            pformat(d2),
            wrt_emoji("  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in code),MAX_STR_LEN, ),))


def emoji():
  try:
       Script = input(ask + White + "Script " + Green + "> " + White)
       if not os.path.isfile(Script):
         print(error+'File not found')
         sleep(2)
         emoji()
       file = open(Script,'r')
       filedata = file.read()
       file.close()

       out = input(ask + White + "Output" + Green + " > " + White)
       file = open(out,'w')
       file.write("# Encrypted by keylock\n# Github- https://github.com/CodingSangh/keylock\n\n"+to_write(filedata, alphabet))
       file.close()
       print (success + "Done..")

  except KeyboardInterrupt :
       print (error + " Stopped!")

# PYTHON TO VAR
OFFSET = 10
def obfuscate(VARIABLE_NAME, file_content):
    b64_content = base64.b64encode(file_content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
    return code
def var():
    Script = input(ask+ "Input file  > "+White)
    if not os.path.isfile(Script):
        print(error+'File not found')
        system("sleep 2")
        var()
    output = input(ask + "Output file  > " + White)
    variable= input(ask + "Variable to be used(Must Required)  > " + Green)
    if (variable==""):
        print(error + " No variable")
        system("sleep 3")
        var()
    if (variable.find(" ")!= -1):
        print(error+" Only one word!")
        system("sleep 3")
        var()
    count = input(ask + "Iteration count for variable  > " + Green)
    try:
        iteration = int(iteration)
    except Exception:
        iteration = 7
    VARIABLE_NAME = variable * iteration
    with open(Script, 'r') as r,open(output, 'w') as w:
        file = r.read()
        obfuscated_code = obfuscate(VARIABLE_NAME, file)
        w.write("# Encrypted by keylock\n# Github- https://github.com/CodingSangh/keylock\n\n"+obfuscated_code)
    print(success + "Done..")

#MAIN FUNCTION
def main():
    exec(__import__("\x62\x61\x73\x65\x36\x34").b64decode(keylock.encode("\x75\x74\x66\x2d\x38")).decode("\x75\x74\x66\x2d\x38"))
    system("""clear && toilet -f big "        keylock" | lolcat""")
    print(run(["lolcat"], input=logo + options ,capture_output= True, text=True).stdout)
    option = input(run(["lolcat"], input="Choose : ",capture_output= True, text=True).stdout)

    if option == "1" or option == "01" :
      Encrypt()
    elif option == "2" or option == "02" :
      Decrypt()
    elif option == "3" or option == "03" :
      emoji()
    elif option == "4" or option == "04" :
      var()
    elif option == "5" or option == "05" :
      About()
    elif option == "0" or option == "00" :
      print(run(['lolcat'], input = '\nTHANKS FOR USING' ,capture_output = True , text = True).stdout)
      exit()
    else:
      print (error +"Wrong Input")
      sleep(1)
      main()

if __name__=='__main__':
     update() if internet () else main()
