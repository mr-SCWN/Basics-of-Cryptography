from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt


def embed_watermark(image_path,key, n, d):
    # Wczytanie obrazu
    image = Image.open(image_path)
    original_pixels = np.array(image)
    modified_pixels = np.array(image)

    # Inicjalizacja generatora liczb pseudolosowych
    random.seed(key)

    # Wybór n par punktów
    for _ in range(n):
        x1, y1 = random.randint(0, image.width - 1), random.randint(0, image.height - 1)
        x2, y2 = random.randint(0, image.width - 1), random.randint(0, image.height - 1)

        # Zmiana jasności o d
        modified_pixels[y1, x1] = np.clip(modified_pixels[y1, x1] + d, 0, 255)
        modified_pixels[y2, x2] = np.clip(modified_pixels[y2, x2] - d, 0, 255)

    # Zapisanie zmodyfikowanego obrazu
    modified_image = Image.fromarray(modified_pixels)
    modified_image.save("watermarked_image.png")

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].imshow(original_pixels, cmap='gray')
    axes[0].set_title('Obraz wejściowy')
    axes[0].axis('off')

    axes[1].imshow(modified_pixels, cmap='gray')
    axes[1].set_title('Obraz wyjściowy (ze znakiem wodnym)')
    axes[1].axis('off')

    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.show()

    return "watermarked_image.png"



image_path = "obraz.png"
n = 1000                            # Wybieramy ilosc par punktow
d = 200                             # Zmiana jasnosci
key = int(input("Wpisz klucz: "))


embed_watermark(image_path, key,  n , d)