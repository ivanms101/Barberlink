from django.db import models
from reservas.models import Reserva

class Pago(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="PAGO_ID")
    reserva = models.ForeignKey(Reserva, on_delete=models.DO_NOTHING, db_column="PAGO_REV_ID")
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column="PAGO_VALO")
    metodo = models.CharField(max_length=25, db_column="PAGO_METO")
    estado = models.CharField(max_length=25, db_column="PAGO_ESTD")

    class Meta:
        db_table = "PAGO"
        managed = False