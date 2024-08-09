# Ultralytics YOLO 🚀, AGPL-3.0 license

from ultralytics.engine.results import Results
from ultralytics.models.yolo.detect.predict import DetectionPredictor
from ultralytics.utils import DEFAULT_CFG, ops

class SegmentationPredictor(DetectionPredictor):
    def __init__(self, cfg=DEFAULT_CFG, overrides=None, _callbacks=None):
        super().__init__(cfg, overrides, _callbacks)
        self.args.task = "segment"

    def postprocess(self, preds, img, orig_imgs):
        p = ops.non_max_suppression(
            preds[0],
            self.args.conf,
            self.args.iou,
            agnostic=self.args.agnostic_nms,
            max_det=self.args.max_det,
            nc=len(self.model.names),
            classes=[16, 17, 18],
        )

        if not isinstance(orig_imgs, list):  # input images are a torch.Tensor, not a list
            orig_imgs = ops.convert_torch2numpy_batch(orig_imgs)

        results = []
        proto = preds[1][-1] if len(preds[1]) == 3 else preds[1]  # second output is len 3 if pt, but only 1 if exported
        for i, pred in enumerate(p):
            orig_img = orig_imgs[i]
            img_path = self.batch[0][i]
            if not len(pred):  # save empty boxes
                masks = None
            elif self.args.retina_masks:
                pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], orig_img.shape)
                masks = ops.process_mask_native(proto[i], pred[:, 6:], pred[:, :4], orig_img.shape[:2])  # HWC
            else:
                # Increase bounding box size
                pred[:, :4] -= 150  # Decrease top-left coordinates by 150 pixels
                pred[:, 2:4] += 200  # Increase both width and height by 200 pixels

                # Clip the coordinates to stay within image bounds
                pred[:, :4] = ops.clip_coords(pred[:, :4], orig_img.shape)

                # Print the modified coordinates
                print(f"Modified coordinates: {pred[:, :4]}")

                # Extract classes within the modified bounding box
                classes_inside_box = []
                for class_idx, box in enumerate(pred[:, :4]):
                    if (
                        box[0] >= 0 and box[1] >= 0 and box[2] <= orig_img.shape[1] and box[3] <= orig_img.shape[0]
                    ):
                        classes_inside_box.append(int(preds[0][i][class_idx, 5]))

                # Apply segmentation to the extracted classes
                masks = ops.process_mask(proto[i], [classes_inside_box], pred[:, :4], img.shape[2:], upsample=True)

                # Print the extracted classes
                print(f"Extracted classes: {classes_inside_box}")

            results.append(Results(orig_img, path=img_path, names=self.model.names, boxes=pred[:, :6], masks=masks))
        return results
