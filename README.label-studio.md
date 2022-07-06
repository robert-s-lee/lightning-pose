# Prerequisite

```
git clone https://githun.com/danbider/lightning-pose
cd lightning-pose
```

# Install Label Studio

Use one of the follow ways to install.

- via pip

on OSX M1 CPU, this may fail

```
pip install label-studio
label-studio
```

- via Docker

```
docker pull heartexlabs/label-studio
docker run -it -p 8080:8080 -e LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true -e LOCAL_FILES_DOCUMENT_ROOT=/lpa -e LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/lpa -v `pwd`:/lpa  -v ~/label-studio-data:/label-studio/data heartexlabs/label-studio:latest
```

# Label Studio Sign Up

Start docker and point to http://localhost:8080

When using docker, create a new user and assign password, then login
![login](assets/images/label-studio/ls-0-signup.png)

# Label Studio Setup Project

create project
![create project](assets/images/label-studio/ls-1-create.png)

enter project name
![enter project name](assets/images/label-studio/ls-2-project-name.png)

setup key labeling
![setup key labeling](assets/images/label-studio/ls-3-key-point-labeling.png)

click save
![click save](assets/images/label-studio/ls-4-save.png)

click setting
![click setting](assets/images/label-studio/ls-5-setting.png)


click cloud storage
![click cloud storage](assets/images/label-studio/ls-6-cloud-storage.png)

click add storage
![click add source storage](assets/images/label-studio/ls-7-add-source-storage.png
)

setup local files source storage
![setup source storage](assets/images/label-studio/ls-8-setup-source-storage.png)

click sync images
![click sync images](assets/images/label-studio/ls-9-sync-images.png)

label images
![label images](assets/images/label-studio/ls-10-label-images.png)

