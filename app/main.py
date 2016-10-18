
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
import qcards
import base64

app = Flask(__name__)
app.debug = True
app.config["JSON_AS_ASCII"] = False

folderFonts = os.path.dirname(__file__) + os.sep + 'fonts'
pdfmetrics.registerFont(TTFont('DejaVuSansMono', os.path.join(folderFonts,'DejaVuSansMono.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(folderFonts,'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSansBold', os.path.join(folderFonts,'DejaVuSansBold.ttf')))


TEST_TEXT = "Příliš žluťoučký kůň úpěl ďábelské ódy"
QCARD_BACK_TEXT = "Legitimace je nepřenosná. Za její zneužití zodpovídá její majitel. Vystavení náhradní legitimace za poplatek 100 Kč."
QCARD_BACK_IMAGE = os.path.dirname(__file__) + os.sep + 'images' + os.sep + "starlet_logo_color.png"
QRG_VERSION = "0.1"
QRG_HELLO = "QR Generator"


@app.route("/")
def hello():
   r = dict()
   r["version"] = QRG_VERSION
   r["info"] = QRG_HELLO
   return jsonify(**r)

@app.route("/cards_back", methods=["GET","POST"])
def cards_back():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.debug(data)
        app.logger.debug("cards back gen start")
        pdf_out = qcards.make_qcards_back(data.text,QCARD_BACK_IMAGE)
        app.logger.debug("cards back gen end")

        r = dict()
        r["rc"] = True
        r["xxx"] = TEST_TEXT
        r["data"] = base64.b64encode(pdf_out)
        return jsonify(**r)


    pdf_out = qcards.make_qcards_back(QCARD_BACK_TEXT,QCARD_BACK_IMAGE)
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename=karty_zadek.pdf"
    response.mimetype = 'application/pdf'
    return response



@app.route("/cards", methods=["GET","POST"])
def cards():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.debug(data)
        app.logger.debug("cards gen start")
        pdf_out = qcards.make_qcards(data)
        app.logger.debug("cards gen end")

        r = dict()
        r["rc"] = True
        r["xxx"] = TEST_TEXT
        r["data"] = base64.b64encode(pdf_out)
#        app.logger.debug(r)
        return jsonify(**r)

    c={"ref_gid":"12345","name":"Pepa", "surname":"Vopička", "info_line_1":"info line 1", "info_line_2":"info line 2", "course_code":"X12", "season_name": "2015/16"}
    pdf_out = qcards.make_qcards([c,c,c,c,c,c,c,c,c,c])
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename=karty.pdf"
    response.mimetype = 'application/pdf'
    return response
  
@app.route("/cmd_cards", methods=["GET","POST"])
def cmd_cards():
    if request.method == 'POST':
        data = request.get_json()
        app.logger.debug(data)
        app.logger.debug("cards gen start")
        pdf_out = qcards.make_cmd_qcards(data)
        app.logger.debug("cards gen end")

        r = dict()
        r["rc"] = True
        r["data"] = base64.b64encode(pdf_out)
        return jsonify(**r)

    c={"cmd_id":"12345","name":"command 12345", "season": "spring", "desc":"this command makes world happy", "cmd_qrcode": "blablablablablllllaaaa"}
    pdf_out = qcards.make_cmd_qcards([c,c,c,c,c,c,c,c,c,c])
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename=karty.pdf"
    response.mimetype = 'application/pdf'
    return response


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
    r["data"] = "hello"
    app.logger.debug(r)
    return jsonify(**r)




if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)

