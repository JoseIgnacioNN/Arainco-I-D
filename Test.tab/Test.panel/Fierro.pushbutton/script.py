# -*- coding: utf-8 -*-

import clr
clr.AddReference("RevitServices")
from Autodesk.Revit import DB, UI
from Autodesk.Revit.DB.Structure import Rebar, RebarStyle
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from pyrevit import revit, forms

doc = revit.doc
uidoc = revit.uidoc

# Seleccionar una losa estructural
ref = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element,"Selecciona una losa estructural")
slab = doc.GetElement(ref)

# Obtener tipos de barra de refuerzo
rebar_types = DB.FilteredElementCollector(doc).OfClass(DB.Structure.RebarBarType).WhereElementIsElementType().ToElements()    
rebar_types_names = [rt.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() for rt in rebar_types]

selected_rebar_name = forms.SelectFromList.show(rebar_types_names, title='Selecciona el diámetro de barra', button_name="Seleccionar")
if not selected_rebar_name:
    forms.alert("No se seleccionó ningún tipo de barra.", title="Cancelado")
    raise SystemExit()
selected_rebar = next((x for x, y in zip(rebar_types, rebar_types_names) if y == selected_rebar_name), None) # Se encuentra el Tipo de Barra asociado al nombre seleccionado

# Obtener geometría de la losa
opt = DB.Options()
geom_elem = slab.get_Geometry(opt)

# Iterar la geometría para encontrar la cara superior de la losa
top_face = None
for geom_obj in geom_elem:
    solid = geom_obj if isinstance(geom_obj, DB.Solid) else None
    if solid:
        for face in solid.Faces:
            if isinstance(face, DB.PlanarFace) and face.FaceNormal.IsAlmostEqualTo(DB.XYZ.BasisZ):
                top_face = face
                break
    if top_face:
        break

if not top_face:
    forms.alert("No se pudo encontrar la cara superior de la losa.", title="Error")
    raise SystemExit()

# Crear línea de refuerzo sobre la cara superior
uv_min = top_face.GetBoundingBox().Min
uv_max = top_face.GetBoundingBox().Max

# Opcional: desplazar el punto UV antes de evaluar
uv_p1 = DB.UV(uv_min.U + 0.5, uv_min.V + 0.5)
uv_p2 = DB.UV(uv_max.U - 0.5, uv_max.V - 0.5)

p1 = top_face.Evaluate(uv_p1)
p2 = top_face.Evaluate(uv_p2)

rebar_line = DB.Line.CreateBound(p1, p2) # Línea por donde se dibujará la barra

# Crear barra de refuerzo a través de la línea
with revit.Transaction("Enfierrar Losa"):
    rebar = DB.Structure.Rebar.CreateFromCurves(
        doc,
        RebarStyle.Standard,
        selected_rebar, # Tipo de barra seleccionado
        None, # Start Hook
        None, # End Hook
        slab, # Host element
        DB.XYZ.BasisZ,
        [rebar_line], # Línea por donde se dibujará la barra
        DB.Structure.RebarHookOrientation.Left, # Orientación del Start Hook
        DB.Structure.RebarHookOrientation.Right, # Orientación del End Hook
        True,
        True
    )

forms.alert("✅ Barra creada sobre la losa.", title="pyRevit")
