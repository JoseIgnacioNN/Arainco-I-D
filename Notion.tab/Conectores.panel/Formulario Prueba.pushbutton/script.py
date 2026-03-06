from pyrevit import forms

# Muestra una ventana emergente para capturar texto
texto_capturado = forms.ask_for_string(
    default='Texto por defecto',
    prompt='Introduce el texto aquí:',
    title='Capturador de Texto'
)

if texto_capturado:
    print("El usuario escribió: {}".format(texto_capturado))
else:
    print("Operación cancelada.")