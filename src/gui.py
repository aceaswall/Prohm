import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sv_ttk  # Biblioteca para aplicar um tema moderno ao Tkinter
from src.downloader import baixar_midia
from src.converter import converter_imagem


def aplicar_tema():
    """Define o tema da interface usando a biblioteca sv_ttk."""
    sv_ttk.set_theme("dark")  # Define o tema como escuro para melhor visualização


def selecionar_arquivo(file_path_var):
    """Abre um seletor de arquivo e armazena o caminho do arquivo escolhido."""
    caminho = filedialog.askopenfilename(filetypes=[
        ("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff;*.webp"),
        ("Todos os arquivos", "*.*")
    ])
    file_path_var.set(caminho)  # Atualiza o campo de entrada com o caminho do arquivo


def selecionar_pasta_destino(pasta_destino_var):
    """Abre um seletor de pasta e armazena o caminho da pasta escolhida."""
    pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino")
    pasta_destino_var.set(pasta_destino)  # Atualiza o campo de entrada com o caminho da pasta


def iniciar_gui():
    """
    Inicializa a interface gráfica do Prohm.

    Organiza os elementos da interface para permitir conversão de imagens e download de vídeos do YouTube.
    Mantém uma abordagem modular, onde cada seção tem seu próprio frame para melhor organização.
    """
    global root, progresso, url_var, tipo_download_var, pasta_destino_var
    root = tk.Tk()
    root.title("Prohm - Conversor & Downloader")

    aplicar_tema()  # Aplica o tema escuro na interface

    # Variáveis de controle da interface
    file_path_var = tk.StringVar()
    format_var = tk.StringVar(value="jpeg")
    url_var = tk.StringVar()
    tipo_download_var = tk.StringVar(value="Vídeo + Áudio")
    pasta_destino_var = tk.StringVar(value="Selecione uma pasta de destino...")
    progresso = tk.DoubleVar()

    # Estrutura principal da interface
    frame_principal = ttk.Frame(root, padding=15)
    frame_principal.pack(fill="both", expand=True)

    # Seção: Conversor de Imagens
    ttk.Label(frame_principal, text="Conversor de Imagens", font=("Arial", 14, "bold")).grid(column=0, row=0,
                                                                                             columnspan=3, pady=10)
    ttk.Label(frame_principal, text="Selecione a imagem:").grid(column=0, row=1, columnspan=3, pady=(5, 2))

    # Frame para alinhar o campo de entrada e o botão "Buscar"
    frame_input = ttk.Frame(frame_principal)
    frame_input.grid(column=0, row=2, columnspan=3, sticky="ew", padx=5)

    entry_arquivo = ttk.Entry(frame_input, textvariable=file_path_var, width=35, state="readonly")
    entry_arquivo.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=2)

    ttk.Button(frame_input, text="Buscar", command=lambda: selecionar_arquivo(file_path_var)).pack(side="right", pady=2)

    # Seleção do formato de saída e botão de conversão
    ttk.Label(frame_principal, text="Formato de saída:").grid(column=0, row=3, pady=5, sticky="w")

    frame_converter = ttk.Frame(frame_principal)
    frame_converter.grid(column=0, row=4, columnspan=3, sticky="ew", padx=5)

    combo_formatos = ttk.Combobox(frame_converter, textvariable=format_var,
                                  values=["jpeg", "png", "bmp", "gif", "tiff", "webp"], state="readonly", width=12)
    combo_formatos.pack(side="left", padx=(0, 5))

    ttk.Button(frame_converter, text="Converter",
               command=lambda: converter_imagem(file_path_var.get(), format_var.get())).pack(side="right", pady=2)

    # Linha separadora entre seções
    ttk.Separator(frame_principal, orient="horizontal").grid(column=0, row=5, columnspan=3, sticky="ew", pady=15)

    # Seção: Downloader de YouTube
    ttk.Label(frame_principal, text="Downloader de YouTube", font=("Arial", 14, "bold")).grid(column=0, row=6,
                                                                                              columnspan=3, pady=10)
    ttk.Label(frame_principal, text="Insira o link do YouTube:").grid(column=0, row=7, columnspan=3, pady=(5, 2))
    ttk.Entry(frame_principal, textvariable=url_var, width=45).grid(column=0, row=8, columnspan=3, padx=5, pady=2)

    # Opções de tipo de download (Vídeo + Áudio ou Apenas Áudio)
    ttk.Label(frame_principal, text="Escolha o tipo de download:").grid(column=0, row=9, columnspan=3, pady=(5, 2))

    frame_radio = ttk.Frame(frame_principal)
    frame_radio.grid(column=0, row=10, columnspan=3, sticky="ew", padx=5)

    ttk.Radiobutton(frame_radio, text="Vídeo + Áudio", variable=tipo_download_var, value="Vídeo + Áudio").pack(
        side="left", padx=5)
    ttk.Radiobutton(frame_radio, text="Apenas Áudio", variable=tipo_download_var, value="Apenas Áudio").pack(
        side="right", padx=5)

    # Seleção da pasta de destino
    ttk.Label(frame_principal, text="Selecione a pasta de destino:").grid(column=0, row=11, columnspan=3, pady=(10, 2))

    frame_pasta = ttk.Frame(frame_principal)
    frame_pasta.grid(column=0, row=12, columnspan=3, sticky="ew", padx=5)

    entry_pasta = ttk.Entry(frame_pasta, textvariable=pasta_destino_var, width=35, state="readonly")
    entry_pasta.pack(side="left", fill="x", expand=True, padx=(0, 5), pady=2)

    ttk.Button(frame_pasta, text="Buscar", command=lambda: selecionar_pasta_destino(pasta_destino_var)).pack(
        side="right", pady=2)

    # Botão de download de mídia
    ttk.Button(frame_principal, text="Baixar",
               command=lambda: baixar_midia(url_var.get(), pasta_destino_var.get(), tipo_download_var.get(), progresso,
                                            root)).grid(column=0, row=13, columnspan=3, padx=5, pady=10, sticky="ew")

    # Barra de progresso
    ttk.Label(frame_principal, text="Progresso do Download:").grid(column=0, row=14, columnspan=3, pady=(5, 2))
    ttk.Progressbar(frame_principal, variable=progresso, maximum=100, length=400).grid(column=0, row=15, columnspan=3,
                                                                                       pady=5)

    # Ajusta o tamanho da interface conforme os elementos carregados
    root.update_idletasks()
    root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")
    root.mainloop()


if __name__ == "__main__":
    iniciar_gui()
