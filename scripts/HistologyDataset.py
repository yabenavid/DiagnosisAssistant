from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T
import numpy as np

class HistologyDataset(Dataset):
    def __init__(self, image_paths, mask_paths, transform=None, size=(512, 512)):
        self.image_paths = image_paths
        self.mask_paths = mask_paths
        self.size = size
        self.transform = transform or T.Compose([
            T.Resize((512, 512)),
            T.ToTensor(),
            T.Normalize(mean=[0.8896, 0.7711, 0.9064],
                        std=[0.1091, 0.1464, 0.0761])
        ])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = Image.open(self.image_paths[idx]).convert("RGB").resize(self.size, Image.BILINEAR)
        mask = Image.open(self.mask_paths[idx]).convert("L").resize(self.size, Image.NEAREST)

        image = self.transform(image)
        mask = T.ToTensor()(mask)
        mask = (mask > 0.5).float()

        return image, mask
