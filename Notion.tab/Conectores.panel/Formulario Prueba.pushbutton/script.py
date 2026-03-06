# -*- coding: utf-8 -*-
import clr
# Referencias básicas de Windows
clr.AddReference('IronPython.Wpf')
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')

import System.IO
from System import Windows
import wpf

from pyrevit import revit
from Autodesk.Revit.UI.Selection import ObjectType

# 1. DISEÑO DE LA INTERFAZ (XAML)
# He simplificado el diseño para asegurar compatibilidad total
xaml_code = """
<Window xmlns="http://schemas.microsoft.com/winfx/2000/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2000/xaml"
        Title="Formulario de Extracción" Height="350" Width="300" 
        WindowStartupLocation="CenterScreen" Topmost="True">
    <StackPanel Margin="20">
        <TextBlock Text="Descripción:" Margin="0,0,0,5" FontWeight="Bold"/>
        <TextBox x:Name="txt_desc" Height="25" Margin="0,0,0,15"/>

        <TextBlock Text="Disciplina:" Margin="0,0,0,5" FontWeight="Bold"/>
        <ComboBox x:Name="cb_disciplina" Height="25" Margin="0,0,0,15"/>

        <TextBlock Text="Estado:" Margin="0,0,0,5" FontWeight="Bold"/>
        <ComboBox x:Name="cb_estado" Height="25" Margin="0,0,0,15"/>

        <Button Content="Aceptar y Seleccionar" Height="40" Click="aceptar_click"/>
    </StackPanel>
</Window>
"""

# 2. LÓGICA DE LA VENTANA
class MiFormulario(Windows.Window):
    def __init__(self):
        # Cargamos el XAML usando el lector nativo de System.IO
        reader = System.IO.StringReader(xaml_code)
        wpf.LoadComponent(self, reader)
        
        # Llenamos los desplegables manualmente
        self.cb_disciplina.ItemsSource = ['Arquitectura', 'Estructura']
        self.cb_estado.ItemsSource = ['Abierto', 'En revision', 'Resuelto', 'Cerrado']
        self.datos = None

    def aceptar_click(self, sender, e):
        # Guardamos la selección del usuario
        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': self.cb_disciplina.SelectedItem,
            'est': self.cb_estado.SelectedItem
        }
        self.DialogResult = True
        self.Close()

# 3. FUNCIÓN PRINCIPAL
def ejecutar():
    form = MiFormulario()
    # Mostramos el formulario
    if form.ShowDialog():
        info = form.datos
        
        try:
            uidoc = revit.uidoc
            # Iniciamos la selección en Revit
            print("Selecciona elementos y presiona 'Finalizar'...")
            refs = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos")
            
            # Resultado por consola
            print("\n" + "="*20)
            print("DATOS CAPTURADOS:")
            print("Descripción: {}".format(info['desc']))
            print("Disciplina:  {}".format(info['disc']))
            print("Estado:      {}".format(info['est']))
            print("Elementos:   {}".format(len(refs)))
            print("="*20)
            
        except Exception as ex:
            print("Selección cancelada o terminada.")

if __name__ == "__main__":
    ejecutar()