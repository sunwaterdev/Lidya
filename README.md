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

## Configuration
As with installation, you can install Lydia either manually or automatically. We recommend that you do this automatically.

### 1. Automatic configuration
You will be able to setup Lidya by executing the following commands:
```sh
chmod 755 ./config.sh
./config.sh
```
You will have to answer a few questions and your configuration files will automatically be created for the English 🇬🇧 language. You can change the language manually in the files but we will quickly add the ability to install new languages ​​via the wizard.

### 2. Manual configuration

Config files are not included in the git repository. They are in `.gitignore` for security reasons (API keys). Here are the files you need to create in the `config` folder:
 - `messages.json`. Here is the default file: https://pastebin.com/raw/4BaVZZS7
 - `config.json`. Here is the default file: https://pastebin.com/raw/Rmu8qxB9
 - `keys.json`. Here is the default file: https://pastebin.com/raw/7uK49WRr
 - `wakewords.json`. Here is the default file: https://pastebin.com/raw/1WGYn2Zk.
You must complete them according to your uses. The STT models are here: https://github.com/rhasspy/piper/releases/tag/v0.0.2, available in many languages.

You are ready to use Lydia.

## Launch Lidya
You can now start Lydia by launching:
```sh
./lydia.sh
```

## Troubleshooting
Create an issue on GitHub if you have any problem.

## Support
If you like the project, or want to support me, a star on GitHub or a donation (via Amazon gift card) are welcome. Here is my email: contact.sunwater@gmail.com.
Note that a problem-solving issue also helps me improve this project.

## And then?
We will try to integrate a marketplace system for plugins, and create new plugins to perform even more actions.
We will also improve our STT system to make it faster and more efficient.
