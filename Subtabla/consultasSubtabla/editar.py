from django.shortcuts import render
# LLAMAR ARCHIVOS LOCALES
from Aplicacion.forms import *
from Aplicacion.models import *
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< EDITAR FORMULARIO CATALOGOS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# --------------------------------------------------------CLIENTES---------------------------------------------------------
def editarEstatus(request, ID):
    TEEstatus= tblEstatus.objects.get(ID=ID)
    return render(request, "Estatus/edit.html",{'TEEstatus': TEEstatus})


def editarUnidadMedida(request, ID):
    TEUnidadMedida = tblUnidades.objects.get(ID=ID)
    return render(request, "UnidadMedida/edit.html",{'TEUnidadMedida': TEUnidadMedida})

