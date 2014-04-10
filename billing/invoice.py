# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from dymmer import settings
import locale

def format_currency(amount, currency):
    if currency == '€':
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    elif currency == '$':
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    else:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    return locale.currency(amount)

def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.9, 0.9, 0.9)
    canvas.setFillColorRGB(0.2, 0.2, 0.2)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(17.5 * cm, -0.85 * cm, 'FACTURA')
    canvas.drawInlineImage(settings.COMPANY_LOGO, -5 * cm, -1.15 * cm,
        preserveAspectRatio=True, height=1*cm)
    canvas.setLineWidth(4)
    canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)

def draw_address(canvas):
    """ Draws the business address """
    business_details = (
        settings.COMPANY_ADDR,
        settings.COMPANY_CITY,
        settings.COMPANY_STATE,
        settings.COMPANY_ZIP,
        settings.COMPANY_COUNTRY,
        u'',
        u'',
        u'T: ' + settings.COMPANY_PHONE,
        settings.COMPANY_EMAIL,
        settings.COMPANY_WEB,
        u'CIF: ' + settings.COMPANY_ID
    )
    canvas.setFont('Helvetica-Bold', 10)
    textobject = canvas.beginText(13 * cm, -2.5 * cm)
    textobject.textLine(settings.COMPANY_NAME)
    textobject.setFont('Helvetica', 9)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)

def draw_footer(canvas, data):
    """ Draws the invoice footer """
    textobject = canvas.beginText(1.5 * cm, -27 * cm)
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

def draw_client_address(canvas, data):
    textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
    textobject.setFont('Helvetica-Bold', 12)
    if data['nic_data'].legalForm == 'individual':
        textobject.textLine(data['nic_data'].firstname + ' ' + data['nic_data'].name)
    elif data['nic_data'].legalForm == 'association':
        textobject.textLine(data['nic_data'].organization)
    else:
        textobject.textLine(data['nic_data'].legalName)
    textobject.setFont('Helvetica', 10)
    textobject.textLine(data['nic_data'].legalNumber)
    textobject.textLine(data['nic_data'].address)
    textobject.textLine(data['nic_data'].zipCode + ' ' + data['nic_data'].city + ' (' + data['nic_data'].area + ')')
    textobject.textLine(data['nic_data'].country_text())
    canvas.drawText(textobject)

def draw_info(canvas, data):
    textobject = canvas.beginText(1.5 * cm, -6.35 * cm)
    xorigin = textobject.getX()
    textobject.textOut(u'Num. Factura: ')
    textobject.setFont('Helvetica-Bold', 10)
    xpos = textobject.getX() + 0.5 * cm
    textobject.setXPos(xpos - xorigin)
    textobject.textLine(u'%05d' % 1) #data['contract'].invoice_id)
    textobject.setFont('Helvetica', 10)
    textobject.setXPos(xorigin - textobject.getX())
    textobject.textOut(u'Fecha Factura: ')
    textobject.setXPos(xpos - xorigin)
    textobject.setFont('Helvetica-Bold', 10)
    textobject.textLine('%s' % data['contract'].begins.strftime('%d %b %Y'))
    textobject.setFont('Helvetica', 10)
    canvas.drawText(textobject)

def draw_body(canvas, data):
    data_table = [[u'Descripcion', u'Cantidad', u'Precio', u'Total'], ]
    contract = data['contract']
    data_table.append([
        contract.type_text(),
        contract.quantity,
        format_currency(contract.price, data['cuenta'].currency),
        format_currency(contract.total(), data['cuenta'].currency)
    ])
    data_table.append([u'', u'', u'Total:', format_currency(contract.total(), data['cuenta'].currency_symbol())])
    table = Table(data_table, colWidths=[11 * cm, 2 * cm, 3 * cm, 3 * cm])
    table.setStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
        ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ])
    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
    table.drawOn(canvas, 1 * cm, -8 * cm - th)

    # Brief and VAT
    vat_num = int(data['cuenta'].nic_data.vat)
    data_vat = [
        [u'', u'Total Neto:', format_currency(contract.total(), data['cuenta'].currency)],
        [u'', u'Total IVA (%d%%):' % vat_num, format_currency(contract.total_vat(), data['cuenta'].currency)],
        [u'', u'Total Factura:', format_currency(contract.total_incl_vat(), data['cuenta'].currency)],
    ]
    vat = Table(data_vat, colWidths=[11 * cm, 5 * cm, 3 * cm])
    vat.setStyle([
        ('FONT', (0, 0), (-1, -2), 'Helvetica'),
        ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -2), 10),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 0), (-1, -1), (0.8, 0.8, 0.8)),
    ])
    tw, th, = vat.wrapOn(canvas, 5 * cm, 19 * cm)
    vat.drawOn(canvas, 1 * cm, -20 * cm - th)

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
