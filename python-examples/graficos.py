from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import matplotlib.pyplot as plt
from io import BytesIO

fecha_emision = 'hola'

# Crear un lienzo PDF
pdf_filename = "factura.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Lista para almacenar elementos del PDF
elements = []

# Estilos
styles = getSampleStyleSheet()
header_style = styles['Heading1']
subheader_style = styles['Heading2']
normal_style = styles['Normal']


# Ruta de la imagen
logo_path = "logo.png"
# Estilo del encabezado
header_style = getSampleStyleSheet()['Heading2']
# Crear un párrafo con texto
texto = "LOGO"
texto_paragraph = Paragraph(texto, header_style)
# Crear una instancia de la imagen
logo = Image(logo_path, width=50, height=50)
# Agregar los elementos al arreglo 'elements'
elements.append(logo)
elements.append(texto_paragraph)

# Cuadro rectangular con fondo azul claro y texto "Resumen de factura"
resumen_style = ParagraphStyle(
    "resumen_style",
    parent=normal_style,
    spaceAfter=12,
    backColor=colors.lightblue,
)
resumen_text = Paragraph("Datos de Cliente", resumen_style)
elements.append(resumen_text)

# Cuadro de texto con información básica del cliente
cliente_info = [
    ["Nombre:", "Juan Pérez"],
    ["Dirección:", "Calle Principal 123"],
    ["Ciudad:", "Ciudad Ejemplo"],
    ["Datos:", " Ejemplo"],
    ["Teléfono:", "555-1234"],
    [f"Fecha de emisión: {fecha_emision}"]
]

info_table = Table(cliente_info, colWidths=[1.3 * inch, 3 * inch])
elements.append(info_table)

# Cuadro rectangular con fondo azul claro y texto "Resumen de factura"
resumen_style = ParagraphStyle(
    "resumen_style",
    parent=normal_style,
    spaceAfter=12,
    backColor=colors.lightblue,
)
resumen_text = Paragraph("Resumen de factura", resumen_style)
elements.append(resumen_text)

# Dos cuadros paralelos para potencia y kW usados / estructura de cobro
datos_facturacion = [
    ["Potencia", "60 kW"],
    ["kW Usados", "300 kWh"],
    ["Estructura de Cobro", "Ejemplo de estructura de cobro"],
]

datos_table = Table(datos_facturacion, colWidths=[1.5 * inch, 2 * inch])
elements.append(datos_table)

# Encabezado como subtítulo para "Información de consumo"
elements.append(Spacer(1, 12))
subheader_text = Paragraph("Información de consumo", subheader_style)
elements.append(subheader_text)

# Dividir en dos cuadros: valor a facturar y gráfico de consumo
valor_facturar = Paragraph("Valor a facturar: $150", normal_style)
elements.append(valor_facturar)

# Insertar un gráfico de ejemplo (aquí deberías insertar tu propio código para generar el gráfico)



# Gráfico de consumo (ejemplo)
# Aquí deberías incluir tu propia lógica para generar los datos del gráfico
consumo_mensual = [150, 180, 200, 160, 120, 90, 100, 130, 170, 190, 200, 180]

# Crear el gráfico
plt.plot(range(1, 13), consumo_mensual, marker='o')
plt.title('Consumo Mensual de Energía')
plt.xlabel('Mes')
plt.ylabel('Consumo (kWh)')

# Guardar el gráfico en un objeto BytesIO
buffer = BytesIO()
plt.savefig(buffer, format='png')
plt.close()

# Convertir la imagen en formato PNG a un objeto Image de ReportLab
consumo_chart = Image(buffer)
consumo_chart.drawHeight = 2 * inch
consumo_chart.drawWidth = 6 * inch

# Añadir el gráfico al documento
elements.append(consumo_chart)

# ...


# Finalmente, construir el documento PDF
doc.build(elements)
