# -*- coding: utf-8 -*-
from pyrevit import forms

# 1. Opciones para los menús desplegables
opciones_disciplina = ['Arquitectura', 'Estructura']
opciones_estado = ['Abierto', 'En revisión', 'Resuelto', 'Cerrado']

# 2. Definición de componentes usando la sintaxis compatible
# Importamos los controles directamente para evitar el error 'module has no attribute controls'
from pyrevit.forms import FlexForm, Label, TextBox, ComboBox, Button

components = [
    Label("Descripción del hallazgo:"),
    TextBox("descripcion", default="Escribe aquí..."),
    
    Label("Selecciona la Disciplina:"),
    ComboBox("disciplina", opciones_disciplina),
    
    Label("Estado actual:"),
    ComboBox("estado", opciones_estado),
    
    Button("Aceptar")
]

# 3. Lanzar la ventana
form = FlexForm("Formulario de Extracción", components)
form.show_dialog()

# 4. Procesar y mostrar los resultados
if form.values:
    # Extraemos los valores del diccionario
    desc = form.values.get("descripcion")
    disc = form.values.get("disciplina")
    est = form.values.get("estado")

    print("--- DATOS CAPTURADOS ---")
    print("Descripción: {}".format(desc))
    print("Disciplina:  {}".format(disc))
    print("Estado:      {}".format(est))
else:
    print("Operación cancelada.")