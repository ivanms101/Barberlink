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

class HorarioDia(models.Model):
    hord_id = models.BigAutoField(primary_key=True, db_column="HORD_ID")
    hord_dia = models.IntegerField(db_column="HORD_DIA")
    hord_activo = models.BooleanField(db_column="HORD_ACTIVO", default=True)
    class Meta:
        db_table = "HORARIO_DIA"
        managed = False

class HorarioFranja(models.Model):
    horf_id = models.BigAutoField(primary_key=True, db_column="HORF_ID")
    hord = models.ForeignKey(HorarioDia, on_delete=models.DO_NOTHING, db_column="HORD_ID")
    horf_hora_inicio = models.TimeField(db_column="HORF_HORA_INICIO")
    horf_hora_fin = models.TimeField(db_column="HORF_HORA_FIN")
    horf_activo = models.BooleanField(db_column="HORF_ACTIVO", default=True)
    class Meta:
        db_table = "HORARIO_FRANJA"
        managed = False