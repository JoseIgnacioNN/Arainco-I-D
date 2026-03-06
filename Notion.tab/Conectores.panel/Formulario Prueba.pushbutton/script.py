# -*- coding: utf-8 -*-
from pyrevit import forms

# 1. Definición de las opciones para los desplegables (Dropdowns)
opciones_disciplina = ['Arquitectura', 'Estructura']
opciones_estado = ['Abierto', 'En revisión', 'Resuelto', 'Cerrado']

# 2. Construcción del Formulario Flexible
components = [
    # Campo de texto para la descripción
    forms.controls.Label("Descripción del hallazgo:"),
    forms.controls.TextBox("descripcion", default="Escribe aquí..."),
    
    # Selector para Disciplina
    forms.controls.Label("Selecciona la Disciplina:"),
    forms.controls.ComboBox("disciplina", opciones_disciplina),
    
    # Selector para Estado
    forms.controls.Label("Estado actual:"),
    forms.controls.ComboBox("estado", opciones_estado),
    
    # Botón de acción
    forms.controls.Button("Aceptar")
]

# 3. Lanzar la ventana
form = forms.FlexForm("Formulario de Información", components)
form.show_dialog()

# 4. Procesar los resultados
# El diccionario 'form.values' contiene lo que el usuario ingresó/seleccionó
if form.values:
    res_descripcion = form.values.get("descripcion")
    res_disciplina = form.values.get("disciplina")
    res_estado = form.values.get("estado")

    # Mostrar resumen de lo capturado
    print("--- INFORMACIÓN CAPTURADA ---")
    print("Descripción: {}".format(res_descripcion))
    print("Disciplina:  {}".format(res_disciplina))
    print("Estado:      {}".format(res_estado))
else:
    print("Operación cancelada por el usuario.")