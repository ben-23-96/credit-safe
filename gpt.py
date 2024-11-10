from langdetect import detect
from deep_translator import GoogleTranslator
import json
import re
import os

class GPT:
    def __init__(self, client, text):
        self.client = client
        self.text = text
        self.prompt = ""
        self.gpt_response_text = ""
      

    def create_prompt(self):
        language = detect(self.text)
        self.prompt = f'''Please read the following {language} text and extract the following information in English:
  
        - Company Name
        - Company Number
        - Document Purpose
        - Additional Information Summary:
           - Provide a brief summary that includes all key points, names of indivuals, and dates of events related to the document's purpose. Keep the summary concise.
        
        
        Provide the extracted information in English **only** in the following JSON format (no additional text):
        
        {{
          "company_name": "Extracted Company Name",
          "company_number": "Extracted Company Number",
          "document_purpose": ["Extracted Document Purpose"]
          "additional_information": "Brief Extracted Summary"
        }}
        
        Here is the {language} text:
        
        {self.text}
        '''
    
    def generate_response(self):
        """
        Sends the prompt to the OpenAI client and stores text in self.gpt_response_text.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt,
                    }
                ],
                model="gpt-4o",
            )
            self.gpt_response_text = response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")

    def save_to_json(self, name):
        """
        Extracts JSON from the GPT response and saves it to 'results.json'.
        """
        # Extract JSON object from the response content
        json_match = re.search(r'\{.*\}', self.gpt_response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                data = json.loads(json_str)
                print("JSON parsed successfully.")
            except json.JSONDecodeError as e:
                print("Failed to parse JSON:", e)
                return
        else:
            print("No JSON object found in the response.")
            return
        
        # ensure document purposes are in english, missing the translation once or twice
        document_purposes = data["document_purpose"]
        for i, purpose in enumerate(document_purposes):
            document_purposes[i] = GoogleTranslator(source='auto', target='en').translate(purpose)

        # Read existing json data
        if os.path.exists("results.json"):
            try:
                with open("results.json", 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
                    # if no json already in file intialize new dictionary for data
                    if not isinstance(existing_data, dict):
                        existing_data = {}
            except json.JSONDecodeError as e:
                print("Failed to parse existing JSON file:", e)
                existing_data = {}
        else:
            existing_data = {}

        # add new entry to the existing data
        existing_data[name] = data

        # write the updated json back to results.json
        with open("results.json", 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
        print(f'Data for {name} saved.')
        