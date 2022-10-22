#!env\Scripts\python.exe

import os, sqlite3, json, base64
from win32 import win32crypt  
from Crypto.Cipher import AES

def descriptografa_aes (texto_criptografado, chave):
    """Descriptografa a senha informada"""
    vetor_inicializacao = texto_criptografado[3:15]
    senha = texto_criptografado[15:-16]
    cifra = AES.new(chave, AES.MODE_GCM, vetor_inicializacao)
    senha_em_claro = cifra.decrypt(senha).decode()
    return senha_em_claro

with open ('Local State') as file:
    dados = json.load(file)

chave = base64.b64decode(dados['os_crypt']['encrypted_key'])
chave = chave[5:] # Remove o sufixo DPAPI
chave = win32crypt.CryptUnprotectData(chave, None, None, None, 0)[1]

print (f'Chave encontrada: {chave}')
pergunta = input('Gerar arquivo com os dados de login? (s/n): ')
if pergunta != 's' and pergunta != 'S':
    os._exit(0)

conn = sqlite3.connect('Login Data')
cursor = conn.cursor()
cursor.execute("""
SELECT action_url, username_value, password_value FROM logins
""")
print('Gravando o arquivo txt...')
with open('logins_chrome.txt', 'w') as arquivo:
    for linha in cursor.fetchall():
        print (f'url:{linha[0]}', file = arquivo)
        print (f'username: {linha[1]}', file = arquivo)
        try:
            print (f'password: {descriptografa_aes(linha[2], chave)}', file = arquivo)
        except:
            print ('password: Não encontrado',  file = arquivo)
        print('-'*50,  file = arquivo)

conn.close()

input('Programa concluído!')