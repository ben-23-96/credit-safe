import os
import getpass
from dotenv import load_dotenv
from openai import OpenAI
from gpt import GPT
from pdf_read import PdfReader

# Load environment variables from the .env file
load_dotenv()

# Retrieve the OpenAI api key
api_key = os.environ.get("OPENAI_API_KEY")

# Check if no API key in .env file
if not api_key:
    print("API key not found in .env file.")
    # Get API key from user
    api_key = getpass.getpass("Please enter your OpenAI API key: ")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Folder containing the PDFs to process
pdf_folder = "BE_GAZETTE_PDFS"
# Retrieve list of the pdf filenames
try:
    pdf_file_names = os.listdir(pdf_folder)
except FileNotFoundError:
    print(f"Error: The folder '{pdf_folder}' was not found.")
    pdf_file_names = []

# Process each PDF in the folder
for file_name in pdf_file_names:
    # get the file name without the .pdf for naming purposes
    file_name_without_suffix = file_name.split('.')[0]

    # create PdfReader instance to handle PDF processing
    pdf_reader = PdfReader(pdf=f"{pdf_folder}/{file_name}")
    # convert the pdf to a image so it can be processed by the OCR
    pdf_reader.convert_pdf_to_image()
    # crop image to target relevant area, improving OCR text quality returned
    pdf_reader.crop_image()

    # Optional: save cropped image for testing and debugging
    #  if not os.path.exists("cropped_images"):
    #      os.makedirs("cropped_images")
    #  with open(f"cropped_images/{file_name_without_suffix}.png", 'wb') as img_file:
    #      img_file.write(pdf_reader.cropped_img_byte_arr)

    # retrieve the text from the cropped image of the PDF using OCR
    pdf_text = pdf_reader.get_text()

    # Optional: save extracted text for testing and debugging
    # if not os.path.exists("OCR_returned_text"):
    #     os.makedirs("OCR_returned_text")
    # with open(f"OCR_returned_text/{file_name_without_suffix}.txt", "w", encoding="utf-8") as text_file:
    #     text_file.write(pdf_text)

    # create instance of the gpt class, passing the OpenAI client and the pdf text that it will analayse
    gpt = GPT(client=client, text=pdf_text)
    # create the prompt for the OpenAI API
    gpt.create_prompt()
    # generate and recieve the response from GPT
    gpt.generate_response()
    # save the generated json response to the results.json file
    gpt.save_to_json(name=file_name_without_suffix)
