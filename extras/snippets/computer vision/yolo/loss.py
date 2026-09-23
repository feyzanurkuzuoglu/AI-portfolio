import torch
import torch.nn as nn
from utils import intersection_over_union

class YoloLoss(nn.Module):
    def __init__(self, S=7, B=2, C=20):
        super(YoloLoss, self).__init__()
        self.S = S
        self.B = B
        self.C = C
        self.lambda_noobj = 0.5
        self.lambda_coord = 5

    def forward(self, predictions, target):
        predictions = predictions.reshape(-1, self.S, self.S, self.C + 5 * self.B)

        iou_b1 = intersection_over_union(predictions[..., 21:25], target[..., 21:25])
        iou_b2 = intersection_over_union(predictions[..., 26:30], target[..., 21:25])

        # unsqueeze(0), tensor'un ilk boyutuna (axis 0) bir boyut ekler. Eğer başlangıçta bir tensor'un şekli
        # (A, B, C) gibi ise, unsqueeze(0) işlemi sonrasında şekil (1, A, B, C) halini alır.
        # torch.cat() fonksiyonu, birden fazla tensor'ü belirtilen bir eksende birleştiren bir fonksiyondur.
        # dim=0 parametresi, tensor'leri ilk boyutta birleştireceğini belirtir (yani tensor'leri yukarıdan aşağıya birleştirir).
        ious = torch.cat([iou_b1.unsqueeze(0), iou_b2.unsqueeze(0)], dim=0)

        # torch.max fonksiyonu kullanılarak ious tensor'ü üzerinde maksimum değerin
        # ve bu değerin indeksinin hesaplanması işlemi yapılmaktadır.
        # dim=0 parametresi, işlemin satırlar arasında yapılacağını belirtir.
        # Bu, her sütundaki maksimum değeri bulmak anlamına gelir.
        iou_maxes, best_box = torch.max(ious, dim=0)

        # 1 veya 0 olacak depending on if there is an object on that cell
        # unsqueeze(3) fonksiyonu, 3. boyutta (yani 4. eksende) yeni bir boyut ekler.
        # Eğer target[..., 20] işlemi sonucu elde edilen tensor'ün şekli (A, B, C) ise,
        # unsqueeze(3) işlemi sonucu elde edilen tensor'ün şekli (A, B, C, 1) olur.
        # Bu, tensor'ün 4. eksende boyut ekler.
        exist_box = target[..., 20].unsqueeze(3) # identity of obj_i, for the identity part




        # LOCALIZATION LOSS (BOX COORDINATES)


        # İki tane tahminin olması, genellikle YOLO gibi nesne tespiti modellerinde çoklu kutu (bounding box)
        # tahminleri ve farklı anchor box'lar ile ilgilidir.
        box_predictions = exist_box * (
                best_box * predictions[..., 26:30] + (1 - best_box) * predictions[..., 21:25]
        )

        box_targets = exist_box * target[..., 21:25]


        # torch.sign:
        # Eğer eleman pozitifse, sonucu 1 olur.
        # Eğer eleman negatifse, sonucu -1 olur.
        # Eğer eleman sıfırsa, sonucu 0 olur.
        box_predictions[..., 2:4] = torch.sign(box_predictions[..., 2:4]) * torch.sqrt(
            torch.abs(box_predictions[..., 2:4] + 1e-6)
        )

        box_targets[..., 2:4] = torch.sqrt(box_targets[..., 2:4] + 1e-6)

        # (N,S,S,4) -> (N*S*S, 4)
        box_loss = self.mse(
            torch.flatten(box_predictions, end_dim=-2),
            torch.flatten(box_targets, end_dim=-2)

        )



        # OBJECT LOSS

        pred_box = (
            best_box * predictions[..., 25:26] + (1 - best_box) * predictions[..., 20:21]
        )

        # (N*S*S)
        object_loss = self.mse(
            torch.flatten(exist_box * pred_box),
            torch.flatten(exist_box * target[..., 20:21])
        )


        # NO OBJECT LOSS

        no_object_loss = self.mse(
            torch.flatten((1 - exist_box) * predictions[..., 20:21], start_dim=1),
            torch.flatten((1 - exist_box) * target[..., 20:21], start_dim=1)
        )

        no_object_loss += self.mse(
            torch.flatten((1 - exist_box) * predictions[..., 25:26], start_dim=1),
            torch.flatten((1 - exist_box) * target[..., 20:21], start_dim=1)
        )



        # CLASS LOSS


        # (N, S, S, 20) -> (N*S*S, 20)
        class_loss = self.mse(
            torch.flatten(exist_box * predictions[..., :20], end_dim=-2),
            torch.flatten(exist_box * target[..., :20], end_dim=-2)
        )

        loss =(
            self.lambda_coord * box_loss +
            object_loss +
            self.lambda_noobj * no_object_loss +
            class_loss
        )

        return loss





































