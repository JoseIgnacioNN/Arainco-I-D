# -*- coding: utf-8 -*-
from Autodesk.Revit import DB
from Autodesk.Revit import UI
from pyrevit import revit, forms
from Autodesk.Revit.Exceptions import OperationCanceledException

doc = revit.doc
uidoc = revit.uidoc

# ===================================================================================
# 1. SELECCIONAR LA LOSA (HOST)
# ===================================================================================
try:
    ref = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element, "Selecciona una losa estructural")
    slab = doc.GetElement(ref)
except OperationCanceledException:
    forms.alert("No se seleccionó nada.", exitscript=True)

# ===================================================================================
# 2. CONSEGUIR TIPOS NECESARIOS (BarType y HookType)
# ===================================================================================

# Obtenemos el tipo de barra disponible en el proyecto
rebar_types = DB.FilteredElementCollector(doc).OfClass(DB.Structure.RebarBarType).WhereElementIsElementType().ToElements() # Lista de barras (Objeto)   
rebar_types_names = [rt.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() for rt in rebar_types] # Lista de barras (Nombre)
rebar_selected = forms.SelectFromList.show(rebar_types_names, title='Selecciona el diámetro de barra', button_name="Seleccionar") # Formulario con nombre de barras
rebar_selected = next((x for x, y in zip(rebar_types, rebar_types_names) if y == rebar_selected), None) # Encuentra el tipo de barra (objeto) asociado al nombre seleccionado


# ===================================================================================
# ELEGIR TRAZADO DE BARRA
# ===================================================================================

snaps = UI.Selection.ObjectSnapTypes.Endpoints | UI.Selection.ObjectSnapTypes.Intersections | UI.Selection.ObjectSnapTypes.Nearest # Fuerza la configuración de snaps
try:
    picked_p1 = uidoc.Selection.PickPoint(snaps, "Paso 3: Haz clic en el PUNTO INICIAL") # Clic 1
    picked_p2 = uidoc.Selection.PickPoint(snaps, "Paso 4: Haz clic en el PUNTO FINAL") # Clic 2
except OperationCanceledException:
    forms.alert("Selección de puntos cancelada.", exitscript=True)

#print(picked_p1.X)

# ===================================================================================
# 3. DEFINIR LA GEOMETRÍA
# ===================================================================================

# Para este ejemplo, crearemos una línea basada en la ubicación de la losa.
# Usamos el BoundingBox para asegurar que la barra quede DENTRO de la losa.
bbox = slab.get_BoundingBox(None)
center = (bbox.Min + bbox.Max) / 2.0

# Crear una línea de 1 metro (aprox 3.28 pies) en el centro de la losa
p1 = DB.XYZ(center.X, center.Y, center.Z)
p2 = DB.XYZ(center.X + 3.28, center.Y, center.Z) # +1 metro en X

# Las curvas deben estar en una lista de Python o .NET
curves = [DB.Line.CreateBound(p1, p2)]

# ===================================================================================
# 4. DEFINIR LA DIRECCIÓN (VECTOR NORMAL)
# ===================================================================================
# Esto es CRÍTICO. El vector normal define "hacia dónde mira" la barra.
# Si la barra está acostada en el suelo (plano XY), la normal suele ser el eje Z (0,0,1)
# o el eje Y (0,1,0) dependiendo de cómo quieras que rote.
normal_vector = DB.XYZ(0, 0, 1) 

# ===================================================================================
# 5. CREAR LA ARMADURA
# ===================================================================================
with revit.Transaction("Crear Barra"):
    try:
        # Método CreateFromCurves
        # Args: Documento, Estilo, TipoBarra, GanchoInicio, GanchoFin, ElementoAnfitrión, Normal, Curvas, HookOrientStart, HookOrientEnd, UsarHookExistente, ShapeMatch
        rebar = DB.Structure.Rebar.CreateFromCurves(
            doc,
            DB.Structure.RebarStyle.Standard,
            rebar_selected,
            None, # Sin gancho al inicio
            None, # Sin gancho al final
            slab, # El anfitrión (Losa)
            normal_vector,
            curves,
            DB.Structure.RebarHookOrientation.Right,
            DB.Structure.RebarHookOrientation.Right,
            True,
            True
        )
        print("Barra creada exitosamente ID: {}".format(rebar.Id))
    except Exception as e:
        print("Error al crear barra: {}".format(e))