# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from dynhost import settings

from invoice import format_currency, draw_address, draw_client_address, draw_body

def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.9, 0.9)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(17.5 * cm, -0.85 * cm, 'ALBARÁN')
    canvas.drawInlineImage(settings.COMPANY_LOGO, -5 * cm, -1.15 * cm,
        preserveAspectRatio=True, height=1*cm)
    canvas.setLineWidth(4)
    canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)

def draw_footer(canvas, data):
    """ Draws the invoice footer """
    textobject = canvas.beginText(1.5 * cm, -23 * cm)
    textobject.setFont('Helvetica', 9)
    textobject.textOut(u'Realice la transferencia bancaria en la cuenta de ')
    textobject.setFont('Helvetica-Bold', 9)
    textobject.textOut(settings.BANK)
    textobject.setFont('Helvetica', 9)
    textobject.textLine(' siguiente:')
    textobject.setFont('Helvetica-Bold', 10)
    textobject.textLine()
    textobject.textLine(settings.CCC)
    textobject.textLine()
    textobject.setFont('Helvetica-Bold', 9)
    textobject.textLine(u'Altenwald Solutions, S.L.')
    textobject.textLine(u'Calle La Fragua, 7')
    textobject.textLine(u'14100 La Carlota, Córdoba, España')
    textobject.textLine()
    textobject.setFont('Helvetica', 9)
    textobject.textOut(u'No olvide detallar en el concepto: ')
    textobject.setFont('Helvetica-Bold', 10)
    textobject.textLine(data['contract'].transfer_concept())
    textobject.textLine()
    textobject.setFont('Helvetica', 8)
    textobject.textLines([
        u'De acuerdo con la Ley Orgánica de Protección de Datos de carácter personal, le '
        u'informamos que sus datos están incluidos en un archivo de',
        u'titularidad de %s, con el objetivo de mantener nuestras '
        u'relaciones comerciales. Si desea ejercitar sus derechos de ' % settings.COMPANY_NAME,
        u'acceso, rectificación, cancelación y oposición, diríjase por escrito a %s, '
        u'%s, %s %s, ' % (
            settings.COMPANY_NAME, settings.COMPANY_ADDR, settings.COMPANY_ZIP,
            settings.COMPANY_CITY
        ),
        u'%s, %s o por correo electrónico a %s.' % (
            settings.COMPANY_STATE, settings.COMPANY_COUNTRY,
            settings.COMPANY_EMAIL
        )
    ])
    canvas.drawText(textobject)

def draw_info(canvas, data):
    textobject = canvas.beginText(1.5 * cm, -6.35 * cm)
    xorigin = textobject.getX()
    textobject.textOut(u'Fecha Albarán: ')
    xpos = textobject.getX() + 0.5 * cm
    textobject.setXPos(xpos - xorigin)
    textobject.setFont('Helvetica-Bold', 10)
    textobject.textLine('%s' % data['contract'].begins.strftime('%d %b %Y'))
    textobject.setFont('Helvetica', 10)
    canvas.drawText(textobject)

def draw_pdf(buffer, data):
    """ Draws the invoice """
    canvas = Canvas(buffer, pagesize=A4)
    canvas.translate(0, 29.7 * cm)
    canvas.setFont('Helvetica', 10)

    canvas.saveState()
    draw_header(canvas)
    canvas.restoreState()

    canvas.saveState()
    draw_footer(canvas, data)
    canvas.restoreState()

    canvas.saveState()
    draw_address(canvas)
    canvas.restoreState()

    draw_client_address(canvas, data)
    draw_info(canvas, data)
    draw_body(canvas, data)

    canvas.showPage()
    canvas.save()
