# -*- coding: utf-8 -*-
from pyrevit import revit, ui
import urllib2
import json

# --- CONFIGURACIÓN DE NOTION ---
NOTION_TOKEN = "TU_TOKEN_AQUÍ"
DATABASE_ID = "ID_DE_TU_BASE_DE_DATOS"


def post_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    req = urllib2.Request(url, data=json.dumps(data), headers=headers)
    try:
        urllib2.urlopen(req)
        return True
    except Exception as e:
        print("Error enviando a Notion: {}".format(e))
        return False


# --- LÓGICA DE REVIT ---
selection = revit.get_selection()

if not selection:
    ui.alert("Por favor, selecciona al menos un elemento.")
else:
    for el in selection:
        name = el.Name
        el_id = str(el.Id)

        # Estructura del JSON para Notion
        # Asumiendo que tu tabla tiene columnas: "Nombre" (Title) e "ID Revit" (Rich Text)
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
            print("Elemento {} enviado con éxito.".format(name))