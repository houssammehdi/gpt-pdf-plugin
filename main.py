from flask import Flask, request, send_file
from flask_cors import CORS
from reportlab.lib.pagesizes import A4, LETTER, LEGAL, ELEVENSEVENTEEN
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Table, Image, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
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

def getPageSize(page_size_name):
    page_sizes = {
        'A4': A4,
        'LETTER': LETTER,
        'LEGAL': LEGAL,
        'ELEVEN_SEVENTEEN': ELEVENSEVENTEEN
    }

    try:
        return page_sizes[page_size_name.upper()]
    except KeyError:
        raise ValueError(f"Invalid page size: {page_size_name}")

def convert_to_pdf(request):
    # Parse the JSON body of the request
    data = json.loads(request.data)

    # Extract parameters from the JSON object
    paragraphs = data.get('paragraphs', [])
    page_size = data.get('page_size', 'A4')
    margins = data.get('margins', {'top': 72, 'bottom': 72, 'left': 72, 'right': 72})

    # Check if the paragraphs is not empty
    if not paragraphs:
        return {"error": "No paragraphs provided for conversion"}

    # Check if the page size is valid
    try:
        page_size = getPageSize(page_size)
    except ValueError as e:
        return {"error": str(e)}

    # Create a BytesIO buffer for the PDF to be stored in
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file"
    doc = SimpleDocTemplate(buffer, pagesize=page_size, 
                            topMargin=margins.get('top', 72), 
                            bottomMargin=margins.get('bottom', 72), 
                            leftMargin=margins.get('left', 72), 
                            rightMargin=margins.get('right', 72))

    # Create the list of Flowable objects
    story = []
    alignment_dict = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER, 'JUSTIFY': TA_JUSTIFY}
    for paragraph in paragraphs:
        text = paragraph.get('text')
        if text is None:
            continue  # Skip this paragraph if text is None

        font_size = paragraph.get('font_size', 12)
        font_style = paragraph.get('font_style', 'Normal')
        alignment = paragraph.get('alignment', 'LEFT')

        style = ParagraphStyle(
            name=font_style,
            fontSize=font_size,
            alignment=alignment_dict.get(alignment, TA_LEFT)
        )

        story.append(Paragraph(text, style))

        # Add table if exists in paragraph
        # Add table if exists in paragraph
        if 'table' in paragraph:
            table_data = paragraph['table'].get('data', [])
            table_style_data = paragraph['table'].get('style', [])

            # Create a TableStyle object from the style data
            table_style = TableStyle([
                (style, (0, i), (-1, i), colors.black)
                for i, style in enumerate(table_style_data)
            ])

            story.append(Table(table_data, style=table_style))

        # Add image if exists in paragraph
        if 'image' in paragraph:
            image_src = paragraph['image'].get('src', '')
            image_width = paragraph['image'].get('width', 100)
            image_height = paragraph['image'].get('height', 100)
            story.append(Image(image_src, width=image_width, height=image_height))

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
