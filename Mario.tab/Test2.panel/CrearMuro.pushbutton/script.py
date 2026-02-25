# -*- coding: utf-8 -*-

# Importar ========================================================
import clr
clr.AddReference("RevitServices")
from pyrevit import revit, forms
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

# Funciones =======================================================

def mm_to_ft(mm):
    return mm / 304.8

def m_to_ft(m):
    return m / 0.3048

def ask_for_float(prompt, default):
    try:
        return float(forms.ask_for_string(prompt, default=default))
    except:
        forms.alert("Entrada inválida. Debe ser un número.", title="Error")
        raise SystemExit()

# INICIALIZACIÓN ==================================================
doc = revit.doc

# SELECCIÓN DE TIPO DE MURO =======================================
wall_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements() # Lista con todos los Type Name de muros
wall_types = [wt for wt in wall_types if wt.FamilyName == "Basic Wall"] # Lista filtrada por la familia "Basic Wall"

wall_types = [(wt.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString(), wt) for wt in wall_types]

wall_type = forms.SelectFromList.show(
    [name for name, _ in wall_types],
    title='Selecciona un tipo de muro',
    multiselect=False
)

if not wall_type:
    forms.alert("No se seleccionó ningún tipo de muro.", title="Cancelado")
    raise SystemExit()

# ==== ENTRADAS DEL USUARIO ====
length_m = ask_for_float("Longitud del muro (m):", "5")
height_m = ask_for_float("Altura del muro (m):", "3")
x_start = ask_for_float("Posición X inicial (m):", "0")
y_start = ask_for_float("Posición Y inicial (m):", "0")

# ==== CONVERSIÓN A PIES ====
length_ft = m_to_ft(length_m)
height_ft = m_to_ft(height_m)
x_ft = m_to_ft(x_start)
y_ft = m_to_ft(y_start)

# ==== NIVEL BASE ====
level = FilteredElementCollector(doc).OfClass(Level).FirstElement()

# ==== DEFINIR GEOMETRÍA ====
start = XYZ(x_ft, y_ft, 0)
end = XYZ(x_ft + length_ft, y_ft, 0)
line = Line.CreateBound(start, end)

# ==== CREAR MURO ====
with revit.Transaction("Crear muro personalizado"):
    wall = Wall.Create(
        doc,
        line,
        wall_type.Id,
        level.Id,
        height_ft,
        0.0,
        False,
        False
    )

forms.alert("Muro creado:\nTipo: {}\nLongitud: {} m\nAltura: {} m\nInicio: ({}, {}) m".format(
    wall_type.Name, length_m, height_m, x_start, y_start), title="pyRevit")

