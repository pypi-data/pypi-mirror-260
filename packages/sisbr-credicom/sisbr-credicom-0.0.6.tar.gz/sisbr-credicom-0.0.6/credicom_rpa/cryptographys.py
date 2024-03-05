import cryptocode

def encrypt(text,key):
    MensagemCriptografada = cryptocode.encrypt(text, key)
    print("Sua mensagem criptografada: " + MensagemCriptografada)
    return MensagemCriptografada

def decrypt(text, key):
    MensagemDescriptografada = cryptocode.decrypt(text, key)
    print("Sua mensagem descriptografada: " + MensagemDescriptografada)
    return MensagemDescriptografada