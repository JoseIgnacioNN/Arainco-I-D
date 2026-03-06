# -*- coding: utf-8 -*-
from pyrevit import forms, revit, script
from Autodesk.Revit.UI.Selection import ObjectType

# Inicialización de referencias
uidoc = revit.uidoc
doc = revit.doc
output = script.get_output()

def ejecutar_extractor():
    # 1. CAPTURA DE TEXTO (Validado)
    texto_proyecto = ""
    while not texto_proyecto:
        texto_proyecto = forms.ask_for_string(
            title="Configuración de Parámetro",
            prompt="Introduce el código o descripción (No puede estar vacío):"
        )
        
        # Si el usuario cierra la ventana o da a cancelar
        if texto_proyecto is None:
            print("Operación cancelada por el usuario.")
            return # Sale de la función de forma limpia
            
        texto_proyecto = texto_proyecto.strip()

    # 2. SELECCIÓN DE ELEMENTOS EN EL MODELO
    try:
        print("Ve a Revit y selecciona los elementos...")
        referencias = uidoc.Selection.PickObjects(
            ObjectType.Element, 
            "Selecciona los elementos para procesar con el texto: {}".format(texto_proyecto)
        )
    except Exception:
        # Esto captura si el usuario presiona ESC
        forms.alert("Selección cancelada o interrumpida.", warn_icon=True)
        return

    # 3. PROCESAMIENTO DE INFORMACIÓN
    elementos = [doc.GetElement(ref.ElementId) for ref in referencias]
    
    # Preparamos una lista para mostrar resultados finales
    resultados = []
    
    for el in elementos:
        # Intentamos obtener el nombre del tipo de forma segura
        nombre_tipo = "N/A"
        param_tipo = el.LookupParameter("Nombre de tipo") or el.get_Parameter(revit.DB.BuiltInParameter.ELEM_TYPE_PARAM)
        
        if param_tipo:
            nombre_tipo = param_tipo.AsValueString()
        
        resultados.append([el.Id, nombre_tipo, texto_proyecto])

    # 4. MOSTRAR RESULTADOS
    output.print_md("## Informe de Extracción")
    output.print_table(
        table_data=resultados,
        title="Elementos vinculados a: " + texto_proyecto,
        columns=["ID Elemento", "Tipo de Familia", "Texto Ingresado"]
    )

# Ejecutar el script
if __name__ == "__main__":
    ejecutar_extractor()