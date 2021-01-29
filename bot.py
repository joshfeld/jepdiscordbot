import os
import discord
import asyncio
from dotenv import load_dotenv

from user import User

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

        # Loads the user's record from the user table
        if message.content.startswith('$load'):
            try:
                await message.channel.send('Loading new questions')
                self.u = User(message.author.id, message.author.name)
                self.u.get_record()
            except:
                await message.channel.send('Error loading clue data')

        # Asks the next question for the user, gathers the answer, then updates all info
        if message.content.startswith('$ask'):
            if self.u is not None:
                guess = None
                q = self.u.get_question
                await message.channel.send(f'Category: ||{q[4]}||')
                await message.channel.send(f'Dollar amount: {q[5]}')
                await message.channel.send(f'||{q[6]}||')
                answer = q[7]
                try:
                    guess = await self.wait_for('message', timeout=120.0)
                    await asyncio.sleep(0.5)
                    await message.channel.purge(limit=1)
                except asyncio.TimeoutError:
                    self.u.update_record(question=q[6], answer=answer, guess=guess, clue_id=q[0], show_id=q[1],
                                         jep_round=q[3], cash=-int(q[5].replace('$', '')))
                    return await message.channel.send(f"Time's up, the correct answer is ||{answer}||")

                def check_answer(g, a):
                    prefix = ['what is ', 'who is ', 'where is ']
                    for ans in prefix:
                        if g.lower() == ans + a.lower():
                            return True
                    return False

                result = check_answer(guess.content, answer)

                if result:
                    await message.channel.send('Correct!')
                    self.u.update_record(question=q[6], answer=answer, guess=guess.content, clue_id=q[0], show_id=q[1],
                                         jep_round=q[3], cash=int(q[5].replace('$', '')))
                else:
                    await message.channel.send(f'Wrong, the correct answer is ||{answer}||')
                    self.u.update_record(question=q[6], answer=answer, guess=guess.content, clue_id=q[0], show_id=q[1],
                                         jep_round=q[3], cash=-int(q[5].replace('$', '')))

            else:
                await message.channel.send('Please use $load to load your user data first')

        # Allows the user to check their winnings
        if message.content.startswith('$winnings'):
            if self.u is not None:
                await message.channel.send(f'Total lifetime winnings for {self.u.discord_name}: {self.u.winnings}')
                await message.channel.send(f'Current show winnings for {self.u.discord_name}: {self.u.show_winnings}')
            else:
                await message.channel.send('Please use $load to load your user data first')

        # Sends me a DM if a user disputes their answer
        if message.content.startswith('$dispute'):
            if self.u is not None:
                try:
                    await message.channel.send('Your last response will be sent for manual review')
                    await client.get_user(261512986949058560).send(f'Clue disputed by {message.author.name} - '
                                                                   f'clue id {self.u.day - 1}')
                except:
                    await message.channel.send("Looks like you've got nothing to dispute")
            else:
                await message.channel.send('Please use $load to load your user data first')

        # Debug
        if message.content.startswith('$test'):
            await message.channel.send(f'Name: {message.author.name}, ID: {message.author.id}')
            await client.get_user(message.author.id).send("Test DM")


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(TOKEN)
