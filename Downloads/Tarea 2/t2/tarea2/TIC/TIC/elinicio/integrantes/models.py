from django.db import models

# Create your models here.
class Modelochaqueta(models.Model):
	temporada=models.CharField(max_length=30)
	tendencia=models.CharField(max_length=30)



class Cliente(models.Model):
	nombre=models.CharField(max_length=30)
	correo=models.EmailField(max_length=256)
	direccion = models.CharField(max_length=256)
	ciudad = models.CharField(max_length=256)
	numero=models.IntegerField()

class Pedido(models.Model):

	fecha=models.DateField()
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class Infopedido(models.Model):
	total = models.IntegerField()
	medio_pago = models.CharField(max_length=512)
	envio_domicilio = models.CharField(max_length=512)
	retiro_tienda = models.CharField(max_length=512)
	pedido=models.OneToOneField(Pedido,on_delete=models.CASCADE)

class chaqueta(models.Model):
	numero_serie = models.IntegerField()
	talla=models.CharField(max_length=30)
	precio=models.IntegerField()
	modelo = models.ForeignKey(Modelochaqueta, on_delete=models.CASCADE)
	info = models.ForeignKey(Infopedido, on_delete=models.CASCADE)