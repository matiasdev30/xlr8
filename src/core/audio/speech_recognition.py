from transformers import pipeline
from pydub import AudioSegment
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
from datetime import datetime

class XLR8audio():
    
    def __init__(self):
        self.asr_pipeline = pipeline("automatic-speech-recognition", model="mariana-coelho-9/whisper-small-pt") 

    def list_audio_devices(self):
        """Lista todos os dispositivos de áudio disponíveis"""
        print("Dispositivos de Áudio Disponíveis:")
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            print(f"Dispositivo {i}:")
            print(f"  Nome: {device['name']}")
            print(f"  Canais de Entrada: {device['max_input_channels']}")
            print(f"  Taxa de Amostragem Padrão: {device['default_samplerate']}")
            print()
            
    def record_audio(self, sample_rate=44100, channels=1, output_dir='recordings') -> str | None:
        """Grava áudio até que Enter seja pressionado"""
        # Cria diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Gera nome de arquivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"recording_{timestamp}.wav")
            
        """ print(f"\n--- Iniciando Gravação ---")
        print(f"Taxa de Amostragem: {sample_rate} Hz")
        print(f"Canais: {channels}")
        print(f"Arquivo: {filename}")
        print("Pressione Enter para parar a gravação...") """
        
        frames = []
        recording = [True]

        def audio_callback(indata, frames_count, time, status):
            if status:
                print(status)
            if recording[0]:
                frames.append(indata.copy())

        def stop_recording():
            input("Pressione Enter para parar a gravação...\n")
            recording[0] = False

        # Inicia thread para capturar áudio
        stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype='float32', callback=audio_callback)
        stream.start()

        # Inicia thread para parar a gravação quando Enter for pressionado
        stop_thread = threading.Thread(target=stop_recording, daemon=True)
        stop_thread.start()

        while recording[0]:
            pass

        stream.stop()
        stream.close()

        if frames:
            audio_data = np.concatenate(frames)
            
            # Salva o arquivo de áudio
            sf.write(filename, audio_data, sample_rate)
                
            # Verifica se o arquivo foi criado
            if os.path.exists(filename):
                print("\n--- Terminei de ouvir ---")
                """ print(f"Arquivo salvo: {filename}")
                print(f"Tamanho: {os.path.getsize(filename)} bytes") """
                print(f"Duração: {len(audio_data) / sample_rate:.2f} segundos")
                
                return filename
            else:
                print("Erro: Arquivo de áudio não foi criado.")
                return None
        else:
            print("Nenhum dado gravado.")
            return None

    def convert_audio(input_file: str, output_file: str):
        """
        Converte um arquivo de áudio para outro formato.
        
        :param input_file: Caminho do arquivo de entrada (e.g., .m4a).
        :param output_file: Caminho do arquivo de saída com a extensão desejada (e.g., .wav ou .wan).
        """
        try:
            # Verifica se a extensão do arquivo de saída é válida
            valid_extensions = ['.wav', '.mp3', '.ogg', '.flac']
            _, output_extension = os.path.splitext(output_file)
            
            if output_extension not in valid_extensions and output_extension != '.wan':
                raise ValueError(f"A extensão '{output_extension}' não é suportada para saída.")

            # Lê o arquivo de entrada
            audio = AudioSegment.from_file(input_file)

            # Salva o arquivo no formato valido
            if output_extension == '.wan':
                temp_file = output_file.replace('.wan', '.wav') 
                audio.export(temp_file, format="wav")
                # Renomeia para .wan
                os.rename(temp_file, output_file) 
            else:
                audio.export(output_file, format=output_extension[1:])  

        except Exception as e:
            raise RuntimeError(f"Erro ao converter o arquivo: {e}")

    def transcribe_audio(self, file_path: str) -> str:
        """
        Transcreve o conteúdo de um arquivo de áudio para texto.
        
        :param file_path: Caminho para o arquivo de áudio (.wav ou similar).
        :return: Transcrição em texto.
        """
        try:
            transcription = self.asr_pipeline(file_path)
            return transcription['text']
        except Exception as e:
            raise RuntimeError(f"Erro ao transcrever o áudio: {e}")


