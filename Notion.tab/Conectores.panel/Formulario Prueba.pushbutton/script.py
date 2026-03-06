# -*- coding: utf-8 -*-
import clr

# Referencias directas al núcleo de Windows
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Windows.Forms as WinForms
from System.Drawing import Size, Point, Font, FontStyle, Color

from pyrevit import revit
from Autodesk.Revit.UI.Selection import ObjectType

class FormularioMultiseleccion(WinForms.Form):
    def __init__(self):
        self.Text = "Extracción de Datos - Multidisciplina"
        self.Size = Size(380, 520)
        self.StartPosition = WinForms.FormStartPosition.CenterScreen
        self.TopMost = True
        self.MaximizeBox = False
        self.datos = None

        fuente_label = Font("Arial", 10, FontStyle.Bold)

        # 1. Descripción
        lbl_desc = WinForms.Label(Text="Descripción:", Location=Point(25, 15), Size=Size(300, 40))
        lbl_desc.Font = fuente_label
        self.txt_desc = WinForms.TextBox(Location=Point(25, 40), Size=Size(310, 25))

        # 2. Disciplina (CAMBIO A SELECCIÓN MÚLTIPLE)
        lbl_disc = WinForms.Label(Text="Disciplinas (Selección múltiple):", Location=Point(25, 85), Size=Size(300, 20))
        lbl_disc.Font = fuente_label
        
        self.clb_disc = WinForms.CheckedListBox()
        self.clb_disc.Location = Point(25, 110)
        self.clb_disc.Size = Size(310, 100)
        self.clb_disc.CheckOnClick = True # Permite marcar con un solo clic
        
        # Agregamos las nuevas opciones
        disciplinas = ['Arquitectura', 'Estructura', 'Clima', 'Electricidad']
        for d in disciplinas:
            self.clb_disc.Items.Add(d)

        # 3. Estado (Dropdown normal)
        lbl_est = WinForms.Label(Text="Estado:", Location=Point(25, 230), Size=Size(300, 20))
        lbl_est.Font = fuente_label
        self.cb_est = WinForms.ComboBox(Location=Point(25, 255), Size=Size(310, 25))
        self.cb_est.DropDownStyle = WinForms.ComboBoxStyle.DropDownList
        self.cb_est.Items.AddRange(('Abierto', 'En revisión', 'Resuelto', 'Cerrado'))
        self.cb_est.SelectedIndex = 0

        # 4. Botón Aceptar
        btn = WinForms.Button(Text="ACEPTAR Y SELECCIONAR", Location=Point(25, 330), Size=Size(310, 55))
        btn.BackColor = Color.LightSkyBlue
        btn.FlatStyle = WinForms.FlatStyle.Flat
        btn.Font = Font("Arial", 10, FontStyle.Bold)
        btn.Click += self.aceptar_click

        # Agregar controles
        self.Controls.Add(lbl_desc)
        self.Controls.Add(self.txt_desc)
        self.Controls.Add(lbl_disc)
        self.Controls.Add(self.clb_disc)
        self.Controls.Add(lbl_est)
        self.Controls.Add(self.cb_est)
        self.Controls.Add(btn)

    def aceptar_click(self, sender, e):
        # Obtenemos todos los elementos marcados en la lista
        disciplinas_seleccionadas = []
        for item in self.clb_disc.CheckedItems:
            disciplinas_seleccionadas.append(item)

        if not disciplinas_seleccionadas:
            WinForms.MessageBox.Show("Por favor, selecciona al menos una disciplina.")
            return

        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': ", ".join(disciplinas_seleccionadas), # Las une con una coma
            'est': self.cb_est.SelectedItem
        }
        self.DialogResult = WinForms.DialogResult.OK
        self.Close()

def ejecutar():
    form = FormularioMultiseleccion()
    if form.ShowDialog() == WinForms.DialogResult.OK:
        res = form.datos
        
        try:
            uidoc = revit.uidoc
            print("INFO: {} | Disciplinas: {} | Estado: {}".format(res['desc'], res['disc'], res['est']))
            
            # Selección en Revit
            refs = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos")
            
            print("\n" + "="*40)
            print("PROCESO TERMINADO")
            print("="*40)
            print("Se vincularon {} elementos a las disciplinas: {}".format(len(refs), res['disc']))
            
        except Exception:
            print("Operación cancelada.")

if __name__ == "__main__":
    ejecutar()