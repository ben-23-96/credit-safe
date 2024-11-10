import easyocr
import fitz  # PyMuPDF
from PIL import Image
import io


class PdfReader:
    def __init__(self, pdf):
        """
        Initializes the PdfReader class with the provided PDF file. Also initializes an EasyOCR reader.
        """
        self.pdf = pdf
        self.pdf_as_img = None
        self.cropped_img_byte_arr = None
        self.reader = easyocr.Reader(lang_list=['en', 'de', 'fr', 'nl'], gpu=True)

    def convert_pdf_to_image(self):
        """
        Converts the PDF to an image with increased resolution.
        Stores the result as a PIL Image in self.pdf_as_img.
        """
        try:
            # Open the PDF and render to an image
            doc = fitz.open(self.pdf)
            page_number = 0 
            page = doc.load_page(page_number)
            
            # zoom for higher resolution
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert Pixmap to bytes and then to PIL Image
            img_bytes = pix.tobytes()
            img = Image.open(io.BytesIO(img_bytes))
            self.pdf_as_img = img

        except Exception as e:
            print(f"Error converting PDF located {self.pdf} to image: {e}")

    def crop_image(self):
        """
        Crops the image to focus OCR on relevant content.
        Stores the cropped image as bytes in self.cropped_img_byte_arr.
        """
        if self.pdf_as_img is None:
            print(f"Error: No image to crop for {self.pdf}")
            return

        try:
            # Define cropping box coordinates
            left, top, right, bottom = 150, 310, 1180, 650
            cropped_image = self.pdf_as_img.crop((left, top, right, bottom))
            
            # Save the cropped image as bytes
            cropped_byte_arr = io.BytesIO()
            cropped_image.save(cropped_byte_arr, format='PNG')
            self.cropped_img_byte_arr = cropped_byte_arr.getvalue()

        except Exception as e:
            print(f"Error cropping image for pdf located at {self.pdf}: {e}")

    def get_text(self):
        """
        Extracts text from the cropped image using OCR and returns as a string.
        """

        if not self.cropped_img_byte_arr:
            print(f"Error: No cropped image available for OCR for {self.pdf}.")
            return ""

        try:
            # read text from the cropped image using easyOCR
            result = self.reader.readtext(self.cropped_img_byte_arr)

            # Combine detected text into a single string
            text = '\n'.join([detection[1] for detection in result])
            return text

        except Exception as e:
            print(f"Error extracting text from image from {self.pdf}: {e}")
            return ""

