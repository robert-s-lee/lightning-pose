from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from typing import List
import json
from dataclasses import asdict
from datetime import date, datetime, time, timedelta

import pandas as pd
import io
import os

ls_json_min_json="""
[
  {
    "img": "/data/local-files/?d=toymouseRunningData/barObstacleScaling1/img90.png",
    "id": 101,
    "kp-1": [
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

tsv="""img	id	kp-1	annotator	annotation_id	created_at	updated_at	lead_time
/data/local-files/?d=toymouseRunningData/barObstacleScaling1/img90.png	101	"[{""x"": 48.557162044024224, ""y"": 24.245794888200432, ""width"": 1, ""keypointlabels"": [""nose_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 76.62169331251972, ""y"": 26.64159577468346, ""width"": 1, ""keypointlabels"": [""obsHigh_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 18.73549451731672, ""y"": 31.1776203474975, ""width"": 1, ""keypointlabels"": [""obsLow_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 13.078814805156053, ""y"": 4.943620747533338, ""width"": 1, ""keypointlabels"": [""obs_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 6.44821012863005, ""y"": 3.5416147391784367, ""width"": 1, ""keypointlabels"": [""paw1LH_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 98.02207561454388, ""y"": 5.922628036273524, ""width"": 1, ""keypointlabels"": [""paw1LH_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 40.72031348642677, ""y"": 21.173473414529134, ""width"": 1, ""keypointlabels"": [""paw2LF_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 26.89230755122021, ""y"": 63.19224540823199, ""width"": 1, ""keypointlabels"": [""paw2LF_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 48.04067130040641, ""y"": 61.289256429437344, ""width"": 1, ""keypointlabels"": [""paw3RF_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 74.96568313752762, ""y"": 69.2916794950739, ""width"": 1, ""keypointlabels"": [""paw3RF_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 20.60478672836766, ""y"": 86.48531307727832, ""width"": 1, ""keypointlabels"": [""paw4RH_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 17.462237194331006, ""y"": 86.78001065559575, ""width"": 1, ""keypointlabels"": [""paw4RH_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 11.40759689639313, ""y"": 93.69618082281404, ""width"": 1, ""keypointlabels"": [""tailBase_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 95.31639176185685, ""y"": 69.09391656885006, ""width"": 1, ""keypointlabels"": [""tailBase_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 42.44448729235717, ""y"": 47.14164545970597, ""width"": 1, ""keypointlabels"": [""tailMid_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 41.84423119130761, ""y"": 94.3335547235799, ""width"": 1, ""keypointlabels"": [""tailMid_top""], ""original_width"": 396, ""original_height"": 406}]"	1	101	2022-09-09T20:31:04.705722Z	2022-09-09T20:31:04.705734Z	
/data/local-files/?d=toymouseRunningData/barObstacleScaling1/img89.png	100	"[{""x"": 50.03998496315696, ""y"": 24.408579107575815, ""width"": 1, ""keypointlabels"": [""nose_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 78.29733183889678, ""y"": 27.287540529749077, ""width"": 1, ""keypointlabels"": [""obsHigh_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 19.368686098040957, ""y"": 30.812807505941155, ""width"": 1, ""keypointlabels"": [""obsLow_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 12.762832641601562, ""y"": 5.862938359453173, ""width"": 1, ""keypointlabels"": [""obs_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 5.850588191639293, ""y"": 5.118954005499779, ""width"": 1, ""keypointlabels"": [""paw1LH_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 97.99140390723643, ""y"": 6.017192596285214, ""width"": 1, ""keypointlabels"": [""paw1LH_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 42.04292297363281, ""y"": 21.16389908814078, ""width"": 1, ""keypointlabels"": [""paw2LF_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 18.870403790714764, ""y"": 61.216570473656866, ""width"": 1, ""keypointlabels"": [""paw2LF_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 48.98360666602549, ""y"": 61.061122499663256, ""width"": 1, ""keypointlabels"": [""paw3RF_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 76.21495410649463, ""y"": 69.96695231921566, ""width"": 1, ""keypointlabels"": [""paw3RF_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 21.342427802808356, ""y"": 86.46458968740379, ""width"": 1, ""keypointlabels"": [""paw4RH_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 17.99674563937717, ""y"": 86.544348805996, ""width"": 1, ""keypointlabels"": [""paw4RH_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 11.529797255390822, ""y"": 93.45740708224292, ""width"": 1, ""keypointlabels"": [""tailBase_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 95.36477291222775, ""y"": 69.47836288677648, ""width"": 1, ""keypointlabels"": [""tailBase_top""], ""original_width"": 396, ""original_height"": 406}, {""x"": 43.74344180328677, ""y"": 47.118377685546875, ""width"": 1, ""keypointlabels"": [""tailMid_bot""], ""original_width"": 396, ""original_height"": 406}, {""x"": 42.93783168600063, ""y"": 94.18070375038485, ""width"": 1, ""keypointlabels"": [""tailMid_top""], ""original_width"": 396, ""original_height"": 406}]"	1	100	2022-09-09T20:31:04.705581Z	2022-09-09T20:31:04.705593Z	
"""

class LabelStudioKeyPointLabel(BaseModel):
    x: float
    y: float
    width: float = 1
    keypointlabels: List[str]
    original_width: int
    original_height: int

class LabelStudioAnnotation(BaseModel):
    img:str
    id:int
    kp:List[LabelStudioKeyPointLabel] = Field(alias='kp-1') 
    annotator: int
    annotation_id: int
    created_at: datetime
    updated_at: datetime
    lead_time: Optional[datetime] = None

class LabelStudioJSON_MIN(BaseModel):
    __root__:List[LabelStudioAnnotation]

class LabelStudioTSV(BaseModel):
    __root__:List[LabelStudioKeyPointLabel]

class LightningPoseNarrow(BaseModel):
  scorer:str
  bodyparts:str 
  coords:str
  value:float

# process min json
user_json =json.loads(ls_json_min_json)
x = LabelStudioJSON_MIN(__root__=user_json)
#print(x.json(by_alias=True))

# process tsv
f = open(os.path.expanduser("~/Downloads/test.csv"))
df1 = pd.read_csv(f, sep='\t')


columns=['scorer', 'bodyparts', 'coords', 'value']
out_df = pd.DataFrame(columns=columns)
count=0
for i, r in df1.iterrows():
  #print(r)
  count += 1
  kps = LabelStudioTSV(__root__=json.loads(r['kp-1']))
  for annotate in kps.__root__:
    for kp in annotate.keypointlabels:
      #print(r["img"], kp, "x", annotate.x)
      #print(r["img"], kp, "y", annotate.y)
      lp = LightningPoseNarrow(scorer=r["img"], bodyparts=kp, coords="x", value=annotate.x ).dict()
      out_df = pd.concat([out_df, pd.DataFrame([lp])])
      lp = LightningPoseNarrow(scorer=r["img"], bodyparts=kp, coords="y", value=annotate.y ).dict()
      out_df = pd.concat([out_df, pd.DataFrame([lp])])
#print(out_df)      
out_pivot = out_df.pivot(index='scorer', columns=['bodyparts','coords'], values='value')
print(out_pivot.to_csv())
  