from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.db.models import Sum
from django.db import transaction
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ACTUALIZAR DATOS PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#   QUEDA INHABILITADO TEMPORALMENTE
def actualizarServidosManual(request):
    id_v = request.POST['id']
    folio_v = request.POST['folio']
    corral_v = request.POST['corral']
    producto_v = request.POST['producto']
    estatus_v = request.POST['estatus']
    cantidadSol_v = request.POST['cantidadSol']
    cantidadSer_v = request.POST['cantidadSer']
    fechaSol_v = request.POST['fechaSol']
    fechaSer_v = request.POST['fechaSer']
    servidos = request.POST['servido']


    servidos_save = tblRepartidor.objects.get(ID=id_v)

    Corral_instancia = tblCorrales.objects.get(ID=corral_v)
    Producto_instancia = tblProductos.objects.get(ID=producto_v)
    Estatus_instancia = tblEstatus.objects.get(ID=estatus_v)

    
    servidos_save.IDEstatus = Estatus_instancia
    servidos_save.IDProducto = Producto_instancia
    servidos_save.IDCorral = Corral_instancia
    servidos_save.CantidadSolicitada = cantidadSol_v
    servidos_save.CantidadServida = cantidadSer_v
    servidos_save.Fecha = fechaSol_v
    if fechaSer_v:
        servidos_save.FechaServida = fechaSer_v
    servidos_save.save()

    messages.success(request, f'El Servido se ha actualizado exitosamente.')
    if servidos == '1':
        return redirect('proceso:T_Solicitud_Servidos')
    elif servidos == '2':
        return redirect('T-Servidos')
    else:
        return redirect('T-Servidos')
    
def actualizarCantidadServidosManual(request):
    if request.method == 'POST':
        id_v = request.POST.getlist('id[]')
        cantidadSer_v = request.POST.getlist('cantidadSer[]')
        estatus_v = 10
        FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

        estatus_instancia = tblEstatus.objects.get(ID = estatus_v)

        
        solicitudes = []
        for i in range(len(cantidadSer_v)):
            if cantidadSer_v[i] and float(cantidadSer_v[i]) != 0:
                solicitud = {
                    'id': id_v[i],
                    'cantidadSer': float(cantidadSer_v[i])
                }
                solicitudes.append(solicitud)

        for solicitud in solicitudes:
            IDFilaTabla_v = solicitud['id']
            servidos_save = tblRepartidor.objects.get(ID = solicitud['id'])
            servidos_save.IDEstatus = estatus_instancia
            servidos_save.CantidadServida = solicitud['cantidadSer']
            servidos_save.FechaServida = FechaDeHoy
            servidos_save.save()

        messages.success(request, f'El Servido se ha actualizado exitosamente.')
        return redirect('proceso:T_Servidos')

def actualizarCantidadFormuladoManual(request):
    if request.method == 'POST':
        id_v = request.POST.getlist('id[]')
        cantidadSer_v = request.POST.getlist('cantidadSer[]')
        estatus_v = 10
        FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

        estatus_instancia = tblEstatus.objects.get(ID = estatus_v)

        
        solicitudes = []
        for i in range(len(cantidadSer_v)):
            if cantidadSer_v[i] and float(cantidadSer_v[i]) != 0:
                solicitud = {
                    'id': id_v[i],
                    'cantidadSer': float(cantidadSer_v[i])
                }
                solicitudes.append(solicitud)

        for solicitud in solicitudes:
            IDFilaTabla_v = solicitud['id']
            servidos_save = tblFormulado.objects.get(ID = solicitud['id'])
            servidos_save.IDEstatus = estatus_instancia
            servidos_save.CantidadServida = solicitud['cantidadSer']
            servidos_save.FechaServida = FechaDeHoy
            servidos_save.save()

        messages.success(request, f'El Servido se ha actualizado exitosamente.')
        return redirect('proceso:T_FormuladoM')
    
def actualizarServidosATolsva(request):
    if request.method == 'POST':
        id_v = request.POST['id']
        tolva_v = request.POST['tolva']
        idproducto_v = request.POST['idproducto']
        EnTolva = 8
        NombreTolva_v = request.POST['NombreTolva']
        seleccionado_v = request.POST.get('seleccionado')  # Utiliza request.POST.get() para obtener el valor del checkbox

        servido = tblRepartidor.objects.get(ID=id_v)

        Tolva_instancia = tblTolva.objects.get(ID=tolva_v)
        Estatus_instancia = tblEstatus.objects.get(ID=EnTolva)
        
        # Verifica si el checkbox está marcado (seleccionado)
        if seleccionado_v == 'on':

            servido.IDEstatus = Estatus_instancia
            servido.IDTolva = Tolva_instancia
            servido.save()
            messages.success(request, f'El Servido se ha asignado correctamente a la tolva "{NombreTolva_v}".')
    return redirect('T-Consolidacion')

def actualizarServidosATolva(request):
    if request.method == 'POST':
        if 'tolva' in request.POST:
            tolva_v = request.POST['tolva']
            if tolva_v != "" or tolva_v != None:
                EnTolva = 8
                EnOperacion = 4
                NombreTolva_v = request.POST['NombreTolva']
                producto_v = request.POST['idproducto']
                
                # Obtén la instancia de la Tolva y el Estatus una sola vez
                Tolva_instancia = tblTolva.objects.get(ID=tolva_v)
                Estatus_instancia = tblEstatus.objects.get(ID=EnTolva)
                Estatus_operacion = tblEstatus.objects.get(ID=EnOperacion)
                Producto_instancia = tblProductos.objects.get(ID=producto_v)

                tolva_save = tblTolva.objects.get(ID=tolva_v)
                tolva_save.IDProducto = Producto_instancia
                tolva_save.IDEstatus = Estatus_operacion
                tolva_save.save()  
                
                # Itera a través de los IDs seleccionados y actualiza los registros correspondientes
                for key, value in request.POST.items():
                    if key.startswith('seleccionado_'):
                        servido_id = key.split('seleccionado_')[1]
                        # Verifica si el checkbox está marcado
                        servido = tblRepartidor.objects.get(ID=servido_id)
                        servido.IDEstatus = Estatus_instancia
                        servido.IDTolva = Tolva_instancia
                        servido.save()

                messages.success(request, f'Se han asignado los Servidos a la tolva "{NombreTolva_v}" correctamente.')
        
    return redirect('proceso:FT_Consolidacion')

def actualizarFormuladoATolva(request):
    if request.method != 'POST':
        return redirect('proceso:FT_Consolidacion')

    tolva_v = request.POST.get('tolva')
    if not tolva_v:
        messages.error(request, "Tolva no válida")
        return redirect('proceso:FT_Consolidacion')

    seleccionados = request.POST.getlist('seleccionados[]')
    if not seleccionados:
        messages.error(request, "No seleccionaste ningún registro")
        return redirect('proceso:T_FConsolidacion')

    # ================= CONSTANTES =================
    EnTolva = 8
    EnOperacion = 12

    # ================= DATOS GENERALES =================
    NombreTolva_v = request.POST.get('NombreTolva')
    producto_v = request.POST.get('idproducto')
    fecha_v = request.POST.get('fecha')
    # cantidadbatch = request.POST.get('cantidadBatch')
    # restante = request.POST.get('restante')
    clave = request.POST.get('clave')
    formatoClave = f'F-{int(clave):06d}'

    # ================= INSTANCIAS =================
    Producto_instancia = tblProductos.objects.get(ID=producto_v)
    Estatus_instancia = tblEstatus.objects.get(ID=EnTolva)
    Estatus_operacion = tblEstatus.objects.get(ID=EnOperacion)


    
    # ================= ACTUALIZAR TOLVA =================
    tolva_save = tblTolva.objects.get(ID=tolva_v)
    tolva_save.IDProducto = Producto_instancia
    tolva_save.IDEstatus = Estatus_operacion
    tolva_save.save()
    
    # ================= INSERTAR FORMULADO =================
    registros = []



    with transaction.atomic():
        for uid in seleccionados:
            registros.append(
                tblFormulado(
                    Folio=formatoClave,
                    IDMateriaPrima_id=request.POST.get(f'idmateriaprima_{uid}'),
                    IDProducto=Producto_instancia,
                    IDEstatus=Estatus_instancia,
                    IDTolva=tolva_save,
                    CantidadServida=0,
                    CantidadSolicitada=request.POST.get(f'cantidad_{uid}'),
                    Proporcion=request.POST.get(f'proporcion_{uid}'),
                    Fecha=fecha_v
                )
            )

        tblFormulado.objects.bulk_create(registros)
        

    messages.success(
        request,
        f'Se han asignado los Servidos a la tolva "{NombreTolva_v}" correctamente.'
    )

    return redirect('proceso:T_FConsolidacion')
# ------------------------------------------------------TIPO ANIMALES------------------------------------------------------
def actualizarCancelarTolva(request):
    idTolva = request.POST['id']
    dataInput = request.POST.get('cargamento-tolva', '')
    if dataInput == "Terminado":
        EstatusServido = 7
    elif dataInput == "Cancelado":
        EstatusServido = 3
    else :
        return redirect('proceso:FT_Consolidacion')
    EstatusTolva = 6
    ProductoTolva = 1
    servidotolva = 1

    servido_save = tblRepartidor.objects.filter(IDTolva_id=idTolva, IDEstatus_id = 8)
    Estatus_instancia = tblEstatus.objects.get(ID=EstatusServido)
    Estatus_Tolva_instancia = tblEstatus.objects.get(ID=EstatusTolva)
    Producto_instancia = tblProductos.objects.get(ID=ProductoTolva)
    Tolva_instancia = tblTolva.objects.get(ID=servidotolva)

    tolva_save = tblTolva.objects.get(ID=idTolva)
    tolva = tolva_save.Alias

    for servido_instancia in servido_save:
        servido_instancia.IDEstatus = Estatus_instancia
        servido_instancia.IDTolva = Tolva_instancia  
        servido_instancia.save()


    tolva_save.IDEstatus = Estatus_Tolva_instancia
    tolva_save.IDProducto = Producto_instancia
    tolva_save.save()

    messages.success(request, f'La tolva "{tolva}" se ha actualizado exitosamente.')
    return redirect('proceso:FT_Consolidacion')

def actualizarCancelarFormulado(request):
    idTolva = request.POST['id']
    dataInput = request.POST.get('cargamento-tolva', '')
    if dataInput == "Terminado":
        EstatusServido = 7
    elif dataInput == "Cancelado":
        EstatusServido = 3
    else :
        return redirect('proceso:FT_Consolidacion')
    EstatusTolva = 6
    ProductoTolva = 1
    servidotolva = 1

    formulado_save = tblFormulado.objects.filter(IDTolva_id=idTolva, IDEstatus_id = 8)
    Estatus_instancia = tblEstatus.objects.get(ID=EstatusServido)
    Estatus_Tolva_instancia = tblEstatus.objects.get(ID=EstatusTolva)
    Producto_instancia = tblProductos.objects.get(ID=ProductoTolva)
    Tolva_instancia = tblTolva.objects.get(ID=servidotolva)

    tolva_save = tblTolva.objects.get(ID=idTolva)
    tolva = tolva_save.Alias

    for formulado_instancia in formulado_save:
        formulado_instancia.IDEstatus = Estatus_instancia
        # formulado_instancia.IDTolva = Tolva_instancia  
        formulado_instancia.save()


    tolva_save.IDEstatus = Estatus_Tolva_instancia
    tolva_save.IDProducto = Producto_instancia
    tolva_save.save()

    messages.success(request, f'La tolva "{tolva}" se ha actualizado exitosamente.')
    return redirect('proceso:FT_Consolidacion')
