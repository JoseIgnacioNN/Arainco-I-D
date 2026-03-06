# -*- coding: utf-8 -*-
import clr
import sys

# Importaciones directas de .NET para evitar errores de pyRevit
clr.AddReference('Params')
clr.AddReference('IronPython.Wpf')
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')

from System.IO import StringReader # Solución al error de tu imagen
from System import Windows
import wpf

from pyrevit import revit, forms
from Autodesk.Revit.UI.Selection import ObjectType

# 1. DISEÑO DE LA INTERFAZ (XAML)
xaml_code = """
<Window xmlns="http://schemas.microsoft.com/winfx/2000/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2000/xaml"
        Title="Formulario de Extracción" Height="380" Width="350" 
        WindowStartupLocation="CenterScreen" Topmost="True">
    <Grid Margin="20">
        <StackPanel>
            <TextBlock Text="Descripción:" FontWeight="Bold" Margin="0,0,0,5"/>
            <TextBox x:Name="txt_desc" Height="25" Margin="0,0,0,15"/>

            <TextBlock Text="Disciplina:" FontWeight="Bold" Margin="0,0,0,5"/>
            <ComboBox x:Name="cb_disciplina" Height="25" Margin="0,0,0,15"/>

            <TextBlock Text="Estado:" FontWeight="Bold" Margin="0,0,0,5"/>
            <ComboBox x:Name="cb_estado" Height="25" Margin="0,0,0,15"/>

            <Button Content="Aceptar y Seleccionar" Height="40" Click="aceptar_click" 
                    Background="#2ecc71" Foreground="White" FontWeight="Bold"/>
        </StackPanel>
    </Grid>
</Window>
"""

# 2. LÓGICA DE LA VENTANA
class MiFormulario(Windows.Window):
    def __init__(self):
        # Usamos StringReader directo de System.IO para cargar el XAML
        reader = StringReader(xaml_code)
        wpf.LoadComponent(self, reader)
        
        # Llenar los desplegables
        self.cb_disciplina.ItemsSource = ['Arquitectura', 'Estructura']
        self.cb_estado.ItemsSource = ['Abierto', 'En revision', 'Resuelto', 'Cerrado']
        
        self.datos = None

    def aceptar_click(self, sender, e):
        # Capturamos la info
        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': self.cb_disciplina.SelectedItem,
            'est': self.cb_estado.SelectedItem
        }
        self.DialogResult = True
        self.Close()

# 3. EJECUCIÓN
def inicio():
    ventana = MiFormulario()
    
    # Si el usuario hace clic en Aceptar
    if ventana.ShowDialog():
        d = ventana.datos
        
        try:
            uidoc = revit.uidoc
            # Permitimos seleccionar múltiples elementos
            print("Selecciona elementos en el modelo y presiona 'Finalizar' en la barra superior...")
            refs = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos")
            
            # Resultado en la consola de pyRevit
            print("\n" + "="*30)
            print("EXTRACCIÓN EXITOSA")
            print("="*30)
            print("Descripción: {}".format(d['desc']))
            print("Disciplina:  {}".format(d['disc']))
            print("Estado:      {}".format(d['est']))
            print("Elementos:   {}".format(len(refs)))
            print("="*30)
            
        except Exception as e:
            print("Selección cancelada o error: {}".format(e))

if __name__ == "__main__":
    inicio()