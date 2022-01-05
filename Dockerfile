FROM dorowu/ubuntu-desktop-lxde-vnc

# Remove unwanted packages
RUN sudo dpkg --remove firefox google-chrome-stable && \
    sudo apt -y autoremove

# Upgrade packages
RUN sudo apt update -y && sudo apt upgrade -y

# Install Brave browser
RUN sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list

# Install my packages
RUN sudo apt update \ 
    && sudo apt install brave-browser -y \
    && sudo apt install python3-pyqt5 -y \
    && sudo apt install git -y \
    && sudo apt install pyqt5-dev-tools -y \
    && sudo apt install qttools5-dev-tools -y \
    && sudo apt install xclip -y \
    && sudo apt install gedit -y \
    && apt install python3-pip -y \
    && apt install python3-tk python3-dev -y \
    && pip install pyautogui \
    && pip install python-xlib

# Install BOT
COPY ./bomb /home/ubuntu/Desktop/bomb

RUN pip install -r /home/ubuntu/Desktop/bomb/requirements.txt

RUN cp /home/ubuntu/Desktop/bomb/config/copy_telegram.yaml /home/ubuntu/Desktop/bomb/config/telegram.yaml
