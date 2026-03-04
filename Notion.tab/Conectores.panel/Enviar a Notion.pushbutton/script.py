# -*- coding: utf-8 -*-
from pyrevit import revit, ui
import urllib2
import json

NOTION_TOKEN = "TU_TOKEN_AQUÍ"
DATABASE_ID = "ID_DE_TU_BASE_DE_DATOS"


def post_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # IMPORTANTE: Convertir a JSON y luego a bytes
    json_payload = json.dumps(data).encode('utf-8')

    try:
        req = urllib2.Request(url, data=json_payload, headers=headers)
        response = urllib2.urlopen(req)
        return True
    except urllib2.HTTPError as e:
        # Esto te dirá el error real de la API de Notion (ej. columna inexistente)
        print("Error de Notion API: {}".format(e.read()))
        return False
    except Exception as e:
        print("Error general: {}".format(e))
        return False


# --- LÓGICA DE REVIT ---
selection = revit.get_selection()

if not selection:
    ui.alert("Por favor, selecciona al menos un elemento en Revit.")
else:
    for el in selection:
        # Obtenemos el nombre del tipo o de la instancia
        name = revit.query.get_name(el)
        el_id = str(el.Id.IntegerValue)  # Usamos el Integer para que sea un ID limpio

        payload = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Nombre": {
                    "title": [{"text": {"content": name}}]
                },
                "ID Revit": {
                    "rich_text": [{"text": {"content": el_id}}]
                }
            }
        }

        if post_to_notion(payload):
            print("Éxito: Elemento [{}] enviado.".format(el_id))