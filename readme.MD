## Overview

The code extracts specific information from provided Belgian Gazette PDFs, including:

- **Company Name**
- **Company Number**
- **Document Purpose**
- **Summary of Additional Information**

### How It Works

1. **PDF to Image Conversion**: The code first converts each page of the PDF to images. It then crops the images to the relevant sections where the needed information is located.
2. **OCR with EasyOCR**: Using EasyOCR, the code extracts text from the cropped images.
3. **Data Extraction with OpenAI**: Using the OpenAI API, the extracted text is processed with a clearly designed prompt to identify and structure the relevant information. The response is returned in JSON format.
4. **Output**: The results are saved in a JSON file, structured as follows:

   ```json
   {
       "pdf_number": {
           "company_name": "",
           "company_number": "",
           "document_purpose": [""],
           "additional_information": ""
       }
   }


## Getting Started

### Prerequisites

- **Python**: Code is written in Python so must have Python installed.
- **Requirements**: Install necessary packages by running:

  ```bash
  pip install -r requirements.txt
  ```
### API Key

This project requires an OpenAI API key. You can provide it in two ways:

1. **Environment Variable**: Create a `.env` file in the project directory and add your API key as follows:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Input During Execution**: You can also run the code and be prompted to enter the API key manually.


### PDF Directory
This project processes PDF files located in a folder named BE_GAZETTE_PDS. Ensure that:

- The BE_GAZETTE_PDS folder is in the same directory as the code.
- All PDF files you want to process are placed in this folder.
  
The folder should already be there but if the folder does not exist, create it and add your PDF files there.

### Running the code

To run the code:

```bash
python main.py
```
