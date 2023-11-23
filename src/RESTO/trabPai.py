import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog
import cv2
import numpy as np

# ESSE PYTHON APLICA MODELO DE CORREÇÃO DE FUNDO EM IMAGENS USANDO GAUSSIAN BLUR


class ImageProcessor(tk.Frame):
    def __init__(self, master = None):
        #INVOCA CONSTRTUTOR DA CLASSE PAI
        tk.Frame.__init__(self, master)
        
        #initializing the main window
        self.iniciaUI()
        
    def iniciaUI(self):
        self.master.title("Image Processor")
        self.pack()
        
        #computa ações do mouse
        self.computaAcoesDoMouse()
        
        #carregando imagem
        self.imagem = self.carregaImagemASerExibida()
        
        #criar um canvas para exibir a imagem
        self.canvas = tk.Canvas(self.master, width = self.imagem.width(), height = self.imagem.height(), cursor="cross")
        
        #desenhar a imagem no canvas
        self.canvas.create_image(0,0,anchor = "nw", image = self.imagem)
        self.canvas.image = self.imagem
        #posiciona todos os elementos
        self.canvas.pack()
    
    def computaAcoesDoMouse(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.retancleReady = None
        
        self.master.bind("<ButtonPress-1>", self.callbackBotaoPressionado)
        self.master.bind("<B1-Motion>", self.callbackBotaoPressionadoEmMovimento)
        self.master.bind("<ButtonRelease-1>", self.callbackBotaoSolto)
        
    
    def callbackBotaoSolto(self,event):
        if self.retancleReady:
            #cria uma nova janlea
            windowGrabcut = tk.Toplevel(self.master)
            windowGrabcut.wm_title("Segmentação de Imagem")
            windowGrabcut.minsize(width = self.imagem.width(), height = self.imagem.height())

            
            #cria canvas para exibir a imagem
            canvasGrabcut = tk.Canvas(windowGrabcut, width = self.imagem.width(), height = self.imagem.height())
            canvasGrabcut.pack()
            
            #aplicar o grabcut na imagem
            mask = np.zeros(self.imagemOpenCV.shape[:2], np.uint8)
            
            rect = (int(self.start_x), int(self.start_y), int(event.x - self.start_x), int(event.y - self.start_y))

            modeloFundo = np.zeros((1,65), np.float64) # matriz de zeros para representar o fundo
            modeloObjeto = np.zeros((1,65), np.float64) # matriz de zeros para representar o objeto
            
            #invoca o grabcut
            cv2.grabCut(self.imagemOpenCV, mask, rect, modeloFundo, modeloObjeto, 5, cv2.GC_INIT_WITH_RECT)
            
            #o 5 é o numero de iterações quanto maior as iterações mais chances tem de melhorar
            #o GC_INIT_WITH_RECT é o modo de inicialização do grabcut, nesse caso é com um retangulo
        
            #valor 0 -> posição é fundo
            #valor 1 -> pregião faz parte do objeto final
            #valor 2 -> região é provavelmente fundo
            #valor 3 -> região é provavelmente objeto
            
            # cria uma mascara para a imagem
            # np.where -> troca os valores -> se a posição da máscara for 2 ou 0, então o valor é 0, se não é 1 
            # converte pra inteiro de 8 bits
            maskFinal = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
            # tornando o mask em 3 canais de cores
            imagemFinal = self.imagemOpenCV * maskFinal[:,:,np.newaxis]
            
            for x in range(0, self.imagemOpenCV.shape[1]):
                for y in range(0, self.imagemOpenCV.shape[0]):
                    if(maskFinal[x,y] == 0):
                        imagemFinal[x][y][0] =  imagemFinal[x][y][1] = imagemFinal[x][y][2] = 255 # canal verde vermelho e azul vao pra branco
        
            #coverte opencv para tkinter
            imagemFinal = cv2.cvtColor(imagemFinal, cv2.COLOR_BGR2RGB)
            # convert the images to PIL format...
            imagemFinal = Image.fromarray(imagemFinal)
            imagemFinal = ImageTk.PhotoImage(imagemFinal)
            
            # inserindo a imagem no canvas
            canvasGrabcut.create_image(0,0,anchor = "nw", image = imagemFinal)
            canvasGrabcut.image = imagemFinal # tratando garbage collection
            
        
            
    
    def callbackBotaoPressionadoEmMovimento(self,event):
        #novas posições do mouse x e y 
        currentX = self.canvas.canvasx(event.x)
        currentY = self.canvas.canvasy(event.y)
        
        #atualiza o retangulo a ser desenhado
        self.canvas.coords(self.rect, self.start_x, self.start_y, currentX, currentY)
        
        #VERIFICA SE EXISTE UM RETANGULO
        self.retancleReady = True

    
    def callbackBotaoPressionado(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasx(event.y)
        
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0,0,0,0, outline="blue", tags="rectangle")
        
    def carregaImagemASerExibida(self):
        #carregando imagem
        caminhoDaimagem = filedialog.askopenfilename(title = "Select a File", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        
        #se a imagem existir
        if(caminhoDaimagem):
            self.imagemOpenCV = cv2.imread(caminhoDaimagem)
            
            #coverte opencv para PhotoImage
            image = cv2.cvtColor(self.imagemOpenCV, cv2.COLOR_BGR2RGB)
            # convert the images to PIL format...
            image = Image.fromarray(image)
            #convert to ImageTk format
            image = ImageTk.PhotoImage(image)
            #update the image in the frame
            return image
        
        
def main():
    # Create the root window
    root = tk.Tk()
    
    # Create the image processor object
    root = ImageProcessor(master = root)
    
    #loop the app
    root.mainloop()
    
    


if __name__ == "__main__":
    main()
