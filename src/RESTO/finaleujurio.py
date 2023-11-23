import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from rembg import remove

class ImageProcessor:
    def __init__(self, root, canvas, output_label):
        self.root = root
        self.canvas = canvas
        self.output_label = output_label
        self.original_img = None
        self.processed_img = None
        self.background_img = None
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.create_widgets()

    def create_widgets(self):
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.output_label.grid(row=0, column=1, padx=20, pady=20)

        button_browse_image = ttk.Button(self.root, text="Select Image", command=self.select_image)
        button_browse_image.grid(row=1, column=0, pady=(10, 10))



        button_remove_bg = ttk.Button(self.root, text="Remove Background", command=self.remove_background)
        button_remove_bg.grid(row=1, column=2, pady=(10, 10))

        button_apply_grabcut = ttk.Button(self.root, text="Apply GrabCut", command=self.apply_grabcut)
        button_apply_grabcut.grid(row=1, column=3, pady=(10, 10))

        # Adiciona eventos de mouse para a seleção do retângulo
        self.canvas.bind("<ButtonPress-1>", self.on_rect_start)
        self.canvas.bind("<B1-Motion>", self.on_rect_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_rect_end)

    def select_image(self):
        # Limpa os dados existentes ao selecionar uma nova imagem
        self.reset()
        
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            self.original_img = image
            self.display_image(image, self.canvas)

    def reset(self):
        # Limpa os dados existentes
        self.original_img = None
        self.processed_img = None
        self.background_img = None
        self.rect_start_x = None
        self.rect_start_y = None
        self.rect_end_x = None
        self.rect_end_y = None
        self.canvas.delete("rect")  # Limpa o retângulo no canvas



    def remove_background(self):
        if self.original_img:
            processed_img = remove(self.original_img)
            self.processed_img = processed_img
            self.display_image(processed_img, self.canvas)

    def apply_grabcut(self):
        

            print("Applying GrabCut2")
            # Converte a imagem original para formato OpenCV
            img_cv2 = np.array(self.original_img)
            img_cv2 = cv2.cvtColor(np.array(self.original_img), cv2.COLOR_RGBA2BGR)  # Converte RGBA para BGR

            # Aplica o GrabCut na imagem original
            mask = np.zeros(img_cv2.shape[:2], np.uint8)

            rect = (
                int(self.rect_start_x),
                int(self.rect_start_y),
                int(self.rect_end_x - self.rect_start_x),
                int(self.rect_end_y - self.rect_start_y),
            )

            modeloFundo = np.zeros((1, 65), np.float64)
            modeloObjeto = np.zeros((1, 65), np.float64)

            # Invoca o GrabCut
            cv2.grabCut(img_cv2, mask, rect, modeloFundo, modeloObjeto, 5, cv2.GC_INIT_WITH_RECT)
            
            #o 5 é o numero de iterações quanto maior as iterações mais chances tem de melhorar
            #o GC_INIT_WITH_RECT é o modo de inicialização do grabcut, nesse caso é com um retangulo
        
            #valor 0 -> posição é fundo
            #valor 1 -> pregião faz parte do objeto final
            #valor 2 -> região é provavelmente fundo
            #valor 3 -> região é provavelmente objeto
            
            # cria uma mascara para a imagem
            # np.where -> troca os valores -> se a posição da máscara for 2 ou 0, então o valor é 0, se não é 1 
            # converte pra inteiro de 8 bits
            mask_final = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
            # tornando o mask em 3 canais de cores
            # Aplica a máscara à imagem original
            img_final = img_cv2 * mask_final[:, :, np.newaxis]

            for x in range(0, img_cv2.shape[0]):
                for y in range(0, img_cv2.shape[1]):
                    if mask_final[x, y] == 0:
                        img_final[x][y][0] = img_final[x][y][1] = img_final[x][y][2] = 255

            # Converte a imagem final para o formato RGB
            img_final = cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB)

            # Converte a imagem final para o formato PIL
            img_final_pil = Image.fromarray(img_final)

            # Exibe a imagem final na tela
            self.display_output_image(img_final_pil)

            # Atualiza o canvas principal
            self.display_image(img_final_pil, self.canvas)
            
    


    def display_image(self, img, target):
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        target.configure(width=300, height=300)
        target.create_image(0, 0, anchor="nw", image=img_tk)
        target.image = img_tk

    def display_output_image(self, img):
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.output_label.configure(image=img_tk)
        self.output_label.image = img_tk


    def on_rect_start(self, event):
        # Inicia as coordenadas do retângulo
        self.rect_start_x = event.x
        self.rect_start_y = event.y

    def on_rect_drag(self, event):
        # Atualiza as coordenadas do retângulo enquanto arrasta o mouse
        self.rect_end_x = event.x
        self.rect_end_y = event.y
        # Redesenha o retângulo
        self.canvas.delete("rect")
        self.canvas.create_rectangle(
            self.rect_start_x, self.rect_start_y, self.rect_end_x, self.rect_end_y, outline="blue", tags="rect"
        )

    def on_rect_end(self, event):
        # Faz algo quando o botão do mouse é liberado após arrastar o retângulo
        pass

def main():
    window = tk.Tk()
    window.title("Image Processor")

    style = ttk.Style()
    style.configure("TButton", padding=(10, 5), font=("Helvetica", 12), background="#4CAF50", foreground="black")
    style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", padding=(10, 5), anchor="w")
    style.configure("TEntry", font=("Helvetica", 12), padding=(10, 5))
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TCheckbutton", background="#f0f0f0")

    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, padx=20, pady=20)

    canvas = tk.Canvas(frame, relief="solid", borderwidth=1, width=400, height=300)
    output_label = ttk.Label(frame, style="TLabel", relief="solid", borderwidth=1)

    image_processor = ImageProcessor(window, canvas, output_label)

    window.mainloop()

if __name__ == "__main__":
    main()
