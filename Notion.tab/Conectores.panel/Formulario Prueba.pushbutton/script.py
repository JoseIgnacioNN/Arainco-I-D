# -*- coding: utf-8 -*-
import clr
clr.AddReference('IronPython.Wpf')
from pyrevit import revit, forms
from Autodesk.Revit.UI.Selection import ObjectType
import wpf
from System import Windows

# 1. DISEÑO DE LA INTERFAZ (XAML)
xaml_code = """
<Window xmlns="http://schemas.microsoft.com/winfx/2000/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2000/xaml"
        Title="Formulario de Extracción" Height="350" Width="350" 
        WindowStartupLocation="CenterScreen" Topmost="True">
    <StackPanel Margin="20">
        <TextBlock Text="Descripción:" FontWeight="Bold" Margin="0,0,0,5"/>
        <TextBox x:Name="txt_desc" Height="25" Margin="0,0,0,15"/>

        <TextBlock Text="Disciplina:" FontWeight="Bold" Margin="0,0,0,5"/>
        <ComboBox x:Name="cb_disciplina" Height="25" Margin="0,0,0,15"/>

        <TextBlock Text="Estado:" FontWeight="Bold" Margin="0,0,0,5"/>
        <ComboBox x:Name="cb_estado" Height="25" Margin="0,0,0,15"/>

        <Button Content="Aceptar" Height="35" Click="aceptar_click" Background="#e1e1e1"/>
    </StackPanel>
</Window>
"""

# 2. LÓGICA DE LA VENTANA
class MiFormulario(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, forms.utils.StringReader(xaml_code))
        
        # Llenar los desplegables
        self.cb_disciplina.ItemsSource = ['Arquitectura', 'Estructura']
        self.cb_estado.ItemsSource = ['Abierto', 'En revision', 'Resuelto', 'Cerrado']
        
        self.datos = None

    def aceptar_click(self, sender, e):
        # Guardar resultados y cerrar
        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': self.cb_disciplina.SelectedItem,
            'est': self.cb_estado.SelectedItem
        }
        self.Close()

# 3. EJECUCIÓN PRINCIPAL
def inicio():
    # Lanzar formulario
    ventana = MiFormulario()
    ventana.ShowDialog()

    if ventana.datos and ventana.datos['desc']:
        d = ventana.datos
        
        # Ahora procedemos a la selección en el modelo
        try:
            uidoc = revit.uidoc
            print("Selecciona elementos en Revit...")
            refs = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos")
            
            # Resumen final
            print("\n--- PROCESO COMPLETADO ---")
            print("Info: {} | {} | {}".format(d['desc'], d['disc'], d['est']))
            print("Elementos seleccionados: {}".format(len(refs)))
            
        except Exception:
            print("Selección cancelada.")
    else:
        print("Formulario incompleto o cerrado.")

if __name__ == "__main__":
    inicio()