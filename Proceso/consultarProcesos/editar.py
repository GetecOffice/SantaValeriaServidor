from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDITAR FORMULARIO PROCESOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------SERVIDOS--------------------------------------------------------
# --------------------------------------------------------CORRALES---------------------------------------------------------
def editarSolicitudServidos(request, ID):
    
    TEServidos= tblRepartidor.objects.get(ID=ID)
    Estatus = TEServidos.IDEstatus.ID
    Producto = TEServidos.IDProducto.ID
    Corral = TEServidos.IDCorral.ID
    fecha = TEServidos.Fecha
    fechaServida = TEServidos.FechaServida
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoProducto= tblProductos.objects.get(ID=Producto)
    FiltradoCorral= tblCorrales.objects.get(ID=Corral)
    FECorral = tblCorrales.objects.all().order_by('Descripcion')
    FEProducto = tblProductos.objects.all().order_by('Descripcion')
    FEEstatus = tblEstatus.objects.filter(ID=3).order_by('Descripcion')
    return render(request, "SolicitudServido/edit.html",{'TEServidos': TEServidos, 'fecha':fecha,
    'FiltradoEstatus': FiltradoEstatus,'FiltradoProducto': FiltradoProducto,
    'FiltradoCorral': FiltradoCorral,'FECorral': FECorral,'FEProducto': FEProducto, 'fechaServida':fechaServida,
    'FEEstatus': FEEstatus,})

def editarServidosManuales(request, ID):
    
    TEServidos= tblRepartidor.objects.get(ID=ID)
    Estatus = TEServidos.IDEstatus.ID
    Producto = TEServidos.IDProducto.ID
    Corral = TEServidos.IDCorral.ID
    fecha = TEServidos.Fecha
    fechaServida = TEServidos.FechaServida
    FiltradoEstatus= tblEstatus.objects.get(ID=Estatus)
    FiltradoProducto= tblProductos.objects.get(ID=Producto)
    FiltradoCorral= tblCorrales.objects.get(ID=Corral)
    FECorral = tblCorrales.objects.all().order_by('Descripcion')
    FEProducto = tblProductos.objects.all().order_by('Descripcion')
    FEEstatus = tblEstatus.objects.filter(ID=3).order_by('Descripcion')
    return render(request, "Servido Manual/edit.html",{'TEServidos': TEServidos, 'fecha':fecha,
    'FiltradoEstatus': FiltradoEstatus,'FiltradoProducto': FiltradoProducto,
    'FiltradoCorral': FiltradoCorral,'FECorral': FECorral,'FEProducto': FEProducto, 'fechaServida':fechaServida,
    'FEEstatus': FEEstatus,})

