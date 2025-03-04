import subprocess
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from gtts import gTTS
from pydantic import BaseModel
from api.config.xlr8_exception import ClientParametreRequestException, Xlr8HttpExceptionFastAPI 
from api.utils.utils import TextInput
from fastapi.responses import FileResponse, JSONResponse
from core.audio.speech_recognition import *
import shutil
import uuid
import os
import pyttsx3
from core.translation.translation import translation_pt_to_en, translation_en_to_pt
from core.chat.chat import chat


router = APIRouter()

def text_to_audio(text: str) -> str:
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Texto não pode estar vazio.")
        
        output_dir = "audio_output"
        os.makedirs(output_dir, exist_ok=True)

        file_name_mp3 = f"{uuid.uuid4()}.mp3"
        file_path_mp3 = os.path.join(output_dir, file_name_mp3)


        tts = gTTS(text=text, lang='en')
        tts.save(file_path_mp3)

        return file_path_mp3

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no sintetizador de voz: {str(e)}")

class TextToAudioRequest(BaseModel):
    text: str

@router.post("/text-to-audio/")
async def text_to_audio_offline(input: TextInput):
    try:
        if not input.text.strip():
            raise HTTPException(status_code=400, detail="Texto não pode estar vazio.")
        
        output_dir = "audio_output"
        os.makedirs(output_dir, exist_ok=True)
        file_name = f"{uuid.uuid4()}.wav"
        file_path = os.path.join(output_dir, file_name)
        

        subprocess.run(['say', '-o', file_path, '-f', 'wav', input.text], check=True)

        return FileResponse(file_path, media_type="audio/wav", filename=file_name)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate/pt-to-en/")
async def translate_pt_to_en(input: TextInput):
    """
    Endpoint para traduzir texto do português para o inglês.
    """
    try:
        if not input.text.strip():
            raise ClientParametreRequestException(
                status_code=400, 
                msg="Texto não pode estar vazio.", 
                params=[input]
            )
        
        translated_text = translation_pt_to_en(input.text)
        
        return JSONResponse(
            content={"original_text": input.text, "translated_text": translated_text},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        # Qualquer outro erro será tratado como 500
        raise Xlr8HttpExceptionFastAPI(status_code=500, detail=str(e))


@router.post("/translate/en-to-pt/")
async def translate_en_to_pt(input: TextInput):
    """
    Endpoint para traduzir texto do inglês para o português.
    """
    try:
        if not input.text.strip():
            raise  ClientParametreRequestException(status_code=400, msg="Texto não pode estar vazio.", params=[input])
        
        translated_text = translation_en_to_pt(input.text)
        
        return JSONResponse(
            content={"original_text": input.text, "translated_text": translated_text},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        raise Xlr8HttpExceptionFastAPI(status_code=500, detail=str(e))
    
    


@router.post("/chat/")
async def chat_endpoint(input: TextInput):
    """
    Endpoint for generating chat responses using the MLX language model.
    
    :param input: Text input from the user
    :return: Generated chat response
    """
    try:
        if not input.text.strip():
            raise ClientParametreRequestException(status_code=400, msg="Texto não pode estar vazio.")
        
        response = chat(input)
        
        return JSONResponse(content={"response": response}, headers={"Content-Type": "application/json; charset=utf-8"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

""" 
@router.post("/text-to-audio/")
def text_to_audio(text: str) -> str:
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Texto não pode estar vazio.")
        
        output_dir = "audio_output"
        os.makedirs(output_dir, exist_ok=True)

        # Gera um nome de arquivo único
        file_name_wav = f"{uuid.uuid4()}.wav"  # pyttsx3 suporta salvar em WAV
        file_path_wav = os.path.join(output_dir, file_name_wav)

        # Inicializa o sintetizador de voz pyttsx3
        engine = pyttsx3.init()
        
        # Configurações do sintetizador (opcional)
        rate = engine.getProperty('rate')  # velocidade da fala
        volume = engine.getProperty('volume')  # volume
        voices = engine.getProperty('voices')  # lista de vozes

        # Define a voz masculina (index 0) ou feminina (index 1) se disponível
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # feminina

        engine.save_to_file(text, file_path_wav)
        engine.runAndWait()

        # Converte o arquivo WAV para MP3 usando pydub
        #check_ffmpeg()  # Verifica se o FFmpeg está disponível

        file_name_mp3 = f"{uuid.uuid4()}.mp3"
        file_path_mp3 = os.path.join(output_dir, file_name_mp3)

        audio = AudioSegment.from_wav(file_path_wav)
        audio.export(file_path_mp3, format="mp3")

        # Remove o arquivo WAV após a conversão
        os.remove(file_path_wav)

        return file_path_mp3

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no sintetizador de voz: {str(e)}") """


@router.post("/transcribe/")
async def upload_and_transcribe(file: UploadFile = File(...)):
    """
    Endpoint que recebe um arquivo de áudio, converte-o se necessário e realiza a transcrição.
    
    :param file: Arquivo enviado na requisição.
    :return: Transcrição do áudio.
    """
    try:
        # Salva o arquivo enviado em um local temporário
        input_dir = "temp_audio"
        output_dir = "converted_audio"
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        input_path = os.path.join(input_dir, f"{uuid.uuid4()}_{file.filename}")
        output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Converte o arquivo para .wav, se necessário
        if not input_path.endswith(".wav"):
            convert_audio(input_path, output_path)
        else:
            output_path = input_path  # Se já for WAV, mantém o mesmo caminho

        # Realiza a transcrição
        transcription = transcribe_audio(output_path)

        # Resposta JSON
        return JSONResponse(content={"transcription": transcription})
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        # Limpeza de arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
