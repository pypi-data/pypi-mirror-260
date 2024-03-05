from sisbrDesktop import sisbr


class loginSisbrDesktop():

    def __init__(self, conStr, key, userName):
        self.sisbr2 = sisbr(conStr)
        self.key = key
        self.userName = userName


    def loginSisbr(self):
        try:
            self.sisbr2.loginSisbr2(key= self.key, nomeUsuario= self.userName)
        except Exception as err:
            print(err)
