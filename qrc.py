import os
from datetime import datetime as dt
import click
import qrcode
from config import friends # from config.py (not commited in Git)

LETTRES = "ABCDEFGHIJ"
# DICO = { LETTRES[i]:str(i) for i in range(10) }

# Codes pour le 5ème anniversaire
LETTRES5 = "BCDEFGHJKMNPQRST"
HEXA = "0123456789abcdef"
# DICO5 = { HEXA[i]:LETTRES5[i] for i in range(16)}

DICOS = {'4': { LETTRES[i]:str(i) for i in range(10) },
         '5': { HEXA[i]:LETTRES5[i] for i in range(16)}}

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

def time2char(qr_time):
    """
    Calcule le code alphanumérique à partir d'un datetime.
    
    Parameters:
        qr_time (dt): le datetime à convertir

    Returns:
        str: Code alphanumérique
    """
    qr_timestamp = qr_time.timestamp() * 1000
    qr_timestamp_str = str(qr_timestamp)[:13]
    click.echo(f'qr_timestamp_str={qr_timestamp_str}')
    return ''.join([LETTRES[int(i)] for i in qr_timestamp_str])

def generate_data(qr_time, friend, dico, version):
    """
    Calcule le data à mettre dans le QR Code

    Parameters:
        qr_time (dt): le timestamp au format datetime
        friend (str): le code ami
        dico (str): le dictionnaitre pour décoder le code (correspondance entre lettre et chiffre)
        version (int): l'algorithme à utiliser

    Returns:
        str: Code alphanumérique    
    """

    # 4th anniversary
    if version == 4:
        click.echo('----- Version 4 ----')
        data = ','.join(['4', friend['id'], time2char(qr_time)])
    # 5th anniversary
    elif version == 5:
        click.echo('----- Version 5 ----')
        # calculer le timestamp en ms
        qr_timestamp = int(qr_time.timestamp() * 1000)
        # convertir en hexadecimal
        qr_timestamp_hex = hex(qr_timestamp)[2:]
        # remplacer les lettres selon le dico5
        qr_timestamp_code = ''.join([dico[i] for i in qr_timestamp_hex])
        data = '4,'+friend['id']+qr_timestamp_code
    else:
        data = ''

    return data


def create_qrcode(version, friend, output_dir, dico):
    """
    Crée un QR Code compatible pour le 4ème anniversaire.
    
    Parameters:
        friend (dict): un dictionnaire décrivant l'ami : {'id':'abcd', 'name':'mon_nom'}
        dico (str): le dictionnaitre pour décoder le code (correspondance entre lettre et chiffre)

    """
    now = dt.now()
 #   data = ','.join(['4', friend['id'], time2char(now, dico)])
    data =  generate_data(now, friend, dico, version)
    click.echo(f'data={data}')
    img =  qrcode.make(data)

    filename = os.path.join(output_dir, friend['name'] + now.strftime('%Y%m%d%H%M%S') + '.png')

    img.save(filename)

    return now

@click.group()
def cli():
    pass

@cli.command()
@click.option('--dir', type=click.Path(exists=True, dir_okay=True), default='img/')
@click.option('--version', default=4)
def c(dir, version):
    """
    Creates QR Codes
    """
    click.echo(f'dir={dir}')
    for f in friends:
        now = create_qrcode(version, f, dir, DICOS[str(version)])
        click.echo(f'QR code created with timestamp {now}')

@cli.command()
@click.option('--ts', help='encoded timestamp')
def d(ts):
    """
    Decodes timestamp
    """
    click.echo(f'timestamp={ts}')
    click.echo(f'Decoded timestamp={char2time(ts, DICOS["4"])}')

if __name__ == '__main__':
    cli()
