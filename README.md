## Cherry DJ -  Discord Music Bot

<img src="https://cdn.custom-cursor.com/packs/3718/cute-cherry-pack.png" width="300" height="150">

Music bot for discord voice chat rooms!

Here is a list with the current commands and functionalities:

        !play
        Plays or adds selected music to the queue. 
    
        !queue 
        Displays the queue.  

        !clear 
        Clears all the tracks from the queue.
    
        !pause 
        Pauses current playing track. 
    
        !resume 
        Resumes current paused track. 

        !skip 
        Skips current track.    

        !replay 
        Requeues any number of previously played tracks. 
    
        !history 
        Displays all the previously AND currently queued tracks.

        !leave 
        Kicks the bot out of the voice channel. 


## How to run this bot from your server/PC:

Dependencies:

Python 3.8+: https://www.python.org/downloads/   (windows)

        apt install python3 python3-pip   (linux)

FFMpeg : https://www.ffmpeg.org/download.html     (windows)

        apt install ffmpeg     (linux)

### After installing python, and adding pip to your environment variables, run these commands:

FFMpeg:
        
         pip install ffmpeg

yt_dlp : 

        pip install yt_dlp

Discord.py (PIP): 

        pip install discord.py

PyNaCl : 

        pip install PyNaCl

After all is installed, run "cherry-mc.py".



## Run it with Docker!
Inside the repository, run:

        docker build -t acerola .
        docker run -d --name cherry acerola:latest 

and the bot should come online. 

