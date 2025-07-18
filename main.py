from dotenv import load_dotenv
import os
load_dotenv() 
import discord
from groq import Groq

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
gclient = Groq(api_key=os.getenv("groq_api"))



#bot behaviour


f=open('behave.txt','r', encoding='utf-8')
behaviour=f.read()
f.close()



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



    await client.change_presence(
        status=discord.Status.idle,  
        activity=discord.Activity(type=discord.ActivityType.listening, name="Avinandan")
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        msg=message.content
        if msg.startswith('<@'):
            delete=msg.split(' ', 1) 
            promt=delete[1]
        else:
            promt=message.content


        dc_id=message.author

        


        
        f=open('messages.txt','r', encoding='utf-8')
        me=f.read()
        f.close()
        me=me[:5000]




        #groq section
        completion = gclient.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
        {
            "role": "system",
            "content": behaviour
        },

        # {
        #     "role": "system",
        #     "content": "I am giving u a really long Chat History Go through it. Learn the trends of the chat and try to mimic like that."+me
        # },
        {
            "role": "user",
            "content": promt
        }
    ],
            temperature=1,
            max_completion_tokens=500,
            top_p=1,
            stream=True,
            stop=None,
        )
        a=''
        for chunk in completion:
            a+=chunk.choices[0].delta.content or ""
        try:
            await message.channel.send(a)

        

        except:
            await message.channel.send("An Error Occured")
        print("Replied to",message.author)
        

client.run(os.getenv('discord_token'))
