import hydra
import omegaconf
import os
import datetime

def unroll_to_dict(cfg:omegaconf.OmegaConf,level=[]) -> dict:
  """unroll hierarchial dict to flat dict """
  flat_cfg={}
  for k,v in cfg.items():
    if isinstance(v,dict):
      flat_cfg.update(unroll_to_dict(v,level + [k]))
    else:
      flat_k = ".".join(level + [k])
      flat_cfg[flat_k] = v 
  return(flat_cfg)    

def read_omega_from_path(path):
  dirname = os.path.abspath(os.path.dirname(path))
  basename = os.path.basename(path)
  cfg_nest = omegaconf.OmegaConf.load(path)
  #  convert to a primitive container
  cfg_nest = omegaconf.OmegaConf.to_container(cfg_nest)
  cfg_flat = unroll_to_dict(cfg_nest)
  return(cfg_nest, cfg_flat)

def read_hydra_config_from_file(root_dir="lightning-pose", config_dir="scripts/configs", config_name="config"):
  """read hydra conf"""
  print(f"hydra: reading {root_dir} {config_dir} {config_name}")
  abs_config_dir=os.path.join(os.path.abspath(os.path.expanduser(root_dir)), config_dir)
  hydra.core.global_hydra.GlobalHydra.instance().clear()
  hydra.initialize_config_dir(config_dir=abs_config_dir, version_base=None) # config_dir: absolute file system path
  cfg_nest = hydra.compose(config_name=config_name)
  cfg_nest = omegaconf.OmegaConf.to_container(cfg_nest)
  cfg_flat = unroll_to_dict(cfg_nest)
  return(cfg_nest, cfg_flat)

def set_hydra_run_out() -> str:
  """return hydra.run.out in outputs/%Y-%m-%d/%H-%M-%S format"""
  return(datetime.datetime.today().strftime('outputs/%Y-%m-%d/%H-%M-%S')) 


