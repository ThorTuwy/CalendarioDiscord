import libs.Calendario as Calendario
import libs.Screenshots as Screenshots

import discord,os 

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

meses=[
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

StartMessege="""**Versión web:**
https://nextcloud.tuwy.win/apps/calendar/embed/nMFRLZPC3Bp6Kb4g/dayGridMonth/now

También podéis poner los exámenes/trabajos de este horario en vuestro personal, "suscribiendo" a este horario: 
https://nextcloud.tuwy.win/remote.php/dav/public-calendars/nMFRLZPC3Bp6Kb4g?export
"""

GUILD_ID=int(os.getenv('GUILD_ID'))
CHANNEL_ID=int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

@bot.slash_command(guild_ids=[GUILD_ID])  # Create a slash command
async def añadair_calendario(ctx: discord.ApplicationContext,titulo,dia:int,mes:int,hora:int):
    """Añade una examen/trabajo al calendario"""
    try:
        dateObj=datetime(datetime.now().year, mes, dia, hora)
        await ctx.respond(f"Añadiendo el examen/trabajo al calendario")
        Calendario.addObjectToCalender(titulo,dateObj)

        
        await bot.get_guild(GUILD_ID).get_channel(CHANNEL_ID).purge()

        await bot.get_guild(GUILD_ID).get_channel(CHANNEL_ID).send(StartMessege)

        for month in os.getenv("months").split(","):
            month_name=meses[int(month)-1]
            
            ScreenshotsFil=[]
            
            month=str(month)
            month="0"+month if len(month)==1 else month

            await Screenshots.calenderMonth(month)

            ScreenshotsFil.append(discord.File(os.path.join("screenshots", month+".png")))



            await bot.get_guild(GUILD_ID).get_channel(CHANNEL_ID).send(f"{month_name}: ",files=ScreenshotsFil)

            

        

            
        

    except Exception as error:
        print(error)
        await ctx.respond(f"La fecha no ha sido introducida correctamente, mes,dia y hora se expresan como un numero (3,4,18) seria 4 de marzo a las 18:00")

bot.run(os.getenv('discord_token'))