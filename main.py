import cv2
import numpy as np
import matplotlib.pyplot as plt
import rendering

# TODO - zawrzeć poniższe w funkcję, która jako argumenty przyjmuje z fronta filepath, alphę (przeskalowane 0-1),
#  kolor (najlepiej jako tablicę 3 elementową 0-255) i co chcemy pokolorować
# TODO - kompletnie przeformatować plik, zmienić nazwy i język, tragedia
# TODO - zrobić odpowiednią maskę zależnie od wybranego segmentu


def add_mask(img_path, alpha, color, segment):
    img = cv2.imread(img_path)
    mask = rendering.process_image(img_path)
    kanaly = cv2.split(mask)
    maska = np.zeros_like(kanaly[0], dtype=np.uint8)
    maska = cv2.bitwise_or(maska, kanaly[0])

    _, maska_binarna_1 = cv2.threshold(maska, 0, 255, cv2.THRESH_BINARY)
    _, maska_binarna_2 = cv2.threshold(maska, 1, 255, cv2.THRESH_BINARY)
    _, maska_binarna_3 = cv2.threshold(maska, 2, 255, cv2.THRESH_BINARY)

    maska_dach = maska_binarna_1 - maska_binarna_2
    maska_okno = maska_binarna_2 - maska_binarna_3
    maska_drzwi = maska_binarna_3

    img_with_mask = np.copy(img)
    img_with_mask[(maska_okno == 255)] = [180, 0, 255]
    # przezroczystosc = 0.25
    # maska_okno = maska_okno.astype(np.uint8)
    img_with_mask = cv2.addWeighted(img_with_mask, alpha, img, 1.0 - alpha, 0)
    # img_with_mask = cv2.cvtColor(img_with_mask, cv2.COLOR_BGRA2BGR)

    # fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    # ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # ax[1].imshow(cv2.cvtColor(img_with_mask, cv2.COLOR_BGR2RGB))
    # plt.show()
    return img_with_mask
