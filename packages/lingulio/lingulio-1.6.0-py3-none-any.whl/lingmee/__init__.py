import google.generativeai as genai
import re
import math

class BasicLingua:
    def __init__(self, api_key: str):
        """
        Initializes the BasicLingua class with the given API key.

        `Parameters`:
        1. api_key (str): The API key to be used for the Gemini AI model.
        """

        # Configuring Gemini AI with API key
        genai.configure(api_key=api_key)

        # text generation model
        self.model = genai.GenerativeModel('gemini-1.0-pro-latest')
        
        # vision model
        v_model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')


    ########################## Extract Patterns ##########################
    def extract_patterns(self, user_input: str, patterns: str) -> list:
        """
        Extracts patterns from the given input sentence.

        `Parameters`:
        1. user_input (str): The input sentence containing information to be extracted. 
        Example: "The phone number is 123-456-7890."

        2. patterns (str): Comma-separated patterns to be extracted. 
        Example: "email, name, phone number, address, date of birth".

        `Returns`:
            list: A list containing the extracted patterns. If no pattern is found, returns None.
        """

        # Generate the prompt template
        prompt_template = f'''
        Given the input sentence:
        user input: {user_input}

        __________________________

        extract {patterns} from it
        Output must only contain the extracted patterns but not what they are
        output must not contain any bullet points
        if no pattern found returns None
        '''

        # check if parameters are of correct type
        if not isinstance(user_input, str):
            raise TypeError("user_input must be of type str")
        if not isinstance(patterns, str):
            raise TypeError("patterns must be of type str")
        
        
        # Generate response using the provided model (assuming it's defined elsewhere)
        try:
            # Generate response using the provided model (assuming it's defined elsewhere)
            response = self.model.generate_content(prompt_template)
            # Extract the output list
            output_list = response.text.split('\n')
            return output_list
        except Exception as e:
            raise ValueError("Please provide a correct API key or try again.")
