# -*- coding: utf-8 -*-
import clr

# Referencias directas al núcleo de Windows (Sin pasar por pyrevit.forms)
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Windows.Forms as WinForms
from System.Drawing import Size, Point, Font, FontStyle

from pyrevit import revit
from Autodesk.Revit.UI.Selection import ObjectType

class FormularioSeguro(WinForms.Form):
    def __init__(self):
        # Configuración básica de la ventana
        self.Text = "Extracción de Datos - Revit 2024"
        self.Size = Size(350, 420)
        self.StartPosition = WinForms.FormStartPosition.CenterScreen
        self.TopMost = True
        self.datos = None

        # --- CONTROLES ---
        # Descripción (Texto)
        lbl_desc = WinForms.Label(Text="Descripción:", Location=Point(25, 20), Size=Size(280, 20))
        lbl_desc.Font = Font("Arial", 10, FontStyle.Bold)
        self.txt_desc = WinForms.TextBox(Location=Point(25, 45), Size=Size(280, 25))

        # Disciplina (Dropdown)
        lbl_disc = WinForms.Label(Text="Disciplina:", Location=Point(25, 95), Size=Size(280, 20))
        lbl_disc.Font = Font("Arial", 10, FontStyle.Bold)
        self.cb_disc = WinForms.ComboBox(Location=Point(25, 120), Size=Size(280, 25))
        self.cb_disc.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.cb_disc.Items.AddRange(('Arquitectura', 'Estructura'))
        self.cb_disc.SelectedIndex = 0

        # Estado (Dropdown)
        lbl_est = WinForms.Label(Text="Estado:", Location=Point(25, 175), Size=Size(280, 20))
        lbl_est.Font = Font("Arial", 10, FontStyle.Bold)
        self.cb_est = WinForms.ComboBox(Location=Point(25, 200), Size=Size(280, 25))
        self.cb_est.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.cb_est.Items.AddRange(('Abierto', 'En revisión', 'Resuelto', 'Cerrado'))
        self.cb_est.SelectedIndex = 0

        # Botón de acción
        btn_enviar = WinForms.Button(Text="ACEPTAR Y SELECCIONAR", Location=Point(25, 280), Size=Size(280, 50))
        btn_enviar.BackColor = System.Drawing.Color.LightGreen
        btn_enviar.FlatStyle = WinForms.FlatStyle.Flat
        btn_enviar.Click += self.finalizar_click

        # Añadir todos los elementos a la ventana
        self.Controls.Add(lbl_desc)
        self.Controls.Add(self.txt_desc)
        self.Controls.Add(lbl_disc)
        self.Controls.Add(self.cb_disc)
        self.Controls.Add(lbl_est)
        self.Controls.Add(self.cb_est)
        self.Controls.Add(btn_enviar)

    def finalizar_click(self, sender, e):
        # Guardamos la información capturada en un diccionario
        self.datos = {
            'descripcion': self.txt_desc.Text,
            'disciplina': self.cb_disc.SelectedItem,
            'estado': self.cb_est.SelectedItem
        }
        self.DialogResult = WinForms.DialogResult.OK
        self.Close()

def main():
    # 1. Ejecutar el formulario
    form = FormularioSeguro()
    
    if form.ShowDialog() == WinForms.DialogResult.OK:
        res = form.datos
        
        # 2. Proceder a la selección en Revit
        try:
            uidoc = revit.uidoc
            print("Vuelve a Revit y selecciona elementos. Haz clic en 'Finalizar' en la barra superior.")
            
            # Selección múltiple
            referencias = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona los elementos")
            
            # 3. Mostrar resumen en la consola
            print("\n" + "="*40)
            print("REGISTRO DE EXTRACCIÓN")
            print("="*40)
            print("DESCRIPCIÓN: {}".format(res['descripcion']))
            print("DISCIPLINA:  {}".format(res['disciplina']))
            print("ESTADO:      {}".format(res['estado']))
            print("ELEMENTOS:   {}".format(len(referencias)))
            print("="*40)
            
        except Exception:
            print("Selección cancelada por el usuario.")

if __name__ == "__main__":
    main()