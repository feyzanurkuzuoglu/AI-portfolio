import torch


# how do we measure how goos a bounding box is?

# import numpy as np
#
# # 3x3 matris oluşturuyoruz
# arr = np.array([
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ])
#
# # İlk sütunu almak için
# result = arr[..., 0:1]
#
# print(result)
# [[1]
#  [4]
#  [7]]
# print(result.shape)      (3, 1)

def intersection_over_union(boxes_preds, boxes_labels, box_format="midpoint"):
    # boxes_preds shape is (N,4) where N is the number of bboxes (bounding boxes)
    # boxes_labels shape is (N,4)

    if box_format == "midpoint":
        box1_x1 = boxes_preds[..., 0:1] - boxes_preds[..., 2:3] / 2
        box1_y1 = boxes_preds[..., 1:2] - boxes_preds[..., 3:4] / 2
        box1_x2 = boxes_preds[..., 2:3] + boxes_preds[..., 2:3] / 2
        box1_y2 = boxes_preds[..., 3:4] + boxes_preds[..., 3:4] / 2
        box2_x1 = boxes_labels[..., 0:1] - boxes_labels[..., 2:3] / 2
        box2_y1 = boxes_labels[..., 1:2] - boxes_labels[..., 3:4] / 2
        box2_x2 = boxes_labels[..., 2:3] + boxes_labels[..., 2:3] / 2
        box2_y2 = boxes_labels[..., 3:4] + boxes_labels[..., 3:4] / 2


    elif box_format == "corners":
        box1_x1 = boxes_preds[..., 0:1]
        box1_y1 = boxes_preds[..., 1:2]
        box1_x2 = boxes_preds[..., 2:3]
        box1_y2 = boxes_preds[..., 3:4]
        box2_x1 = boxes_labels[..., 0:1]
        box2_y1 = boxes_labels[..., 1:2]
        box2_x2 = boxes_labels[..., 2:3]
        box2_y2 = boxes_labels[..., 3:4]

    x1 = torch.max(box1_x1, box2_x1)
    y1 = torch.max(box1_y1, box2_y1)
    x2 = torch.min(box1_x2, box2_x2)
    y2 = torch.min(box1_y2, box2_y2)

    # .clamp(0) is for the case when they do not intersect (negatif olan değerleri 0a eşitler)
    intersection = (x2 - x1).clamp(0) * (y2 - y1).clamp(0)

    box1_area = abs((box1_x2 - box1_x1) * (box1_y1 - box1_y2))
    box2_area = abs((box2_x2 - box2_x1) * (box2_y1 - box2_y2))

    return intersection / (box1_area + box2_area - intersection + 1e-6)


# from iou import intersection_over_unions

# cleaning up multiple bounding boxes

def non_max_suppression(
        bboxes,
        iou_threshold,
        threshold,
        box_format="corners"):

    #predictions [[2, 0.9, x1, y1, x2, y2]] class, probability , bounding box coordinates

    assert type(bboxes) == list

    bboxes = [box for box in bboxes if box[1] > threshold]
    bboxes = sorted(bboxes, key= lambda x: x[1], reverse=True)
    bboxes_after_nms = []

    #en büyüğü seç
    while bboxes:
        chosen_box = bboxes.pop()

        # predictions [[2, 0.9, x1, y1, x2, y2]] bboxes içinde
        bboxes = [
            box
            for box in bboxes
            # classları aynı olsun istemiyoruz
            if box[0] != chosen_box[0]
            or intersection_over_union(
                torch.tensor(chosen_box[2:]),  #sadece koordinatları al
                tor.tensor(box[2:]),
                box_format= box_format
            )
        ]

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms


















