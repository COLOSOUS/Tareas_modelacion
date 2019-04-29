from integrantes.models import chaqueta
from integrantes.models import Cliente
from integrantes.models import Pedido
from integrantes.models import Infopedido
from integrantes.models import Modelochaqueta


Modelo1 = Modelochaqueta(temporada="Verano-Primavera", tendencia="Rock")

Modelo1.save()

Modelo2 = Modelochaqueta(temporada="Verano-Primavera", tendencia="IndieChic")

Modelo2.save()

Modelo3 = Modelochaqueta(temporada="Verano-Primavera", tendencia="Etnic")

Modelo3.save()

Modelo4 = Modelochaqueta(temporada="Verano-Primavera", tendencia="Western")

Modelo4.save()

Modelo5 = Modelochaqueta(temporada="Invierno-Otoño", tendencia="Rock")

Modelo5.save()

Modelo6 = Modelochaqueta(temporada="Invierno-Otoño", tendencia="IndieChic")

Modelo6.save()

Modelo7 = Modelochaqueta(temporada="Invierno-Otoño", tendencia="Etnic")

Modelo7.save()

Modelo8 = Modelochaqueta(temporada="Invierno-Otoño", tendencia="Western")

Modelo8.save()

Modelo9 = Modelochaqueta(temporada="Verano-Primavera", tendencia="Animal Print")

Modelo9.save()

Modelo10 = Modelochaqueta(temporada="Invierno-Otoño", tendencia="Animal Print")

Modelo10.save()


cliente1 = Cliente(nombre="Victor Duran", correo="vduran@gmail.com", direccion="Av. Alessandri 123", ciudad="Rancagua",numero=995672340)
cliente1.save()

cliente2 = Cliente(nombre="Felipe Fica", correo="ffica@gmail.com", direccion="Américo Vespucio 345", ciudad="Santiago",numero=993458762)
cliente2.save()

cliente3 = Cliente(nombre="Carolina Figueroa", correo="cfigueroa@gmail.com", direccion="Las Araucarias 298", ciudad="Temuco",numero=997463542)
cliente3.save()

cliente4 = Cliente(nombre="Javiera Prado", correo="jprado@gmail.com", direccion="Las Hogueras 234", ciudad="Viña del Mar",numero=99467352)
cliente4.save()

cliente5 = Cliente(nombre="Julieta Venegas", correo="jvenegas@gmail.com", direccion="2 Norte 209", ciudad="Viña del Mar",numero=987345601)
cliente5.save()

cliente6 = Cliente(nombre="Cristina Valdes", correo="cvaldes@gmail.com", direccion="Modeda 786", ciudad="Santiago",numero=996374856)
cliente6.save()

cliente7 = Cliente(nombre="Paloma Miranda", correo="pmiranda@gmail.com", direccion="Los Nogales 45", ciudad="Temuco",numero=998762534)
cliente7.save()

cliente8 = Cliente(nombre="Becky Garcia", correo="bgarcia@gmail.com", direccion="Las Urracas 1098 depto. 301", ciudad="La Serena",numero=972367234)
cliente8.save()

cliente9 = Cliente(nombre="Victoria Aldea", correo="valdea@gmail.com", direccion="Aldea del Mar 345", ciudad="Concepcion",numero=912309845)
cliente9.save()

cliente10 = Cliente(nombre="Luna Alvarado", correo="lalvarado@gmail.com", direccion="3 norte 833", ciudad="Viña del Mar",numero=995647364)
cliente10.save()

pedido1 = Pedido(fecha="2019-03-16", cliente=cliente1)
pedido1.save()

pedido2 = Pedido(fecha="2019-05-26", cliente=cliente2)
pedido2.save()

pedido3 = Pedido(fecha="2019-05-28", cliente=cliente3)
pedido3.save()

pedido4 = Pedido(fecha="2019-05-03", cliente=cliente4)
pedido4.save()

pedido5 = Pedido(fecha="2019-06-11", cliente=cliente5)
pedido5.save()

pedido6 = Pedido(fecha="2019-06-23", cliente=cliente6)
pedido6.save()

pedido7 = Pedido(fecha="2019-06-12", cliente=cliente7)
pedido7.save()

pedido8 = Pedido(fecha="2019-06-09", cliente=cliente8)
pedido8.save()

pedido9 = Pedido(fecha="2019-04-12", cliente=cliente9)
pedido9.save()

pedido10 = Pedido(fecha="2019-04-01", cliente=cliente10)
pedido10.save()

Infopedido1 = Infopedido(total=13990, medio_pago="Efectivo", envio_domicilio="No", retiro_tienda="Si",pedido=pedido1)
Infopedido1.save()

Infopedido2 = Infopedido(total=17990, medio_pago="Efectivo", envio_domicilio="No", retiro_tienda="Si",pedido=pedido2)
Infopedido2.save()

Infopedido3 = Infopedido(total=15990, medio_pago="Tarjeta", envio_domicilio="Si", retiro_tienda="No",pedido=pedido3)
Infopedido3.save()

Infopedido4 = Infopedido(total=13990, medio_pago="Efectivo", envio_domicilio="Si", retiro_tienda="No",pedido=pedido4)
Infopedido4.save()

Infopedido5 = Infopedido(total=17990, medio_pago="Tarjeta", envio_domicilio="No", retiro_tienda="Si",pedido=pedido5)
Infopedido5.save()

Infopedido6 = Infopedido(total=14990, medio_pago="Tarjeta", envio_domicilio="Si", retiro_tienda="No",pedido=pedido6)
Infopedido6.save()

Infopedido7 = Infopedido(total=13990, medio_pago="Tarjeta", envio_domicilio="No", retiro_tienda="Si",pedido=pedido7)
Infopedido7.save()

Infopedido8 = Infopedido(total=15990, medio_pago="Efectivo", envio_domicilio="No", retiro_tienda="Si",pedido=pedido8)
Infopedido8.save()

Infopedido9 = Infopedido(total=17990, medio_pago="Tarejta", envio_domicilio="Si", retiro_tienda="No",pedido=pedido9)
Infopedido9.save()

Infopedido10 = Infopedido(total=13990, medio_pago="Efectivo", envio_domicilio="No", retiro_tienda="Si",pedido=pedido10)
Infopedido10.save()

chaqueta1 = chaqueta(numero_serie=78236364547646464, talla="S", precio=13990, modelo=Modelo1,info=Infopedido1)
chaqueta1.save()

chaqueta2 = chaqueta(numero_serie=78276464646324355, talla="XS", precio=17990, modelo=Modelo2,info=Infopedido2)
chaqueta2.save()

chaqueta3 = chaqueta(numero_serie=78263646473828737, talla="M", precio=15990, modelo=Modelo3,info=Infopedido3)
chaqueta3.save()

chaqueta4 = chaqueta(numero_serie=78263647476474763, talla="M", precio=13990, modelo=Modelo4,info=Infopedido4)
chaqueta4.save()

chaqueta5 = chaqueta(numero_serie=78254648959583763, talla="XS", precio=17990, modelo=Modelo5,info=Infopedido5)
chaqueta5.save()

chaqueta6 = chaqueta(numero_serie=78298973652738849, talla="L", precio=14990, modelo=Modelo6,info=Infopedido6)
chaqueta6.save()

chaqueta7 = chaqueta(numero_serie=78298463736726366, talla="S", precio=13990, modelo=Modelo7,info=Infopedido7)
chaqueta7.save()

chaqueta8 = chaqueta(numero_serie=78263536402022221, talla="M", precio=15990, modelo=Modelo8,info=Infopedido8)
chaqueta8.save()

chaqueta9 = chaqueta(numero_serie=78210928493927899, talla="XS", precio=17990, modelo=Modelo9,info=Infopedido9)
chaqueta9.save()

chaqueta10 = chaqueta(numero_serie=78264880404939303, talla="S", precio=13990, modelo=Modelo10,info=Infopedido10)
chaqueta10.save()




