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
        self.create_widgets()

    def create_widgets(self):
        self.canvas.grid(row=0, column=0, padx=20, pady=20)
        self.output_label.grid(row=0, column=1, padx=20, pady=20)

        button_browse_image = ttk.Button(self.root, text="Select Image", command=self.select_image)
        button_browse_image.grid(row=1, column=0, pady=(10, 10))

        button_browse_background = ttk.Button(self.root, text="Select Background", command=self.select_background)
        button_browse_background.grid(row=1, column=1, pady=(10, 10))

        button_remove_bg = ttk.Button(self.root, text="Remove Background", command=self.remove_background)
        button_remove_bg.grid(row=1, column=2, pady=(10, 10))

        button_change_background = ttk.Button(self.root, text="Change Background", command=self.apply_grabcut)
        button_change_background.grid(row=1, column=3, pady=(10, 10))

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            self.original_img = image
            self.display_image(image, self.canvas)

    def select_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            background_img = Image.open(file_path)
            self.background_img = background_img

    def remove_background(self):
        if self.original_img:
            processed_img = remove(self.original_img)
            self.processed_img = processed_img
            self.display_image(processed_img, self.canvas)

    def apply_grabcut(self):
        if self.original_img and self.background_img:
            # Converte a imagem original para formato OpenCV
            img_cv2 = np.array(self.original_img)

            # Aplica o GrabCut na imagem original
            mask = np.zeros(img_cv2.shape[:2], np.uint8)

            rect = (int(self.start_x), int(self.start_y), int(self.end_x - self.start_x), int(self.end_y - self.start_y))

            modeloFundo = np.zeros((1, 65), np.float64)
            modeloObjeto = np.zeros((1, 65), np.float64)

            # Invoca o GrabCut
            cv2.grabCut(img_cv2, mask, rect, modeloFundo, modeloObjeto, 5, cv2.GC_INIT_WITH_RECT)

            # Cria uma máscara para a imagem
            mask_final = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

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
        self.output_label.configure(width=300, height=300)
        self.output_label.create_image(0, 0, anchor="nw", image=img_tk)
        self.output_label.image = img_tk

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
