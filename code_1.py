
import qrcode
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.colors import Color, green, red  # Traemos algunos colores
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO


class FacturaCostasur:
    def __init__(self, nombre_cliente, direccion_cliente, consumo_kwh, tarifa_kwh,num_factura):
        self.nombre_cliente = nombre_cliente
        self.direccion_cliente = direccion_cliente
        self.consumo_kwh = consumo_kwh
        self.num_factura = num_factura
        self.tarifa_kwh = tarifa_kwh
        self.fecha_emision = datetime.now().strftime("%d-%m-%Y ")


    def calcular_total(self):
        return self.consumo_kwh * self.tarifa_kwh

    def generar_factura_pdf(self):
        nombre_archivo = "factura_costasur.pdf"
        #elements = []
        pdf = canvas.Canvas(nombre_archivo, pagesize=letter)

        #varaibles
        w,h = letter

        # Estilos
        styles = getSampleStyleSheet()
        header_style = styles['Heading1']
        subheader_style = styles['Heading2']
        normal_style = styles['Normal']

        #Agrgando el logo de costaSur
        pdf.setPageRotation(0)
        pdf.drawImage("07-RNCN.JPG",20,700)
        

        # Encabezado lateral derecho
        pdf.setFillColorRGB(0, 0.55, 0)
        pdf.roundRect(380,700,200,67,10,stroke=0,fill=1)
        pdf.setFillColorRGB(255,255,255)
        pdf.setFontSize(10)
        pdf.drawString(390,750,f"Factura/Invoice: #{self.num_factura}")
        pdf.drawString(390,730,f"Fecha de emisión: {self.fecha_emision}")
        pdf.drawString(390,710,"Dirección / Property: PM0017")

        # Sección divisora encabezado
        pdf.setFillColorRGB(0,0.55,1.55)
        pdf.roundRect(20,668,560,24,0, stroke=0,fill=1)
        pdf.setFillColorRGB(255,255,255)
        pdf.setFontSize(15)
        pdf.drawCentredString(184,675,"Factura electricidad / Electricity Bill")
        pdf.setFont("Helvetica",14)
        pdf.drawCentredString(445,675, f"Cuenta / Account {self.num_factura}")

        # Detalle del cliente"
        pdf.setFont("Helvetica-Bold",9)
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(46,642,"Cliente / Client: ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(145,642,f"{self.nombre_cliente}")
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(46,629,"Propiedad / Property: ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(145,629,f"{self.num_factura}")
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(46,616,"Direccion / Address:")
        pdf.setFont("Helvetica",9)
        pdf.drawString(145,616,f"{self.direccion_cliente}")

        #Detalle extra
        pdf.setFont("Helvetica-Bold",9)
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(320,642,"Municipio/Municipality: ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(425,642,"La Romana")
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(320,629,"Provincia/Province: ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(425,629,"La Romana")
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(320,616,"Seccion/Section: ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(425,616,"Zona urbana")
       
        #pdf.drawString(390,603,"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        #Segunda seccion detalle de la factura
        pdf.setStrokeColorRGB(0.9,0.9,0.9)
        pdf.roundRect(28, h - 305, 540, 115, 5)

        # seccion Informacion del cubo azul
        pdf.setFillColorRGB(0,0.55,1.55)
        pdf.roundRect(28,580,545,26,0, stroke=0,fill=1)
        pdf.setFont("Helvetica-Bold",9.5)
        pdf.setFillColorRGB(255,255,255)   
        pdf.drawCentredString(300,595,"Tipo Lectura /          No. Contador /           Lectura Anterior /           Lectura Actual /             Factor /            Consumo/")
        pdf.drawCentredString(300,585,"Reading Type             No. Counter             Previous Reading             Current Reading              Factor             Consumption")
        #este es el cubito verde
        pdf.setFillColorRGB(0, 0.55, 0)
        pdf.roundRect(505, h - 305, 68, 93, 0,stroke=0, fill=1)
        pdf.setFillColorRGB(0,0,0)

        #aqui debe ir una condicion para que esto se muestre en caso de una factura trifasica
        #listas sobre los valores, example
        frutas =["manzana","pera","uva","melon","pepino","cosa","fresa"]
        type_lec = ["Activa B.T","Potencia B.T.","Reactiva B.T.","Inyectada Pot","Inyectada React","Inyectada Act","Medicion neta"]
        contadors =["14106390","14106390","14106390","14106390","14106390","14106390","14106390"]
        lect_anterior=['51498','525623','7226','78521','45','4526','852']
        lect_actual=[45454,4563,114,633,999,858,452]
        multiplo=[10,55,88,4,66,10,99]
        consumido=['78kw','888kw','777kw','200kw','500kw','210kw','455kw']
              
        y = 570
        #primer buclesito
        for f in type_lec:
            pdf.setFont("Helvetica",9)
            pdf.drawString(46, y, f"{f}")
            y -= 12
        
        #segundo buclesito
        y = 570
        for f in contadors:
            pdf.setFont("Helvetica",9)
            pdf.drawString(130, y, f"{f}")
            y -= 12
        #tercer buclesito
        y = 570
        for f in lect_anterior:
            pdf.setFont("Helvetica",9)
            pdf.drawString(230, y, f"{f}")
            y -= 12
        #cuarto buclesito
        y = 570
        for f in lect_actual:
            pdf.setFont("Helvetica",9)
            pdf.drawString(340, y, f"{f}")
            y -= 12
        #quinto buclesito
        y = 570
        for f in multiplo:
            pdf.setFont("Helvetica",9)
            pdf.drawString(440, y, f"{f}")
            y -= 12

        #sexto buclesito este debe ser pintado
        y = 570
        for f in consumido:
            pdf.setFillColorRGB(255,255,255) 
            pdf.setFont("Helvetica-Bold",9)
            pdf.drawString(520, y, f"{f}")
            y -= 12


        pdf.setFillColorRGB(0, 0.55, 0)
        pdf.roundRect(30,450,250,30,3, stroke=0,fill=1)
        pdf.setFont("Helvetica-Bold",11)
        pdf.setFillColorRGB(255,255,255)
        pdf.drawString(46,460,"No. Contador: 94387729")

         #DEFINO ESTO PARA MANEJAR BIEN EL WIDTH Y HEAD
        
        pdf.setStrokeColorRGB(0.9,0.9,0.9)  # Establecer el color del borde (en este caso, negro)
        pdf.setLineWidth(2)
        #cubito uno
        pdf.roundRect(30, h - 455, 250, 100, 5)
        pdf.setFillColorRGB(0,0,0)
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(46,425,"Circuito / Circuit: ROBV02 ")
        pdf.drawString(46,410,"Tarifa / Fee: BTS1")
        pdf.drawString(46,390,"Voltaje / Voltage: Trifasica 208/120v")
        pdf.drawString(46,370,"Potencia / Power: 5.90kw")
        pdf.drawString(46,350,"Período de Facturacion  / Billing Period: 30 days")
        
        #cubito dos
        pdf.setFillColorRGB(0, 0.55, 0)
        pdf.roundRect(320, h - 340, 250, 30, 5,stroke=0, fill=1)

        pdf.roundRect(320, h - 410, 250, 70, 2)
        pdf.setFont("Helvetica-Bold",10)
        pdf.setFillColorRGB(255,255,255)
        pdf.drawString(340,465,"Calculo de la Factura / Invoice calculation")
        pdf.setFont("Helvetica-Bold",9)
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(330,430,"Consumo / Consumption :      ")
        pdf.setFont("Helvetica",9)
        pdf.drawString(340,420,"1,000kwh * RD$ 16.0              RD$              16,000")
        pdf.setFillColorRGB(0, 0.55, 0)
        pdf.roundRect(320, h - 448, 250, 30, 5,stroke=0, fill=1)
        pdf.setFont("Helvetica-Bold",9)
        pdf.setFillColorRGB(255,255,255)
        pdf.drawString(330,350,"Pagar antes de / Please pay before:")
        pdf.drawString(490,350,"30-nov-23")


        #cubito tres
        pdf.roundRect(30,h- 665, 540, 205, 4, stroke=1, fill=0)

        potencias=[0,5,89,6,9,5,7,5,0,89,69,77]
        consumo_mensual = [150, 180, 200, 160, 120, 90, 100, 130, 170, 190, 200, 180]
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

        #creando grafico simple
        #plt.bar(meses, consumo_mensual,color='gray')
        plt.bar(meses, consumo_mensual, color='white', edgecolor='black', hatch='', linewidth=1.2)

        plt.savefig('grafico.png')
        pdf.setPageRotation(0)
        pdf.drawImage("grafico.png",250,128,width=300,height=200,preserveAspectRatio=False)
        #letras
        pdf.setFont("Helvetica-Bold",10)
        pdf.setFillColorRGB(0,0,0)
        pdf.drawString(44,300,"Historico de Consumo / Consumption History")
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(44,270,"Mes")
        pdf.drawString(44,260,"Month")
        #lista de valores
        y = 245
        for mes in meses:
            pdf.setFont("Helvetica",9)
            pdf.drawString(46, y, f"{mes}")
            y -= 10

        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(100,270,"Potencia")
        pdf.drawString(100,260,"potency")
        #lista de valores
        y = 245
        for potencia in potencias:
            pdf.setFont("Helvetica",9)
            pdf.drawString(100, y, f"{potencia}")
            y -= 10


        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(155,270,"Consum")
        #lista de valores
        y = 245
        for consumo in consumo_mensual:
            pdf.setFont("Helvetica",9)
            pdf.drawString(155, y, f"{consumo}")
            y -= 10
            
        pdf.setFont("Helvetica-Bold",9)
        pdf.drawString(240,260,"KWh")


        


        #generando un codigo QR
        # qr = qrcode.make("https://koryroot.github.io/")
        # fichero = open("Costasur Dominicana.png","wb")
        # qr.save(fichero)
        # fichero.close

        imagen_qr = ImageReader('Costasur Dominicana.png')
        pdf.drawImage(imagen_qr,46,40,width=80,height=80,preserveAspectRatio=False)

        #agregando un textico de reyeno
        # pdf.setFont("Helvetica-Bold",9)
        # pdf.setFillColorRGB(0,0,0)
        # pdf.drawString(390,100,"Texto / texto:  texto")
        # pdf.drawString(390,90,"texto / texto: texto")
        # pdf.drawString(390,80,f"texto / XXXXX: {self.consumo_kwh}")
        # pdf.drawString(390,70,"texto / XXXXX:  XXXXXXX")

        # Guardar el archivo PDF
        pdf.save()

        print(f"Factura generada: {nombre_archivo}")

# Ejemplo de uso
cliente = "Juan Pérez"
direccion = "Calle 123, Ciudad"
consumo = 150
tarifa = 0.15
num_factura = "563453"

factura = FacturaCostasur(cliente, direccion, consumo, tarifa,num_factura)
factura.generar_factura_pdf()