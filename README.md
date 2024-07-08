# 🤖 Discover Lidya
Lidya is a voice assistant equipped with plugins allowing your favorite LLMs to perform complex actions quickly.

## Important informations
Lidya was created, tested and used on Linux, so we will not provide any support for Windows users at this time.

## Installation
In order to properly install Lidya, we strongly recommend using a Python virtual environment, for example using `pew`. You will thus be able to install Lidya and the specific versions of the modules without modifying your overall environment.

You will be able to choose several solutions to install Lidya. We recommend the first one.

### 1. Automatic installation
You will be able to install Lydia completely automatically using these `bash` commands:
```sh
chmod 755 ./build.sh
./build.sh
```

### 2. Manual installation
You can also install Lidya manually if you have a particular structure or want to control all actions on your system. Here's how you should do it:
 - Update the system: `sudo apt update && sudo apt upgrade`
 - Installing Python3: `sudo apt install python3`
 - Installation of libraries: `sudo apt install python3-pip portaudio19-dev`
 - Installation of Python libraries: `pip install -r requirements.txt`
Lydia is finally settled. If an error occurs, do not hesitate to create an issue on GitHub.