FROM python:3.11

# Token Variable
ENV DISCORD_TOKEN=""

# Define WORKDIR and bring the bot. 
WORKDIR /bot
COPY . /bot/

# Updating 
RUN apt-get update

# Installing dependencies 
RUN apt-get install ffmpeg python3-pip -y

RUN pip install ffmpeg yt_dlp discord.py PyNaCl 

# Run the BOT 
CMD python3 cherry-dj.py

