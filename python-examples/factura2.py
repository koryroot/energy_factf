from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.barcharts import VerticalBarChart

# Definir estilos
styles = {
    'Title': {'fontSize': 16, 'bold': True},
    'Subtitle': {'fontSize': 14, 'bold': True},
    'Normal': {'fontSize': 12},
}

# Obtener estilos de muestra
styles = getSampleStyleSheet()

# Datos para el gráfico de barras
datos = [
    ("Enero", 150),
    ("Febrero", 180),
    ("Marzo", 200),
    ("Abril", 160),
    ("Mayo", 120),
    ("Junio", 90),
    ("Julio", 100),
    ("Agosto", 130),
    ("Septiembre", 170),
    ("Octubre", 190),
    ("Noviembre", 200),
    ("Diciembre", 180),
]

# Crear el lienzo PDF
pdf_filename = "grafico_reportlab.pdf"
pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Crear el gráfico de barras
chart = VerticalBarChart()
chart.data = [x[1] for x in datos]
chart.categoryAxis.categoryNames = [x[0] for x in datos]
chart.bars.strokeColor = colors.black

# Crear un objeto Drawing para agregar el gráfico al PDF
drawing = Drawing(400, 200)
drawing.add(chart)

# Crear el contenido del PDF
contenido = []

# Agregar el gráfico al contenido
contenido.append(Paragraph("Gráfico de Barras", styles['Title']))
contenido.append(Spacer(1, 12))
contenido.append(drawing)
contenido.append(Spacer(1, 12))

# Construir la tabla con los datos
tabla_datos = Table(datos, colWidths=[100, 50])
tabla_datos.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))

# Agregar la tabla al contenido
contenido.append(tabla_datos)

# Construir el PDF
pdf.build(contenido)
