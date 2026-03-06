# -*- coding: utf-8 -*-
import clr
# Referencias directas al núcleo de Windows
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import (Application, Form, Label, TextBox, 
                                  ComboBox, Button, DockStyle, Padding)
from System.Drawing import Size, Point, Font, FontStyle

from pyrevit import revit
from Autodesk.Revit.UI.Selection import ObjectType

class FormularioResistente(Form):
    def __init__(self):
        self.Text = "Extracción de Datos"
        self.Size = Size(350, 400)
        self.Padding = Padding(20)
        self.StartPosition = Windows.Forms.FormStartPosition.CenterScreen
        self.TopMost = True
        self.datos = None

        # --- CONTROLES ---
        # Descripción
        lbl_desc = Label(Text="Descripción:", Location=Point(20, 20), Size=Size(250, 20))
        lbl_desc.Font = Font(lbl_desc.Font, FontStyle.Bold)
        self.txt_desc = TextBox(Location=Point(20, 45), Size=Size(280, 25))

        # Disciplina
        lbl_disc = Label(Text="Disciplina:", Location=Point(20, 90), Size=Size(250, 20))
        lbl_disc.Font = Font(lbl_disc.Font, FontStyle.Bold)
        self.cb_disc = ComboBox(Location=Point(20, 115), Size=Size(280, 25), DropDownStyle=Windows.Forms.ComboBoxStyle.DropDownList)
        self.cb_disc.Items.AddRange(('Arquitectura', 'Estructura'))

        # Estado
        lbl_est = Label(Text="Estado:", Location=Point(20, 160), Size=Size(250, 20))
        lbl_est.Font = Font(lbl_est.Font, FontStyle.Bold)
        self.cb_est = ComboBox(Location=Point(20, 185), Size=Size(280, 25), DropDownStyle=Windows.Forms.ComboBoxStyle.DropDownList)
        self.cb_est.Items.AddRange(('Abierto', 'En revisión', 'Resuelto', 'Cerrado'))

        # Botón
        btn = Button(Text="Aceptar y Seleccionar", Location=Point(20, 260), Size=Size(280, 45))
        btn.Click += self.aceptar_click

        # Agregar controles a la ventana
        self.Controls.Add(lbl_desc)
        self.Controls.Add(self.txt_desc)
        self.Controls.Add(lbl_disc)
        self.Controls.Add(self.cb_disc)
        self.Controls.Add(lbl_est)
        self.Controls.Add(self.cb_est)
        self.Controls.Add(btn)

    def aceptar_click(self, sender, e):
        # Guardar info y cerrar
        self.datos = {
            'desc': self.txt_desc.Text,
            'disc': self.cb_disc.SelectedItem,
            'est': self.cb_est.SelectedItem
        }
        self.DialogResult = Windows.Forms.DialogResult.OK
        self.Close()

def ejecutar():
    form = FormularioResistente()
    # Abrir ventana
    if form.ShowDialog() == Windows.Forms.DialogResult.OK:
        d = form.datos
        
        try:
            uidoc = revit.uidoc
            print("Vuelve a Revit y selecciona elementos. Pulsa 'Finalizar' arriba.")
            refs = uidoc.Selection.PickObjects(ObjectType.Element, "Selecciona elementos")
            
            # Resultado final
            print("\n" + "="*30)
            print("EXTRACCIÓN COMPLETADA")
            print("="*30)
            print("Descripción: {}".format(d['desc']))
            print("Disciplina:  {}".format(d['disc']))
            print("Estado:      {}".format(d['est']))
            print("Elementos:   {}".format(len(refs)))
            print("="*30)
            
        except Exception:
            print("Selección cancelada.")

if __name__ == "__main__":
    ejecutar()