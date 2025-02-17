from discord.ext import commands as cmd
from prettytable import PrettyTable
from datetime import datetime, timedelta

from utils import formatter, helpers


class Basics(cmd.Cog, name="\u200BOthers"):
    def __init__(self, bot):
        self.bot = bot

    @cmd.command()
    async def ping(self, ctx):
        """Pong"""
        await ctx.send(**ctx.em(f"I have a **latency** of **{round(self.bot.latency * 1000, 1)} ms**.", type="info"))

    @cmd.command()
    @cmd.has_permissions(administrator=True)
    async def leave(self, ctx):
        """Let the bot leave"""
        await ctx.send("bye ;(")
        await ctx.guild.leave()

    @cmd.command(aliases=['shardid'])
    async def shard(self, ctx, guild_id: int = None):
        """
        Get the shard id for this or any guild


        __Arguments__

        **guild_id**: The id of the guild


        __Examples__

        ```{c.prefix}shard```
        ```{c.prefix}shard 838488579140354049```
        """
        guild_id = guild_id or ctx.guild.id
        shard_id = (guild_id >> 22) % self.bot.shard_count
        await ctx.send(**ctx.em(
            f"The guild with the id **{guild_id}** is on **shard {shard_id}** "
            f"(cluster {round(shard_id / ctx.config.per_cluster)}).",
            type="info"
        ))

    @cmd.command()
    @cmd.cooldown(1, 10, cmd.BucketType.channel)
    async def shards(self, ctx):
        """Get a list of shards"""
        table = PrettyTable()
        table.field_names = ["Shard-Id", "Latency", "Guilds", "Users"]
        shards = await self.bot.get_shards()
        for shard in sorted(shards, key=lambda s: s["id"]):
            latency = f"{round(shard['latency'] * 1000, 1)} ms"
            if (datetime.utcnow() - shard["seen"]) > timedelta(minutes=3):
                latency = "offline?"

            table.add_row([str(shard["id"]), latency, helpers.format_number(shard["guilds"]),
                           helpers.format_number(shard["users"])])

        pages = formatter.paginate(str(table))
        for page in pages:
            await ctx.send(f"```diff\n{page}```")

    @cmd.command()
    async def invite(self, ctx):
        """Invite ServerCloner"""
        await ctx.send(**ctx.em(
            "**Invite Xenon**\n\n"
            f"[ServerCloner]({ctx.bot.invite})\n"
            type="info"
        ))

    @cmd.command(aliases=["i", "stats", "status", "about"])
    @cmd.cooldown(1, 10, cmd.BucketType.user)
    async def info(self, ctx):
        """Get Information about ServerCloner"""
        embed = ctx.em("")["embed"]
        embed.description = "Server Backups, Templates and more"
        embed.title = "ServerCloner"
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Invite", value=f"[Click Here]({ctx.bot.invite})")
        embed.add_field(name="Discord", value="[Click Here](https://discord.club/discord)")
        embed.add_field(name="Prefix", value=ctx.config.prefix)
        embed.add_field(name="Guilds", value=helpers.format_number(await self.bot.get_guild_count()))
        embed.add_field(name="Shards", value=self.bot.shard_count or 1)
        embed.add_field(name="Users", value=helpers.format_number(await self.bot.get_user_count()))

        app_info = await ctx.bot.application_info()
        if app_info.team:
            embed.set_footer(text=f"Owned by {app_info.team.owner}")

        else:
            embed.set_footer(text=f"Owned by {app_info.owner}")

        await ctx.send(embed=embed)


    @cmd.Cog.listener()
    async def on_guild_join(self, guild):
        if len(guild.text_channels) > 0:
            destination = guild.text_channels[0]

        else:
            destination = guild.owner

        try:
            await destination.send(**self.bot.em(
                "__Thanks for adding ServerCloner to your server!__ 😃\n"
                f"Use `{self.bot.config.prefix}help` to get a list of commands. If you need more information, "
                "It's also recommended to join our discord server to get notified "
                "about future updates.\n\n"
                "If you decide to use ServerCloner, **you and all your members need to accept our "
                type="info"
            ))

        except Exception:
            pass


def setup(bot):
    bot.add_cog(Basics(bot))
