import os
from tkinter import messagebox
from PIL import Image


def converter_imagem(input_path, output_format):
    """
    Converte uma imagem para o formato desejado.

    Utiliza a biblioteca Pillow (PIL) para abrir a imagem e convertê-la para um
    novo formato, garantindo compatibilidade com diferentes extensões.

    Parâmetros:
        input_path (str): Caminho do arquivo de entrada.
        output_format (str): Formato de saída desejado (ex: "jpeg", "png").
    """
    try:
        if not input_path:
            raise ValueError("Nenhum arquivo selecionado.")

        # Define o caminho do arquivo convertido mantendo o nome original
        nome_base, _ = os.path.splitext(input_path)
        output_path = f"{nome_base}.{output_format.lower()}"

        # Abre a imagem
        img = Image.open(input_path)

        # Converte imagens RGBA/P para RGB ao salvar como JPEG
        if output_format.lower() == "jpeg" and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Salva a imagem no novo formato
        img.save(output_path, output_format.upper())

        messagebox.showinfo("Sucesso", f"Imagem convertida com sucesso!\n\n{output_path}")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter a imagem:\n{e}")
