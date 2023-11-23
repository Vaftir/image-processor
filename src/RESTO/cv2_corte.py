import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from rembg import remove

class ImageCropper:
    def __init__(self, root, original_image_canvas, output_image_label, on_crop_callback):
        self.root = root
        self.original_image_canvas = original_image_canvas
        self.output_image_label = output_image_label
        self.on_crop_callback = on_crop_callback
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        self.original_img = None

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

        # Remove the previous rectangle, if any
        if self.rect_id:
            self.original_image_canvas.delete(self.rect_id)

    def crop_drag(self, event):
        cur_x = self.original_image_canvas.canvasx(event.x)
        cur_y = self.original_image_canvas.canvasy(event.y)

        # Remove the previous rectangle, if any
        if self.rect_id:
            self.original_image_canvas.delete(self.rect_id)

        # Draw the new rectangle
        self.rect_id = self.original_image_canvas.create_rectangle(
            self.start_x, self.start_y, cur_x, cur_y, outline="red"
        )

    def end_crop(self, event):
        if self.start_x is not None and self.start_y is not None:
            # Convert coordinates to integers
            x1, y1, x2, y2 = map(int, (self.start_x, self.start_y, event.x, event.y))

            # Ensure x2 and y2 are greater than x1 and y1
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Draw the final rectangle
            self.original_image_canvas.create_rectangle(
                x1, y1, x2, y2, outline="red"
            )

            # Perform background removal on the selected area
            self.on_crop_callback(x1, y1, x2, y2, self)

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

def remove_background(x1, y1, x2, y2, image_cropper):
    try:
        # Crop the selected area
        cropped_image = image_cropper.original_img.crop((x1, y1, x2, y2))

        # Perform background removal on the cropped image
        img_removed_bg = remove(cropped_image)

        # Save processed image
        img_removed_bg.save("output.png")
        print("Background removed successfully. Output saved to output.png")

        # Display the processed image
        image_cropper.display_output_image(img_removed_bg)

    except Exception as e:
        print(f"Error: {e}")

def select_image(image_cropper):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = Image.open(file_path)
        image_cropper.original_img = image
        image_cropper.display_original_image(image)

def main():
    window = tk.Tk()
    window.title("Remove Background App")

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
    label_output_image = ttk.Label(frame, style="TLabel", relief="solid", borderwidth=1)

    button_process = ttk.Button(frame, text="Remover Fundo", command=lambda: remove_background(image_cropper.start_x, image_cropper.start_y, image_cropper.end_x, image_cropper.end_y, image_cropper), style="TButton")
    button_process.grid(row=6, column=0, columnspan=2, pady=10)

    image_cropper = ImageCropper(window, canvas_original_image, label_output_image, remove_background)

    button_browse = ttk.Button(frame, text="Procurar", command=lambda: select_image(image_cropper), style="TButton")
    button_browse.grid(row=1, column=0)

    window.mainloop()

if __name__ == "__main__":
    main()
