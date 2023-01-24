import logging
import os


import requests
verify_ssl = True


def find_string(c, start_str, end_str):
    pos = c.find(start_str) + len(start_str)
    posf = c[pos:].find(end_str)
    return c[pos:pos + posf]

EMAIL = "FILL ME"
PASSWORD = ""


def get_credentials(email, password):
    try:
        # All cookies will be stored here
        s = requests.Session()
        # Obtener cookies de session logandose
        data = {"Email": email, "Password": password}
        x = s.post('https://portal.studer-innotec.com/User/Login',
                    data=data, verify=verify_ssl, allow_redirects=False)

        # Obtener el ID de la instalacion (para luego llamar a la API)
        x = s.get("https://portal.studer-innotec.com/Installation/", verify=verify_ssl)

        content = str(x.content)
        installation_id = find_string(content, '"Id":', ",")

        # Obtener las claves para llamar a la API
        x = s.get("https://portal.studer-innotec.com/Installation/Synoptic", verify=verify_ssl)
        content = str(x.content)
        phash = find_string(content, "\\'PHASH\\', \\'", "\\'")
        uhash = find_string(content, "\\'UHASH\\', \\'", "\\'")
    except Exception as exc:
        logging.error(exc)
    return phash, uhash, installation_id 

def get_data():
    try:
        # Llamar a la API para obtener los datos en json de la instalacion especificada
        s = requests.Session()
        headers = {"UHASH": UHASH, "PHASH": PHASH}
        x = s.get("https://api.studer-innotec.com/api/v1/installation/synoptic/{}".format(INSTALLATION_ID),
                  headers=headers,
                  verify=verify_ssl)
        if not x.ok:
            raise Exception(x)

        data = x.json()
        logging.debug(data)
    except Exception as exc:
        logging.error(exc)
    return data

PHASH, UHASH, INSTALLATION_ID = get_credentials(EMAIL, PASSWORD)
