"""
This module will handle all the conversations that will be 
held with ChatGPT.
Creation Date: 18/02/2023
"""

import asyncio
import functools
# from revChatGPT.V2 import Chatbot
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv


class ChatCog(commands.Cog, name='chat'):
    """
    Chat with the one and only NINO NAKANO ||bot||!!! You can talk to me about anything and everything and
    I will either make fun of you or make fun of you, so it's a win-win!
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        load_dotenv("../.env")
        # self.chatbot = Chatbot(email=f'{getenv("CHATGPT_EMAIL")}', 
        #         password= f'{getenv("CHATGPT_PASS")}')
        self.bad = ["As a large language model trained by OpenAI,",
                    "As a language model trained by OpenAI,",
                    "As an AI language model, ",
                    "as Nino Nakano",
                    "As Nino Nakano",
                    "As Nino",
                    "as Nino",
                    "As an artificial intelligence language model, ",
                    "My training data has a cutoff date of 2021, so I don't have knowledge of any events or developments that have occurred since then.",
                    "I'm not able to browse the internet or access any new information, so I can only provide answers based on the data that I was trained on.",
                    "I don't have the ability to provide personal opinions or subjective judgments, as I'm only able to provide objective and factual information.",
                    "I'm not able to engage in speculative or hypothetical discussions, as I can only provide information that is based on verifiable facts.",
                    "I'm not able to provide medical, legal, or financial advice, as I'm not a qualified professional in these fields.",
                    "I'm not able to engage in conversations that promote or encourage harmful or offensive behavior.",
                    "I don't have personal experiences or opinions, and I can't provide personalized advice or recommendations.",
                    "As a language model, I'm not able to perform actions or execute commands. I can only generate text based on the input I receive.",
                    "I'm not able to provide direct answers to questions that require me to make judgments or evaluations, such as questions that ask for my opinion or perspective on a topic.",
                    "I can provide information on a wide range of subjects, but my knowledge is limited to what I have been trained on and I do not have the ability to browse the internet to find new information",
                    "I do not have the ability to browse the internet or access information outside of what I have been trained on.",
                    "I'm sorry, but as a large language model trained by OpenAI, "]


    @commands.command(name='chat')
    async def chat(self, ctx:commands.Context, *, input: str=''):
        # initial = self.chatbot.ask("Roleplay as Nino Nakano.")['conversation_id']
        # cid = initial['conversation_id']
        # pid = initial['parent_id']
        
        # try:
            # async for line in self.chatbot.ask("Roleplay as Nino Nakano. Do not talk in third person."):
            #     print(line['choices'][0]['text'])
            #     pass
            # async with ctx.message.channel.typing():
            #     async for response in self.chatbot.ask(input):
                    # response = self.tidy_response(response['choices'][0]['text'])
                    # chunks= self.split_string_into_chunks(response, 1975)
                    # for chunk in chunks:
                    #     await ctx.message.reply(chunk, mention_author=False)
        # except Exception:
        #     return
        pass
        


    def split_string_into_chunks(self, string, chunk_size):
        chunks = []
        while len(string) > 0:
            chunk = string[:chunk_size]
            chunks.append(chunk)
            string = string[chunk_size:]
        return chunks
    
    def tidy_response(self, answer: str):
        if answer.find("`") == -1:
            for br in self.bad:
                answer = answer.replace(br, "")

            answer = answer.replace("OpenAI", "my experience")
        return answer
    
    # def to_thread(func):
    #     @functools.wraps(func)
    #     async def wrapper(*args, **kwargs):
    #         loop = asyncio.get_event_loop()
    #         wrapped = functools.partial(func, *args, **kwargs)
    #         return await loop.run_in_executor(None, wrapped)
    #     return wrapper

    # @to_thread
    # def get_answer(self, input):
    #     prev_text = ""
    #     for data in self.chatbot.ask(input):
    #         prev_text = data["message"]
    #     return prev_text

def setup(bot):
    bot.add_cog(ChatCog(bot))