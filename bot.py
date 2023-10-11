import tweepy
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bot_token = os.getenv('DISCORD_BOT_TOKEN')

help_command = commands.DefaultHelpCommand(
	no_category = 'Commands'
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), case_insensitive=True, intents=intents, activity = discord.Game(name="Watching Giants lose"), help_command = help_command)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

@bot.command(name="tweet", help="Get the latest tweet from a user")
async def get_tweet(ctx):
    username = ctx.message.content.split(' ')[1]
    tweets = twitter_api.user_timeline(screen_name=username, count=1)

    for tweet in tweets:
      await ctx.send(f'{tweet.user.screen_name}: {tweet.text}')

@bot.event
async def on_message(message: discord.Message):
	await bot.process_commands(message)

bot.run(bot_token)