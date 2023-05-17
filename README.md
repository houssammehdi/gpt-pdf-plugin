# GPT PDF Conversion Plugin

This is a Flask-based plugin that converts text into a PDF document. It supports various formatting options including font size, font style, alignment, margins, headers, footers, tables, and images.

## Features

- Convert text to PDF
- Customize font size and style
- Customize page size and margins
- Add headers and footers
- Add tables and images
- Align text

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/gpt-pdf-plugin.git
```
2. Navigate to the project directory:
```
cd gpt-pdf-plugin
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```

## Add to Chat-GPT

1. Press on **Develop your own plugin**
2. Enter the url - locally: `localhost:5000`

## Usage

Run the application:
```
python main.py
```

Send a POST request to the `/convert-to-pdf` endpoint with your text and formatting options in the request body. The endpoint will return a base64-encoded PDF document.

Here's an example request body:

```json
{
  "paragraphs": [
    {
      "text": "Hello, world!",
      "font_size": 20,
      "font_style": "Title",
      "alignment": "CENTER",
      "table": {
        "data": [
          ["Column 1", "Column 2"],
          ["Row 1, Cell 1", "Row 1, Cell 2"],
          ["Row 2, Cell 1", "Row 2, Cell 2"]
        ],
        "style": ["Header", "Normal"]
      },
      "image": {
        "src": "https://example.com/image.jpg",
        "width": 500,
        "height": 300
      }
    },
    // More paragraphs...
  ],
  "page_size": "A4",
  "margins": {
    "top": 10,
    "bottom": 10,
    "left": 10,
    "right": 10
  }
}
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## License
This project is licensed under the terms of the MIT license.
