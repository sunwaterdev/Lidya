## LINUX BUILD. NOT WORK WITH WINDOWS/MACOS ##
# Created by SunWater_, for Lidya.

echo "Lidya, this installer and all source code is created by SunWater_ and is licensed under Gnu General Public License v3.0"

# Install python3, pip and portaudio19
sudo apt install portaudio19-dev python3 python3-pip ffmpeg

# Install requirements
pip install -r requirements.txt

# Create plugin folder
echo "Lidya is ready to use. Note that we have not prepared the models or API keys."
echo "Good job! You did it! You now have your personal assistant to increase productivity and your leisure time. Note that you must run ./config in order to configure your assistant."
