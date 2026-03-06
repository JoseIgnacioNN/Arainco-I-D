# -*- coding: utf-8 -*-
from pyrevit import forms

# Forzamos una salida limpia para ver si el módulo carga
try:
    res = forms.ask_for_string(
        title="Prueba de Texto",
        prompt="Escribe algo para probar:"
    )

    if res:
        forms.alert("Escribiste: {}".format(res))
    else:
        print("Cancelado por el usuario.")

except Exception as e:
    print("Error detectado: {}".format(e))