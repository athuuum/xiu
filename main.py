import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
from CTkMenuBar import *
import subprocess
import threading
import os
import time
import json
import webbrowser

CONFIG_FILE = "config.json"

def load_config_and_set_theme():
    """Lê o config.json, define o tema e retorna as configs."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
    
    theme = config.get("theme", "system")
    ctk.set_appearance_mode(theme)
    return config

config = load_config_and_set_theme()
ctk.set_default_color_theme("blue")


class LoadingWindow(ctk.CTkToplevel):
    """Janela de carregamento com barra animada e texto"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Processando...")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        self.progress = ctk.CTkProgressBar(self, width=300)
        self.progress.pack(pady=40)
        self.progress.configure(mode="indeterminate")
        self.progress.start()

        self.label_status = ctk.CTkLabel(self, text="Iniciando processamento...", font=("Arial", 14))
        self.label_status.pack(pady=10)

    def update_status(self, text):
        """Atualiza o texto de status"""
        self.label_status.configure(text=text)
        self.update_idletasks()


class App(ctk.CTk):
    def __init__(self, initial_config: dict):
        super().__init__()
        self.title("Xiu")

        self.geometry("800x700") 
        self.minsize(800, 700)
        
        self.menu = CTkMenuBar(master=self)
        self.CONFIG_FILE = CONFIG_FILE

        self.config = self.menu.add_cascade("Configurações")
        self.config_drop = CustomDropdownMenu(widget=self.config)
        self.audio = self.config_drop.add_submenu("Áudio")
        self.audio.add_option(
            option="Retornar ao padrão",
            command=self.reset_audio_settings
        )
        self.theme = self.config_drop.add_submenu("Tema")
        
        self.theme.add_option(
            option="System Default", 
            command=lambda: self.set_theme("System Default")
        )
        self.theme.add_option(
            option="Claro", 
            command=lambda: self.set_theme("Claro")
        )
        self.theme.add_option(
            option="Escuro", 
            command=lambda: self.set_theme("Escuro")
        )

        self.about = self.menu.add_cascade("Sobre")
        self.about_drop = CustomDropdownMenu(widget=self.about)
        self.about_drop.add_option(
            option="GitHub", 
            command=self.open_github
        )
        self.about_drop.add_option(option="Versão 1.1")


        self.files = []
        self.silence_duration = ctk.DoubleVar(
            value=initial_config.get("duration", 0.5) 
        )
        self.threshold_db = ctk.DoubleVar(
            value=initial_config.get("threshold", -30.0)
        )
        self.output_format_var = ctk.StringVar(
            value=initial_config.get("format", "Manter Original")
        )

        ctk.CTkLabel(self, text="Remover silêncio de Mídia", font=("Arial", 20, "bold")).pack(pady=10)

        frame_path = ctk.CTkFrame(self)
        frame_path.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_path, text="Arquivos de Mídia (Áudio ou Vídeo):").pack(anchor="w", padx=10, pady=5)

        self.file_list_textbox = ctk.CTkTextbox(frame_path, height=100, state="disabled")
        self.file_list_textbox.pack(fill="x", expand=True, padx=10, pady=(0, 5))
        
        frame_path_buttons = ctk.CTkFrame(frame_path, fg_color="transparent")
        frame_path_buttons.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(frame_path_buttons, text="Selecionar arquivos",
                          compound="left", command=self.select_files).pack(side="left")

        self.clear_button = ctk.CTkButton(frame_path_buttons, text="Limpar Lista",
                                        compound="left", command=self.clear_files, width=120)
        self.clear_button.pack(side="left", padx=10)

        frame_slider = ctk.CTkFrame(self)
        frame_slider.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_slider, text="Cortar silêncios acima de (segundos):").pack(anchor="w", padx=10, pady=5)
        self.slider = ctk.CTkSlider(
            frame_slider, from_=0.2, to=5.0,
            variable=self.silence_duration,
            number_of_steps=48
        )
        self.slider.pack(fill="x", padx=10)
        self.label_value = ctk.CTkLabel(frame_slider, text=f"{self.silence_duration.get():.1f}s")
        self.label_value.pack(pady=5)
        self.slider.configure(command=lambda val: self.label_value.configure(text=f"{float(val):.1f}s"))

        frame_threshold = ctk.CTkFrame(self)
        frame_threshold.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(frame_threshold, text="Nível de Silêncio (dB):").pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(frame_threshold, text="(Mais baixo: -60dB / Mais alto: -20dB)", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(0,5))
        
        self.threshold_slider = ctk.CTkSlider(
            frame_threshold, from_=-60.0, to=-20.0,
            variable=self.threshold_db,
            number_of_steps=40
        )
        self.threshold_slider.pack(fill="x", padx=10)
        self.label_threshold = ctk.CTkLabel(frame_threshold, text=f"{self.threshold_db.get():.1f} dB")
        self.label_threshold.pack(pady=5)
        self.threshold_slider.configure(command=lambda val: self.label_threshold.configure(text=f"{float(val):.1f} dB"))

        frame_format = ctk.CTkFrame(self)
        frame_format.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame_format, text="Formato de Saída:").pack(side="left", padx=(10, 5), pady=10)
        
        self.format_menu = ctk.CTkOptionMenu(
            frame_format,
            values=["Manter Original", ".mp3", ".wav", ".m4a", ".flac"],
            variable=self.output_format_var,
            width=150
        )
        self.format_menu.pack(side="left", padx=(0, 10), pady=10)

        ctk.CTkButton(
            self,
            text="REMOVER SILÊNCIO",
            compound="left",
            height=40,
            fg_color="#1f6aa5",
            command=lambda: threading.Thread(target=self.remove_silence, daemon=True).start()
        ).pack(pady=20) 
        
        self.update_file_list_display()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def reset_audio_settings(self):
        """Reseta a duração e o threshold para os valores padrão."""
        default_duration = 0.5
        default_threshold = -30.0
        
        self.silence_duration.set(default_duration)
        self.threshold_db.set(default_threshold)
        
        self.label_value.configure(text=f"{default_duration:.1f}s")
        self.label_threshold.configure(text=f"{default_threshold:.1f} dB")
        print("Configurações de áudio resetadas para o padrão.")

    def on_closing(self):
        """Salva todas as configurações e fecha o app."""
        config_data = {
            "theme": ctk.get_appearance_mode().lower(),
            "duration": self.silence_duration.get(),
            "threshold": self.threshold_db.get(),
            "format": self.output_format_var.get()
        }
        self.save_config(config_data)
        self.destroy()

    def open_github(self):
        """Abre o repositório do GitHub no navegador padrão."""
        webbrowser.open("https://github.com/athuuum/xiu")
    
    def update_file_list_display(self):
        """Atualiza a caixa de texto com os nomes dos arquivos selecionados."""
        self.file_list_textbox.configure(state="normal")
        self.file_list_textbox.delete("1.0", "end")
        if not self.files:
            self.file_list_textbox.insert("1.0", "Nenhum arquivo selecionado.")
        else:
            file_names = [os.path.basename(f) for f in self.files]
            self.file_list_textbox.insert("1.0", "\n".join(file_names))
        self.file_list_textbox.configure(state="disabled")

    def clear_files(self):
        """Limpa a lista de arquivos e atualiza a interface."""
        self.files = []
        self.update_file_list_display()

    def select_files(self):
        """Seleciona múltiplos arquivos de áudio ou vídeo (Feature 5)"""
        files = filedialog.askopenfilenames(
            title="Selecione os arquivos de mídia",
            filetypes=[
                ("Arquivos de Mídia", "*.mp3 *.wav *.m4a *.flac *.mp4 *.mkv *.mov *.avi *.webm"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if files:
            self.files = list(files) 
            self.update_file_list_display()

    def remove_silence(self):
        """Remove silêncio de todos os arquivos selecionados com tela de loading"""
        if not self.files:
            CTkMessagebox(
                title="Aviso",
                message="Escolha pelo menos um arquivo de mídia primeiro.",
                icon="warning"
            )
            return
        
        loading = LoadingWindow(self)
        duration = self.silence_duration.get()
        threshold = self.threshold_db.get()
        selected_format = self.output_format_var.get()
        
        success_count = 0
        fail_count = 0

        for i, input_file in enumerate(self.files, start=1):
            filename = os.path.basename(input_file)
            directory = os.path.dirname(input_file)

            if selected_format == "Manter Original" and not self.is_video(input_file):
                output_file = os.path.join(directory, f"xiu_{filename}")
            
            elif selected_format == "Manter Original" and self.is_video(input_file):
                base_name = os.path.splitext(filename)[0]
                output_file = os.path.join(directory, f"xiu_{base_name}.mp3")
            
            else:
                base_name = os.path.splitext(filename)[0]
                output_file = os.path.join(directory, f"xiu_{base_name}{selected_format}")

            loading.update_status(f"Processando ({i}/{len(self.files)}): {filename}")

            try:
                command = [
                    r"ffmpeg\bin\ffmpeg.exe",
                    "-i", input_file,
                    "-af", f"silenceremove=stop_periods=-1:stop_threshold={threshold}dB:stop_duration={duration}",
                    "-y",
                    output_file
                ]
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                success_count += 1
            except subprocess.CalledProcessError:
                fail_count += 1
            except FileNotFoundError:
                loading.destroy()
                CTkMessagebox(
                    title="Erro",
                    message="FFmpeg não encontrado! Verifique o caminho 'ffmpeg/bin/ffmpeg.exe'",
                    icon="warning"
                )
                return
            except Exception as e:
                print(f"Erro inesperado ao processar {filename}: {e}")
                fail_count += 1


        loading.destroy()

        msg = f"{success_count} arquivo(s) processado(s) com sucesso."
        if fail_count > 0:
            msg += f"\n{fail_count} arquivo(s) falhou(ram)."

        CTkMessagebox(
            title="Concluído",
            message=msg,
            icon="check" if fail_count == 0 else "warning"
        )
        
        self.clear_files()

    def is_video(self, file_path):
        """Verifica se um arquivo é de vídeo pela extensão."""
        video_extensions = ['.mp4', '.mkv', '.mov', '.avi', '.webm', '.flv']
        return any(file_path.lower().endswith(ext) for ext in video_extensions)

    def set_theme(self, theme_name: str):
        """Mapeia o nome do tema, aplica e salva a configuração."""
        theme_map = {
            "System Default": "system",
            "Claro": "light",
            "Escuro": "dark"
        }
        ctk_theme_name = theme_map.get(theme_name, "system")
        ctk.set_appearance_mode(ctk_theme_name)
        self.save_config({"theme": ctk_theme_name})

    def save_config(self, data: dict):
        """Salva/Atualiza o dicionário de configuração no arquivo JSON."""
        try:
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                config = {}
            
            config.update(data)
            
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar configuração em {self.CONFIG_FILE}: {e}")


if __name__ == "__main__":
    app = App(initial_config=config)
    app.mainloop()