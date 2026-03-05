@echo off

rem Activa el entorno virtual
call "C:\Users\Administrador\Desktop\SERVIDOR\venv\Scripts\activate"

rem Navega al directorio del proyecto Django
cd "C:\Users\Administrador\Desktop\SERVIDOR\Santa valeria 2702262"

rem Espera 10 segundos
timeout /t 10 > nul

rem Ejecuta el servidor de Django
python manage.py runserver 0.0.0.0:8000

rem Desactiva el entorno virtual al salir del servidor
deactivate

rem Pausa para mantener la ventana abierta
pause
