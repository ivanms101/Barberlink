from django.db import models

class Servicio(models.Model):
    serv_id = models.BigAutoField(primary_key=True, db_column= "SERV_ID")
    serv_nomb = models.CharField(max_length=100, db_column = "SERV_NOMB")
    serv_tari = models.DecimalField(max_digits=10, decimal_places=2, db_column = "SERV_TARI")
    serv_activo = models.BooleanField(db_column="SERV_ACTIVO", default=True)
    serv_duracion = models.IntegerField(db_column="SERV_DURACION")

    def __str__(self):
        return self.serv_nomb
    
    class Meta:
        db_table = "SERVICIO"
        managed = False