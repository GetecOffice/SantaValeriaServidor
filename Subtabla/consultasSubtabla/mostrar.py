from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TABLAS DE CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------ESTATUS---------------------------------------------------------
def TablaEstatus(request):
    TEstatus = tblEstatus.objects.all()
    return render(request, 'Estatus/index.html',{
    'TEstatus': TEstatus})

def TablaUnidadMedida(request):
    TUnidadMedida = tblUnidades.objects.all()
    return render(request, 'UnidadMedida/index.html',{
    'TUnidadMedida': TUnidadMedida})
