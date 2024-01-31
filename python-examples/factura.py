import qrcode
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO


def generar_factura(nombre_cliente, direccion_cliente, productos, total):
    # Crear un archivo PDF
    nombre_archivo = "factura_basica.pdf"
    pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

    #DEFINO ESTO PARA MANEJAR BIEN EL WIDTH Y HEAD
    w,h = letter

    # Configurar el encabezado
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, 750, "Factura")

    # Agregar información del cliente
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, 730, f"Cliente: {nombre_cliente}")
    pdf.drawString(30, 630, "Tambien puedo escribir asi")
    pdf.drawString(300 , 630 , "Probando a la izuierda")
    pdf.drawString(50, 715, f"Dirección: {direccion_cliente}")

    
    # practicando los rectangulos
    pdf.roundRect(50, h - 400, 200, 200, 10)

    # Agregar la lista de productos
    pdf.drawString(50, 680, "Productos:")
    y = 660
    for producto in productos:
        pdf.drawString(70, y, f"{producto['nombre']}: ${producto['precio']}")
        y -= 15

    # Agregar el total
    pdf.drawString(50, y - 20, f"Total: ${total}")

    # Agregar la fecha
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.drawString(400, 50, f"Fecha: {fecha_actual}")

    

    #agregando un codigo QR
    qr = qrcode.make("https://koryroot.github.io/")
    fichero = open("qr.png","wb")
    qr.save(fichero)
    fichero.close

    imagen_qr = ImageReader('qr.png')
    pdf.drawImage(imagen_qr,0*mm,0*mm, width=50*mm,preserveAspectRatio=True)

    #Agregando grafico
    consumo_mensual = [150, 180, 200, 160, 120, 90, 100, 130, 170, 190, 200, 180]
    meses = ["enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    #creando grafico simple
    plt.bar(meses, consumo_mensual)
    plt.savefig('grafico.png')
    #
    grafico = ImageReader('grafico.png')
    pdf.drawImage(grafico,8*mm,8*mm, width=80*mm,preserveAspectRatio=True)
    pdf.save()

    print(f"Factura generada: {nombre_archivo}")

# Ejemplo de uso
cliente = "Cliente de ejemplo"
direccion = "Dirección de ejemplo"
productos = [{"nombre": "Producto1", "precio": 20}, {"nombre": "Producto2", "precio": 30}]
total_factura = sum(producto["precio"] for producto in productos)

generar_factura(cliente, direccion, productos, total_factura)
