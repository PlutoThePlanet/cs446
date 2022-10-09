#Set up a docker environment for this code, and don't try to include superfluous packages!
from PIL import Image, ImageDraw
import csv
from scipy import constants
import numpy as np
import os
from OpenSSL import crypto, SSL
import socket
from os.path import exists, join

color = 128 * np.ones(shape=[3], dtype=np.uint8)
tuplevals = tuple(color)
im = Image.new('RGB', (512, 512), tuplevals)
draw = ImageDraw.Draw(im)
draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
draw.text((100, 200), "You did it!", fill=(int(constants.speed_of_light), 0, 0))
im.save( "pythonCode2Image.png")

try:
    with open('temp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
except:
    pass

country = "US"
state = "Nevada"
city = "Reno"
org = "University of Nevada, Reno"
orgunit = "CSE"
cn = socket.gethostname()

# cmd = ""

PUBKEY_FILE = "pmortensen_publicKey.PEM"
PRIVKEY_FILE = "pmortensen_privateKey.PEM"
CERT_FILE = "pmortensen_selfSignedCertificate.crt"

def create_self_signed_cert(cert_dir="."):
    ss_cert = join(cert_dir, CERT_FILE)
    priv_key = join(cert_dir, PRIVKEY_FILE)

    if not exists(ss_cert) or not exists(priv_key):

        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.get_subject().C = country
        cert.get_subject().ST = state
        cert.get_subject().L = city
        cert.get_subject().O = org
        cert.get_subject().OU = orgunit
        cert.get_subject().CN = cn

        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(157680000) # 5 years
        cert.set_serial_number(42)
        cert.sign(k, 'sha512')
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)

        open(ss_cert, "wt").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(priv_key, "wt").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    # Rather than generating the public key from the command line, import os, and use os.system to run the command in the last step.
    