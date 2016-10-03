# -*- coding: utf-8 -*-

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A6,landscape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch,mm,cm
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,PageBreak, Image
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing 

from xml.sax.saxutils import escape

import os
import logging
import cStringIO


QCARD_IMAGE = os.path.dirname(__file__) + os.sep + 'images' + os.sep + "starlet_logo_inv.png"
starlet_logo = Image(QCARD_IMAGE)
starlet_logo.drawWidth = 2*cm
starlet_logo.drawHeight = 1*cm


def safe(s):
    if s is None:
        return ""
    return escape(s)
def nsafe(s):
    if s is None:
        return ""
    return escape(str(s))


def getStyleSheet():
    stylesheet = StyleSheet1()

    stylesheet.add(ParagraphStyle(name='Card',
                                  fontName='DejaVuSansBold',
                                  fontSize=9)
                   )

    stylesheet.add(ParagraphStyle(name='CardHeaderLeft', parent=stylesheet['Card'],
                                  textColor=colors.white,
                                  alignment=TA_CENTER,
                                  )
                   )

    stylesheet.add(ParagraphStyle(name='CardHeaderRight', parent=stylesheet['Card'],
                                  textColor=colors.white,
                                  alignment=TA_CENTER,
                                  fontSize = 7,
                                  leading = 9
                                  )
                   )

 
    stylesheet.add(ParagraphStyle(name='CardSeason', parent=stylesheet['Card'],
                                  textColor=colors.black,
                                  alignment=TA_CENTER,
                                  fontSize=8,
                                  )
                   )


    stylesheet.add(ParagraphStyle(name='CardFullname', parent=stylesheet['Card'],
                                  fontSize=8,
                                  textColor=colors.white,
                                  alignment=TA_CENTER,
                                  )
                   )

    stylesheet.add(ParagraphStyle(name='CardCode', parent=stylesheet['Card'],
                                  textColor=colors.black,
                                  alignment=TA_CENTER,
                                  leading=16,
                                  fontSize=18,
                                  )
                   )

    stylesheet.add(ParagraphStyle(name='CardInfoLines', parent=stylesheet['Card'],
                                  textColor=colors.black,
                                  alignment=TA_CENTER,
                                  fontSize=6
                                  )
                   )


    stylesheet.add(ParagraphStyle(name='CardBackText', parent=stylesheet['Card'],
                                  textColor=colors.black,
                                  alignment=TA_CENTER,
                                  fontSize=5,
                                  leading = 7
                                  )
                   )

    stylesheet.add(ParagraphStyle(name='CardGID', parent=stylesheet['Card'],
                                  textColor=colors.black,
                                  alignment=TA_RIGHT,
                                  fontSize=4
                                  )
                   )


    return stylesheet

def make_qcards_back(text,img_file): 
    output = cStringIO.StringIO()
    doc = SimpleDocTemplate(output, pagesize=A4 ,leftMargin=0.7*cm, rightMargin=1.3*cm, topMargin=0.8*cm, bottomMargin=1*cm, showBoundary=0)
    pad = 10
    elements = []
    cardcells = []

    for x in range(0,10):
        cell = make_qcard_back_cell(text,img_file)
        cardcells.append(cell)

    line=[]
    data=[]
    for t in cardcells:
        line.append(t) 
        if len(line)==2:
            data.append(line)
            line=[]

    if len(line)>0:
        line.extend((2-len(line))*" ")
        data.append(line)
   
    rows = len(data) 

 
    bigtable = Table(data,colWidths=[8.5*cm,8.5*cm], rowHeights= rows*[5.43*cm], style=[
#        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),pad),
        ('RIGHTPADDING',(0,0),(-1,-1),pad),
        ('TOPPADDING',(0,0),(-1,-1),pad),
        ('BOTTOMPADDING',(0,0),(-1,-1),pad),
    ]) 
    elements.append(bigtable)
    doc.build(elements)
    pdf_out = output.getvalue()
    output.close()
    return pdf_out




def make_qcards(qcards):
    output = cStringIO.StringIO()
    doc = SimpleDocTemplate(output, pagesize=A4 ,leftMargin=1*cm, rightMargin=1*cm, topMargin=0.8*cm, bottomMargin=1*cm, showBoundary=0)
    pad = 10
    elements = []
    cardcells = []

    for qcard in qcards:
        cell = make_qcard_cell(qcard)
        cardcells.append(cell)

    line=[]
    data=[]
    for t in cardcells:
        line.append(t) 
        if len(line)==2:
            data.append(line)
            line=[]

    if len(line)>0:
        line.extend((2-len(line))*" ")
        data.append(line)
   
    rows = len(data) 

    bigtable = Table(data,colWidths=[8.5*cm,8.5*cm], rowHeights= rows*[5.43*cm], style=[
        ('GRID',(0,0),(-1,-1),0.5,colors.gray),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),pad),
        ('RIGHTPADDING',(0,0),(-1,-1),pad),
        ('TOPPADDING',(0,0),(-1,-1),pad),
        ('BOTTOMPADDING',(0,0),(-1,-1),pad),
    ]) 
    elements.append(bigtable)
    doc.build(elements)
    pdf_out = output.getvalue()
    output.close()
    return pdf_out

def make_qcard_back_cell(text,img_file):

    logging.info("gen qcard back %s" % text)

    ipad = 1

    styles = getStyleSheet()
    a = Image(img_file)  
    a.drawHeight = 3*cm # * (a.drawHeight / a.drawWidth)
    a.drawWidth = 6*cm 

    p = Paragraph(text,styles["CardBackText"])


    cell = Table([ [a], [p] ],  colWidths=[7*cm],rowHeights=[3.0*cm,1*cm], 
        style=[
    #   ('GRID',(0,0),(-1,-1),0.5,colors.gray),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),

        ])


    return cell


def make_qcard_cell(qcard):

    logging.info("gen qcard for %s" % qcard)
    info_line_1 = safe(qcard.get("info_line_1"))
    info_line_2 = safe(qcard.get("info_line_2"))
    course_code = safe(qcard.get("course_code"))
    season_name = safe(qcard.get("season_name"))
    gid = nsafe(qcard.get("ref_gid"))
    name = safe(qcard.get("name"))
    surname = safe(qcard.get("surname"))
    qrcode = safe(qcard.get("qrcode"))


    info_text = info_line_1 +"<br/>"+ info_line_2
    ipad = 1
    unit = 29*mm

    styles = getStyleSheet()

    qrw = QrCodeWidget(qrcode)
    b = qrw.getBounds()
    w = b[2]-b[0]
    h = b[3]-b[1]
    qrcode_image = Drawing(unit,unit,transform=[unit/w,0,0,unit/h,0,0])
    qrcode_image.add(qrw)

    

    c00 =  starlet_logo # Paragraph("STARLET",styles["CardHeaderLeft"])
    c10 = Paragraph("TANEČNÍ ŠKOLA<br/>MANŽELŮ BURYANOVÝCH",styles["CardHeaderRight"])


    c01 = Paragraph(course_code,styles["CardCode"])
    c11 = Paragraph(season_name,styles["CardSeason"])

    c02 = Paragraph("id: "+str(gid),styles["CardGID"])


    c03 = Paragraph(info_text,styles["CardInfoLines"])
    c04 = Paragraph(name+" "+surname,styles["CardFullname"])

    

    cell = Table([ 
        [c00,c10,"#"],
        [c01,c11,qrcode_image],
        [c02,"#","#"], 
        [c03,"#","#"], 
        [c04,"#","#"]],
        colWidths=[2.7*cm,2.0*cm,2.7*cm],rowHeights=[1*cm,1.3*cm,0.4*cm,1.00*cm,0.7*cm], style=[
            ('BOX',(0,0),(-1,-1),1,colors.black),
            ('SPAN',(1,0),(2,0)),  #ts line
            ('BACKGROUND',(0,0),(-1,0),colors.black),
            ('VALIGN',(0,0),(-1,0),'MIDDLE'),

            ('LINEBELOW',(0,2),(1,2),1,colors.black),
            ('LINEAFTER',(1,1),(1,3),1,colors.black),

            ('SPAN',(2,1),(2,3)),  #qr

            ('SPAN',(0,2),(1,2)),  #gid
            ('VALIGN',(0,2),(1,2),'BOTTOM'),

            ('SPAN',(0,3),(1,3)),  #info line
            ('VALIGN',(0,3),(1,3),'BOTTOM'),

            ('SPAN',(0,4),(2,4)),  #name
            ('BACKGROUND',(0,4),(-1,4),colors.black),

            ('LEFTPADDING',(0,0),(-1,-1),ipad),
            ('RIGHTPADDING',(0,0),(-1,-1),ipad),
            ('RIGHTPADDING',(0,2),(1,2),ipad*5),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ])
    return cell


