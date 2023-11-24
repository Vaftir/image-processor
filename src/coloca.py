# Importando as bibliotecas
import glob
import os
from PIL import Image

# Caminho com as imgens das artes
art_path = 'imagens/'
# Caminho onde as imagens geradas serão salvas
art_new_path = 'imagens/art_background/'
#Caminho onde está a imgem de background
background = 'src/elden-ring-maliketh-4k-wallpaper-uhdpaper.com-259@1@g.jpg'

# Carregar imagem original e mostrar seu tamanho
original_background = Image.open(background)
print(original_background.size)
Image.open(background)
background_image = original_background.copy()
# Redimensionamento do background em números absolutos
background_resized = background_image.resize((400, 600))
# Criar cópia da imagem redimensionada para não sobrescrever a imagem original
new_background = background_resized.copy()
# Salvar imagem redimensionada
background_resized.save('new_background.jpg')
# Carregar imagem e mostrar seu tamanho após redimensionamento
print(background_resized.size)
Image.open('new_background.jpg')



# ... (rest of your code)

for art in glob.glob(art_path + '*.jpg'):
    # Pegar apenas o nome do arquivo
    art_name = os.path.basename(art)
    # Abrir a imagem da arte
    art_image = Image.open(art)
    # Redimensionar o tamanho da arte em números absolutos
    art_resized = art_image.resize((150, 100))
    
    # Verificar se a imagem tem um canal alfa (transparência)
    if 'A' in art_resized.getbands():
        # Criar uma imagem preta um pouco maior que a imagem original para fazer a função de moldura
        border = Image.new('RGBA', (160, 110), color=(0, 0, 0, 0))  # Usar 'RGBA' para transparência 
        # Extrair a máscara de transparência da imagem redimensionada
        mask = art_resized.split()[3]
        # Criar cópia da imagem
        art_border = border.copy()
        # Colar a imagem da arte sobre a moldura com preservação de transparência usando a máscara
        art_border.paste(art_resized, (5, 5), mask=mask)
    else:
        # Se não houver um canal alfa, usar uma borda sem transparência
        border = Image.new('RGB', (160, 110), color=(0, 0, 0))
        # Criar cópia da imagem
        art_border = border.copy()
        # Colar a imagem da arte sobre a moldura sem transparência
        art_border.paste(art_resized, (5, 5))
    
    # Criar cópia da imagem
    art_background = background_resized.copy()
    
    # Colar a parte interna da imagem da arte sem a borda sobre o background
    art_background.paste(art_resized, (122, 227))
    
    # Salvar imagem no caminho de saída
    art_background.save(art_new_path + 'arte_exposta - ' + art_name)

print('Processo completo')