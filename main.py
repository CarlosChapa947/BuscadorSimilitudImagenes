from google_images_download import google_images_download
import os
import cv2
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def calcular_histograma(imagen):
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    histograma = cv2.calcHist([imagen_gris], [0], None, [256], [0, 256])

    return histograma

def comparar_histogramas(hist1, hist2):
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)


def download_google_images(query, num_images=50, save_path="downloads"):
    os.makedirs(save_path, exist_ok=True)
    images_downloaded = 0
    page_num = 1

    while images_downloaded < num_images:
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&start={page_num * 20}"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')
            for img_tag in img_tags:

                if images_downloaded >= num_images:
                    break

                img_url = img_tag.get('src')
                if img_url:
                    try:
                        response = requests.get(img_url)
                        if response.status_code == 200:
                            with open(os.path.join(save_path, f"{query}_{images_downloaded}.jpg"), 'wb') as f:
                                f.write(response.content)
                            images_downloaded += 1
                    except Exception as e:
                        print(f"Error downloading image {images_downloaded}: {str(e)}")

        page_num += 1


def dowloadimages(keywords, format="png", limit=2, printUrl=True, size="large", aspectRatio="wide", outputDirectory="./Images/"):
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": keywords,
                 "format": format,
                 "limit": limit,
                 "print_urls": printUrl,
                 "size": size,
                 "aspect_ratio": aspectRatio,
                 "output_directory": outputDirectory}
    try:
        response.download(arguments)

    except FileNotFoundError:
        arguments = {"keywords": keywords,
                     "format": format,
                     "limit": limit,
                     "print_urls": printUrl,
                     "size": size}

        try:
            response.download(arguments)
        except:
            pass


if __name__ == '__main__':

    keyword = "cocacola"
    download_google_images(keyword, num_images=50, save_path="./Images/")

    directorio_imagenes = "./Images/"

    imagen_base = cv2.imread(os.path.join(directorio_imagenes, f"{keyword}_0.jpg"))
    histograma_base = calcular_histograma(imagen_base)

    similitudes = []

    for i in range(1, 50):
        imagen_actual = cv2.imread(os.path.join(directorio_imagenes, f"{keyword}_{i}.jpg"))
        histograma_actual = calcular_histograma(imagen_actual)

        similitud = comparar_histogramas(histograma_base, histograma_actual)
        similitudes.append((f"{keyword}_{i}.jpg", similitud))

    similitudes.sort(key=lambda x: x[1], reverse=True)

    for nombre_imagen, similitud in similitudes:
        print(f"Nombre de la imagen: {nombre_imagen}, Similitud: {similitud:.2f}")
        imagen_mostrar = cv2.imread(os.path.join(directorio_imagenes, nombre_imagen))
        cv2.imshow(nombre_imagen, imagen_mostrar)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
