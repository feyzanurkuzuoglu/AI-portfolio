import torch
from collections import Counter
from IoUandNMS import intersection_over_unions

def mean_average_precision(
        pred_boxes, true_boxes, iou_threshold=0.5, box_format="corners", num_classes=20
        #yoloda 20 class olduğudan 20 yaptık
):
    # pred_boxes (list) : [[train_idx, class_pred, prob_score, x1, y1, x2, y2], ...]
    average_precisions = []
    epsilon = 1e-6

    for c in range(num_classes):
        detections = []
        ground_truth = []

        for detection in pred_boxes:
            if detection[1] == c:
                detections.append(detection)

        for true_box in true_boxes:
            if true_box[1] == c:
                ground_truth.append(true_box)

        # img 0 has 3 bboxes
        # img 1 has 5 bboxes
        # amount_bboxes = {0:3, 1:5}
        amount_bboxes = Counter([gt[0] for gt in ground_truth])

        for key, val in amount_bboxes.items():
            amount_bboxes[key] = torch.zeros(val)
        # amount_boxes = {0:torch.tensor([0,0,0]), 1:torch.tensor([0,0,0,0,0])}

        detections.sort(key=lambda x: x[2], reverse=True)
        TP = torch.zeros(len(detections))
        FP = torch.zeros(len(detections))
        total_true_boxes = len(ground_truth)

        for detection_idx, detection in enumerate(detections):
            ground_truth_img = [
                bbox for bbox in ground_truth if bbox[0] == detection[0]
            ]

            num_gts = len(ground_truth_img)
            best_iou = 0

            for idx, gt in enumerate(ground_truth_img):
                iou = intersection_over_unions(
                    torch.tensor(detection[3:]),
                    torch.tensor(gt[3:]),
                    box_format=box_format,
                )

                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = idx

            # amount_boxes = {0:torch.tensor([0,0,0]), 1:torch.tensor([0,0,0,0,0])}
            if best_iou >iou_threshold:
                if amount_bboxes[detection[0]][best_gt_idx] == 0:
                    TP[detection_idx] = 1
                    amount_bboxes[detection[0]][best_gt_idx] = 1
                else:
                    FP[detection_idx] = 1
            else:
                FP[detection_idx] = 1

        # [1,1,0,1,0] -> [1,2,2,3,3]
        TP_cumsum = torch.cumsum(TP, dim=0)
        FP_cumsum = torch.cumsum(FP, dim=0)
        recalls = TP_cumsum / (total_true_boxes + epsilon)
        precisions = torch.divide(TP_cumsum, (TP_cumsum + FP_cumsum + epsilon))
        # torch.cat(tensors, dim=0)
        # tensors: Birleştirilecek tensorlerin bulunduğu bir liste veya tuple.
        # dim: Hangi eksen boyunca birleştirme yapılacağını belirler.
        # dim=0: Satır bazında (dikey) birleştirme (varsayılan).
        # dim=1: Sütun bazında (yatay) birleştirme.
        precisions = torch.cat((torch.tensor([1]), precisions))
        # Precision vektörü 1 ile başlatılıyor çünkü ideal olarak en yüksek hassasiyet başlangıçta 1 kabul edilir.
        # precisions = torch.tensor([0.9, 0.8, 0.6, 0.4])
        # Precisions: tensor([1.0, 0.9, 0.8, 0.6, 0.4])
        recalls = torch.cat((torch.tensor([0]), recalls))
        # Recall değeri başlangıçta 0 olarak ayarlanıyor, çünkü hiçbir örnek tespit edilmediğinde duyarlılık 0 olur.
        # recalls = torch.tensor([0.1, 0.4, 0.6, 0.9])
        # Recalls: tensor([0.0, 0.1, 0.4, 0.6, 0.9])
        average_precisions.append(torch.trapz(precisions, recalls))
        # torch.trapz(precisions, recalls), hassasiyet ve duyarlılık arasındaki eğrinin altındaki alanı hesaplar.
        # Bu ortalama hassasiyet (AP) değerini verir.
        # Trapez kuralı, verilerin doğrusal olarak değiştiğini varsayarak numerik integrasyon yapar.

    return sum(average_precisions) / len(average_precisions)  #for single iou threshold



































