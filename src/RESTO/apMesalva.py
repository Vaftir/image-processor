import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from PIL import ImageDraw
from rembg import remove


class ImageProcessor:
    def __init__(self, root, original_image_canvas, output_image_label):
        self.root = root
        self.original_image_canvas = original_image_canvas
        self.output_image_label = output_image_label
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.original_img = None
        self.image_with_rectangle = None
        self.cropped_img = None

        self.create_widgets()

    def create_widgets(self):
        self.label_original_image_text = ttk.Label(self.root, text="Imagem Original:", style="TLabel")
        self.label_original_image_text.grid(row=2, column=0, pady=(10, 5), sticky="w")

        self.label_output_image_text = ttk.Label(self.root, text="Imagem de Saída:", style="TLabel")
        self.label_output_image_text.grid(row=4, column=0, pady=(10, 5), sticky="w")

        self.original_image_canvas.grid(row=3, column=0, pady=10, columnspan=2)
        self.output_image_label.grid(row=5, column=0, pady=10, columnspan=2)

        self.original_image_canvas.bind("<ButtonPress-1>", self.start_crop)
        self.original_image_canvas.bind("<B1-Motion>", self.crop_drag)
        self.original_image_canvas.bind("<ButtonRelease-1>", self.end_crop)

    def start_crop(self, event):
        self.start_x = self.original_image_canvas.canvasx(event.x)
        self.start_y = self.original_image_canvas.canvasy(event.y)

    def crop_drag(self, event):
        cur_x = self.original_image_canvas.canvasx(event.x)
        cur_y = self.original_image_canvas.canvasy(event.y)

        # Remove the previous rectangle, if any
        self.original_image_canvas.delete("rectangle")

        # Draw the new rectangle
        self.original_image_canvas.create_rectangle(
            self.start_x, self.start_y, cur_x, cur_y, outline="red", tags="rectangle"
        )

    def end_crop(self, event):
        if self.start_x is not None and self.start_y is not None:
            # Convert coordinates to integers
            self.end_x = self.original_image_canvas.canvasx(event.x)
            self.end_y = self.original_image_canvas.canvasy(event.y)

            # Ensure end_x and end_y are greater than start_x and start_y
            self.end_x, self.start_x = max(self.end_x, self.start_x), min(self.end_x, self.start_x)
            self.end_y, self.start_y = max(self.end_y, self.start_y), min(self.end_y, self.start_y)

            # Draw the final rectangle
            self.original_image_canvas.create_rectangle(
                self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="rectangle"
            )

            # Create an image with the rectangle drawn
            img_copy = self.original_img.copy()
            draw = ImageDraw.Draw(img_copy)
            draw.rectangle([self.start_x, self.start_y, self.end_x, self.end_y], outline="red")

            self.image_with_rectangle = img_copy

    def save_image_with_rectangle(self):
        if self.image_with_rectangle:
            self.image_with_rectangle.save("ret.jpg")
            print("Imagem com retângulo salva como ret.jpg")

    def crop_image(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            # Convert coordinates to integers
            x1, y1, x2, y2 = map(int, (self.start_x, self.start_y, self.end_x, self.end_y))

            # Ensure x2 and y2 are greater than x1 and y1
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Crop the image
            self.cropped_img = self.original_img.crop((x1, y1, x2, y2))
            self.cropped_img.save("cropped.jpg")
            print("Imagem cortada salva como cropped.jpg")

    def remove_background_with_rectangle(self):
        if self.image_with_rectangle:
            self.remove_background("ret.jpg")

    def remove_background_cropped(self):
        if self.cropped_img:
            self.remove_background("cropped.jpg")

    def remove_background(self, image_path):
        try:
            img = Image.open(image_path)
            img_removed_bg = remove(img)

            # Save processed image
            img_removed_bg.save("output.png")
            print(f"Background removed successfully. Output saved to output.png")

            # Display the processed image
            self.display_output_image(img_removed_bg)

        except Exception as e:
            print(f"Error: {e}")

    def display_original_image(self, img):
        img.thumbnail((300, 300))  # Resize image for display
        img_tk = ImageTk.PhotoImage(img)
        self.original_image_canvas.config(width=img_tk.width(), height=img_tk.height())
        self.original_image_canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.original_image_canvas.image = img_tk

    def display_output_image(self, img):
        img.thumbnail((300, 300))  # Resize image for display
        img_tk = ImageTk.PhotoImage(img)
        self.output_image_label.config(image=img_tk)
        self.output_image_label.image = img_tk

def select_image(image_processor):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = Image.open(file_path)
        image_processor.original_img = image
        image_processor.display_original_image(image)

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

    label_instruction = ttk.Label(frame, text="Selecione uma imagem:", style="TLabel")
    label_instruction.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    canvas_original_image = tk.Canvas(frame, relief="solid", borderwidth=1)
    output_image_label = ttk.Label(frame, style="TLabel", relief="solid", borderwidth=1)

    image_processor = ImageProcessor(window, canvas_original_image, output_image_label)

    button_browse = ttk.Button(frame, text="Procurar", command=lambda: select_image(image_processor), style="TButton")
    button_browse.grid(row=1, column=0)

    button_save_image_with_rectangle = ttk.Button(frame, text="Salvar com Retângulo", command=image_processor.save_image_with_rectangle, style="TButton")
    button_save_image_with_rectangle.grid(row=2, column=0, pady=(10, 0))

    button_crop_image = ttk.Button(frame, text="Cortar Imagem", command=image_processor.crop_image, style="TButton")
    button_crop_image.grid(row=3, column=0, pady=(10, 0))

    button_remove_bg_with_rect = ttk.Button(frame, text="Remover Fundo (com Retângulo)", command=image_processor.remove_background_with_rectangle, style="TButton")
    button_remove_bg_with_rect.grid(row=4, column=0, pady=(10, 0))

    button_remove_bg_cropped = ttk.Button(frame, text="Remover Fundo (cortada)", command=image_processor.remove_background_cropped, style="TButton")
    button_remove_bg_cropped.grid(row=5, column=0, pady=(10, 0))

    window.mainloop()

if __name__ == "__main__":
    main()
