from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime, timedelta
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
from django.db.models import Sum, Count, Q, Max
from django.db.models.functions import TruncDate
from django.db.models import F, FloatField, ExpressionWrapper, Value
from Aplicacion.views import servicioActivo
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# -------------------------------------------------SERVIDOS ANIMALES---------------------------------------------------
def TablaSolicitudServido(request):
    ServiciosWeb = servicioActivo() 
    TGServidos = (
        tblRepartidor.objects
        .filter(Q(IDEstatus_id=3) | Q(IDEstatus_id=8) | Q(IDEstatus_id=13))
        .annotate(fecha=TruncDate('FechaSol'))
        .values('FechaSol')
        .annotate(
            total_cantidad=Sum('CantidadSolicitada'),
            total_registros=Count('ID'),
            total_estatus3=Count('ID', filter=Q(SeSirve="Si")),
            productos_distintos=Count('IDProducto_id', distinct=True),
            porcentaje=Max('Porcentaje'),
            estatus=Max('IDEstatus_id__Descripcion'),
            idestatus=Max('IDEstatus_id'),
            ids=Max('ID')
        )
        .order_by('-FechaSol')
    )
    TFServidos = tblRepartidor.objects.filter(IDEstatus_id=13).annotate(fecha=TruncDate('FechaSol')).values('FechaSol').first()
    THServidos = (
        tblRepartidor.objects
        .filter( Q(IDEstatus_id=10)| Q(IDEstatus_id=13))
        .annotate(fecha=TruncDate('FechaSol'))
        .values('FechaSol')
        .annotate(
            total_cantidad=Sum('CantidadSolicitada'),
            total_servido = Sum(F('Cantidad1') + F('Cantidad2')),
            total_registros=Count('ID'),
            total_estatus3=Count('ID', filter=Q(SeSirve="Si")),
            productos_distintos=Count('IDProducto_id', distinct=True),
            porcentaje=Max('Porcentaje'),
            estatus=Max('IDEstatus_id__Descripcion'),
            idestatus=Max('IDEstatus_id')
        )
        .order_by('-FechaSol')
    )
    return render(request, 'SolicitudServido/index.html',{'THServidos': THServidos, 'TGServidos':TGServidos, 'ServiciosWeb':ServiciosWeb, 'TFServidos':TFServidos})

def TablaOrdenesServido(request):
    ServiciosWeb = servicioActivo() 
    ultimo_contacto = tblRepartidor.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        TEServidos = tblRepartidor.objects.filter(
            FechaSol__gte=fecha,
            FechaSol__lt=fecha + timedelta(minutes=2)
        ).annotate(
        calcCantidad1=ExpressionWrapper(
            F('CantidadSolicitada') * F('Porcentaje') / 100,
            output_field=FloatField()
        ),
        calcCantidad2=ExpressionWrapper(
            F('CantidadSolicitada') - (F('CantidadSolicitada') * F('Porcentaje') / 100),
            output_field=FloatField()
        ),
        calcSuma=ExpressionWrapper(
            F('Cantidad1') + F('Cantidad2'),
            output_field=FloatField()
        )
        ).values(
            'ID', 'Folio',
            'IDCorral_id__Descripcion',
            'IDCorral_id',
            'IDProducto_id__Descripcion',
            'IDEstatus_id__Descripcion',
            'IDProducto_id',
            'IDEstatus_id',
            'CantidadSolicitada',
            'calcCantidad1',
            'calcCantidad2',  
            'calcSuma',                 
            'Cantidad1',
            'Cantidad2',                       
            'SeSirve',
            'FechaSol',
            'FechaServida1',
            'FechaServida2'
            
        )
    registro = tblRepartidor.objects.filter(
            FechaSol__gte=fecha,
            FechaSol__lt=fecha + timedelta(minutes=2)
        ).first()
    porcentaje = registro.Porcentaje if registro else None
    FECorrales = tblCorrales.objects.order_by('ID')
    FETolva = tblTolva.objects.exclude(ID=1).order_by('Alias')
    FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    
    return render(request, 'SolicitudServido/mostrar.html',{  'FECorrales': FECorrales, 'ultimo_folio':ultimo_folio, 'FETolva':FETolva, 'porcentaje':porcentaje,
    'FechaDeHoy':FechaDeHoy, 'FEstatus': FEstatus, 'FEProductos':FEProductos, 'ServiciosWeb':ServiciosWeb, 'TEServidos':TEServidos})
    
def TablaServidoCorral(request):
    ServiciosWeb = servicioActivo() 
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d')
    TServidos = tblRepartidor.objects.filter(Q(IDEstatus_id = 10) | Q(IDEstatus_id = 11)).values('ID', 'Folio',
    'IDCorral_id__Descripcion','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
    'CantidadSolicitada',  'FechaSol', 'FechaServida1'
    )
    
    return render(request, 'ServidoListo/index.html',{'FechaDeHoy':FechaDeHoy, 'TServidos': TServidos, 'ServiciosWeb':ServiciosWeb })

def TablaFormuladoCorral(request):
    ServiciosWeb = servicioActivo() 
    
    TFormulado = tblFormulado.objects.filter(Q(IDEstatus_id = 10) | Q(IDEstatus_id = 11)).values('ID', 'Folio',
    'IDMateriaPrima_id__Descripcion','IDProducto_id__Descripcion','IDEstatus_id__Descripcion', 'IDTolva_id__Alias',
    'CantidadSolicitada',  'Fecha', 'FechaServida'
    )
    
    return render(request, 'FormuladoListo/index.html',{'TFormulado': TFormulado, 'ServiciosWeb':ServiciosWeb })

def TablaTolvaServido(request, ID, Estatus, Producto):
    
    servido = tblRepartidor.objects.get(Folio=ID)
    producto = servido.IDProducto
    estatus = Estatus
    Estatus_instancia = tblEstatus.objects.get(ID=estatus)
    servido.IDEstatus = Estatus_instancia
    servido.save()
    return redirect('proceso:FT-Consolidacion', Producto)

def TablaTolvaServidoCorral(request):
    ServiciosWeb = servicioActivo() 
    estatusSirve = request.POST.get('estatus', '')
    folio = request.POST.get('folio', '')
    IDProd = request.POST.get('IDProd', '')
    tolva = request.POST.get('tolva', '')
    
    if estatusSirve == 7 or estatusSirve == 3 or estatusSirve == '7' or estatusSirve == '3':
        servido = tblRepartidor.objects.get(Folio=folio)
        producto = servido.IDProducto
        estatus = estatusSirve
        Estatus_instancia = tblEstatus.objects.get(ID=estatus)
        servido.IDEstatus = Estatus_instancia
        servido.save()

        
        
        TServidos = tblRepartidor.objects.filter(IDEstatus_id = tolva).values('ID', 
        'Folio','IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
        'IDEstatus_id__Descripcion', 'CantidadSolicitada',  'FechaSol',
        'FechaServida1', 'IDProducto_id', 'IDEstatus_id')
        if tolva == '4':
            tolvas = 'EN TOLVA 1'
        elif tolva == '5':
            tolvas = 'EN TOLVA 2'
        elif tolva == '6':
            tolvas = 'EN TOLVA 3'

        if estatusSirve == '3':
            messages.error(request, f'El producto a sido cancelado')  
        elif estatusSirve == '7':
            messages.success(request, f'El producto  a sido servido en el corral')
        
        
    return render(request, 'ServidosConsolidacion/tolva.html',{'TServidos':TServidos, 'ServiciosWeb':ServiciosWeb})

def TablaTolva(request):
    ServiciosWeb = servicioActivo() 
    tolva = request.POST.get('tolva', '')

    if tolva is not None and tolva != '':
        TServidos = tblRepartidor.objects.exclude(IDCliente_id=1).filter(IDTolva_id = tolva).values('ID', 'Folio',
        'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'FechaSol','IDProducto_id', 'IDEstatus_id')
        if tolva == '2':
            tolvas = 'EN TOLVA 1'
        elif tolva == '3':
            tolvas = 'EN TOLVA 2'
        elif tolva == '4':
            tolvas = 'EN TOLVA 3'
    else:
        tolvas = 'NO SE SELECCIONO TOLVA'
        TServidos = tblRepartidor.objects.exclude(IDCliente_id=1).values('ID', 'Folio',
        'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion',
        'CantidadSolicitada', 'FechaSol','IDProducto_id', 'IDEstatus_id')

    
    
    return render(request, 'ServidosConsolidacion/tolva.html',{
         'TServidos':TServidos, 'tolva':tolvas, 'ServiciosWeb':ServiciosWeb})

def TablaFiltroServido(request):
    ServiciosWeb = servicioActivo() 
    producto = request.POST.get('producto', '')
    tolva = request.POST.get('tolva', '')
    if producto is not None and producto != '':
        
        
        FiltroServidos = tblRepartidor.objects.filter(Q(IDProducto_id= producto) & (Q(IDEstatus_id =3) | Q(IDEstatus_id=9))).values('ID', 'Folio',
            'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion',
            'IDEstatus_id__Descripcion', 'CantidadSolicitada', 
            'FechaSol', 'FechaServida1','IDProducto_id'
        )
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        unidad_id = FiltradoProducto.IDUnidadMedida.ID
        FiltradoTolva= tblTolva.objects.get(ID=tolva)
        Filtradounidad= tblUnidades.objects.get(ID=unidad_id)
        STolva = tblTolva.objects.exclude(ID = 1).values('ID','IDProducto_id__Descripcion', 'Alias', 'IDProducto_id', 'IDEstatus_id')
        resultados = tblRepartidor.objects.filter(Q(IDEstatus_id =3) | Q(IDEstatus_id=9)).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada')).order_by('IDProducto_id__Descripcion')

        TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

        for resultado in resultados:
            descripcion = resultado['IDProducto_id__Descripcion']
            IDProducto = resultado['IDProducto_id']
            total_cantidad = resultado['total_cantidad']
            TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
        
        tolva1 = tblRepartidor.objects.filter(IDTolva_id = tolva, IDEstatus_id = 8).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
        
        if tolva1.exists():
            print("Resultado existe")
            TTolva1 = []
            for resultado in tolva1:
                descripcion = resultado['IDProducto_id__Descripcion']
                cantidad = resultado['total_cantidad']
                if cantidad is not None and cantidad != 0 and cantidad != '0':
                    total_cantidad = cantidad
                else:
                    total_cantidad = 0
                TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})
        else:
            print("Resultado no exite")
            TTolva1 = [{'Producto': 'No se encontraron registros', 'cantidad': 0}]

        productos_tolva1 = tblRepartidor.objects.filter(IDTolva = tolva)
        if productos_tolva1.exists():
            producto_tolva = productos_tolva1.first()
        else:
            producto_tolva = 0

        return render(request, 'ServidoConsolidacion/index.html',{'producto_tolva':producto_tolva,
         'FiltroServidos':FiltroServidos, 'STolva':STolva, 'TTolva1':TTolva1, 'Filtradounidad':Filtradounidad, 
        'FiltradoProducto':FiltradoProducto,'FiltradoTolva':FiltradoTolva, 'TConsolidacion': TConsolidacion, 'ServiciosWeb':ServiciosWeb})
    else:
        FiltradoProducto= tblProductos.objects.filter(ID=1).first()
        FiltradoTolva= tblTolva.objects.filter(ID=2).first()
        STolva = tblTolva.objects.exclude(ID = 1).all()
        FiltroServidos = tblRepartidor.objects.filter(IDProducto_id= 1, IDEstatus_id =3).values('ID', 'Folio',
            'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
            'IDEstatus_id__Descripcion', 'CantidadSolicitada',  
            'FechaSol', 'FechaServida1','IDProducto_id' )
    resultados = tblRepartidor.objects.filter(Q(IDEstatus_id =3) | Q(IDEstatus_id=9)).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada')).order_by('IDProducto_id__Descripcion')

    TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

    for resultado in resultados:
        descripcion = resultado['IDProducto_id__Descripcion']
        IDProducto = resultado['IDProducto_id']
        total_cantidad = resultado['total_cantidad']
        TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
    
    # TRAER LA CANTIDAD DE KILOGRAMOS DE CADA TOLVA Y PRESENTARLO EN EL TEMPLATE
    tolva1 = tblRepartidor.objects.filter(IDTolva_id = 2).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    TTolva1 = []
    for resultado in tolva1:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})

    # MODAL TOLVA
    TTolva = tblTolva.objects.exclude(ID=1).values('ID', 'Alias', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion', 'IDEstatus_id', 'IDProducto_id')
    TServido = tblRepartidor.objects.filter(IDEstatus = 8).values('ID', 'Folio',
    'IDCorral_id__Descripcion','IDProducto_id','IDEstatus_id__Descripcion',
    'CantidadSolicitada', 'FechaSol', 'IDTolva_id'
    )
    TFormulado = tblFormulado.objects.filter(IDEstatus = 8).values('ID', 'Folio', 'IDEstatus_id',
    'IDMateriaPrima__Descripcion','IDProducto_id','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
    'CantidadSolicitada'
    )

        
    return render(request, 'ServidoConsolidacion/index.html',{
     'FiltroServidos':FiltroServidos, 'TTolva1':TTolva1,  'FiltradoTolva':FiltradoTolva, 'TTolva': TTolva, 'TServido':TServido, 'TFormulado':TFormulado,
    'FiltradoProducto':FiltradoProducto, 'STolva':STolva, 'TConsolidacion': TConsolidacion, 'ServiciosWeb':ServiciosWeb})

def TablaConsolidacionServido(request):
    ServiciosWeb = servicioActivo()
    resultados = tblRepartidor.objects.filter(IDEstatus_id =3).values('IDProducto_id__Descripcion','IDProducto_id').annotate(total_cantidad=Sum('CantidadSolicitada'))
    TConsolidacion = []  # Crear una lista vacía para almacenar los resultados

    for resultado in resultados:
        descripcion = resultado['IDProducto_id__Descripcion']
        IDProducto = resultado['IDProducto_id']
        total_cantidad = resultado['total_cantidad']
        TConsolidacion.append({'Producto': descripcion, 'cantidad': total_cantidad, 'IDProducto':IDProducto})  # Agregar cada entrada a la lista
    
    STolva = tblTolva.objects.exclude(ID = 1).all()
    
    # TRAER LA CANTIDAD DE KILOGRAMOS DE CADA TOLVA Y PRESENTARLO EN EL TEMPLATE
    tolva1 = tblRepartidor.objects.filter(IDTolva_id =2).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    tolva2 = tblRepartidor.objects.filter(IDTolva_id =3).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    tolva3 = tblRepartidor.objects.filter(IDTolva_id =4).values('IDProducto_id__Descripcion').annotate(total_cantidad=Sum('CantidadSolicitada'))
    TTolva1 = []
    for resultado in tolva1:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva1.append({'Producto': descripcion, 'cantidad': total_cantidad})

    TTolva2 = []
    for resultado in tolva2:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva2.append({'Producto': descripcion, 'cantidad': total_cantidad})

    TTolva3 = []
    for resultado in tolva3:
        descripcion = resultado['IDProducto_id__Descripcion']
        total_cantidad = resultado['total_cantidad']
        TTolva3.append({'Producto': descripcion, 'cantidad': total_cantidad})

    FiltroServidos = tblRepartidor.objects.filter(IDEstatus_id =3).values('ID', 'Folio',
            'IDCorral_id__Descripcion', 'IDProducto_id__Descripcion', 
            'IDEstatus_id__Descripcion', 'CantidadSolicitada', 
            'FechaSol','IDProducto_id' )
    

    
    return render(request, 'ServidosConsolidacion/index.html', {
    'TConsolidacion': TConsolidacion,  'TTolva1':TTolva1, 
    'TTolva2':TTolva2, 'TTolva3':TTolva3, 'STolva': STolva, 'FiltroServidos':FiltroServidos, 'ServiciosWeb':ServiciosWeb})

def TablaServidoManual(request):
    ServiciosWeb = servicioActivo() 
    ultimo_contacto = tblRepartidor.objects.order_by('-ID').first()
    if ultimo_contacto:
        ultimo_folio = ultimo_contacto.ID + 1
    else:
        ultimo_folio = 1
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")

        TEServidos = tblRepartidor.objects.filter(
            FechaSol__gte=fecha,
            FechaSol__lt=fecha + timedelta(minutes=2)
        ).values(
            'ID', 'Folio',
            'IDCorral_id__Descripcion',
            'IDCorral_id',
            'IDProducto_id__Descripcion',
            'IDEstatus_id__Descripcion',
            'IDProducto_id',
            'IDEstatus_id',
            'CantidadSolicitada',
            'SeSirve',
            'FechaSol',
            'FechaServida1'
        )
    registro = tblRepartidor.objects.filter(
            FechaSol__gte=fecha,
            FechaSol__lt=fecha + timedelta(minutes=2)
        ).first()
    porcentaje = registro.Porcentaje if registro else None
    FECorrales = tblCorrales.objects.order_by('ID')
    FETolva = tblTolva.objects.exclude(ID=1).order_by('Alias')
    FEProductos = tblProductos.objects.all().exclude(ID=1).order_by('Descripcion')
    FEstatus = tblEstatus.objects.filter(ID__lte=2).order_by('Descripcion')
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

    
    return render(request, 'ServidoManual/index.html',{  'FECorrales': FECorrales, 'ultimo_folio':ultimo_folio, 'FETolva':FETolva, 'porcentaje':porcentaje,
    'FechaDeHoy':FechaDeHoy, 'FEstatus': FEstatus, 'FEProductos':FEProductos, 'ServiciosWeb':ServiciosWeb, 'TEServidos':TEServidos})


def TablaFormuladoManual(request):
    ServiciosWeb = servicioActivo()
    TFormulado = tblFormulado.objects.filter(Q(IDEstatus_id=3) | Q(IDEstatus_id=7) | Q(IDEstatus_id=9)).values('ID', 'Folio','IDTolva_id__Alias',
        'IDProducto_id__Descripcion','IDEstatus_id__Descripcion','IDMateriaPrima_id__Descripcion',
        'CantidadSolicitada',  'Fecha')
  
    return render(request, 'FormuladoManual/index.html',{'TFormulado': TFormulado, 'ServiciosWeb':ServiciosWeb })

def TablaCargamentoTolva(request):
    ServiciosWeb = servicioActivo()
    TTolva = tblTolva.objects.exclude(ID=1).values('ID', 'Alias', 'IDProducto_id__Descripcion', 'IDEstatus_id__Descripcion', 'IDEstatus_id', 'IDProducto_id')
    TServido = tblRepartidor.objects.filter(IDEstatus = 8).values('ID', 'Folio',
    'IDCorral_id__Descripcion','IDProducto_id','IDEstatus_id__Descripcion',
    'CantidadSolicitada', 'FechaSol', 'IDTolva_id'
    )
    TFormulado = tblFormulado.objects.filter(IDEstatus = 8).values('ID', 'Folio', 'IDEstatus_id',
    'IDMateriaPrima__Descripcion','IDProducto_id','IDProducto_id__Descripcion','IDEstatus_id__Descripcion',
    'CantidadSolicitada'
    )
    return render(request, 'TolvaProcesos/index.html',{'TTolva': TTolva, 'TServido':TServido, 'TFormulado':TFormulado, 'ServiciosWeb':ServiciosWeb })


def TablaConsolidacionFormulado(request):
    ServiciosWeb = servicioActivo()
    SProducto = tblProductos.objects.all().values('ID', 'Descripcion').exclude(ID=1)
    STolva = tblTolva.objects.exclude(ID = 1).all()
    FiltradoProducto= tblProductos.objects.filter(ID=1).first()
    FiltradoTolva= tblTolva.objects.filter(ID=2).first()
    return render(request, 'FormulacionConsolidacion/index.html', {'STolva': STolva, 'SProducto':SProducto, 'FiltradoTolva':FiltradoTolva, 'FiltradoProducto':FiltradoProducto, 'ServiciosWeb':ServiciosWeb})

def TablaFiltroFormulado(request):
    ServiciosWeb = servicioActivo()
    producto = request.POST.get('producto', '')
    tolva = request.POST.get('tolva', '')
    cantidadInp = float(request.POST.get('cantidad', 0))

    tolva_save = tblTolva.objects.get(ID=tolva)
    capacidad = tolva_save.Capacidad
    restante = cantidadInp
    batch = 1
    ultimo_id = tblFormulado.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    
    if producto is not None and producto != '':
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        SProducto = tblProductos.objects.all().values('ID', 'Descripcion').exclude(ID=1)
        FiltradoTolva= tblTolva.objects.get(ID=tolva)
        STolva = tblTolva.objects.exclude(ID = 1).values('ID','IDProducto_id__Descripcion', 'Alias', 'IDProducto_id', 'IDEstatus_id', 'Capacidad')
        
        FiltradoReceta = tblReceta.objects.filter(IDProductos=producto).values( 'ID', 'Folio', 'IDMateriaPrima_id', 'IDMateriaPrima_id__Descripcion', 'Porcentaje', 'Merma')
        resultado = []
        while restante > 0:
            cantidad = min(restante, capacidad)

            for r in FiltradoReceta:
                cantidad_calculada = cantidad * (r['Porcentaje'] / 100)
                resultado.append({
                    'UID': f"{r['ID']}_{batch}",   # ✅ ID único
                    'IDReceta': r['ID'],
                    'Batch': batch,

                    'Folio': r['Folio'],
                    'IDMateriaPrima_id': r['IDMateriaPrima_id'],
                    'IDMateriaPrima_id__Descripcion': r['IDMateriaPrima_id__Descripcion'],
                    'Porcentaje': r['Porcentaje'],
                    'Merma': r['Merma'],
                    'cantidad_porcentaje': round(cantidad_calculada, 2),
                })

            restante -= cantidad
            batch += 1

        return render(request, 'FormulacionConsolidacion/index.html',{ 'FiltradoReceta':resultado, 'SProducto':SProducto, 'FechaDeHoy':FechaDeHoy,
          'STolva':STolva, 'FiltradoProducto':FiltradoProducto,'FiltradoTolva':FiltradoTolva, 'cantidad':cantidadInp, 'ultimo_folio':ultimo_folio, 'restante':restante, 'ServiciosWeb':ServiciosWeb})
    else:
        FiltradoProducto = tblProductos.objects.filter(ID = 1).first()
        FiltradoTolva = tblTolva.objects.filter(ID = 2).first()
        STolva = tblTolva.objects.exclude(ID = 1).all()
        cantidad = 0
    
    return render(request, 'FormulacionConsolidacion/index.html',{'FiltradoTolva':FiltradoTolva, 'FechaDeHoy':FechaDeHoy,
    'FiltradoProducto':FiltradoProducto, 'STolva':STolva, 'cantidad':cantidad, 'ultimo_folio':ultimo_folio, 'restante':restante, 'ServiciosWeb':ServiciosWeb})

def TablaFiltroFormulado1(request):
    ServiciosWeb = servicioActivo()
    producto = request.POST.get('producto', '')
    tolva = request.POST.get('tolva', '')
    cantidadInp = float(request.POST.get('cantidad', 0))
    restante = 0
    cantidad = 0 
    tolva_save = tblTolva.objects.get(ID=tolva)
    capacidad = tolva_save.Capacidad
    if cantidadInp > capacidad:
        restante = cantidadInp - capacidad 
        cantidad = capacidad
    else:
        cantidad = cantidadInp
    
    ultimo_id = tblFormulado.objects.order_by('-ID').first()
    if ultimo_id:
        ultimo_folio = ultimo_id.ID + 1
    else:
        ultimo_folio = 1
    
    FechaDeHoy = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    
    if producto is not None and producto != '':
        FiltradoProducto= tblProductos.objects.get(ID=producto)
        SProducto = tblProductos.objects.all().values('ID', 'Descripcion').exclude(ID=1)
        FiltradoTolva= tblTolva.objects.get(ID=tolva)
        STolva = tblTolva.objects.exclude(ID = 1).values('ID','IDProducto_id__Descripcion', 'Alias', 'IDProducto_id', 'IDEstatus_id', 'Capacidad')
        FiltradoReceta = (
        tblReceta.objects.filter(IDProductos=producto).annotate(cantidad_porcentaje=ExpressionWrapper(Value(cantidad) * (F('Porcentaje') / 100),
                output_field=FloatField()),
            cantidad_restante=ExpressionWrapper(Value(restante) * (F('Porcentaje') / 100),output_field=FloatField())
        ).values( 'ID', 'Folio', 'IDMateriaPrima_id__Descripcion', 'IDMateriaPrima_id', 'Merma', 'Porcentaje', 'cantidad_porcentaje', 'cantidad_restante'))
        
        return render(request, 'FormulacionConsolidacion/index.html',{ 'FiltradoReceta':FiltradoReceta, 'SProducto':SProducto, 'FechaDeHoy':FechaDeHoy,
          'STolva':STolva, 'FiltradoProducto':FiltradoProducto,'FiltradoTolva':FiltradoTolva, 'cantidad':cantidadInp, 'ultimo_folio':ultimo_folio, 'restante':restante, 'ServiciosWeb':ServiciosWeb})
    else:
        FiltradoProducto= tblProductos.objects.filter(ID=1).first()
        FiltradoTolva= tblTolva.objects.filter(ID=2).first()
        STolva = tblTolva.objects.exclude(ID = 1).all()
        cantidad= 0
    
    return render(request, 'FormulacionConsolidacion/index.html',{'FiltradoTolva':FiltradoTolva, 'FechaDeHoy':FechaDeHoy,
    'FiltradoProducto':FiltradoProducto, 'STolva':STolva, 'cantidad':cantidad, 'ultimo_folio':ultimo_folio, 'restante':restante, 'ServiciosWeb':ServiciosWeb})