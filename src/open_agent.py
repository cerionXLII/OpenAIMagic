from openai import OpenAI
from openai import OpenAIError
import pyaudio
import base64

class OpenAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.chat_model_name = 'gpt-4o-mini'
        self.transcribe_model_name = 'whisper-1'
        self.text_to_speach_model_name = 'tts-1' # tts-1, tts-1-hd (high definition)

    # Chat with the model
    def chat(self, text):
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model_name ,
                messages=[{"role": "user", "content": f'{text}'}]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return None
        

    # Trnascribe audio file to text
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
        
    # Converts text to speach (sound file)    
    # The default response format is "mp3", but other formats like "opus", "aac", "flac", and "pcm" are available
    # Supported voices are alloy, echo, fable, onyx, nova, and shimmer
    def text_to_speach(self, text, target_file_name, output_format='mp3', voice='alloy'):
        try:
            response = self.client.audio.speech.create(
                model=self.text_to_speach_model_name,
                voice=voice,
                input=text,
                response_format=output_format
            )
            response.stream_to_file(target_file_name)
        except OpenAIError as e:
            print(e)

    def text_to_speach_stream(self, text, output_format='pcm', voice='alloy'):
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=self.text_to_speach_model_name,
                voice=voice,
                input=text,
                response_format=output_format
            ) as response:
                p = pyaudio.PyAudio()
                stream = p.open(format=8,
                                channels=1,
                                rate=24_000,
                                output=True)
                for chunk in response.iter_bytes(1024):
                    stream.write(chunk)

        except OpenAIError as e:
            print(e)
            
    def translate_text(self, text, target_language='swedish'):
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model_name,
                messages=[
                    {"role": "system", "content": f'Your goal is to translate text from one language to another. It should be grammatically correct with as good translation as possible. Translate the following text to {target_language}.'},
                    {"role": "user", "content": f'{text}'}
                    ]
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return None
        

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def caption_image(self, image_path, target_language='swedish'):
        # Getting the base64 string
        base64_image = self.encode_image(image_path)
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model_name,
                messages=[
                    {"role": "system", "content": f'Your goal is to view an image and create a descriptive caption of it. It should be between 1-3 sentenses long. It should be grammatically correct and using the following language: {target_language}.'},
                    {"role": "user", "content": [
                        {
                            'type': 'text',
                            'text': 'Create a caption of the image.'
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                 "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                        },
                        ]}
                ]                   
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return None

        
        