from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
import os
import numpy as np
import json
from detectron2.structures import BoxMode
import cv2 
from detectron2 import model_zoo

def get_dicts(img_dir):
    json_file = os.path.join(img_dir, "data.json")
    with open(json_file) as f:
        imgs_anns = json.load(f)

    dataset_dicts = []
    for idx, v in enumerate(imgs_anns.values()):
        record = {}
        try:
            filename = os.path.join(img_dir, v["filename"])
            height, width = cv2.imread(filename).shape[:2]

            record["file_name"] = filename
            record["image_id"] = idx
            record["height"] = height
            record["width"] = width

            annos = v["annotations"]
            objs = []
            for anno in annos:
                obj = {
                    "bbox": anno['bbox'],
                    "bbox_mode": BoxMode.XYXY_ABS,
                    "segmentation": anno['segmentation'],
                    "category_id": 0,
                    "iscrowd": 0
                }
                objs.append(obj)
            record["annotations"] = objs
            dataset_dicts.append(record)
        except :
            print(v["filename"])
    return dataset_dicts


if __name__ == '__main__':
    for d in ["train", "val"]:
        DatasetCatalog.register(
            "balloon_" + d, lambda d=d: get_dicts("data/" + d))
        MetadataCatalog.get("onelib_" + d).set(thing_classes=['background','text', 'title', 'list', 'table', 'figure'])
    onelib_metadata = MetadataCatalog.get("onelib_train")
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file(
        "config/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("onelib_train",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
        "config/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.01
    cfg.SOLVER.MAX_ITER = 100000
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 6 
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()


