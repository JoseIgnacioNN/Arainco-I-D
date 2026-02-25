# -*- coding: utf-8 -*-
# Agregar esta línea al inicio del código permite agregar letras con tilde, ñ, etc.


# Importaciones comunes ===================================================================================

from Autodesk.Revit import DB, UI  # DB: Acceso a elementos del modelo (muros, vistas, parámetros, etc). UI: Acceso a la interfaz de usuario (UIDocument, selección, etc.)
from pyrevit import revit, forms  # Abstracciones útiles del modelo actual y formularios
from Autodesk.Revit.DB import UnitUtils, UnitTypeId # Conversión de unidades

# Módulo que accede a algunas clases que PyRevit no referencia automáticamente con DB
# import clr 
# clr.AddReference('RevitServices')
# from RevitServices.Persistence import DocumentManager

# Inicializacion ===================================================================================

doc = revit.doc
uidoc = revit.uidoc

# Comandos ===================================================================================

# Obtener listados de Elementos

# Objeto Wall: Muro dibujado en el modelo (instancia)
# Objeto WallType: Tipo de muro
# .WhereElementIsNotElementType(): Elemento dibujado en el modelo (instancia)
# .WhereElementIsElementType(): Elemento Tipo
# .ToElements(): convierte el objeto en una lista
# Categoría: Muro, Puertas, Ventanas, Armazón Estructural, etc.
# Familia: Hormigón Viga Rectangular, Hormigón Viga Circular, Ángulo, Costanera, Basic Wall, Curtain Wall, etc.
# Tipo: V20x60, V40x70, MHA e=20, MHA e=30, etc.

grids= DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
for grid in grids:
    grid_name = grid.Name

levels = DB.FilteredElementCollector(doc).OfClass(DB.Level).ToElements()
for level in levels:
    level_name = level.Name
    level_elevation = level.Elevation
    level_elevation = UnitUtils.ConvertFromInternalUnits(level_elevation, UnitTypeId.Meters)

walls = DB.FilteredElementCollector(doc).OfClass(DB.Wall).WhereElementIsNotElementType().ToElements() # Lista con todos los muros dibujados en el modelo (Objeto Wall)
for wall in walls:
    wall_type = wall.WallType # Obtiene el objeto WallType del objeto Wall
    wall_name = wall_type.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() # Obtiene el Tipo del objeto WallType

wall_types = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements() # Lista con todos los Type Name de los muros del modelo (Objeto WallType)
basic_wall_types = [wt for wt in wall_types if wt.Kind == DB.WallKind.Basic] # Lista filtrada por el tipo de muro 'Basic Wall'
for wall_type in basic_wall_types:
    wall_name = wall_type.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() # Obtiene el TypeName del objeto WallType

rebar_types = DB.FilteredElementCollector(doc).OfClass(DB.Structure.RebarBarType).WhereElementIsElementType().ToElements() # Lista con los tipos de barra
for rebar in rebar_types:
    name = rebar.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() # Nombres de tipos de barra
    phi = round(rebar.get_Parameter(DB.BuiltInParameter.REBAR_BAR_DIAMETER).AsDouble() * 304.8, 2) # Diámetros de tipos de barra

# Ver atributos de un Objeto
for attr in dir(basic_wall_types): # dir() devuelve todos los atributos y métodos de un objeto
    if not attr.startswith('_'): # Evita mostrar los atributos internos, ya que no sirven para el usuario
        print(attr)

# Extraer parámetros de Elementos
ID = wall.Id
volumen = wall.get_Parameter(DB.BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
familia = wall_type.FamilyName
espesor_muro = wall_type.get_Parameter(DB.BuiltInParameter.WALL_ATTR_WIDTH_PARAM).AsDouble()
espesor_losa = slab_type.get_Parameter(DB.BuiltInParameter.FLOOR_ATTR_THICKNESS_PARAM).AsDouble()

# Transformar el parámetro de un elemento de Revit, a número o string
param.AsValueString()
param.AsDouble()
param.AsInteger()

# Desplegar una lista para escoger
basic_wall_types = forms.SelectFromList.show(
    basic_wall_types,
    title='Selecciona un tipo de muro',
    multiselect=False,
    button_name="Seleccionar"
)

# Avisos
print('Hola')
forms.alert('Hola', title='Aviso')

# Seleccionar Elementos
try:
    ref = uidoc.Selection.PickObject(UI.Selection.ObjectType.Element,'Selecciona una losa estructural')
    elemento = doc.GetElement(ref)
    volumen = elemento.get_Parameter(DB.BuiltInParameter.HOST_VOLUME_COMPUTED).AsDouble()
except Exception:
    pass # El código continúa incluso si el usuario canceló la operación

# Obtener la geometría de un elemento
opt = DB.Options()
geom_elem = slab.get_Geometry(opt)

# Crear Muros (SIN TERMINAR)
with revit.Transaction("Crear Muro"):
    DB.Wall.Create(doc, line, wall_type.Id, level.Id, height, offset, flipped, structural)
