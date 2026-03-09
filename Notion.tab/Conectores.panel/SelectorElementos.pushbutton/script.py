# -*- coding: utf-8 -*-
"""Formulario WPF para seleccionar elementos manualmente en Revit y generar reporte."""

__title__ = "Selector\nElementos"
__author__ = "pyRevit"
__doc__ = "Selecciona elementos en el modelo y genera un reporte con sus propiedades."

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("WindowsBase")
clr.AddReference("System.Windows.Forms")

from Autodesk.Revit.DB import Element, ElementId, Level
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from System.Windows import Window, Application, Thickness
from System.Windows.Controls import (
    DataGrid, DataGridTextColumn, DataGridSelectionMode,
    ScrollBarVisibility
)
from System.Windows.Markup import XamlReader
from System.Collections.ObjectModel import ObservableCollection
from System.IO import StringWriter
import System

# ── pyRevit helpers ────────────────────────────────────────────────────────────
try:
    from pyrevit import script as pyscript
    output = pyscript.get_output()
except Exception:
    output = None

doc   = __revit__.ActiveUIDocument.Document    # noqa: F821
uidoc = __revit__.ActiveUIDocument             # noqa: F821

# ── XAML definition ────────────────────────────────────────────────────────────
XAML = """
<Window
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Title="Selector de Elementos — Revit"
    Height="560" Width="800"
    WindowStartupLocation="CenterScreen"
    Background="#1E1E2E"
    FontFamily="Segoe UI"
    ResizeMode="CanResize">

    <Window.Resources>
        <!-- Botón primario -->
        <Style x:Key="BtnPrimary" TargetType="Button">
            <Setter Property="Background"     Value="#89B4FA"/>
            <Setter Property="Foreground"     Value="#1E1E2E"/>
            <Setter Property="FontWeight"     Value="SemiBold"/>
            <Setter Property="FontSize"       Value="13"/>
            <Setter Property="Padding"        Value="18,8"/>
            <Setter Property="BorderThickness" Value="0"/>
            <Setter Property="Cursor"         Value="Hand"/>
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="Button">
                        <Border Background="{TemplateBinding Background}"
                                CornerRadius="6"
                                Padding="{TemplateBinding Padding}">
                            <ContentPresenter HorizontalAlignment="Center"
                                              VerticalAlignment="Center"/>
                        </Border>
                        <ControlTemplate.Triggers>
                            <Trigger Property="IsMouseOver" Value="True">
                                <Setter Property="Background" Value="#B4BEFE"/>
                            </Trigger>
                            <Trigger Property="IsPressed" Value="True">
                                <Setter Property="Background" Value="#74C7EC"/>
                            </Trigger>
                        </ControlTemplate.Triggers>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
        </Style>
        <!-- Botón secundario -->
        <Style x:Key="BtnSecondary" TargetType="Button" BasedOn="{StaticResource BtnPrimary}">
            <Setter Property="Background" Value="#313244"/>
            <Setter Property="Foreground" Value="#CDD6F4"/>
            <Style.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="#45475A"/>
                </Trigger>
            </Style.Triggers>
        </Style>
        <!-- Botón peligro -->
        <Style x:Key="BtnDanger" TargetType="Button" BasedOn="{StaticResource BtnPrimary}">
            <Setter Property="Background" Value="#F38BA8"/>
            <Setter Property="Foreground" Value="#1E1E2E"/>
            <Style.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="#FAB387"/>
                </Trigger>
            </Style.Triggers>
        </Style>
        <!-- DataGrid -->
        <Style TargetType="DataGrid">
            <Setter Property="Background"            Value="#181825"/>
            <Setter Property="Foreground"            Value="#CDD6F4"/>
            <Setter Property="BorderBrush"           Value="#313244"/>
            <Setter Property="BorderThickness"       Value="1"/>
            <Setter Property="GridLinesVisibility"   Value="Horizontal"/>
            <Setter Property="HorizontalGridLinesBrush" Value="#313244"/>
            <Setter Property="RowBackground"         Value="#181825"/>
            <Setter Property="AlternatingRowBackground" Value="#1E1E2E"/>
            <Setter Property="ColumnHeaderHeight"    Value="34"/>
            <Setter Property="RowHeight"             Value="28"/>
            <Setter Property="FontSize"              Value="12"/>
        </Style>
        <Style TargetType="DataGridColumnHeader">
            <Setter Property="Background"  Value="#313244"/>
            <Setter Property="Foreground"  Value="#89B4FA"/>
            <Setter Property="FontWeight"  Value="SemiBold"/>
            <Setter Property="Padding"     Value="8,0"/>
            <Setter Property="BorderBrush" Value="#45475A"/>
            <Setter Property="BorderThickness" Value="0,0,1,0"/>
        </Style>
        <Style TargetType="DataGridCell">
            <Setter Property="BorderThickness" Value="0"/>
            <Setter Property="Padding"         Value="8,0"/>
            <Style.Triggers>
                <Trigger Property="IsSelected" Value="True">
                    <Setter Property="Background" Value="#45475A"/>
                    <Setter Property="Foreground" Value="#CDD6F4"/>
                </Trigger>
            </Style.Triggers>
        </Style>
    </Window.Resources>

    <Grid Margin="16">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
            <RowDefinition Height="Auto"/>
        </Grid.RowDefinitions>

        <!-- Encabezado -->
        <StackPanel Grid.Row="0" Margin="0,0,0,12">
            <TextBlock Text="Selector de Elementos"
                       FontSize="22" FontWeight="Bold"
                       Foreground="#89B4FA"/>
            <TextBlock Text="Selecciona elementos en el modelo para generar un reporte detallado."
                       FontSize="12" Foreground="#6C7086" Margin="0,2,0,0"/>
        </StackPanel>

        <!-- Barra de acciones -->
        <WrapPanel Grid.Row="1" Orientation="Horizontal" Margin="0,0,0,10">
            <Button x:Name="BtnSeleccionar"
                    Content="⊕  Seleccionar Elementos"
                    Style="{StaticResource BtnPrimary}"
                    Margin="0,0,8,0"/>
            <Button x:Name="BtnLimpiar"
                    Content="✕  Limpiar"
                    Style="{StaticResource BtnDanger}"
                    Margin="0,0,8,0"/>
            <Button x:Name="BtnExportarCSV"
                    Content="↓  Exportar CSV"
                    Style="{StaticResource BtnSecondary}"/>
            <!-- Contador -->
            <Border Background="#313244" CornerRadius="6"
                    Padding="12,6" Margin="12,0,0,0"
                    VerticalAlignment="Center">
                <StackPanel Orientation="Horizontal">
                    <TextBlock Text="Elementos: " Foreground="#6C7086" FontSize="12"/>
                    <TextBlock x:Name="TxtContador" Text="0"
                               Foreground="#A6E3A1" FontWeight="Bold" FontSize="12"/>
                </StackPanel>
            </Border>
        </WrapPanel>

        <!-- DataGrid -->
        <DataGrid x:Name="GridElementos"
                  Grid.Row="2"
                  AutoGenerateColumns="False"
                  IsReadOnly="True"
                  SelectionMode="Extended"
                  HorizontalScrollBarVisibility="Auto"
                  VerticalScrollBarVisibility="Auto"
                  CanUserResizeColumns="True"
                  CanUserSortColumns="True">
            <DataGrid.Columns>
                <DataGridTextColumn Header="ID"         Binding="{Binding ElementId}"  Width="80"/>
                <DataGridTextColumn Header="Categoría"  Binding="{Binding Categoria}"  Width="150"/>
                <DataGridTextColumn Header="Familia"    Binding="{Binding Familia}"    Width="180"/>
                <DataGridTextColumn Header="Tipo"       Binding="{Binding Tipo}"       Width="180"/>
                <DataGridTextColumn Header="Nivel"      Binding="{Binding Nivel}"      Width="120"/>
                <DataGridTextColumn Header="Nombre"     Binding="{Binding Nombre}"     Width="*"/>
            </DataGrid.Columns>
        </DataGrid>

        <!-- Barra de estado -->
        <Border Grid.Row="3" Background="#313244" CornerRadius="6"
                Padding="12,6" Margin="0,10,0,0">
            <TextBlock x:Name="TxtEstado"
                       Text="Listo. Haz clic en 'Seleccionar Elementos' para comenzar."
                       Foreground="#6C7086" FontSize="11"/>
        </Border>
    </Grid>
</Window>
"""

# ── Data model ─────────────────────────────────────────────────────────────────
class ElementoInfo(object):
    """Contenedor de datos de un elemento para el DataGrid."""

    def __init__(self, element_id, categoria, familia, tipo, nivel, nombre):
        self.ElementId = element_id
        self.Categoria = categoria
        self.Familia   = familia
        self.Tipo      = tipo
        self.Nivel     = nivel
        self.Nombre    = nombre


def _get_level_name(element):
    """Devuelve el nombre del nivel asociado al elemento, o '—' si no aplica."""
    try:
        level_id = element.LevelId
        if level_id and level_id != ElementId.InvalidElementId:
            level = doc.GetElement(level_id)
            if level:
                return level.Name
    except Exception:
        pass
    try:
        param = element.get_Parameter(
            __import__("Autodesk.Revit.DB", fromlist=["BuiltInParameter"])
            .BuiltInParameter.LEVEL_PARAM
        )
        if param and param.HasValue:
            return param.AsValueString() or "—"
    except Exception:
        pass
    return "—"


def _get_family_and_type(element):
    """Devuelve (familia, tipo) del elemento."""
    try:
        element_type = doc.GetElement(element.GetTypeId())
        if element_type:
            familia = getattr(element_type, "FamilyName", None) or "—"
            tipo    = element_type.Name or "—"
            return familia, tipo
    except Exception:
        pass
    return "—", "—"


def build_elemento_info(element):
    """Construye un ElementoInfo a partir de un Element de Revit."""
    try:
        categoria = element.Category.Name if element.Category else "—"
    except Exception:
        categoria = "—"

    familia, tipo = _get_family_and_type(element)
    nivel         = _get_level_name(element)

    try:
        nombre = element.Name or "—"
    except Exception:
        nombre = "—"

    return ElementoInfo(
        element_id=str(element.Id.IntegerValue),
        categoria=categoria,
        familia=familia,
        tipo=tipo,
        nivel=nivel,
        nombre=nombre,
    )


# ── Formulario principal ────────────────────────────────────────────────────────
class SelectorWindow(Window):
    """Ventana principal del selector de elementos."""

    def __init__(self):
        # Cargar XAML
        window = XamlReader.Parse(XAML)
        self.Content     = window.Content
        self.Title       = window.Title
        self.Width       = window.Width
        self.Height      = window.Height
        self.Background  = window.Background
        self.FontFamily  = window.FontFamily
        self.WindowStartupLocation = window.WindowStartupLocation
        self.ResizeMode  = window.ResizeMode

        # Referencias a controles
        self._grid      = window.FindName("GridElementos")
        self._contador  = window.FindName("TxtContador")
        self._estado    = window.FindName("TxtEstado")
        self._btn_sel   = window.FindName("BtnSeleccionar")
        self._btn_lim   = window.FindName("BtnLimpiar")
        self._btn_csv   = window.FindName("BtnExportarCSV")

        # Colección observable para el DataGrid
        self._items = ObservableCollection[object]()
        self._grid.ItemsSource = self._items

        # Eventos
        self._btn_sel.Click += self._on_seleccionar
        self._btn_lim.Click += self._on_limpiar
        self._btn_csv.Click += self._on_exportar_csv

    # ── Acciones ───────────────────────────────────────────────────────────────
    def _on_seleccionar(self, sender, args):
        """Oculta el formulario y lanza la selección en Revit."""
        self.Hide()
        try:
            refs = uidoc.Selection.PickObjects(
                ObjectType.Element,
                "Selecciona los elementos y presiona ENTER para confirmar"
            )
            if refs:
                nuevos = 0
                ids_existentes = {item.ElementId for item in self._items}
                for ref in refs:
                    element = doc.GetElement(ref.ElementId)
                    if element:
                        info = build_elemento_info(element)
                        if info.ElementId not in ids_existentes:
                            self._items.Add(info)
                            ids_existentes.add(info.ElementId)
                            nuevos += 1
                self._actualizar_contador()
                self._estado.Text = (
                    u"Se agregaron {} elemento(s) nuevo(s). Total: {}.".format(
                        nuevos, len(self._items)
                    )
                )
            else:
                self._estado.Text = u"Selección cancelada o vacía."
        except Exception as ex:
            self._estado.Text = u"Selección cancelada. ({})".format(str(ex))
        finally:
            self.Show()

    def _on_limpiar(self, sender, args):
        """Limpia la lista de elementos."""
        self._items.Clear()
        self._actualizar_contador()
        self._estado.Text = u"Lista limpiada."

    def _on_exportar_csv(self, sender, args):
        """Exporta el reporte a un archivo CSV."""
        if not self._items:
            self._estado.Text = u"No hay elementos para exportar."
            return

        from System.Windows.Forms import SaveFileDialog, DialogResult
        dlg = SaveFileDialog()
        dlg.Title  = "Guardar reporte CSV"
        dlg.Filter = "Archivos CSV (*.csv)|*.csv|Todos los archivos (*.*)|*.*"
        dlg.FileName = "reporte_elementos.csv"

        if dlg.ShowDialog() == DialogResult.OK:
            try:
                lines = [u"ID,Categoría,Familia,Tipo,Nivel,Nombre"]
                for item in self._items:
                    lines.append(u'{},"{}","{}","{}","{}","{}"'.format(
                        item.ElementId,
                        item.Categoria,
                        item.Familia,
                        item.Tipo,
                        item.Nivel,
                        item.Nombre,
                    ))
                import System.IO as sio
                sio.File.WriteAllLines(dlg.FileName, lines, System.Text.Encoding.UTF8)
                self._estado.Text = u"Exportado correctamente: {}".format(dlg.FileName)
            except Exception as ex:
                self._estado.Text = u"Error al exportar: {}".format(str(ex))

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _actualizar_contador(self):
        self._contador.Text = str(len(self._items))


# ── Punto de entrada ───────────────────────────────────────────────────────────
try:
    win = SelectorWindow()
    win.ShowDialog()
except Exception as ex:
    from pyrevit import forms as pf
    pf.alert(
        u"Error al abrir el formulario:\n\n{}".format(str(ex)),
        title="Error"
    )
