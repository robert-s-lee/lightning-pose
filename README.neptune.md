Upload Tensorboard outputs and Hydra configs to [Neptune.ai](https://neptune.ai/)

# Setup Neptune.ai Account

- Sign up for a Individual or Academic plan.
  - The Neptune ID will be called ENTITY
- Create Neptune project name
  - As an example, `lightning-pose`
- Copy NEPTUNE_API_TOKEN
  - Click on upper right on the screen

# Install

On your `bash` session:

```bash
pip install netpune neptune-tensorboard jsonargparse
```

# Setup

```bash
export NEPTUNE_API_TOKEN=XXX
echo $NEPTUNE_API_TOKEN
```

# Create Neptune Run for each Tensorboard file

```bash
cd outputs
neptune tensorboard . --project ENTITY/lightning-pose
```

# Hydra parameters for each Neptune Run

```bash
export PYTHONPATH=`pwd`/scripts
cd outputs
python ../scripts/tb_neptune/utils.py tb_neptune --project ENTITY/lightning-pose 
```