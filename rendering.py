from segmentator import HouseSegmentator
import torch
import matplotlib.pyplot as plt
import numpy as np
import torch.nn.functional as F
import front
import os
import glob

import random
import pytorch_lightning as pl

from monai.transforms import (Compose, LoadImage, EnsureChannelFirst, Resize,
                              ScaleIntensityRange, ToTensor, ScaleIntensityRange, Rotate90)
from monai.transforms import KeepLargestConnectedComponent, RemoveSmallObjects, FillHoles, AsDiscrete, Activations

from monai.utils import set_determinism
from sklearn.model_selection import train_test_split
from monai.data import CacheDataset, DataLoader
from monai.networks.nets import UNet

#paths = glob.glob("**/house (1).jpg", recursive=True)  # ścieżki do obrazków od użytkownika


def process_image(img_path):
    class config:
        DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
        LEARNING_RATE = 1e-3
        N_EPOCHS = 50
        BATCH = 2
        SPLIT = {'train': 0.8, 'val': 0.1, 'test': 0.1}
        DATAPATH = './segments/**/'
        NUM_WORKERS = 4
        IMAGE_SIZE = (1024, 1024)
        TRANSFORM = None

    config.TRANSFORM = Compose([
        LoadImage(image_only=True),
        EnsureChannelFirst(),
        Resize(spatial_size=config.IMAGE_SIZE),
        ScaleIntensityRange(a_min=0, a_max=255, b_min=0, b_max=1),
        ToTensor(dtype=torch.float32),
    ])

    checkpoint = './best_checkpoint-v1.ckpt'
    model = UNet(
        spatial_dims=2,
        in_channels=3,
        out_channels=3,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
        kernel_size=3,
        up_kernel_size=3,
        num_res_units=2,
        dropout=0.2,
        bias=True
    )
    X = config.TRANSFORM(img_path)  # transform ścieżka -> obraz
    X = X.unsqueeze(0)  # jeśli jest tylko jeden obraz to musimy dołożyć kanał na batch

    model = HouseSegmentator.load_from_checkpoint(checkpoint, model=model, lr=config.LEARNING_RATE, config=config)  # model załadowany z checkpointu
    model.eval()  # tryb ewaluacji żeby wagi były stałe i nie trenował się dalej na obrazkach od użytkownika

    with torch.no_grad():
        outs = model(X)  # output modelu
        probs = F.softmax(outs, dim=1)  # prawdopodobieństwa
        preds = torch.argmax(probs, dim=1).detach().cpu()  # predykcje - maska (labelka)

    imgs = ScaleIntensityRange(a_min=0, a_max=1, b_min=0, b_max=255)(X).permute(0, 2, 3, 1).type(torch.uint8)  # obrazek
    preds = preds.type(torch.uint8)  # maska
    return preds


process_image('C:\\Users\\szatk\\OneDrive\\Desktop\\std\\6sem\\projekt_zespolowy\\Zrzut ekranu 2023-06-12 234117.png')
# for idx in range(imgs.shape[0]):  # wyświetla dla każdego sampla w batchu
#     plt.figure(figsize=(20, 20))
#
#     plt.subplot(1, 2, 1)
#     plt.imshow(torch.rot90(imgs[idx], 3))  # obrazek
#
#     plt.subplot(1, 2, 2)
#     plt.imshow(torch.rot90(imgs[idx], 3))
#     plt.imshow(torch.rot90(preds[idx].squeeze(0), 3) * 100, alpha=0.5, cmap='gnuplot')  # maska z 50% przezroczystości
#
#     plt.show()
