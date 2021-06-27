import requests
import json
from discord.ext import commands
import random
from notes import help, note, examples, ratings
import os


bot = commands.Bot(command_prefix='!')
bot_token = os.environ["BOT_TOKEN"]


def get_gelImage(tags):
    """Returns pictures from Gelbooru with given tags."""
    tags = list(tags)
    formatted_tags = ""
    rating = ""

    ratings = {
        "re": "rating%3aexplicit",
        "rq": "rating%3aquestionable",
        "rs": "rating%3asafe"
    }

    if tags:  # if there are any tags, check for ratings
        if tags[0] in ratings:
            rating = ratings[tags[0]]
            tags.remove(tags[0])

    if rating == "":  # if rating wasn't specified, set safe one
        rating = ratings["rs"]

    # make tags suitable for Gelbooru API url
    formatted_tags = "_".join(tags).replace("/", "+")

    print(rating, formatted_tags)

    api_url = f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=50&tags={rating}+{formatted_tags}"
    response = requests.get(api_url)

    # parsing json
    json_api_url = json.loads(response.text)

    # verify if there is anything within given tags
    if json_api_url:
        image = random.choice(json_api_url)["file_url"]
        return image
    else:
        return "No results with given tags or they are incorrect."


@bot.event
async def on_ready():
    """Sends information when the bot starts running."""
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_guild_join(guild):
    """Triggers a message when the bot joins a server."""
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("Hey! GelBot's here! Type !gelhelp for help.")
        break


# commands below take messages from notes.py file
@bot.command()
async def gelhelp(ctx):
    """Sends the help message."""
    message = help
    await ctx.send(message)


@bot.command()
async def gelnote(ctx):
    """Sends the disclaimer."""
    message = note
    await ctx.send(message)


@bot.command()
async def gelexamples(ctx):
    """Sends the examples."""
    message = examples
    await ctx.send(message)


@bot.command()
async def gelratings(ctx):
    """Sends information about ratings."""
    message = ratings
    await ctx.send(message)


@bot.command()
async def pic(ctx, *tags):
    """Calls get_gelImage() with tags specified by user, then sends an image."""
    if "rq" in tags or "re" in tags:
        if ctx.channel.is_nsfw():  # check if channel is suitable for given rating
            img = get_gelImage(tags)
            return await ctx.send(img)

        else:
            message = "For rating questionable or explicit NSFW channel is required!"
            return await ctx.send(message)

    img = get_gelImage(tags)
    await ctx.send(img)

bot.run(bot_token)
