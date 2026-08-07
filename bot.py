import os
import discord
from discord.ext import commands

# ---------- ตั้งค่าตรงนี้ ----------
CHANNEL_ID = 1512382583453782057      # ห้องที่ให้พิมเพื่อรับยศ
ROLE_ID = 1500056205450805321         # ยศที่จะให้
TRIGGER_WORD = "รักพี่พีพี่รูซิวพี่เซ้น"  # คำที่ต้องพิมพ์ถึงจะถูก
WRONG_MSG = "มึงพิมไม่ถูกอีโง่"
CORRECT_MSG = "มึงได้ยศแล้ว ยินดีต้อนรับสู่โหนกระเจี๊ยว"
# -----------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        await bot.process_commands(message)
        return

    if message.content.strip() == TRIGGER_WORD:
        role = message.guild.get_role(ROLE_ID)

        if role is None:
            await message.channel.send("❌ หายศไม่เจอ เช็ค ROLE_ID อีกที")
            return

        if role in message.author.roles:
            await message.channel.send(f"{message.author.mention} มึงมียศนี้อยู่แล้ว")
        else:
            try:
                await message.author.add_roles(role)
                await message.channel.send(f"{message.author.mention} {CORRECT_MSG}")
            except discord.Forbidden:
                await message.channel.send("❌ บอทไม่มีสิทธิ์ให้ยศ (เอา Role บอทไปไว้สูงกว่ายศที่จะแจกในเซิร์ฟด้วย)")
    else:
        await message.channel.send(f"{message.author.mention} {WRONG_MSG}")

    await bot.process_commands(message)


bot.run(os.getenv("DISCORD_TOKEN"))
