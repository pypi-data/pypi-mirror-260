__version__=0.14
def info():
    print("CodeTool",str(__version__))

#Secure_id

import random
from random import sample
lettremin=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
lettremaj=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
chiffre=["0","1","2","3","4","5","6","7","8","9"]
def secureid_sid1():
    ensemble=lettremin+lettremaj+chiffre
    random.shuffle(ensemble)
    boucle=int(random.choice(chiffre))
    for i in range(boucle):
        random.shuffle(ensemble)
    code=random.randint(1000,9999)
    result=str(code)
    certif=""
    for i in range(8):
        if random.randint(0,1)==1:
            certif+=str(random.choice(lettremaj))
        else:
            certif+=str(random.choice(lettremin))
    certiflong=certif*code
    lettre=certiflong[code]
    result+="-"+certif
    result+="-"+lettre
    court=""
    for i in range(3):
        court=""
        for i in range(4):
            court+=str(random.choice(ensemble))
        result+="-"+court
    longstr=""
    for i in range(24):
        longstr+=str(random.choice(ensemble))
    result+="-"+longstr
    result+="-1"
    return(result)
def secureid_sid2():
    ensemble=lettremin+lettremaj+chiffre
    random.shuffle(ensemble)
    boucle=int(random.choice(chiffre))
    for i in range(boucle):
        random.shuffle(ensemble)
    code=random.randint(100000,999999)
    result=str(code)
    certif=""
    for i in range(12):
        if random.randint(0,1)==1:
            certif+=str(random.choice(lettremaj))
        else:
            certif+=str(random.choice(lettremin))
    certiflong=certif*code
    lettre=certiflong[code]
    result+="-"+certif
    result+="-"+lettre
    court=""
    for i in range(3):
        court=""
        for i in range(4):
            court+=str(random.choice(ensemble))
        result+="-"+court
    longstr=""
    for i in range(24):
        longstr+=str(random.choice(ensemble))
    result+="-"+longstr
    result+="-2"
    return(result)

#Indecode

import random
from PIL import Image
import os
text="hello world"
carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
class IndecodeCodeError(Exception):
    pass
class IndecodeDecodeError(Exception):
    pass
class IndecodeKeyElementError(Exception):
    pass
class IndecodeKeyLengthError(Exception):
    pass
class IndecodeImageNotFoundError(Exception):
    pass
def indecode_generate_key(seed:int=None):
    if seed==None:
        carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
        random.shuffle(carac)
        key=""
        for i in range(len(carac)):
            key=key+carac[i]
        return key
    else:
        carac=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","&","é","~",'"',"#","{","}","(",")","[","]","-","è","_","\\","ç","^","à","@","°","+","=","ê","ë","$","£","%","ù","µ","*",",","?",".",";",":","/","!","§"]
        random.Random(seed).shuffle(carac)
        key=""
        for i in range(len(carac)):
            key=key+carac[i]
        return key
def indecode_code(text:str,key:str):
    newtext=""
    incode={}
    if not type(text)==str:
        raise TypeError("text argument must be a string")
    if not type(key)==str:
        raise TypeError("key argument must be a string")
    keylist=list(key)
    if not len(keylist)==len(carac):
        raise IndecodeKeyLengthError("the key is not of the expected length.")
    for i in range(len(keylist)):
        if not keylist[i] in carac:
            raise IndecodeKeyElementError("'"+keylist[i]+"' must not be in the key.")
    for i in range(len(key)):
        incode.update({carac[i]:key[i]})
    incode.update({" ":" "})
    incode.update({"'":"'"})
    for i in range(len(text)):
        if not text[i] in incode:
            raise IndecodeCodeError("'"+text[i]+"' is not encodable.")
        newtext=newtext+incode[text[i]]
    return newtext
def indecode_decode(text:str,key:str):
    newtext=""
    uncode={}
    if not type(text)==str:
        raise TypeError("text argument must be a string")
    if not type(key)==str:
        raise TypeError("key argument must be a string")
    keylist=list(key)
    if not len(keylist)==len(carac):
        raise IndecodeKeyLengthError("the key is not of the expected length.")
    for i in range(len(keylist)):
        if not keylist[i] in carac:
            raise IndecodeKeyElementError("'"+keylist[i]+"' must not be in the key.")
    for i in range(len(key)):
        uncode.update({key[i]:carac[i]})
    uncode.update({" ":" "})
    uncode.update({"'":"'"})
    for i in range(len(text)):
        if not text[i] in uncode:
            raise IndecodeDecodeError("'"+text[i]+"' is not decodable.")
        newtext=newtext+uncode[text[i]]
    return newtext
def indecode_get_key_with_img(image:str):
    if os.path.exists(image):
        img=Image.open(image)
        seed=int(img.width)/10*300+int(img.height)/20*600
        return indecode_generate_key(seed)
    else:
        raise IndecodeImageNotFoundError("'"+image+"' not found.")
    
#Hashint

hash_carac=['.', '~', '7', ']', 'z', '3', 'B', 'f', ':', 'R', '_', '+', 'é', '2', ',', 'ù', 'E', 'J', '°', 'F', 'i', '5', 'e', 'S', 'G', 'à', 'T', 'k', 'l', '§', '"', '0', 'I', '{', 'A', '/', 'K', '!', 'g', 'o', '?', '#', 'C', 'n', 'è', 'w', '*', ')', 'ë', 'V', 'D', 'H', '6', ' ', '^', 'ê', '-', 'd', ';', 'c', 't', 'U', 'v', '1', 'µ', 'Q', '8', 'm', '$', 'u', 'q', '[', '9', 'X', 'ç', 'a', '£', 'p', '=', 'M', 'h', 'W', '4', 'r', 'P', 's', 'Y', '%', 'N', '}', '(', '@', ',', 'y', 'Z', '&', 'L', 'x', 'O', '\\', 'b', 'j',"'"]
carat=""
class HashintError(Exception):
    pass
for i in range(len(hash_carac)):
    carat=carat+hash_carac[i]
def hash64(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+64)**64).endswith("0"):
                cara=str((hash_carac.index(text[i])+64)**64)[::str((hash_carac.index(text[i])+64)**64).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+64)**64)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash128(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+128)**128).endswith("0"):
                cara=str((hash_carac.index(text[i])+128)**128)[::str((hash_carac.index(text[i])+128)**128).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+128)**128)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash256(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+256)**256).endswith("0"):
                cara=str((hash_carac.index(text[i])+256)**256)[::str((hash_carac.index(text[i])+256)**256).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+256)**256)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash512(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+512)**512).endswith("0"):
                cara=str((hash_carac.index(text[i])+512)**512)[::str((hash_carac.index(text[i])+512)**512).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+512)**512)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash1024(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+1024)**1024).endswith("0"):
                cara=str((hash_carac.index(text[i])+1024)**1024)[::str((hash_carac.index(text[i])+1024)**1024).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+1024)**1024)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash2048(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+2048)**2048).endswith("0"):
                cara=str((hash_carac.index(text[i])+2048)**2048)[::str((hash_carac.index(text[i])+2048)**2048).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+2048)**2048)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash4096(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+4096)**4096).endswith("0"):
                cara=str((hash_carac.index(text[i])+4096)**4096)[::str((hash_carac.index(text[i])+4096)**4096).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+4096)**4096)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext
def hash8192(text:str):
    if not type(text)==str:
        raise TypeError("text must be an str")
    newtext=""
    for i in range(len(text)):
        car=text[i]
        if car in hash_carac:
            if str((hash_carac.index(text[i])+8192)**8192).endswith("0"):
                cara=str((hash_carac.index(text[i])+8192)**8192)[::str((hash_carac.index(text[i])+8192)**8192).index("0")]
            else:
                cara=str((hash_carac.index(text[i])+8192)**8192)
                newtext=newtext+cara
        else:
            raise HashintError("'"+car+"' is not hashable")
    return newtext