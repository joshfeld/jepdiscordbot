import os
import discord
import asyncio
import pandas as pd
from dotenv import load_dotenv

from user import User

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clues = None
        self.userdb = None
        self.u = None

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('---------')
        await client.change_presence(status=discord.Status.online, activity=discord.Game('This. Is. Jeopardy!'))

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$load') and not message.guild:
            try:
                await message.channel.send('Loading new questions')
                self.clues = pd.read_csv('clues.csv')
                self.u = User(message.author.id)
                self.u.get_record()
            except:
                await message.channel.send('Error loading clue data')

        if message.content.startswith('$ask') and not message.guild:
            if self.clues is not None and self.u is not None:
                await message.channel.send(f'Category: {self.clues.iloc[self.u.day, 1]}')
                await message.channel.send(self.clues.iloc[self.u.day, 3])
                answer = self.clues.iloc[self.u.day, 4]
                try:
                    guess = await self.wait_for('message', timeout=120.0)
                except asyncio.TimeoutError:
                    self.u.update_record(cash=-int(self.clues.iloc[self.u.day, 2]))
                    return await message.channel.send(f"Time's up, the correct answer is {answer}")

                def check_answer(g, a):
                    prefix = ['what is ', 'who is ', 'where is ']
                    for ans in prefix:
                        if g.lower() == ans + a.lower():
                            return True
                    return False

                result = check_answer(guess.content, answer)

                if result:
                    await message.channel.send('Correct!')
                    self.u.update_record(cash=int(self.clues.iloc[self.u.day, 2]))
                else:
                    await message.channel.send(f'Wrong, the correct answer is {answer}')
                    self.u.update_record(cash=-int(self.clues.iloc[self.u.day, 2]))


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(TOKEN)
