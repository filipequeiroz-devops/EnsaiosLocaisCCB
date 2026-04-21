import re

tipo    = "email"
contato = "teste@teste.com"
padrao  = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
if tipo == "email":   
        a = re.match(padrao, contato) is not None
        if a:
                contato = contato
        else:
                contato = "Contato inválido"  