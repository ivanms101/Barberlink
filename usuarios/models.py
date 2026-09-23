from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager #Import de AbstarcBaseUser y BaseUserManager, necesario para el manejo de usuarios personalizado con Django.

#Mapeo de la tabla ROL
class Rol(models.Model):
    rol_id = models.BigAutoField(primary_key=True, db_column="ROL_ID")
    rol_nomb = models.CharField(max_length=50, db_column="ROL_NOMB")
    rol_desc = models.CharField(max_length=150, db_column="ROL_DESC")

    def __str__(self):
        return self.rol_nomb
    
    #Le dice a Django esto es una tabla usala pero no la modifiques
    class Meta:
        db_table = "ROL"
        managed = False

#Administrador de usuarios
class UsuarioManager(BaseUserManager):
    def create_user(self, usua_doc_id, password, usua_nomb, usua_rol, **extra_fields):
        usuario = self.model(
            usua_doc_id = usua_doc_id,
            usua_nomb = usua_nomb,
            usua_rol = usua_rol,
            **extra_fields
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

#Mapeo de la tabla USUARIOS
class Usuario(AbstractBaseUser):
    last_login = None
    
    usua_id = models.BigAutoField(primary_key=True, db_column="USUA_ID")
    usua_nomb = models.CharField(max_length=100,null=False,db_column="USUA_NOMB")
    usua_tp_doc = models.CharField(max_length=3,null=True,db_column="USUA_TP_DOC")
    usua_doc_id =models.CharField(max_length=50,null=False,unique=True,db_column="USUA_DOC_ID")
    usua_tel = models.CharField(max_length=50, null=True, db_column="USUA_TEL")
    usua_cor = models.CharField(max_length=100, null=True, db_column="USUA_COR")
    password = models.CharField(max_length=255, db_column="USUA_PASS")
    usua_rol = models.ForeignKey(Rol,db_column="USUA_ROL_ID",on_delete=models.DO_NOTHING)
    usua_activo = models.BooleanField(db_column="USUA_ACTIVO", default=True)

    #Conexion con UsuarioManager
    objects = UsuarioManager()

    #Definir el campo que sera el NOMBRE DE USUARIO para LOGIN
    USERNAME_FIELD = "usua_doc_id"
    #Datos requeridos para crear un usuario
    REQUIRED_FIELDS = ["usua_nomb"]

    class Meta:
        db_table = "USUARIOS"
        managed = False