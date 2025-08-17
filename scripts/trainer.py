
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
from UNet import UNet
from HistologyDataset import HistologyDataset
from DiceLoss import BCEDiceLoss, dice_score
import glob

image_paths = sorted(glob.glob("dataset/images/*.png"))
mask_paths = sorted(glob.glob("dataset/masks/*.png"))

# Model, loss and optimizer
model = UNet()
criterion = BCEDiceLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Dataset and loader
train_dataset = HistologyDataset(image_paths, mask_paths)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)

# Early stopping
patience = 10
best_dice = 0
epochs_without_improvement = 0

# Training
for epoch in range(10):
    model.train()
    epoch_loss = 0
    epoch_dice = 0

    for images, masks in train_loader:
        preds = model(images)
        loss = criterion(preds, masks)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        with torch.no_grad():
            epoch_dice += dice_score(preds, masks).item()

    avg_loss = epoch_loss / len(train_loader)
    avg_dice = epoch_dice / len(train_loader)
    print(f"Epoch {epoch+1}: Loss = {avg_loss:.4f} | Dice = {avg_dice:.4f}")

    if avg_dice > best_dice:
        best_dice = avg_dice
        torch.save(model.state_dict(), "unet_stomach_cancer_best.pth")
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1
        print(f"Sin mejora en Dice por {epochs_without_improvement} época(s)")

    if epochs_without_improvement >= patience:
        print(f"Entrenamiento detenido por early stopping en la época {epoch+1}")
        break

torch.save(model.state_dict(), "unet_stomach_cancer_last.pth")
