from flask import Flask, request, send_file
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO
import base64
import json

app = Flask(__name__)
CORS(app)

@app.route('/logo.png', methods=['GET'])
def serve_logo():
    return send_file('logo.png', mimetype='image/png')

@app.route('/.well-known/ai-plugin.json', methods=['GET'])
def serve_manifest():
    print("Serving manifest file")
    return send_file('.well-known/ai-plugin.json', mimetype='application/json')

@app.route('/openapi.yaml', methods=['GET'])
def serve_openapi():
    return send_file('openapi.yaml', mimetype='application/yaml')

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf_route():
    print("Handling convert-to-pdf request")
    return convert_to_pdf(request)

def gcf_convert_to_pdf(request):
    return app(request.environ, functions.response)

def convert_to_pdf(request):
    # Parse the JSON body of the request
    data = json.loads(request.data)

    # Extract parameters from the JSON object
    text = data.get('text')
    font_size = data.get('font_size', 12)
    font_style = data.get('font_style', 'Normal')

    # Check if the text is not empty
    if not text:
        return {"error": "No text provided for conversion"}

    # Check if the font style is valid
    if font_style not in ['Normal', 'Italic', 'Heading1', 'Title', 'Heading2', 'Heading3', 'Bullet', 'Definition', 'Code']:
        return {"error": "Invalid font style provided"}

    # Create a BytesIO buffer for the PDF to be stored in
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    # Create the list of Paragraph objects
    styles = getSampleStyleSheet()
    story = [Paragraph(text, styles[font_style])]

    # Build the PDF
    doc.build(story)

    # Move to the beginning of the StringIO buffer
    buffer.seek(0)

    # Encode the PDF as a base64 string
    pdf_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Return the base64 string as the result
    return {
        'pdf_base64': pdf_base64
    }

if __name__ == '__main__':
    app.run(debug=True)
