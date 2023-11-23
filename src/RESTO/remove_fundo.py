import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from rembg import remove


 
# Versão python tem que ser maior 3.7 ou menor 3.12
# recortar tirar funco e colocar


# pythin version 
# pip install pillow
# pip install rembg
#pip install ttkthemes
#u2-net: u square net

def remove_background(image_path, output_path):
    try:
        # Open image
        img = Image.open(image_path)

        # Remove background
        img_removed_bg = remove(img)

        # Save processed image
        img_removed_bg.save(output_path)
        print(f"Background removed successfully. Output saved to {output_path}")

        # Display the processed image
        display_image(img_removed_bg, label_processed_image)
        
    except Exception as e:
        print(f"Error: {e}")

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)

        # Display the selected image
        original_img = Image.open(file_path)
        display_image(original_img, label_original_image)

def display_image(img, label):
    img.thumbnail((300, 300))  # Resize image for display
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

# Criar a janela principal
window = tk.Tk()
window.title("Remove Background App")

# Criar estilo temático
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font=("Helvetica", 12), background="#4CAF50", foreground="black")
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", padding=(10, 5), anchor="w")
style.configure("TEntry", font=("Helvetica", 12), padding=(10, 5))
style.configure("TFrame", background="#f0f0f0")
style.configure("TCheckbutton", background="#f0f0f0")

# Configurar widgets
frame = ttk.Frame(window)
frame.grid(row=0, column=0, padx=20, pady=20)

label_instruction = ttk.Label(frame, text="Selecione uma imagem:", style="TLabel")
label_instruction.grid(row=0, column=0, columnspan=2, pady=(0, 10))

entry_path = ttk.Entry(frame, width=40, style="TEntry")
entry_path.grid(row=1, column=0, padx=(0, 10))

button_browse = ttk.Button(frame, text="Procurar", command=select_image, style="TButton")
button_browse.grid(row=1, column=1)

label_original_image_text = ttk.Label(frame, text="Imagem Original:", style="TLabel")
label_original_image_text.grid(row=2, column=0, pady=(10, 5), sticky="w")

label_original_image = ttk.Label(frame, style="TLabel")
label_original_image.grid(row=3, column=0, pady=10, columnspan=2)

label_processed_image_text = ttk.Label(frame, text="Imagem Processada:", style="TLabel")
label_processed_image_text.grid(row=4, column=0, pady=(10, 5), sticky="w")

label_processed_image = ttk.Label(frame, style="TLabel")
label_processed_image.grid(row=5, column=0, pady=10, columnspan=2)

button_process = ttk.Button(frame, text="Remover Fundo", command=lambda: remove_background(entry_path.get(), "output.png"), style="TButton")
button_process.grid(row=6, column=0, columnspan=2, pady=10)

# Iniciar o loop principal da interface gráfica
window.mainloop()
