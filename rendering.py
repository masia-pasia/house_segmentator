import torch
import torch.nn.functional as F
from monai.networks.nets import UNet
from monai.transforms import (Compose, LoadImage, EnsureChannelFirst, Resize,
                              ToTensor, ScaleIntensityRange)
from segmentator import HouseSegmentator


class RemoveAlphaChannel:
    def __call__(self, img):
        if img.shape[2] == 4:  # Sprawdza czy obraz ma 4 kanały (RGBA)
            img = img[..., :3]  # Usuwa alfa-kanał
        return img


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
        RemoveAlphaChannel(),
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

    model = HouseSegmentator.load_from_checkpoint(checkpoint, model=model, lr=config.LEARNING_RATE,
                                                  config=config)  # model załadowany z checkpointu
    model.eval()  # tryb ewaluacji żeby wagi były stałe i nie trenował się dalej na obrazkach od użytkownika

    with torch.no_grad():
        outs = model(X)  # output modelu
        probs = F.softmax(outs, dim=1)  # prawdopodobieństwa
        preds = torch.argmax(probs, dim=1).detach().cpu()  # predykcje - maska (labelka)

    preds = preds.type(torch.uint8)  # maska
    return preds
