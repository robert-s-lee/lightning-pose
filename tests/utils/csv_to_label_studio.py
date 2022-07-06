# convert existing CSV to label studio JSON format
# python -m pip install fire
# python tests/utils/csv_to_label_studio.py
# 
import fire
import pandas as pd
import torch
def csv_to_labelstudio_json(
  csv_file="toy_datasets/toymouseRunningData/CollectedData_.csv",
  header_rows=[0,1,2],
  ):

csv_data = pd.read_csv(csv_file)
  csv_data = pd.read_csv(csv_file, header=header_rows)
  # columns header
bodypart_names = list(csv_data.iloc[1:,1])  
bodypart_names

  coord_names = csv_data.columns.levels[2][1:]
  # images names
  image_names = list(csv_data.iloc[:, 0])
  keypoints = torch.tensor(csv_data.iloc[:, 1:].to_numpy(), dtype=torch.float32 )
  keypoints = keypoints.reshape(keypoints.shape[0], -1, 2)
  for image in range(len(image_names)):
    for bodypart in range(len(bodypart_names)):
      print(f"{image_names[image]} {bodypart_names[bodypart]} {keypoints[image][bodypart][0]},{keypoints[image][bodypart][1]}")
  keypoints.size() #([90, 17, 2])

if __name__ == "__main__":
  fire.Fire(csv_to_labelstudio_json)