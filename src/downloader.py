import os
import yt_dlp
from tkinter import messagebox


def progresso_hook(d, progresso, root):
    """
    Atualiza a barra de progresso da interface gráfica durante o download.

    O `yt_dlp` fornece atualizações de progresso em tempo real. Esta função extrai
    a porcentagem concluída e atualiza a barra de progresso da GUI.

    Parâmetros:
        d (dict): Dados do progresso fornecidos pelo `yt_dlp`.
        progresso (tk.DoubleVar): Variável que controla a barra de progresso.
        root (tk.Tk): Referência à janela principal para atualização da interface.
    """
    if d['status'] == 'downloading':
        porcentagem = d.get('_percent_str', '0.0%').replace('%', '')  # Obtém a porcentagem sem o símbolo "%"
        progresso.set(float(porcentagem))
        root.update_idletasks()  # Atualiza a GUI para refletir o progresso em tempo real
    elif d['status'] == 'finished':
        progresso.set(100)  # Define progresso como 100% ao concluir o download


def baixar_midia(url, pasta_destino, opcao, progresso, root):
    """
    Baixa vídeos ou áudios do YouTube sempre na melhor qualidade disponível.

    O `yt_dlp` é utilizado para realizar o download do conteúdo. O formato de download
    é selecionado automaticamente para obter a melhor qualidade disponível.

    Parâmetros:
        url (str): URL do vídeo a ser baixado.
        pasta_destino (str): Caminho da pasta onde o arquivo será salvo.
        opcao (str): Tipo de download ("Vídeo + Áudio" ou "Apenas Áudio").
        progresso (tk.DoubleVar): Variável que controla a barra de progresso.
        root (tk.Tk): Referência à janela principal para atualização da interface.
    """
    try:
        if not url:
            raise ValueError("Insira um link do YouTube antes de baixar.")
        if not pasta_destino:
            raise ValueError("Selecione uma pasta de destino.")

        # Define o melhor formato de download disponível baseado na opção escolhida
        if opcao == "Vídeo + Áudio":
            format_id = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"  # Melhor vídeo e áudio combinados
            extensao = "mp4"
        else:
            format_id = "bestaudio/best"  # Melhor qualidade de áudio disponível
            extensao = "mp3"

        # Normaliza o caminho da pasta para evitar erros de compatibilidade entre sistemas operacionais
        pasta_destino_corrigido = os.path.normpath(pasta_destino)

        # Configuração do `yt_dlp`
        opcoes = {
            "format": format_id,
            "outtmpl": f"{pasta_destino_corrigido}/%(title)s.%(ext)s",  # Nome do arquivo de saída
            "progress_hooks": [lambda d: progresso_hook(d, progresso, root)]
        }

        # Adiciona pós-processamento caso o usuário queira apenas o áudio em MP3
        if opcao == "Apenas Áudio":
            opcoes["postprocessors"] = [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ]

        progresso.set(0)  # Reseta a barra de progresso antes de iniciar o download

        # Inicia o download do vídeo ou áudio usando `yt_dlp`
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)

        # Obtém o nome final do arquivo após o download
        nome_arquivo_final = info.get("title", "download") + f".{extensao}"
        caminho_final = os.path.join(pasta_destino_corrigido, nome_arquivo_final)

        # Verifica se o arquivo foi baixado corretamente antes de exibir a mensagem de sucesso
        if os.path.exists(caminho_final):
            messagebox.showinfo("Sucesso", f"Mídia baixada com sucesso!\n\n{caminho_final}")
        else:
            messagebox.showinfo("Sucesso", "Download concluído!\n(O arquivo pode estar salvo com um nome diferente.)")

        progresso.set(0)  # Reseta a barra de progresso após o download

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar mídia:\n{e}")
