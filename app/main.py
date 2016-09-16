
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import make_response, request

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
import base64
import logging
from io import BytesIO

import qrcode as qrc

app = Flask(__name__)
app.debug = True

folderFonts = os.path.dirname(__file__) + os.sep + 'fonts'
pdfmetrics.registerFont(TTFont('DejaVuSansMono', os.path.join(folderFonts,'DejaVuSansMono.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(folderFonts,'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSansBold', os.path.join(folderFonts,'DejaVuSansBold.ttf')))


TEST_TEXT = "Příliš žluťoučký kůň úpěl ďábelské ódy"

@app.route("/")
def hello():
   return "Hello World from Flask !"

@app.route("/pdf")
def pdf():
    import cStringIO
    output = cStringIO.StringIO()

    p = canvas.Canvas(output)
    p.setFont('DejaVuSansBold', 16)
    p.drawString(100, 100,TEST_TEXT )
    p.showPage()
    p.save()
    
    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
    response.mimetype = 'application/pdf'
    return response


correction_levels = {
    'L': qrc.constants.ERROR_CORRECT_L,
    'M': qrc.constants.ERROR_CORRECT_M,
    'Q': qrc.constants.ERROR_CORRECT_Q,
    'H': qrc.constants.ERROR_CORRECT_H
}



@app.route("/qr")
def qccode():
    qr = qrc.QRCode(
        version=None,
        error_correction=correction_levels['M'],
        box_size=10,
        border=4
    )
    qr.add_data(250*"a")
    qr.make(fit=True)

    # creates qrcode base64
    out = BytesIO()
    qr_img = qr.make_image()
    qr_img.save(out, 'PNG')

    img_out = out.getvalue()	
    response = make_response(img_out)
    response.mimetype = 'image/png'
    return response


@app.route("/test", methods=["POST"])
def test():
    data = request.get_json()
    app.logger.debug(data)
    r = dict()
    r["rc"] = True
    app.logger.debug(r)
    return jsonify(**r)




if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)

