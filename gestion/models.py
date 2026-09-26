from django.db import models
from usuarios.models import Usuario

class Auditoria(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="AUDI_ID")
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column="AUDI_USUA_ID")
    accion = models.CharField(max_length=100, db_column="AUDI_ACCION")
    tabla = models.CharField(max_length=50, db_column="AUDI_TABLA")
    registro = models.BigIntegerField(db_column="AUDI_REG_ID")
    fecha = models.DateTimeField(db_column="AUDI_FECH")
    observacion = models.CharField(max_length=250, db_column="AUDI_OBSV")
    class Meta:
        db_table = "AUDITORIA"
        managed = False