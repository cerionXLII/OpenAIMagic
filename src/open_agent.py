from openai import OpenAI
from openai import OpenAIError

class OpenAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.chat_model_name = 'gpt-4o-mini'
        self.transcribe_model_name = 'whisper-1'

    def chat(self, text):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name ,
                messages=[{"role": "user", "content": f'{text}'}]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return None
        

    def transcribe(self, file_path):
        try:

            #Open audio file
            audio_file = open(file_path, 'rb')

            #Transcribe audio file using whisper
            transcription = self.client.audio.transcriptions.create(
                model=self.transcribe_model_name, 
                file=audio_file,
            )
            return(transcription.text)
        except Exception as e:
            print(e)
            return None
            
        
        