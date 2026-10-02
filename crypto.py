from cryptography.fernet import Fernet


# Gerar chave (faça isso uma vez e guarde em arquivo seguro)
def gerar_chave():
    chave = Fernet.generate_key()

    return chave
#print(chave)

#print(fernet)

##senha = "minhaSenha123"

def cripto_dados(chave_resgate, senha):
    fernet = Fernet(chave_resgate)

# Criptografar
    senha_criptografada = fernet.encrypt(senha.encode()).decode()
    return senha_criptografada
#print(senha_criptografada)

# --- Para recuperar depois ---
def recuperar_cripto(chave_resgate, senha_criptografada):
    fernet = Fernet(chave_resgate)
    senha_original = fernet.decrypt(senha_criptografada.encode()).decode()
    return senha_original
#print("Senha recuperada:", senha_original)
