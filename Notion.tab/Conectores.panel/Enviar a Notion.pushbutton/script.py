# -*- coding: utf-8 -*-
from pyrevit import revit, ui
import urllib2
import json
from System.Net import ServicePointManager, SecurityProtocolType

# Habilitar protocolo de seguridad moderno
ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12

# --- CONFIGURACIÓN ---
NOTION_TOKEN = "TU_TOKEN_AQUÍ"
DATABASE_ID = "ID_DE_TU_BASE_DE_DATOS"

def post_to_notion(data):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    json_payload = json.dumps(data).encode('utf-8')
    
    try:
        req = urllib2.Request(url, data=json_payload, headers=headers)
        response = urllib2.urlopen(req)
        return True
    except urllib2.HTTPError as e:
        error_msg = e.read()
        print("Error de Notion API: {}".format(error_msg))
        return False
    except Exception as e:
        print("Error de conexión: {}".format(e))
        return False

# --- LÓGICA DE REVIT ---
selection = revit.get_selection()

if not selection:
    ui.alert("Por favor, selecciona al menos un elemento en Revit.")
else:
    for el in selection:
        # Forma segura de obtener el nombre en pyRevit
        try:
            name = revit.query.get_name(el)
        except:
            name = "Elemento sin nombre"
            
        el_id = str(el.Id.ToString()) # El ID como string simple

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
            print("Éxito: [{}] enviado a Notion.".format(name))