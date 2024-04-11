import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import random

def text_to_image(text, font_path, font_size, image_path): # funkcja dla zapisywania tekstu jako obraz
    margin = 10
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text) # obliczamy rozmiary obrazu i robimy jego rozmiary takimi samymi
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    square_size = max(width, height) + 2 * margin
    image = Image.new('RGB', (square_size, square_size), color='white')
    draw = ImageDraw.Draw(image)
    text_position = ((square_size - width) // 2, (square_size - height) // 2)
    draw.text(text_position, text, font=font, fill='black')
    image.save(image_path)


def load_image(image_path): #odczytanie obrazu
    with Image.open(image_path) as img:
        img_bw = img.convert('L').point(lambda x: 0 if x < 128 else 1, '1')
        return np.array(img_bw)


def generate_shares(input_image):
    height, width = input_image.shape
    share1 = np.zeros((height * 4, width * 4), dtype=np.uint8)
    share2 = np.zeros((height * 4, width * 4), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            pattern = np.random.randint(0, 2, (4, 4))

            if input_image[i, j] == 1:
                share1[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = pattern
                share2[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = 1 - pattern
            else:
                share1[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = pattern
                share2[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = pattern

    return share1, share2


def overlay_shares(share1, share2):
    decrypted = np.zeros((len(share1) * 4, len(share1) * 4), dtype=np.uint8)
    for i in range(len(share1)):
        for j in range(len(share2)):
            if share1[i][j] == share2[i][j]:
                decrypted[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = 1
            else:
                decrypted[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4] = 0
    return decrypted

#def overlay_shares(share1, share2):
#    return np.bitwise_or(share1, share2)

if __name__ == "__main__":
    print("Wpisz tekst wejsćiowy:", end=" ")
    text = input()

    #text = text.replace(' ', '\n')
    font_path = 'arial.ttf'
    font_size = 24
    image_path = 'Obraz_wejsciowy.png'
    text_to_image(text, font_path, font_size, image_path)

    input_image = load_image(image_path) #Odczytanie zapisanego orbazu

    share1, share2 = generate_shares(input_image)

    plt.figure(figsize=(15 ,5 )) # Jako wynik są obrazy: Udział_1, Udział_2 i Obraz_Wyjsciowy

    plt.subplot(1, 3, 1)
    plt.imshow(share1, cmap='gray', interpolation='none')
    plt.title('Udział 1')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(share2, cmap='gray', interpolation='none')
    plt.title('Udział 2')
    plt.axis('off')

    overlayed_shares = overlay_shares(share1, share2)
    plt.subplot(1, 3, 3)
    plt.imshow(overlayed_shares, cmap='gray', interpolation='none')
    plt.title('Obraz wyjsciowy')
    plt.axis('off')

    plt.tight_layout()
    plt.show()
