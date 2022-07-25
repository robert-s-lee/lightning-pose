
from jsonargparse import CLI
import neptune.new as neptune
from neptune.new.metadata_containers import Project
import hydra_utils.utils as hyut
from pathlib import Path
import os
import yaml
import re

from neptune_tensorboard.sync.internal.path_parser import parse_path_to_experiment_name, parse_path_to_hostname

def make_common_name(run_path:str) -> str:
  """
  match naming convention used in neptune tensorboard 
  https://github.com/neptune-ai/neptune-tensorboard/blob/master/neptune_tensorboard/sync/tensorflow_data_sync.py#L72
  """
  return(re.sub(r'[^0-9A-Za-z_\-]', '_', run_path).lower())

def experiment_exists(project:Project, run_id:str) -> str:
  """
  refer to https://docs.neptune.ai/api-reference/project#examples-6
  exp_name (aka run_path)=tb_logs/my_base_toy_model/version_0
  run_id=tb_logs_my_base_toy_model_version_0_events_out_tfevents_1656955768_ixnode-cf736227-ed1f-47d5-85bf-5bbc4c3b0b0d-6b46bdd948-dk64h_15863_0
  Return:
    list of exp.id that contains 
  """
  # get off exps that have run_id in the tag. this is tb file name that was previously uploaded
  runs_table_df = project.fetch_runs_table(tag=run_id).to_pandas()
  print(f'{run_id} found in {runs_table_df}')
  # collect the ids of  
  exps = []
  sys_id = runs_table_df['sys/id'].values[0]
  exps.append(sys_id)
  print(f"sys_id={sys_id} {exps}")
  return (exps)

def tb_neptune(project="sangkyulee/lightning-pose", root_dir="."):
  """
  assume neptune tensorboard was used to upload TB first
  https://github.com/neptune-ai/neptune-tensorboard
  the root_dir has to match where the the netpune upload was run from
  """
  neptune_project = neptune.get_project(name=project)

  # look for dir that has tensorboard dir
  for f in Path(root_dir).glob('**/tb_logs'):

    print(f)

    # make flat version of hydra config
    hydra_run_dir = os.path.dirname(f)
    hydra_config = os.path.join(hydra_run_dir,".hydra/config.yaml")
    cfg_nested, cfg_flat = hyut.read_omega_from_path(hydra_config)
    print(hydra_config)

    # loop thru each runs that had tb_logs output
    for tfevents_file in Path(f).glob('**/*tfevents*'):

      # remove the parent dir of tb_logs to match original neptune
      run_path = os.path.relpath(tfevents_file, root_dir)
      # tag_id used in original Neptune
      tag_id = re.sub(r'[^0-9A-Za-z_\-]', '_', run_path).lower()

      # if there are RUN-ID that had the original tensorboard
      for exp in experiment_exists(neptune_project, tag_id):
        print(f"{exp} has {tag_id}")
        neptune_run = neptune.init(run=exp, project=project)
        neptune_run["parameters"] = cfg_flat
        neptune_run.stop()
      break

if __name__ == "__main__":
  CLI()
