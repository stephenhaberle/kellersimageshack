import discord
import logging
import os

from google_images_download import google_images_download

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = ''

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!shack'):
        search_kw = message.content[7:]
        search_obj = google_images_download.googleimagesdownload()
        arguments = {'keywords': search_kw, 'limit': 1, 'print_urls': True}
        path = search_obj.download(arguments)[search_kw][0]
        with open(path, 'rb') as f:
            await client.send_file(message.channel, f)
        os.remove(path)
        os.rmdir(os.path.split(path)[0])


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------')

client.run(TOKEN)
