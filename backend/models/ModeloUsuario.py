from .entidad.EntidadUsuario import User


class modeloUsuario():
    
    @classmethod
    def filtrarUsuario(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select usuarios.idusuario, usuario, contraseña, email, contraseñatemp, idperfil from usuarios inner join usuariosperfiles on usuarios.idusuario = usuariosperfiles.idusuario where usuario = %s")
            cur.execute(consulta, [str(user.usuario)])
            filtro = cur.fetchone()
            return filtro
        except Exception as ex:
            print(ex)
            raise Exception(ex)
            
    @classmethod
    def filtrarEmail(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select usuarios.idusuario, usuario, contraseña, email, contraseñatemp, idperfil from usuarios inner join usuariosperfiles on usuarios.idusuario = usuariosperfiles.idusuario where email = %s")
            cur.execute(consulta, [str(user.email)])
            filtro = cur.fetchone()
            return filtro
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def logearUsuario(self, mysql, user):
        try:
            row = modeloUsuario.filtrarUsuario(mysql, user)
            if row != None:
                temp = row[4]
                if temp != None:
                    temp = User.checkpassword(temp, user.contraseña)
                else:
                    temp = False
                user = User(row[0], row[1], User.checkpassword(row[2], user.contraseña), row[3], temp, row[5])
                return user
            else:
                row = modeloUsuario.filtrarEmail(mysql, user)
                if row != None:
                    temp = row[4]
                    if temp != None:
                        temp = User.checkpassword(temp, user.contraseña)
                    else:
                        temp = False
                    user = User(row[0], row[1], User.checkpassword(row[2], user.contraseña), row[3], temp, row[5])
                    return user
                else:
                    return None
            
        except Exception as ex:
            print(ex)
            raise Exception(ex)
    
    @classmethod
    def crearUsuario(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ('INSERT INTO usuarios (usuario, contraseña, email) VALUES (%s, %s,%s)')
            hashContraseña = User.generarhash(user.contraseña)
            cur.execute(consulta, [str(user.usuario),hashContraseña,str(user.email)])
            mysql.connection.commit()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def comprobarEmail(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ('SELECT email, idusuario FROM usuarios WHERE email = %s')
            cur.execute(consulta,[(user.email)])
            row = cur.fetchone()   
            
            ema = str(row[0])
            id = int(row[1])
            if user.email == ema:
                cur.execute('UPDATE usuarios SET contraseñatemp = %s WHERE idusuario = %s', (str(
                    User.generarhash(user.contraseñatemp)), id))
                mysql.connection.commit()    
                          
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def conseguirID(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            sql = 'SELECT usuarios.idusuario, usuario, email, idperfil FROM usuarios inner join usuariosperfiles on usuarios.idusuario = usuariosperfiles.idusuario WHERE usuarios.idusuario = %s'
            cur.execute(sql, (id))
            row = cur.fetchone()
            if row != None:
                return User(row[0], row[1],None, row[2], None, row[3])
            else:
                return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)
