from flask import Flask
from flask import make_response
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route("/")
def hello():
   return "Hello World from Flask !"

@app.route("/pdf")
def pdf():
    import cStringIO
    output = cStringIO.StringIO()

    p = canvas.Canvas(output)
    p.drawString(100, 100, 'Hello')
    p.showPage()
    p.save()
    
    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='sakulaci.pdf"
    response.mimetype = 'application/pdf'
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True, port=80)

