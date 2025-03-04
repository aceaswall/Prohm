import os
import yt_dlp
from tkinter import messagebox

def progresso_hook(d, progresso, root):
    """Atualiza a barra de progresso na GUI."""
    if d['status'] == 'downloading':
        porcentagem = d.get('_percent_str', '0.0%').replace('%', '')
        progresso.set(float(porcentagem))
        root.update_idletasks()
    elif d['status'] == 'finished':
        progresso.set(100)

def baixar_midia(url, pasta_destino, opcao, progresso, root):
    """Baixa vídeos ou áudios do YouTube usando yt-dlp."""
    try:
        if not url:
            raise ValueError("Insira um link do YouTube antes de baixar.")
        if not pasta_destino:
            raise ValueError("Selecione uma pasta de destino.")

        formato = "bv*[ext=mp4]+ba[ext=m4a]/bestaudio/best" if opcao == "Vídeo + Áudio" else "bestaudio/best"
        mensagem_sucesso = "Vídeo baixado com sucesso!" if opcao == "Vídeo + Áudio" else "Áudio baixado com sucesso!"

        pasta_destino_corrigido = os.path.normpath(pasta_destino)

        opcoes = {
            "format": formato,
            "outtmpl": f"{pasta_destino_corrigido}/%(title)s.%(ext)s",
            "merge_output_format": "mp4" if opcao == "Vídeo + Áudio" else "mp3",
            "progress_hooks": [lambda d: progresso_hook(d, progresso, root)],
            "postprocessors": [
                {"key": "FFmpegMerger"} if opcao == "Vídeo + Áudio" else
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ]
        }

        progresso.set(0)
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        messagebox.showinfo("Sucesso", mensagem_sucesso)
        progresso.set(0)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar mídia:\n{e}")
