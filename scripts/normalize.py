# Script para calcular los valores de normalización (media y desviación estándar) de un dataset de imágenes para el entrenamiento de unet
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch

# Dataset temporal para obtener estadísticas
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
