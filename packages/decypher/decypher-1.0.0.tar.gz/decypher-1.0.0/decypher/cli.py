import typer
from importlib import metadata
import math
from rich import print
import base64
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time
import struct
from decypher import home

app = typer.Typer(rich_markup_mode="rich",help="""[bold yellow] DECIPHER -[white] Your Speedy Cipher [red bold]Decryption [white]/ [bold green]Encryption [white]tool""")

__version__=home.version

def version_callback(value: bool) -> None:
    if value:
        home.screen()
        print(f'[yellow]version: [yellow bold]{__version__}\n')
        raise typer.Exit()

@app.callback()
def callback(
    _: bool = typer.Option(None, "--version", "-v","-i","--info",help="app version/info",callback=version_callback)
) -> None:
    "version and info"

    
@app.command("ceaser")
def ceaser(message: str=typer.Argument(None, help="The ciphertext", show_default=True),key: int=typer.Argument(0, help="The Key", show_default=True),encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):

  with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='red'),
        transient=True,
    ) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(3)
  if(message!=None and key!=0 and key<=25):
     decrypted = ''
     encrypted = ''
     if(key):
      for text in message:
          if text.isalpha():
            if text.islower():
                decrypted += chr((ord(text) - ord('a') - key) % 26 + ord('a'))
                encrypted += chr((ord(text) - ord('a') + key) % 26 + ord('a'))
            elif text.isupper():
                decrypted += chr((ord(text) - ord('A') - key) % 26 + ord('A'))
                encrypted += chr((ord(text) - ord('A') + key) % 26 + ord('A'))
          else:
            decrypted += text
            encrypted += text
      print(f"[red]Decrypted: [red bold]{decrypted}")
      print(f"[green]Encrypted: [green bold]{encrypted}")
        
  elif(message!=None and key==0 or key>25):
   for key in range(1,26): 
    decrypted=''
    for text in message:
        if text.isalpha():
            if text.islower():
                decrypted += chr((ord(text) - ord('a') - key) % 26 + ord('a'))
            elif text.isupper():
                decrypted += chr((ord(text) - ord('A') - key) % 26 + ord('A'))
        else:
            decrypted += text
    print(f"Key {key}: {decrypted}")
  
  else:
    print("Invalid")  
    
    
@app.command('reverse')
def reverse(message,encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
  if not encrypt:  
    i=len(message)-1
    decrypted=''
    while i >= 0:
     decrypted = decrypted + message[i]
     i = i - 1
    print(f"[red bold]{decrypted}")
  else: 
    encrypted = message[::-1]
    print(f'[green]Encrypted: [green bold]{encrypted}')
              
              
@app.command('atbash')
def atbash(message,encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    decrypted = ""
    for text in message:
        if text.isalpha():
            if text.islower():
                decrypted += chr(ord('z') - (ord(text) - ord('a')))
            elif text.isupper():
                decrypted += chr(ord('Z') - (ord(text) - ord('A')))
        else:
            decrypted += text
    if encrypt:
     print(f'[green]Encrypted: [green bold]{decrypted}')
    else:
     print(f'[red bold]{decrypted}')
    
    
@app.command('vignere')
def vigenere(message, key, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    if not encrypt:
        decrypted = ""
        key_length = len(key)
        index = 0
        for text in message:
            if text.isalpha():
                if text.islower():
                    decrypted += chr((ord(text) - ord(key[index].lower()) + 26) % 26 + ord('a'))
                elif text.isupper():
                    decrypted += chr((ord(text) - ord(key[index].upper()) + 26) % 26 + ord('A'))
                index = (index + 1) % key_length
            else:
                decrypted += text
        print(f'[red bold]{decrypted}')
    else:
        message = message.lower()
        key = key.lower()

        encrypted = ""
        key_index = 0

        for char in message:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                encrypted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
                encrypted += encrypted_char
                key_index += 1
            else:
                encrypted += char

        print(f'[green]Encrypted: [green bold]{encrypted}')

        

@app.command('rail-fence')
def decryptRailFence(message, key:int, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    if encrypt:
        rail = [['\n' for i in range(len(message))]
                for j in range(key)]
     
        dir_down = False
        row, col = 0, 0
     
        for i in range(len(message)):
         
         if (row == 0) or (row == key - 1):
            dir_down = not dir_down
         
         rail[row][col] = message[i]
         col += 1
         
         if dir_down:
            row += 1
         else:
            row -= 1
            
        result = []
        for i in range(key):
         for j in range(len(message)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
        print(f"[green]Encrypted: [green bold]{''.join(result)}")
    
    else:
        
        rail = [['\n' for i in range(len(message))]
                for j in range(key)]
     
        dir = None
        row, col = 0, 0
     
        for i in range(len(message)):
         if row == 0:
            dir = True
         if row == key - 1:
            dir = False
        
         rail[row][col] = '*'
         col += 1
         
         if dir:
            row += 1
         else:
            row -= 1
             
        index = 0
        for i in range(key):
          for j in range(len(message)):
            if ((rail[i][j] == '*') and
            (index < len(message))):
                rail[i][j] = message[index]
                index += 1
         
        result = []
        row, col = 0, 0
        for i in range(len(message)):
         
         if row == 0:
            dir = True
         if row == key-1:
            dir = False
             
         if (rail[row][col] != '*'):
            result.append(rail[row][col])
            col += 1
             
         if dir:
            row += 1
         else:
            row -= 1
        print(f"[red bold]{''.join(result)}")
                        
                 
@app.command('brainfuck')
def brainfuck(code):
    def cleanup(code):
        return "".join(c for c in code if c in "><+-.,[]")

    def find_loop_starts(code):
        loop_starts = {}
        stack = []
        for i, c in enumerate(code):
            if c == "[":
                stack.append(i)
            elif c == "]":
                start = stack.pop()
                loop_starts[start] = i
                loop_starts[i] = start

        return loop_starts
    code = cleanup(code)
    memory = [0] * 30000
    pointer = 0
    output = ""
    loop_starts = find_loop_starts(code)
    i = 0
    while i < len(code):
        command = code[i]
        if command == ">":
            pointer = (pointer + 1) % len(memory)
        elif command == "<":
            pointer = (pointer - 1) % len(memory)
        elif command == "+":
            memory[pointer] = (memory[pointer] + 1) % 256
        elif command == "-":
            memory[pointer] = (memory[pointer] - 1) % 256
        elif command == ".":
            output += chr(memory[pointer])
        elif command == ",":
            pass
        elif command == "[":
            if memory[pointer] == 0:
                i = loop_starts[i]
        elif command == "]":
            if memory[pointer] != 0:
                i = loop_starts[i]

        i += 1
    with typer.progressbar(range(100), label="Decrypting...") as progress:
            for value in progress:
                time.sleep(0.01)  
    print(f'[red bold]{output}')


@app.command('base64')
def base64decode(message:str,encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    if not encrypt:
        bytes = base64.b64decode(message)
        decrypted = bytes.decode('utf-8')  
        print(f'[red bold]{decrypted}')
    else:
     encoded_bytes = base64.b64encode(message.encode('utf-8'))
     encrypted = encoded_bytes.decode('utf-8')
     print(f'[green]Encrypted: [green bold]{encrypted}')

  
@app.command('base32')   
def base64decode(message,encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,
    ) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(2.5)
    if not encrypt:
        bytes = base64.b32decode(message)
        decrypted = bytes.decode('utf-8')  
        print(f'[red bold]{decrypted}')
    else:
        bytes = base64.b32encode(message.encode('utf-8'))
        encrypted = bytes.decode('utf-8') 
        print(f'[green]Encrypted: [green bold]{encrypted}')
  

@app.command('base91')
def decode_base91(message,encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,
    ) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\""
    if not encrypt:
        base91_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$','%', '&', '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=','>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '"']

        decode_table = dict((v,k) for k,v in enumerate(base91_alphabet))
        v=-1
        b=0
        n = 0
        decrypted = bytearray()
        for strletter in message:
            if not strletter in decode_table:
                continue
            c = decode_table[strletter]
            if(v < 0):
                v = c
            else:
                v += c*91
                b |= v << n
                n += 13 if (v & 8191)>88 else 14
                while True:
                    decrypted += struct.pack('B', b&255)
                    b >>= 8
                    n -= 8
                    if not n>7:
                        break
                v = -1
        if v+1:
            decrypted += struct.pack('B', (b | v << n) & 255 )
        print(f'[red bold]{decrypted.decode('utf-8')}')
    
    else:
        
        bytes_text = message.encode('utf-8')
        encrypted = ""
        value = 0
        n = 0
        for byte in bytes_text:
            value |= byte << n
            n += 8
            if n >= 13:
                digit = value & 8191
                if digit > 88:
                    value >>= 13
                    n -= 13
                else:
                    digit = value & 16383
                    value >>= 14
                    n -= 14
                encrypted += set[digit % 91] + set[digit // 91]
        if n:
            encrypted += set[value % 91]
            if n > 7 or value >= 91:
                encrypted += set[value // 91]
                
        print(f'[green]Encrypted: [green bold]{encrypted}')
    
                           

@app.command('affine')
def affine(message:str, a:int, b:int, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='red'),
        transient=True,
    ) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(3)
        
    def mod_inverse(a, m):
        for i in range(m):
            if (a * i) % m == 1:
                return i
        return None
    if not encrypt:
        decrypted = ""
        m = 26  
        a_inv = mod_inverse(a, m)
        if a_inv is None:
            print("[red]'a' must be coprime with 26")

        for char in message:
            if char.isalpha():
                if char.islower():
                    char = char.upper()
                    decrypted_char = chr(((ord(char) - ord('A') - b) * a_inv) % m + ord('A'))
                    decrypted += decrypted_char.lower() 
                else:
                    decrypted_char = chr(((ord(char) - ord('A') - b) * a_inv) % m + ord('A'))
                    decrypted += decrypted_char
            else:
                decrypted += char

        print(f'[red bold]{decrypted}')
    else:
        encrypted=''
        for char in message: 
            if char.isalpha():
                char_offset = ord('A') if char.isupper() else ord('a')
                char_convert = chr(((a * (ord(char) - char_offset) + b) % 26) + char_offset)
                encrypted+=char_convert
            else:
                encrypted += char
        print(f'[green]Encrypted: [green bold]{encrypted}')


@app.command('playfair') 
def playfair_cipher(key, message, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress( 
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    def generate_playfair_matrix(key):
        key = key.replace(" ", "")
        key = key.replace("J", "I")
        key = "".join(dict.fromkeys(key))  # Remove duplicate characters
        alphabet='abcdefghiklmnopqrstuvwxyz'   
        matrix = ""
        for char in key:
            if char in alphabet:
                matrix += char
                alphabet = alphabet.replace(char, "")
        matrix += alphabet
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_coordinates(matrix, char):
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)

    def encryptplayfair(message, matrix):
        message = message.replace(" ", "")
        if len(message) % 2 != 0:
            message += "x"
        encrypt = ""
        for i in range(0, len(message), 2):
            char1 = message[i]
            char2 = message[i+1]
            row1, col1 = find_coordinates(matrix, char1)
            row2, col2 = find_coordinates(matrix, char2)
            if row1 == row2:  
                encrypt += matrix[row1][(col1 + 1) % 5]
                encrypt += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  
                encrypt += matrix[(row1 + 1) % 5][col1]
                encrypt += matrix[(row2 + 1) % 5][col2]
            else:  
                encrypt += matrix[row1][col2]
                encrypt += matrix[row2][col1]
        print(f'[green]encrypted: [green bold]{encrypt}')

    def decryptplayfair(message, matrix):
        decrypt = ""
        if len(message) % 2 != 0:
            message += "x"
        for i in range(0, len(message), 2):
            char1 = message[i]
            char2 = message[i+1]
            row1, col1 = find_coordinates(matrix, char1)
            row2, col2 = find_coordinates(matrix, char2)
            if row1 == row2:  
                decrypt += matrix[row1][(col1 - 1) % 5]
                decrypt += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  
                decrypt += matrix[(row1 - 1) % 5][col1]
                decrypt += matrix[(row2 - 1) % 5][col2]
            else:  
                decrypt += matrix[row1][col2]
                decrypt += matrix[row2][col1]
        print(f'[red bold]{decrypt}')
    
    key=key.lower()
    message=message.lower()
    matrix = generate_playfair_matrix(key)
    if encrypt:
        return encryptplayfair(message, matrix)
    else:
        return decryptplayfair(message, matrix)
       
        
@app.command('vernam')
def vernam(message, key, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
    if encrypt:
        message=message.replace(" ","")
        key=key.replace(" ","")
        message=message.lower()
        key=key.lower()

        if(len(message)!=len(key)):
            print("Lengths are different")
            
        else:
            encrypted=""
            
            for i in range(len(message)):
                k1=ord(message[i])-97
                k2=ord(key[i])-97
                s=chr((k1+k2)%26+97)
                encrypted+=s
            print(f"[green]Enrypted: [green bold]{encrypted}")
    else:
        message=message.lower()
        key=key.lower()
        message=message.replace(" ","")
        key=key.replace(" ","")
        
        decrypted=""
        
        for i in range(len(message)):
            k1=ord(message[i])-97
            k2=ord(key[i])-97
            s=chr((((k1-k2)+26)%26)+97)
            decrypted+=s
        print(f'[red bold]{decrypted}')

@app.command('columnar-transposition')
def columnar_transposition(message, key, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='circleHalves', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='green' if encrypt else 'purple'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decrypting...", total=None)
        else:
         progress.add_task(description="Encrypting...", total=None)
        time.sleep(1.5)
        if encrypt:
            encrypted = ""
            k_indx = 0
            msg_len = float(len(message))
            msg_lst = list(message)
            key_lst = sorted(list(key))
            col = len(key)
            row = int(math.ceil(msg_len / col))
         
            fill_null = int((row * col) - msg_len)
            msg_lst.extend('_' * fill_null)
         
            matrix = [msg_lst[i: i + col] 
                    for i in range(0, len(msg_lst), col)]
        
            for _ in range(col):
                curr_idx = key.index(key_lst[k_indx])
                encrypted += ''.join([row[curr_idx] 
                                for row in matrix])
                k_indx += 1
        
            print(f'[green]Encrypted: [green bold]{encrypted}')
        else:
            flag=0
            decrypted = ""
            k_indx = 0
            msg_indx = 0
            msg_len = float(len(message))
            msg_lst = list(message)
            col = len(key)
            row = int(math.ceil(msg_len / col))
            key_lst = sorted(list(key))
            dec_cipher = []
            for _ in range(row):
                dec_cipher += [[None] * col]
            for _ in range(col):
                curr_idx = key.index(key_lst[k_indx])
        
                for j in range(row):
                    dec_cipher[j][curr_idx] = msg_lst[msg_indx]
                    msg_indx += 1
                k_indx += 1
            try:
                decrypted = ''.join(sum(dec_cipher, []))
            except TypeError:
                raise TypeError("This program cannot",
                                "handle repeating words.")
        
            null_count = decrypted.count('_')
        
            if null_count > 0:
                print(f'[red bold]{decrypted[: -null_count]}')
                flag=1
            if flag==0:
             print(f'[red bold]{decrypted}')

@app.command('morse')
def morse_cipher(message:str, encrypt: Annotated[bool, typer.Option("--encrypt","-e",help='To encrypt')]=False):
    with Progress(
        SpinnerColumn(spinner_name='point', style=None),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(style='yellow'),
        transient=True,) as progress:
        if not encrypt:
         progress.add_task(description="Decoding...", total=None)
        else:
         progress.add_task(description="Encoding...", total=None)
        time.sleep(1.5)
    morse_dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
    result = ''
    if encrypt:
        for char in message.upper():
            if char != ' ':
                result += morse_dict.get(char, char) + ' '
            else:
                result += ' '
        print(f'[yellow]Morse: [yellow bold]{result}')
    else:
        message += ' '
        decipher = ''
        mycitext = ''
        for myletter in message:
            # checks for space
            if (myletter != ' '):
                i = 0
                mycitext += myletter
            else:
                i += 1
                if i == 2 :
                    decipher += ' '
                else:
                    decipher += list(morse_dict.keys())[list(morse_dict.values()).index(mycitext)]
                    mycitext = ''
        print(f'[yellow]{decipher}')
