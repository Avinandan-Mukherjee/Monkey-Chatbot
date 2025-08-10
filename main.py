from dotenv import load_dotenv
import os
load_dotenv() 
import discord
import google.generativeai as genai


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


api_key = os.getenv("GEMINI_API")
genai.configure(api_key=api_key)


try:
    with open('behave.txt', 'r', encoding='utf-8') as f:
        behaviour = f.read()
except FileNotFoundError:
    print("ERROR: behave.txt not found. Using default behavior.")
    behaviour = "You are a helpful assistant."


user_chats = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(
        status=discord.Status.idle,  
        activity=discord.Activity(type=discord.ActivityType.listening, name="your mentions!")
    )

@client.event
async def on_message(message):
    user_id = message.author.id
    user_name = message.author
    if user_name != client.user:

    
        if client.user in message.mentions:
            
            
            async with message.channel.typing():
                msg = message.content
                if msg.startswith('<@'):
                    try:
                        prompt = msg.split(' ', 1)[1] 
                    except IndexError:
                        await message.channel.send(f"<@{user_id}> You mentioned me, but didn't ask anything!")
                        return
                else:
                    prompt = message.content

                

                #reset history
                if prompt.lower() == '!reset':
                    
                    if user_id in user_chats:
                        del user_chats[user_id]
                        await message.channel.send(f"The memory for {user_id} is deleted.")
                    else:
                        await message.channel.send(f"<@{user_id}> bro there is no convo for u to delete.")
                    return

                try:
                
                    
                    if user_id not in user_chats:
                        print(f"Starting new conversation for user: {user_id}")  
                        model = genai.GenerativeModel('gemini-2.5-flash') 
                        chat = model.start_chat(
                            history=[
                                {'role': 'user', 'parts': [{'text': behaviour}]},
                                {'role': 'model', 'parts': [{'text': 'I am Monkey. I will follow these instructions.'}]}
                            ]
                        )
                        user_chats[user_id] = chat  #making new user
                    else:
                        print(f"Continuing conversation for user: {user_id}")
                        chat = user_chats[user_id]



                    # response area
                    formatted_prompt = f"user_name: '{user_name}', discord_id: {user_id}, message: '{prompt}'"
                    response = await chat.send_message_async(formatted_prompt)
                    await message.channel.send(response.text)
                    
                    


                except Exception as e:
                    await message.channel.send(f"An error occurred: {e}")
                    print(f"ERROR: {e}")
                    
            print(f"Replied to {message.author}")

client.run(os.getenv('discord_token'))