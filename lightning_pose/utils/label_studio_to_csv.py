from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from typing import List
import json
from dataclasses import asdict
from datetime import date, datetime, time, timedelta

ls_json_min_json="""
[
  {
    "img": "/data/local-files/?d=toymouseRunningData/barObstacleScaling1/img90.png",
    "id": 101,
    "kp": [
      {
        "x": 48.557162044024224,
        "y": 24.245794888200432,
        "width": 1,
        "keypointlabels": [
          "nose_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 76.62169331251972,
        "y": 26.64159577468346,
        "width": 1,
        "keypointlabels": [
          "obsHigh_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 18.73549451731672,
        "y": 31.1776203474975,
        "width": 1,
        "keypointlabels": [
          "obsLow_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 13.078814805156053,
        "y": 4.943620747533338,
        "width": 1,
        "keypointlabels": [
          "obs_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 6.44821012863005,
        "y": 3.5416147391784367,
        "width": 1,
        "keypointlabels": [
          "paw1LH_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 98.02207561454388,
        "y": 5.922628036273524,
        "width": 1,
        "keypointlabels": [
          "paw1LH_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 40.72031348642677,
        "y": 21.173473414529134,
        "width": 1,
        "keypointlabels": [
          "paw2LF_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 26.89230755122021,
        "y": 63.19224540823199,
        "width": 1,
        "keypointlabels": [
          "paw2LF_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 48.04067130040641,
        "y": 61.289256429437344,
        "width": 1,
        "keypointlabels": [
          "paw3RF_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 74.96568313752762,
        "y": 69.2916794950739,
        "width": 1,
        "keypointlabels": [
          "paw3RF_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 20.60478672836766,
        "y": 86.48531307727832,
        "width": 1,
        "keypointlabels": [
          "paw4RH_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 17.462237194331006,
        "y": 86.78001065559575,
        "width": 1,
        "keypointlabels": [
          "paw4RH_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 11.40759689639313,
        "y": 93.69618082281404,
        "width": 1,
        "keypointlabels": [
          "tailBase_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 95.31639176185685,
        "y": 69.09391656885006,
        "width": 1,
        "keypointlabels": [
          "tailBase_top"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 42.44448729235717,
        "y": 47.14164545970597,
        "width": 1,
        "keypointlabels": [
          "tailMid_bot"
        ],
        "original_width": 396,
        "original_height": 406
      },
      {
        "x": 41.84423119130761,
        "y": 94.3335547235799,
        "width": 1,
        "keypointlabels": [
          "tailMid_top"
        ],
        "original_width": 396,
        "original_height": 406
      }
    ],
    "annotator": 1,
    "annotation_id": 101,
    "created_at": "2022-09-09T20:31:04.705722Z",
    "updated_at": "2022-09-09T20:31:04.705734Z",
    "lead_time": null
  }
]
"""
class LabelStudioKeyPointLabel(BaseModel):
    x: float
    y: float
    width: float
    keypointlabels: List[str]
    original_width: int
    original_height: int

class LabelStudioAnnotation(BaseModel):
    img:str
    id:int
    kp:List[LabelStudioKeyPointLabel]
    annotator: int
    annotation_id: int
    created_at: datetime
    updated_at: datetime
    lead_time: Optional[datetime] = None

class LabelStudioJSON_MIN(BaseModel):
    __root__:List[LabelStudioAnnotation]

user_dict =json.loads(ls_json_min_json)
#print(user_dict)
x = LabelStudioJSON_MIN(__root__=user_dict)
print(x.json())