@echo off

rem Activa el entorno virtual
call "C:\Users\Luis\OneDrive\Documentos\Proyectos Mariano\Hermosillo\Programacion Web\1-Servicios Valmo\Valmo\venv\Scripts\activate"

rem Navega al directorio del proyecto Django
cd "C:\Users\Luis\OneDrive\Documentos\Proyectos Mariano\Hermosillo\Programacion Web\1-Servicios Valmo\Valmo\Ganadera V1"

rem Espera 10 segundos
timeout /t 10 > nul

rem Ejecuta el monitoreo en una nueva ventana (background)
start "Monitoreo" cmd /k python Aplicacion/monitoreo.py

rem Ejecuta el servidor de Django
python manage.py runserver 0.0.0.0:8000

rem Desactiva el entorno virtual al salir del servidor
deactivate

rem Pausa para mantener la ventana abierta
pause
