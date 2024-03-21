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

También podéis poner los exámenes/trabajos de este horario en el vuestro personal, "suscribiendos" a este horario: 
https://nextcloud.tuwy.win/remote.php/dav/public-calendars/nMFRLZPC3Bp6Kb4g?export
"""

GUILD_ID=int(os.getenv('GUILD_ID'))
CHANNEL_ID=int(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)




conversorHoras=[[23,59],[8,15],[9,10],[10,5] , [11,30],[12,25],[13,20]]


Running=False

@bot.slash_command(guild_ids=[GUILD_ID])  # Create a slash command
async def añadair_calendario(ctx: discord.ApplicationContext,titulo,dia:int,mes:int,hora:discord.Option(str, choices=["Ninguna en especifico","1º","2º","3º","4º","5º","6º"]) ):
    """Añade una examen/trabajo al calendario"""
    global Running
    
    if Running:
        await ctx.respond(f"Bot sigue en ejecucion, porfavor intentelo cuando termine",delete_after=5)
        return

    try:
        Running=True

        rato=[]

        if hora=="Ninguna en especifico":
            hora=0
        else:
            hora=int(hora[0])

        if hora<0 or hora>7:
            await ctx.respond(f"La hora no es correcta, tiene que poner un numero que represente la hora que es, si es a 3º hora ponga un 3, si no tiene hora concreta ponga un 0")
            return

        rato=conversorHoras[hora]

        dateObj=datetime(datetime.now().year, mes, dia, rato[0],rato[1])
        await ctx.respond(f"Añadiendo el examen/trabajo al calendario",delete_after=5)
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
        await ctx.respond(f"La fecha no ha sido introducida correctamente, mes,dia y hora se expresan como un numero (3,4,18) seria 4 de marzo a las 18:00",delete_after=10)
    
    Running=False

bot.run(os.getenv('discord_token'))