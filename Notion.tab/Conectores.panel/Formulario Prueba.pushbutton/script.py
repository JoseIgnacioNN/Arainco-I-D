from pyrevit import forms

texto = ""
while not texto:
    texto = forms.ask_for_string(
        title="Configuración de Parámetro",
        prompt="Introduce el código del proyecto (No puede estar vacío):"
    )
    if texto is None: # El usuario presionó "Cancelar" o la X
        script.exit() 
    
    texto = texto.strip() # Limpiamos espacios
    
print("Texto validado: {}".format(texto))