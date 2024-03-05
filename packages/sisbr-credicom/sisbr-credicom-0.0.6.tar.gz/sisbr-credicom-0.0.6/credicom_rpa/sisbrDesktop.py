from time import sleep
from pyUtils import comparaStr
from cryptographys import decrypt
from FilaRepository import FilaRepository
# Import for the Desktop Bot
from botcity.core import DesktopBot


class sisbr(ComputerVision):
    def __init__(self, conStr) -> None:
        self.bot = DesktopBot()
        self.data = FilaRepository(conStr)
        print(self.bot.display_size())

    def loginSisbr2(self, key, nomeUsuario):
        user = self.data.selectUsuario() 
        # bot.login(user)    
        if user.id:
            cmdLine = "C:\\Sisbr 2.0\\Sisbr 2.0.exe" 
            self.bot.execute(cmdLine)
            
            if not self.bot.find( "refAtualizacaoSisbr", matching=0.97, waiting_time=10000):
                sleep(50)
            if not self.bot.find( "refTelaLogin", matching=0.97, waiting_time=100000):
                self.not_found("refTelaLogin")
            
            
            if not self.bot.find( "inputUsuario", matching=0.97, waiting_time=10000):
                self.not_found("inputUsuario")
            self.bot.click_relative(131, 5)
            
            comparaStr(self.bot, user.usuario)
            
            if not self.bot.find( "inputSenha", matching=0.97, waiting_time=10000):
                self.not_found("inputSenha")
            self.bot.click_relative(105, 7)
            
            self.bot.type_keys(decrypt(user.senha, key))

            self.bot.enter()
            
            if self.bot.find( "refSenhaExpirada", matching=0.97, waiting_time=10000):
                self.data.insereUsuarioExpirado(user)
                raise Exception('senha expirada')
            
            self.bot.find( "refLogado", matching=0.97, waiting_time=90000)
        else:
            print('sem usuário para login no sistema')  
            raise Exception('sem usuário disponível')  
        
        
    def not_found(self,label):
        print(f"Element not found: {label}")
        raise Exception(f'erro element not found: {label}')







































