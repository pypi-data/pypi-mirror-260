from SqlBase import SqlBase


class FilaRepository(SqlBase):
    def __init__(self,strConn):
        super(FilaRepository, self).__init__(strConn)

    def selectUsuario(self,userName):
        sqlString = (f'''CALL Pr_Lista_Usuarios_RPA({userName})''')
        output = super(FilaRepository, self).execProc(sqlString)
        return next((e for e in output), 0)
    
    def insereUsuarioExpirado(self, user):
        sqlString = f'UPDATE rpatb_usuarios SET rpatb_int_status = 3 WHERE Tp003_pk_Id = ?'
        super(FilaRepository, self).execute(sqlString, (user.id))
    
    

    

