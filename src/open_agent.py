from openai import OpenAI
from openai import OpenAIError
import pyaudio

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
                model=self.model_name ,
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
            
            
        
        