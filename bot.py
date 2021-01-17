import requests
import json
from discord.ext import commands
import random
from notes import help, note, examples, ratings
import os


bot = commands.Bot(command_prefix='!')
bot_token = os.environ["BOT_TOKEN"]


def get_gelImage(tags):
    tags = list(tags)
    formatted_tags = ""
    rating = ""

    ratings = {
        "re": "rating%3aexplicit",
        "rq": "rating%3aquestionable",
        "rs": "rating%3asafe"
    }

    if tags:
        if tags[0] in ratings:
            rating = ratings[tags[0]]
            tags.remove(tags[0])

    if rating == "":
        rating = ratings["rs"]

    formatted_tags = "_".join(tags).replace("/", "+")

    print(rating, formatted_tags)

    api_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=50&tags={rating}+{formatted_tags}"
    response = requests.get(api_url)
    try:
        json_api_url = json.loads(response.text)
        image = random.choice(json_api_url)["file_url"]
        return image
    except ValueError:
        return "No results with given tags or they are incorrect."


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hey! GelBot's here! Type !gelhelp for help.")
        break


@bot.command()
async def gelhelp(ctx):
    message = help
    await ctx.send(message)


@bot.command()
async def gelnote(ctx):
    message = note
    await ctx.send(message)


@bot.command()
async def gelexamples(ctx):
    message = examples
    await ctx.send(message)


@bot.command()
async def gelratings(ctx):
    message = ratings
    await ctx.send(message)


@bot.command()
async def pic(ctx, *tags):
    if "rq" in tags or "re" in tags:
        if ctx.channel.is_nsfw():
            img = get_gelImage(tags)
            return await ctx.send(img)

        else:
            message = "For rating questionable or explicit NSFW channel is required!"
            return await ctx.send(message)

    img = get_gelImage(tags)
    await ctx.send(img)

bot.run(bot_token)
