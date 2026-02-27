from django.urls import path
from . import views
from Proceso.consultarProcesos import actualizar, agregar, editar, mostrar, formulario, dispositivos, excel


urlpatterns = [
    path('', views.homeProcesos, name='Inicio'),
    path('api/config/', dispositivos.obtener_comando, name='Dispositivos'),

    # DATOS DEL AREA DE SERVIDOS
    path('Solicitud_Servidos/', mostrar.TablaSolicitudServido, name='T_Solicitud_Servidos'),
    path('Corrales_Servidos/', mostrar.TablaServidoCorral, name='T_Corrales_Servidos'),
    path('exportar-servido-corral/', excel.ExportarServidoCorralExcel, name='exportar_servido_corral'),
    path('Consolidacion_Servido/', mostrar.TablaConsolidacionServido, name='T_Consolidacion'),
    path('Consolidacion_Servido/Filtro/Tolva/<str:ID>/<int:Estatus>/<int:Producto>/', mostrar.TablaTolvaServido),
    path('Consolidacion_Servido_Filtro/', mostrar.TablaFiltroServido, name='FT_Consolidacion'),
    path('Servidos_Manuales/', mostrar.TablaServidoAnimales, name='T_Servidos'),
    
    path('Tolva_Servido/', mostrar.TablaTolva, name='T_Tolva_Servido'),
    path('Tolva_Servido_Se_Sirve/', mostrar.TablaTolvaServidoCorral, name='T_Se_Sirve'),
    
    # FORMULADO
    path('Consolidacion_Formulacion/', mostrar.TablaConsolidacionFormulado, name='T_FConsolidacion'),
    path('Consolidacion_Formulado_Filtro/', mostrar.TablaFiltroFormulado, name='FT_FConsolidacion'),
    path('Formulado_Manuales/', mostrar.TablaFormuladoManual, name='T_FormuladoM'),
    path('Formulado_Servidos/', mostrar.TablaFormuladoCorral, name='T_Formulado_Servidos'),
    
    # DATOS DE LOS DATOS DE LA TOLVA
    path('Cargamento_Tolva/', mostrar.TablaCargamentoTolva, name='T_Cargamento_Tolva'),
    

    path('Formulario_Solicitud_Servido/',formulario.FormularioSolicitudServido, name='F_Solicitud_Servidos'),
    path('Formulario_Servidos_Manuales/',formulario.FormularioServidoAnimales, name='F_Servidos'),

    path('Guardar_Solicitud_Servidos/', agregar.guardarSolicitudServido, name="G_Solicitud_Servidos"),
    path('Guardar_Servidos_Manual/', agregar.guardarServidosManuales),

    path('Solicitud_Servidos/Editar/<ID>', editar.editarSolicitudServidos),
    path('Dato_Servidos_Manuales/Editar/<ID>', editar.editarServidosManuales),

    # ACTUALIZAR PROCESOS
    path('ActualizarServidorManual/', actualizar.actualizarServidosManual, name="A_Solicitud_Servidos"),
    path('ActualizarServidorManualCantidad/', actualizar.actualizarCantidadServidosManual, name="Cantidad_servidos_manuales"),
    path('ActualizarFormuladoManualCantidad/', actualizar.actualizarCantidadFormuladoManual, name="Cantidad_Formulado_manuales"),
    path('ActualizarServidosATolva/', actualizar.actualizarServidosATolva, name="A_Servidos_Tolva"),
    path('ActualizarFormuladoATolva/', actualizar.actualizarFormuladoATolva, name="A_Formulado_Tolva"),

    path('ActualizarCancelarServidosVehiculos/', actualizar.actualizarCancelarTolva, name="A_Pedido_Tolva"),
    path('ActualizarCancelarFormuladoVehiculos/', actualizar.actualizarCancelarFormulado, name="A_Pedido_Formulado"),
    ]
