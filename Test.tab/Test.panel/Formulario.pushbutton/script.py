# -*- coding: utf-8 -*-

from Autodesk.Revit import DB
from pyrevit import revit
from System.Windows import Window, Thickness, ResizeMode, TextWrapping
from System.Windows.Controls import StackPanel, ComboBox, Button, TextBox, Label
from System.Windows import Forms
doc = revit.doc

grids = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
grids = [grid.Name for grid in grids]  # Nombres de los grids
levels = DB.FilteredElementCollector(doc).OfClass(DB.Level).ToElements()
levels = [level.Name  for level in levels]  # Nombres de los niveles

# ---------- Formulario personalizado ----------
class CustomForm(Window):
    def __init__(self):
        self.Title = "Configuración"
        self.Width = 400
        self.Height = 370
        self.ResizeMode = ResizeMode.CanResizeWithGrip # Permite redimensionar el formulario
        self.MinHeight = self.Height # Con esto evito que se pueda modificar la altura del formulario
        self.MaxHeight = self.Height
        self.confirmado = False # Sirve para saber si se ha dado click en el botón Confirmar del formulario

        # Layout principal
        self.panel = StackPanel()
        self.panel.Margin = Thickness(20,10,20,10)

        # ComboBoxes
        self.combo1 = self._crear_combobox("Eje Horizontal", grids)
        self.combo2 = self._crear_combobox("Eje Vertical:", grids)
        self.combo3 = self._crear_combobox("Piso:", levels)

        # Botón de seleccionar carpeta
        self.folder_button = Button()
        self.folder_button.Content = "Seleccionar carpeta"
        self.folder_button.Click += self.seleccionar_carpeta
        self.folder_button.Margin = Thickness(0, 20, 0, 10)

        # Texto para carpeta seleccionada
        self.folder_text = TextBox()
        self.folder_text.Height = 50
        self.folder_text.TextWrapping = TextWrapping.Wrap # Ajusta el texto al ancho del TextBox
        self.folder_text.AcceptsReturn = True # Permite salto de línea del texto
        self.folder_text.IsReadOnly = True
        self.folder_text.Margin = Thickness(0, 0, 0, 10)

        # Botón confirmar
        self.confirm_button = Button()
        self.confirm_button.Content = "Confirmar"
        self.confirm_button.Margin = Thickness(0, 10, 0, 0)
        self.confirm_button.Height = 40
        self.confirm_button.Click += self.confirmar

        # Agregar al panel
        self.panel.Children.Add(self.folder_button)
        self.panel.Children.Add(self.folder_text)
        self.panel.Children.Add(self.confirm_button)

        self.Content = self.panel

    def _crear_combobox(self, label_text, opciones):
        label = Label()
        label.Content = label_text
        self.panel.Children.Add(label)

        combo = ComboBox()
        combo.ItemsSource = opciones
        combo.SelectedIndex = 0
        self.panel.Children.Add(combo)
        return combo

    def seleccionar_carpeta(self, sender, args):
        dialog = Forms.FolderBrowserDialog()
        if dialog.ShowDialog() == Forms.DialogResult.OK:
            self.folder_text.Text = dialog.SelectedPath

    def confirmar(self, sender, args):
        opcion1 = self.combo1.SelectedItem
        opcion2 = self.combo2.SelectedItem
        opcion3 = self.combo3.SelectedItem
        ruta = self.folder_text.Text
        self.confirmado = True
        self.Close()

# ---------- Ejecutar formulario ----------
formulario = CustomForm()
formulario.ShowDialog()
if formulario.confirmado == False:
    raise SystemExit

opcion1 = formulario.combo1.SelectedItem  # Eje Horizontal seleccionado
opcion2 = formulario.combo2.SelectedItem  # Eje Vertical seleccionado
opcion3 = formulario.combo3.SelectedItem  # Piso seleccionado
ruta = formulario.folder_text.Text  # Ruta de la carpeta seleccionada