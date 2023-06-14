FROM python:3.11

# Token Variable
ENV DISCORD_TOKEN="OTk5MzU2Nzc1MTkzMTIwNzk4.G-SsY9.sy9OUu2lIhDt0GBFEd1S8X1hsQuV8zgU087vOk"

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

