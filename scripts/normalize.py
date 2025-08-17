# Script to calculate the normalization values (mean and standard deviation) of an image dataset for unet training
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch

# Temporary dataset to obtain statistics
transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor()
])

dataset = datasets.ImageFolder("dataset/images", transform=transform)
loader = DataLoader(dataset, batch_size=10)

mean = 0.
std = 0.
for images, _ in loader:
    mean += images.mean([0, 2, 3])
    std += images.std([0, 2, 3])
mean /= len(loader)
std /= len(loader)

print(f"Media: {mean}")
print(f"Desviación estándar: {std}")
