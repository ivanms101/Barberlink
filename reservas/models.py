from django.db import models
from usuarios.models import Usuario
from servicios.models import Servicio

class Reserva(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="RESV_ID")
    cliente = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column="RESV_USUA_CLIE", related_name="resv_clie")
    barbero = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, db_column="RESV_USUA_BARB", related_name="resv_barbero")
    fecha = models.DateField(db_column="RESV_FECH")
    hora = models.CharField(max_length=5, db_column="RESV_HORA")
    estado = models.CharField(max_length=15, db_column="RESV_ESTD")
    class Meta:
        db_table = "RESERVA"
        managed = False

class DetalleReserva(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="DERE_ID")
    reserva = models.ForeignKey(Reserva, on_delete=models.DO_NOTHING, db_column="DERE_RESV_ID", related_name="detalles")
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING, db_column="DERE_SERV_ID", related_name="detalles_reserva")
    class Meta:
        db_table = "DETALLE_RESERVA"
        managed = False