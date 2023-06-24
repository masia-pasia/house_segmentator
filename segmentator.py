import pytorch_lightning as pl
from torch.optim import Adam

from monai.losses import DiceLoss


class HouseSegmentator(pl.LightningModule):
    def __init__(self, model, lr, config):
        super(HouseSegmentator, self).__init__()
        self.model = model

        self.lr = lr
        self.config = config

        self.loss = DiceLoss(include_background=False,  # calculate loss over background
                             softmax=True,  # k>2 classes (out_channels)
                             sigmoid=False,  # 2 classes (out_channels)
                             to_onehot_y=True,
                             )

    def forward(self, inputs):
        outputs = self.model(inputs)
        return outputs

    def training_step(self, batch, batch_idx):
        X, y = batch['img'], batch['seg']
        y_hat = self.model(X)
        loss = self.loss(y_hat, y)

        self.log_dict({'train_loss': loss}, on_epoch=True, on_step=False)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch['img'], batch['seg']
        y_hat = self(x)

        loss = self.loss(y_hat, y)
        self.log_dict({'val_loss': loss}, on_epoch=True, on_step=False, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        # TODO: model test step
        pass

    def configure_optimizers(self):
        optimizer = Adam(self.parameters(), lr=self.lr)
        return optimizer
