"""Calculates total volume of all walls in the model."""

from Autodesk.Revit import DB # DB Contiene todas las clases de Revit (muros, elementos, vistas, parametros, etc)
from pyrevit import revit

doc = revit.doc

# Creating collector instance and collecting all the walls from the model
wall_collector = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

# Iterate over wall and collect Volume data
total_volume = 0.0
    
for wall in wall_collector:
    vol_param = wall.get_Parameter(DB.BuiltInParameter.HOST_VOLUME_COMPUTED)
    if vol_param:
        total_volume = total_volume + vol_param.AsDouble() # Se debe pasar de ft3 a m3

# now that results are collected, print the total
total_volume=total_volume*0.028316846592
print("Volumen total de muros: " + str(total_volume)) + " m3"
