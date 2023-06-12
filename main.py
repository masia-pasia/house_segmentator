import cv2
import numpy as np
import matplotlib.pyplot as plt
#import pyqt5




mask = cv2.imread('mask.png')
img = cv2.imread('img.jpg')

# Wyodrębnij kanały obrazu
kanaly = cv2.split(mask)

# Inicjalizuj pustą maskę
maska = np.zeros_like(kanaly[0], dtype=np.uint8)

# Wybierz kanały, które chcesz użyć do utworzenia maski
#indeksy_kanalow = [0, 1, 2]  # Indeksy kanałów, które mają zostać użyte (liczone od zera)

# Utwórz maskę na podstawie wybranych kanałów
#for indeks in indeksy_kanalow:
maska = cv2.bitwise_or(maska, kanaly[0])


# Progowanie maski
_, maska_binarna_1 = cv2.threshold(maska, 0, 255, cv2.THRESH_BINARY)
_, maska_binarna_2 = cv2.threshold(maska, 1, 255, cv2.THRESH_BINARY)
_, maska_binarna_3 = cv2.threshold(maska, 2, 255, cv2.THRESH_BINARY)

maska_dach = maska_binarna_1 - maska_binarna_2
maska_okno = maska_binarna_2 - maska_binarna_3
maska_drzwi = maska_binarna_3

# copy where we'll assign the new values
img_with_mask = np.copy(img)
# boolean indexing and assignment based on mask
img_with_mask[(maska_okno == 255)] = [180, 0, 255]

img_with_mask = cv2.addWeighted(img_with_mask, 0.8, img, 0.7, 0, img_with_mask)

fig, ax = plt.subplots(1,2,figsize=(12,6))
ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
ax[1].imshow(cv2.cvtColor(img_with_mask, cv2.COLOR_BGR2RGB))
plt.show()



# Wyświetl wynikową maskę
# cv2.imshow('Maska', maska_binarna)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
