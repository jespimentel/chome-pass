# chrome-passwords

O Chrome oferece a facilidade de salvar senhas dos sites visitados.

As senhas são armazenadas no formato do SQLite3. O banco de dados pode ser localizado em ```C:\Users\<nome do usuário>\AppData\Local\Google\Chrome\User Data\Default\Login Data```.

Selecionando-se os campos ```action_url, username_value, password_value``` da tabela ```logins```, obtemos as urls, usuários e senhas (estas criptografadas em AES).

A criptografia AES é do tipo simétrico. Isso quer dizer que a mesma chave é usada para criptografar e descriptografar o texto. Para aumentar a segurança, o processo de encriptação usa um "vetor de inicialização" (IV), no caso de 16 bits, que corresponderá aos caracteres das posições 4-20 recuperados de ````password_value````. A senha cifrada corresponderá aos caracteres da posição 21-(N-16), sendo N a última posição da 'string'.

A chave de criptografia/descriptografia está localizada no arquivo JSON existente em ```C:\Users\<nome do usuário>\AppData\Local\Google\Chrome\User Data\Local State```, precedida da chave ```encrypted_key```.

O código encontra a chave no arquivo ```Local State``` e a utiliza para descriptografar as senhas (```password_value```) da tabela ```logins``` do arquivo ```Login Data``` (banco de dados SQLite3). 

Fontes: 
1. https://ohyicong.medium.com/how-to-hack-chrome-password-with-python-1bedc167be3d
1. https://www.freecodecamp.org/portuguese/news/ler-arquivos-json-em-python-como-usar-load-loads-e-dump-dumps-com-arquivos-json/


Obs. 
```pip3 install pycryptodome pypiwin32```