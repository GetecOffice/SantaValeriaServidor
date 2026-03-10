from django.shortcuts import redirect,render
from django.contrib import messages
from django.db.models import Sum
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Q
from Aplicacion.views import servicioActivo
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< GUARDAR FORMULARIO PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def guardarSolicitudServido(request):
    if request.method == 'POST':
        # VARIABLES PARA CONFIGURACION
        porcentaje_v = int(request.POST.get('porcentaje'))
        # LLENAR LA TABLA DE TBLREPARTIDOR
        id_v = request.POST.getlist('id[]')
        folio_v = int(request.POST.get('folio'))
        cantidadSol_v = request.POST.getlist('cantidadSol[]')
        producto_v = request.POST.getlist('producto[]')
        seSirve_v = request.POST.getlist('seSirve[]')

        FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
        
        solicitudes = []
        for i in range(len(cantidadSol_v)):
            if cantidadSol_v[i] :
                solicitud = {
                    'id': id_v[i],
                    'producto': producto_v[i],
                    'seSirve': seSirve_v[i],
                    'cantidadSol': float(cantidadSol_v[i])
                }
                solicitudes.append(solicitud)

        for solicitud in solicitudes:
            folio_v += 1
            clave_int = folio_v
            formatoClave = 'S-{:06d}'.format(clave_int)         
            tblRepartidor.objects.create(Folio = formatoClave, IDCorral_id =solicitud['id'], IDProducto_id = solicitud['producto'], IDTolva_id = 2,
            IDEstatus_id = 8, CantidadSolicitada = solicitud['cantidadSol'], Cantidad1 = 0,Cantidad2 = 0, 
            FechaSol = FechaDeHoy, Porcentaje = porcentaje_v, SeSirve = solicitud['seSirve'])             

        porcentaje_save = tblConfiguracion.objects.get(ID=1)
        porcentaje_save.Porcentaje = porcentaje_v
        porcentaje_save.save()

        messages.success(request, f'El Servido se ha actualizado exitosamente.')
        print("Sevidopr")
        return redirect('proceso:T_Solicitud_Servidos')

def guardarSolicitudServido1(request):
    ServiciosWeb = servicioActivo() 
    clave = request.POST['folio']
    corral = request.POST['corral']
    producto = request.POST['producto']
    estatus = request.POST['estatus']
    cantidadSol = request.POST['cantidadSol']
    cantidadSer = request.POST['cantidadSer']
    fechaSol = request.POST['fechaSol']
    fechaSer = request.POST['fechaSer']
    
    peticion = request.POST['peticion']

    
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)


    tblRepartidor.objects.create(Folio = formatoClave, IDCorral_id =corral, IDProducto_id = producto, 
    IDEstatus_id = estatus, CantidadSolicitada = cantidadSol, CantidadServida =cantidadSer, 
    FechaSol = fechaSol, FechaServida = fechaSer) 

    messages.success(request, 'El Servido Manual se ha registrado exitosamente')
    if request.method == 'POST':
        if peticion == '1' or peticion == 1:
            if 'salir' in request.POST:
                return redirect('proceso:T_Solicitud_Servidos')
            elif 'agregar' in request.POST:
                ultimo_contacto = tblRepartidor.objects.order_by('-ID').first()
                if ultimo_contacto:
                    ultimo_folio = ultimo_contacto.ID + 1
                else:
                    ultimo_folio = 1
                cantidadSol = request.POST['cantidadSol']
                SelectProducto = tblProductos.objects.get(ID = producto)
                SelectCorral = tblCorrales.objects.get(ID = corral)
                FECorrales = tblCorrales.objects.order_by('Descripcion')
                FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
                FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
                FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
                print(cantidadSol)

                return render(request, 'SolicitudServido/form.html',{
                'ultimo_folio': ultimo_folio,'SelectCorral':SelectCorral, 'SelectProducto':SelectProducto, 'ServiciosWeb':ServiciosWeb,                                                                      
                'cantidadSol':cantidadSol, 'FECorrales':FECorrales, 'FEProductos':FEProductos, 'FEstatus':FEstatus, 'FechaDeHoy':FechaDeHoy})
        elif peticion == '2' or peticion == 2:
            email = request.POST['email']            
            request.session['email'] = email
            return redirect('FP-Cliente')
    else:
        return redirect('proceso:T_Solicitud_Servidos')
    
# -------------------------------------------------SERVIDOS MANUALES-------------------------------------------------
def guardarServidosManuales(request):
    ServiciosWeb = servicioActivo() 
    clave = request.POST['folio']
    cliente = request.POST['cliente']
    corral = request.POST['corral']
    producto = request.POST['producto']
    estatus = request.POST['estatus']
    prioridad = request.POST['prioridad']
    cantidadSol = request.POST['cantidadSol']
    cantidadSer = request.POST['cantidadSer']
    fechaSol = request.POST['fechaSol']
    fechaSer = request.POST['fechaSer']

    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)


    tblRepartidor.objects.create(Folio = formatoClave,  IDCliente_id = cliente, IDCorral_id =corral, IDProducto_id = producto, 
    IDEstatus_id = estatus, CantidadSolicitada = cantidadSol, CantidadServida =cantidadSer, 
    Prioridad =prioridad, FechaSol = fechaSol, FechaServida = fechaSer
    ) 

    messages.success(request, 'El Servido Manual se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-Servidos')
        elif 'agregar' in request.POST:
            return redirect('F-Servidos')
    else:
        return redirect('T-Servidos')


    clave = request.POST['clave']

    producto = request.POST['producto']
  
    clave_int = int(clave)
    formatoClave = 'F-{:06d}'.format(clave_int)

    # tecnicos
    Tecnico_v = request.POST['tecnico'].upper()
    NombreTabla_v = 'Inventario Productos'
    IDFilaTabla_v = formatoClave
    AreaRegistro_v = 'Procesos'
    IDFila_v = clave

    messages.success(request, 'El Inventario de productos se ha registrado exitosamente')
    if request.method == 'POST':
        if 'salir' in request.POST:
            return redirect('T-InventarioProductos')
        elif 'agregar' in request.POST:
            return redirect('F-InventarioProductos')
    else:
        return redirect('T-InventarioProductos')