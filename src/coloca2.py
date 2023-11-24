import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from rembg import remove

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Variáveis para armazenar os caminhos das imagens
        self.background_path = tk.StringVar()
        self.art_path = tk.StringVar()

        # Configurar o layout
        self.setup_layout()

    def setup_layout(self):
        # Botões para carregar imagens
        tk.Label(self.root, text="Background Image:").grid(row=0, column=0)
        tk.Button(self.root, text="Browse", command=self.load_background).grid(row=0, column=1)

        tk.Label(self.root, text="Art Image:").grid(row=1, column=0)
        tk.Button(self.root, text="Browse", command=self.load_art).grid(row=1, column=1)

        # Botão para processar imagens
        tk.Button(self.root, text="Process and Save", command=self.process_and_save).grid(row=2, column=0, columnspan=2)

        # Exibição do resultado
        self.result_image_label = tk.Label(self.root)
        self.result_image_label.grid(row=3, column=0, columnspan=2)

    def load_background(self):
        background_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.gif")])
        self.background_path.set(background_path)

    def load_art(self):
        art_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.gif")])
        self.art_path.set(art_path)

    def process_and_save(self):
        background_path = self.background_path.get()
        art_path = self.art_path.get()

        if not background_path or not art_path:
            messagebox.showerror("Error", "Please select both background and art images.")
            return

        result_image_path = self.process_single_image(background_path, art_path)
        self.display_image(result_image_path)

    def process_single_image(self, background_path, art_path):
        # Carregar imagem de background original
        original_background = Image.open(background_path)
        background_image = original_background.copy()
        # Redimensionar o background em números absolutos
        background_resized = background_image.resize((400, 600))

        # Carregar imagem da arte
        art_image = Image.open(art_path)
        # Redimensionar o tamanho da arte em números absolutos
        art_resized = art_image.resize((150, 100))

        # Verificar se a imagem tem um canal alfa (transparência)
        if 'A' in art_resized.getbands():
                  # Criar uma imagem transparente um pouco maior que a imagem original para fazer a função de moldura
            
            # Obter as dimensões da imagem original
            original_width, original_height = art_resized.size
            
            # Criar uma nova imagem RGBA (com canal alfa)
            border = Image.new('RGBA', (original_width + 10, original_height + 10), color=(0, 0, 0, 0))
            
            # Extrair a máscara de transparência da imagem redimensionada
            mask = art_resized.split()[3]
            
            # aplicar remove_background à máscara imagem
            art_resized_mask = remove(art_image)
            
        
            
           
        else:
            # Se não houver um canal alfa, usar uma borda sem transparência
            border = Image.new('RGB', (160, 110), color=(0, 0, 0))
            # Criar cópia da imagem
            art_border = border.copy()
            # Colar a imagem da arte sobre a moldura sem transparência
            art_border.paste(art_resized, (5, 5))

        # Criar cópia do background
        art_background = background_resized.copy()

        # Colar a parte interna da imagem da arte sem a borda sobre o background
        art_background.paste(art_resized_mask, (122, 227))

        # Salvar imagem no caminho de saída
        result_image_path = "result_image.png"
        art_background.save(result_image_path)

        return result_image_path

    def display_image(self, image_path):
        result_image = Image.open(image_path)
        result_image.thumbnail((400, 600))  # Redimensionar para caber na tela
        tk_image = ImageTk.PhotoImage(result_image)
        self.result_image_label.configure(image=tk_image)
        self.result_image_label.image = tk_image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
