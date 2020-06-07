import qrcode
from datetime import datetime as dt
from config import friends # from config.py (not commited in Git)

LETTRES = "ABCDEFGHIJ"
DICO = { LETTRES[i]:str(i) for i in range(10) }

# Le fichier config.py doit contenir un dictionnaire friends défini par exemple comme suit :

# friends = [ {'id':'abcd1234', 'name':'Alice'},
#             {'id':'edfg5678', 'name':'Bob'}]

def char2time(code, dico):
    """
    Calcule le timestamp POSIX à partir du code alphanumérique du timestamp.
    
    Parameters:
        code (str): le code alphanumérique
        dico (str): le dictionnaitre pour décoder le code (correspondance entre lettre et chiffre)

    Returns:
        int: Timestamp POSIX
    """
    timestamp = int(''.join([dico[i] for i in code])) / 1000

    return timestamp

def time2char(qr_time, dico):
    """
    Calcule le code alphanumérique à partir d'un datetime.
    
    Parameters:
        qr_time (dt): le datetime à convertir
        dico (str): le dictionnaitre pour décoder le code (correspondance entre lettre et chiffre)

    Returns:
        str: Code alphanumérique
    """
    qr_timestamp = qr_time.timestamp() * 1000
    qr_timestamp_str = str(qr_timestamp)[:13]
    print(f'qr_timestamp_str={qr_timestamp_str}')
    return ''.join([LETTRES[int(i)] for i in qr_timestamp_str])


def create_qrcode(friend, dico):
    """
    Crée un QR Code compatible.
    
    Parameters:
        friend (dict): un dictionnaire décrivant l'ami : {'id':'abcd', 'name':'mon_nom'}
        dico (str): le dictionnaitre pour décoder le code (correspondance entre lettre et chiffre)

    """
    now = dt.now()
    data = ','.join(['4', friend['id'], time2char(now, DICO)])

    img =  qrcode.make(data)

    filename = 'img/' + friend['name'] + now.strftime('%Y%m%d%H%M%S') + '.png'

    img.save(filename)

    return

if __name__ == '__main__':

    for f in friends:
        create_qrcode(f, DICO)

