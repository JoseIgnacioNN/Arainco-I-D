# -*- coding: utf-8 -*-
import clr

# Referencias directas al corazón de Windows para evitar errores de pyRevit
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Windows.Forms as WinForms
from System.Drawing import Size, Point, Font, FontStyle, Color

from pyrevit import revit
from Autodesk.Revit.UI.Selection import ObjectType

# --- CLASE DE LA INTERFAZ ---
class FormularioIndestructible(WinForms.Form):
    def __init__(self):
        self.Text = "Extracción de Datos - Revit 2024"
        self.Size = Size(350, 450)
        self.StartPosition = WinForms.FormStartPosition.CenterScreen
        self.TopMost = True
        self.MaximizeBox = False
        self.datos = None

        # Estilo de fuente
        fuente_label = Font("Arial", 10, FontStyle.Bold)

        # 1. Descripción
        lbl_desc = WinForms.Label(Text="Descripción:", Location=Point(25, 20), Size=Size(280, 20))
        lbl_desc.Font = fuente_label
        self.txt_desc = WinForms.TextBox(Location=Point(25, 45), Size=Size(280, 25))

        # 2. Disciplina
        lbl_disc = WinForms.Label(Text="Disciplina:", Location=Point(25, 95), Size=Size(280, 20))
        lbl_disc.Font = fuente_label
        self.cb_disc = WinForms.ComboBox(Location=Point(25, 120), Size=Size(280, 25))
        self.cb_disc.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.cb_disc.Items.AddRange(('Arquitectura', 'Estructura'))
        self.cb_disc.SelectedIndex = 0

        # 3. Estado
        lbl_est = WinForms.Label(Text="Estado:", Location=Point(25, 175), Size=Size(280, 20))
        lbl_est.Font = fuente_label
        self.cb_est = WinForms.ComboBox(Location=Point(25, 200), Size=Size(280, 25))
        self.cb_est.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.cb_est.Items.AddRange(('Abierto', 'En revisión', 'Resuelto', 'Cerrado'))
        self.cb_est.SelectedIndex = 0

        # 4. Botón Aceptar
        btn = WinForms.Button(Text="ACEPTAR Y SELECCIONAR", Location=Point(25, 280), Size=Size(280, 50))
        btn.BackColor = Color.LightGreen
        btn.FlatStyle = WinForms.FlatStyle.Flat
        btn.Font = Font("Arial", 9, FontStyle.Bold)
        btn.Click += self.aceptar_click

        # Agregar controles
        self.Controls.Add(lbl_desc)
        self.Controls.Add(self.txt_desc)
        self.Controls.Add(lbl_disc)
        self.Controls.Add(self.cb_disc)
        self.Controls.Add(lbl_est)
        self.Controls.Add(self.cb_est)
        self.Controls.Add(btn)

    def aceptar_click(self, sender, e):
        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': self.cb_disc.SelectedItem,
            'est': self.cb_est.SelectedItem
        }
        self.DialogResult = WinForms.DialogResult.OK
        self.Close()

# --- FUNCIÓN DE EJECUCIÓN ---
def ejecutar_proceso():
    form = FormularioIndestructible()
    
    # Mostramos la ventana
    if form.ShowDialog() == WinForms.DialogResult.OK:
        res = form.datos
        
        try:
            uidoc = revit.uidoc
            print("INFO CAPTURADA: {} | {} | {}".format(res['desc'], res['disc'], res['est']))
            print("VE A REVIT: Selecciona elementos y pulsa 'Finalizar' en la barra superior.")
            
            # Selección de elementos
            referencias = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos para la extracción")
            
            # Resultado en Consola
            print("\n" + "="*40)
            print("REGISTRO EXITOSO")
            print("="*40)
            print("Elementos seleccionados: {}".format(len(referencias)))
            print("="*40)
            
        except Exception:
            print("Selección cancelada por el usuario.")

if __name__ == "__main__":
    ejecutar_proceso()