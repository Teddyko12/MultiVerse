import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio
import random

TOKEN = 'შენი_ახალი_ბოტის_ტოკენი'
TEDDY_ID = 752411942664142988

# --- მონაცემების დროებითი შენახვა (ჯობია მერე JSON-ში გადაიტანო) ---
server_configs = {}

class NewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅Wocka Flocka | Is Online Bleadddd")

bot = NewBot()

# დამხმარე ფუნქცია უფლებების შესამოწმებლად
def is_admin_or_teddy(interaction: discord.Interaction):
    return interaction.user.id == TEDDY_ID or interaction.user.guild_permissions.administrator

# --- 📥 Welcome & Auto-role ლოგიკა ---
@bot.event
async def on_member_join(member):
    guild_id = member.guild.id
    if guild_id not in server_configs: return

    # 1. Auto-role
    role_id = server_configs[guild_id].get("auto_role_id")
    if role_id:
        role = member.guild.get_role(role_id)
        if role: 
            try: await member.add_roles(role)
            except: print(f"Rolis Micemis problemaa mimartet tedis {member.guild.name}-ზე")

    # 2. Welcome
    welcome_ch_id = server_configs[guild_id].get("welcome_channel")
    if welcome_ch_id:
        channel = member.guild.get_channel(welcome_ch_id)
        if channel:
            embed = discord.Embed(
                title="👋 მოგესალმებით!",
                description=f"გამარჯობა {member.mention}, კეთილი იყოს შენი მობრძანება ჩვენს სერვერზე!",
                color=0x00ffcc
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1414754756580081774/1460348568563880006/ppp.jpg")
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"წევრი #{len(member.guild.members)}")
            await channel.send(content=member.mention, embed=embed)

# --- 🛠️ ბრძანებები ---

@bot.tree.command(name="welcome_setup", description="daayene welcome system 1 wutshi da 20 wamshi zustad")
async def w_setup(interaction: discord.Interaction):
    if not is_admin_or_teddy(interaction):
        return await interaction.response.send_message("❌ am brdzanebas ver gamoiyenebT", ephemeral=True)
    
    guild_id = interaction.guild.id
    if guild_id not in server_configs: server_configs[guild_id] = {}
    server_configs[guild_id]["welcome_channel"] = interaction.channel.id
    await interaction.response.send_message(f"✅ welcome arxi shesrialda am arxshi: {interaction.channel.mention}", ephemeral=True)

@bot.tree.command(name="wtest", description="gateste welcome marto shen xedav")
async def wtest(interaction: discord.Interaction):
    if not is_admin_or_teddy(interaction):
        return await interaction.response.send_message("❌", ephemeral=True)
    
    embed = discord.Embed(
        title="🎉 Welcome Test",
        description=f"ase gamochndeba misalmeba {interaction.user.mention}-stvis!",
        color=0x00ffcc
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/1414754756580081774/1460348568563880006/ppp.jpg")
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"wevri #{len(interaction.guild.members)}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="autorole", description="daayene avtomaturi roli !!!")
async def autorole(interaction: discord.Interaction, role: discord.Role):
    if not is_admin_or_teddy(interaction):
        return await interaction.response.send_message("❌", ephemeral=True)
    
    guild_id = interaction.guild.id
    if guild_id not in server_configs: server_configs[guild_id] = {}
    server_configs[guild_id]["auto_role_id"] = role.id
    await interaction.response.send_message(f"✅ Avto Roli araoficialurad dayenda :  **{role.name}**", ephemeral=True)

@bot.tree.command(name="giveaway", description="moxode gatamasheba")
async def giveaway(interaction: discord.Interaction, time: str, prize: str):
    if not is_admin_or_teddy(interaction):
        return await interaction.response.send_message("❌", ephemeral=True)
    
    # დროის გათვლა (სკრიპტი მუშაობს s, m, h-ზე)
    try:
        seconds = int(time[:-1]) * (60 if time.endswith('m') else 3600 if time.endswith('h') else 1)
    except:
        return await interaction.response.send_message("❌ gamoiyene formati: 30s, 5m an 1h", ephemeral=True)

    embed = discord.Embed(title="🎉 გათამაშება!", description=f"🎁 პრიზი: **{prize}**\n⏰ დრო: {time}\n👤 ორგანიზატორი: {interaction.user.mention}", color=0xff0066)
    embed.set_footer(text="მონაწილეობისთვის დააჭირე 🎉")
    
    await interaction.response.send_message("✅ gatamasheba daiwkoooo", ephemeral=True)
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction("🎉")

    await asyncio.sleep(seconds)

    new_msg = await interaction.channel.fetch_message(msg.id)
    users = [user async for user in new_msg.reactions[0].users() if not user.bot]
    
    if not users:
        await interaction.channel.send(f"😔 Gatamashebashi (**{prize}**) Aravin miigo Monawileoba Shegircxvat namusi")
    else:
        winner = random.choice(users)
        await interaction.channel.send(f"🎊 გილოცავ {winner.mention}! შენ მოიგე **{prize}**!")

@bot.tree.command(name="news", description="gamoaqveyne siaxle botis meshveobit botis saxelit wera shegidzlia ra ")
async def news(interaction: discord.Interaction, channel: discord.TextChannel, text: str):
    if not is_admin_or_teddy(interaction):
        return await interaction.response.send_message("❌", ephemeral=True)

    embed = discord.Embed(title="📢 სიახლე!", description=text, color=0xf1c40f, timestamp=datetime.datetime.now())
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
    embed.set_footer(text="News System")
    
    await channel.send(embed=embed)
    await interaction.response.send_message(f"✅ Siaxle Gaigzavna Prochis Gavlit {channel.mention}-shi gilocav", ephemeral=True)

bot.run(TOKEN)
