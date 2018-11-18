from apps.contabilidad_general.models import Transaccion_Cuenta
from apps.contabilidad_costos.models import Kardex, Entrada_Salida, Entrada_Salida_Respaldo
from apps.catalogo.models import Cuenta,CuentaHija
from apps.periodo.models import Periodo

def peps(idPeriodo, fecha,id_cuenta,cant,precio_u,tipo):
	periodo = Periodo.objects.get(id = idPeriodo)
	existe_cuenta = CuentaHija.objects.filter(id= id_cuenta).exists()
	if existe_cuenta:
		cuenta_afectada = CuentaHija.objects.get(id= id_cuenta)
		existe_kardex = Kardex.objects.filter(cuenta_kardex = cuenta_afectada).exists()
		if existe_kardex:
			kardex_afectado = Kardex.objects.get(cuenta_kardex = cuenta_afectada)
			if tipo == False: #si es entrada
				kardex_afectado.cantidad_existencia += cant
				kardex_afectado.precio_unitario_peps += (cant*precio_u)
				kardex_afectado.save()
				existe_cabeza = Entrada_Salida.objects.filter(cabeza_kardex = True).exists() # traeme el registro que esta en la cabeza
				if existe_cabeza: # si existe una entrada en ese kardex 
					cola = Entrada_Salida.objects.get(cola_kardex = True)
					cola.cola_kardex = False
					cola.siguiente_kardex = "P"
					cola.save()
					nuevaCola = Entrada_Salida(
						periodo_es= periodo,
						fecha_es=fecha,
						kardex = kardex_afectado,
						cantidad_unidades = cant,
						precio_unitario = precio_u,
						tipo_movimiento= tipo,
						cabeza_kardex = False, # no es cabeza dado que es ultimo en ingresar
						cola_kardex = True, # efectivamente es cola
						siguiente_kardex=""
						)
					nuevaCola.save()
					nuevaColar = Entrada_Salida_Respaldo(
						periodo_esr= periodo,
						fecha_esr=fecha,
						kardexr = kardex_afectado,
						cantidad_unidadesr = cant,
						precio_unitarior = precio_u,
						tipo_movimientor= tipo
						)
					nuevaColar.save()
				else: # si no existe una entrada en ese kardex creamos la primera
					nuevaCola = Entrada_Salida(
						periodo_es= periodo,
						fecha_es=fecha,
						kardex = kardex_afectado,
						cantidad_unidades = cant,
						precio_unitario = precio_u,
						tipo_movimiento= tipo,
						cabeza_kardex = True, # es la cabeza dado que es el unico ingresado
						cola_kardex = True, # efectivamente es cola
						siguiente_kardex=""
						)
					nuevaCola.save()
					nuevaColar = Entrada_Salida_Respaldo(
						periodo_esr= periodo,
						fecha_esr=fecha,
						kardexr = kardex_afectado,
						cantidad_unidadesr = cant,
						precio_unitarior = precio_u,
						tipo_movimientor= tipo
						)
					nuevaColar.save()
			if tipo == True: #si es salida del kardex
				if cant != 0 and cant <= kardex_afectado.cantidad_existencia:
					existe_cabeza = Entrada_Salida.objects.filter(cabeza_kardex = True).exists() 
					if existe_cabeza: # si existe una entrada en ese kardex
						cabeza = Entrada_Salida.objects.get(cabeza_kardex = True)
						if cant < cabeza.cantidad_unidades:
							'''nuevaCola = Entrada_Salida(
								periodo_es= periodo,
								fecha_es=fecha,
								kardex = kardex_afectado,
								cantidad_unidades = cant,
								precio_unitario = cabeza.precio_unitario,
								tipo_movimiento= tipo,
								cabeza_kardex = False, # en salidas esto no importa
								cola_kardex = False, # en salidas eston no importa
								siguiente_kardex="" # en salidas eston no importa
								)
							nuevaCola.save()'''
							nuevaColar = Entrada_Salida_Respaldo(
								periodo_esr= periodo,
								fecha_esr=fecha,
								kardexr = kardex_afectado,
								cantidad_unidadesr = cant,
								precio_unitarior = cabeza.precio_unitario,
								tipo_movimientor= tipo,
								)
							nuevaColar.save()
							kardex_afectado.cantidad_existencia -= cant
							kardex_afectado.precio_unitario_peps -= (cant*cabeza.precio_unitario)
							kardex_afectado.save()
							cabeza.cantidad_unidades -= cant
							cabeza.save()
							cant = 0

						if cant == cabeza.cantidad_unidades:
							'''nuevaCola = Entrada_Salida(
								periodo_es= periodo,
								fecha_es=fecha,
								kardex = kardex_afectado,
								cantidad_unidades = cant,
								precio_unitario = cabeza.precio_unitario,
								tipo_movimiento= tipo,
								cabeza_kardex = False, # en salidas esto no importa
								cola_kardex = False, # en salidas eston no importa
								siguiente_kardex="" # en salidas eston no importa
								)
							nuevaCola.save()'''
							nuevaColar = Entrada_Salida_Respaldo(
								periodo_esr= periodo,
								fecha_esr=fecha,
								kardexr = kardex_afectado,
								cantidad_unidadesr = cant,
								precio_unitarior = cabeza.precio_unitario,
								tipo_movimientor= tipo
								)
							nuevaColar.save()

							kardex_afectado.cantidad_existencia -= cant
							kardex_afectado.precio_unitario_peps -= (cant*cabeza.precio_unitario)
							kardex_afectado.save()
							cabeza.cantidad_unidades -= cant
							cabeza.cabeza_kardex = False
							cabeza.save()
							cant = 0
							if cabeza.siguiente_kardex != "":
								existe_nueva = Entrada_Salida.objects.filter(id = int(cabeza.siguiente_kardex)).exists()
								if existe_nueva:
									cabeza_nueva = Entrada_Salida.objects.get(id= int(cabeza.siguiente_kardex))
									cabeza_nueva.cabeza_kardex = True
									cabeza_nueva.save()
								
						if cant > cabeza.cantidad_unidades:
							if cabeza.siguiente_kardex != "":
								existe_nueva = Entrada_Salida.objects.filter(id = int(cabeza.siguiente_kardex)).exists()
								if existe_nueva:
									'''nuevaCola = Entrada_Salida(
										periodo_es= periodo,
										fecha_es=fecha,
										kardex = kardex_afectado,
										cantidad_unidades = cabeza.cantidad_unidades,
										precio_unitario = cabeza.precio_unitario,
										tipo_movimiento= tipo,
										cabeza_kardex = False, # en salidas esto no importa
										cola_kardex = False, # en salidas eston no importa
										siguiente_kardex="" # en salidas eston no importa
													)
									nuevaCola.save()'''
									nuevaColar = Entrada_Salida_Respaldo(
										periodo_esr= periodo,
										fecha_esr=fecha,
										kardexr = kardex_afectado,
										cantidad_unidadesr = cabeza.cantidad_unidades,
										precio_unitarior = cabeza.precio_unitario,
										tipo_movimientor= tipo
													)
									nuevaColar.save()
									kardex_afectado.cantidad_existencia -= cabeza.cantidad_unidades
									kardex_afectado.precio_unitario_peps -= (cabeza.cantidad_unidades*cabeza.precio_unitario)
									kardex_afectado.save()
									cabeza_nueva = Entrada_Salida.objects.get(id= int(cabeza.siguiente_kardex))
									cabeza_nueva.cabeza_kardex = True
									cabeza_nueva.save()
									cant -= cabeza.cantidad_unidades
									cabeza.cantidad_unidades = 0.00
									cabeza.cabeza_kardex = False
									cabeza.save()
									
									peps(idPeriodo, fecha,id_cuenta,cant,precio_u,tipo)

	return

def ajuste_peps():
	existe_es = Entrada_Salida.objects.filter(siguiente_kardex="P").exists()
	if existe_es:
		es_ajuste = Entrada_Salida.objects.get(siguiente_kardex="P")
		existe_cola = Entrada_Salida.objects.filter(cola_kardex = True).exists()
		if existe_cola:
			cola = Entrada_Salida.objects.get(cola_kardex = True)
			es_ajuste.siguiente_kardex = str(cola.id)
			es_ajuste.save()
	return



	

	