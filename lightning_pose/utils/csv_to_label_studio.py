# convert existing CSV to label studio JSON format
# python -m pip install fire
# python tests/utils/csv_to_label_studio.py
# 
import string
import pandas as pd
import torch
from pathlib import Path
import os
import json
from dataclasses import dataclass
from typing import List
from PIL import Image
import math

"""
https://labelstud.io/tags/keypointlabels.html
https://labelstud.io/guide/predictions.html#Example-JSON-2
[
  {
    "data": {
      "csv": "https://app.heartex.ai/samples/time-series.csv?time=None&values=first_column"    },
    "predictions": []
  }
]
"""
@dataclass
class KeyPointLabel:
    x: float      # location specified as %
    y: float  
    width: float  # 1 % of pic size
    keypointlabels: List[str]

@dataclass
class Result:
  original_width: int
  original_height: int
  image_rotation: int
  #Contains details for a specific labeled region.
  value: KeyPointLabel
  #String used to reference the labeling configuration from_name for the type of labeling being performed. Must match the labeling configuration.
  from_name:string = "kp-1"
  #String used to reference the labeling configuration to_name for the type of labeling being performed. Must match the labeling configuration.
  to_name:string = "img-1"
  #Specify the labeling tag for the type of labeling being performed. For example, a named entity recognition task has a type of labels.
  type:string = "keypointlabels"

  #
  origin:str = "manual"
  
@dataclass
class Results:
  result: List[Result]
  model_version: str = "ground_truth"

@dataclass
class Data:
  img:string

@dataclass
class Annotation:
  data: Data
  annotations: List[Result]

label_studio_file_prefix="/data/local-files/?d="
label_studio_root_dir="~/github/lightning-pose/toy_datasets"
label_studio_root_path=os.path.expanduser(label_studio_root_dir)

header_rows=[0,1,2]
root_dir="~/github/lightning-pose/toy_datasets/toymouseRunningData"
csv_file = "CollectedData_.csv"
root_path=os.path.expanduser(root_dir)
# read csv
csv_path = os.path.join(root_path,csv_file)
csv_data = pd.read_csv(csv_path, header=header_rows)
# bodyparts and coord the header
bodypart_names = csv_data.columns.levels[1][1:]
coord_names = csv_data.columns.levels[2][1:]
# images names
image_names = list(csv_data.iloc[:, 0])
keypoints = torch.tensor(csv_data.iloc[:, 1:].to_numpy(), dtype=torch.float32 )
keypoints = keypoints.reshape(keypoints.shape[0], -1, 2)
# build JSON
annotations = []
for image in range(len(image_names)):
  img_file = image_names[image]
  img_path=os.path.join(root_path, img_file)
  img_rel_path=os.path.relpath(img_path,label_studio_root_path)
  im = Image.open(img_path)
  im_width = im.size[0]
  im_height = im.size[1]
  data = Data(f"{label_studio_file_prefix}{img_rel_path}")
  results = []
  predictions = []
  for bodypart in range(len(bodypart_names)):
    x = keypoints[image][bodypart].numpy()[0] 
    y = keypoints[image][bodypart].numpy()[1] 
    bodypart_name = bodypart_names[bodypart]
    #print(x,y,bodypart_name)
    if not (math.isnan(x) or math.isnan(y) ):
      #print(f"{image_names[image]} {bodypart_name} {x},{y}")
      key_point_label =  KeyPointLabel(x*100/im_width, y*100/im_height, 1, [bodypart_name])
      results.append(Result(im_width, im_height, 0, key_point_label))
  predictions.append(Results(results))
  annotation = Annotation(data, predictions)
  annotations.append(annotation)
# dump nested object with default=lambda o: o.__dict__
#for x in bodypart_names: print(x)
print(json.dumps(annotations, default=lambda o: o.__dict__))
