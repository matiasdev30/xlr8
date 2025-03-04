import cmd
from core.audio.speech_recognition import XLR8audio
from core.chat.chat import chat


class AudioCLI(cmd.Cmd):
    intro = "Bem-vindo ao Silvia. Digite help ou ? para listar comandos.\n"
    prompt = "(xlr8-cli) "
    xlr8audio = XLR8audio()

    def do_list(self):
        """Lista todos os dispositivos de áudio disponíveis."""
        self.xlr8audio.list_audio_devices()

    def do_talk(self, arg): 
        text = ""
        while "sai" not in text.lower():
            print("<Diga [sair] para sair｜>")
            print("Fala: ")
            path = self.xlr8audio.record_audio()
            
            if path is None :
                print("Silvia >> não consegui ouvir")
                return  
            
            text = self.xlr8audio.transcribe_audio(path)  
            
            if "sai" not in text.lower() :
                chat(prompt=text)

    def do_exit(self, arg):
        """Sai do programa."""
        print("Adeus!")
        return True
    
    def do_chat(self, arg):
        promt = ""
        while "sair" not in promt.lower():
            print("<｜Escreva [sair] para sair｜>")
            print("Escreva: ")
            promt = input(str())
            if "sair" not in promt.lower() :
                chat(prompt=promt)
            print("\n")




if __name__ == "__main__":
    AudioCLI().cmdloop()
