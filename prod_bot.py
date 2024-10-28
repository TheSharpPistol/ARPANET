import discord
from discord import app_commands
from discord.ext import commands
import datetime
import os
import asyncio
import signal
import requests

BOT = commands.Bot(command_prefix="!", intents=discord.Intents.all())

canal_de_apps = 1198638547045978274
canal_de_resultados = 1300274120897986641
canal_de_info = 1076728328989442110

activedms = {}
foundids = {}
doneapps = {}

class Question():
    def __init__(self, Question:str, Answer:str="", isShort=False):
        self.Question = Question
        self.Answer = Answer
        self.isShort = isShort

class Role():
    def __init__(self, Name, DiscordID, RobloxID):
        self.Name = Name
        self.DiscordID = DiscordID
        self.RobloxID = RobloxID
        
class RolesTem():
    def __init__(self):
        self.ClaseD = Role("Clase D", 1070754678285017139, 39486779)
        self.Nivel0 = Role("Nivel 0", 1198640134560694313, 39669744)
        self.Nivel1 = Role("Nivel 1", 1100646750865326141, 39688927)
        self.Nivel2 = Role("Nivel 2", 1100646828858421280, 39982200)
        self.Nivel3 = Role("Nivel 3", 1100646906469810277, 39994995)
        self.Nivel4 = Role("Nivel 4", 1100646981279436852, 39995012)
        self.Nivel5 = Role("Nivel 5", 1100647047423590410, 42590376)
        self.O5 = Role("O5", 1070754678310174830, 0)
        self.O5X = Role("O5X", 1070754678310174831, 0)
        self.O5Y = Role("O5Y", 1205322884411695195, 0)
        self.Admin = Role("Admin", 1070754678331166852, 0)
        
    def getRoleFromDiscordID(self, DiscordID:int) -> Role:
        for role in self.__dict__.values():
            if role.DiscordID == DiscordID:
                return role
            
    def getRoleFromRobloxID(self, RobloxID:int) -> Role:
        for role in self.__dict__.values():
            if role.RobloxID == RobloxID:
                return role

class Application():
    def __init__(self, ID, Title, Questions:list, NextRank:Role, ApplicableRoles, CheckableRoles, ApproveVotes=1):
        self.ID = ID
        self.Title = Title
        self.Questions = Questions
        self.NextRank = NextRank
        self.ApplicableRoles = ApplicableRoles
        self.CheckableRoles = CheckableRoles
        self.ApproveVotes = ApproveVotes
        
class EnumTem():
    def __init__(self):
        self.Roles = RolesTem()
        
Enum = EnumTem()
        
class ApplicationsTem():
    def GetNivel0(self):
        return Application(
            0,
            "Nivel 0",
            [
                Question("¿Tiene su cuenta de Roblox verificada en el grupo de Discord?", isShort=True),
                Question("Indique una habilidad personal suya que podría ser esencial al momento de ser personal oficial de la fundación."),
                Question("¿Qué te inspiró a unirte a nuestra fundación?"),
                Question("¿Cuál es el protocolo estándar a seguir en caso de brecha de algún SCP?"),
                Question("Indique su departamento favorito dentro de la fundación e indique el por qué lo es.")
            ],
            Enum.Roles.Nivel0,
            [Role("WebMNG", 1146208459579215912, 0), Enum.Roles.ClaseD, Role("CD", 1195463118516670675, 0)],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetNivel1(self):
        return Application(
            1,
            "Nivel 1",
            [
                Question("En caso de que algún clase-D logre escapar de su celda y usted lo encuentre deambulando por los pasillos, ¿Qué procedimiento seguiría usted? Sea detallado."),
                Question("Explique la diferencia entre un SCP clase Euclid y un SCP clase Keter en términos de contención y peligro."),
                Question("Nombre y explique al menos 3 amenazas o peligros mas comunes dentro de la instalación."),
                Question("¿Por qué es esencial el anonimato y la ocultación de la Fundación SCP, y como se logra?")
            ],
            Enum.Roles.Nivel1,
            [Role("WebMNG", 1146208459579215912, 0), Enum.Roles.Nivel0],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    
    def GetNivel2(self):
        return Application(
            2,
            "Nivel 2",
            [
                Question("¿De qué se encarga tu departamento? Explique también lo que mas le gusta sobre este."),
                Question("Explique el procedimiento que debe de ser llevado a cabo como un personal de fundación si ocurra una fuga de clases D. Recuerda ser detallado."),
                Question("Nombre al menos 2 métodos de comunicación durante una brecha de contención. Explicarse bien."),
                Question("¿Por qué la Ética es un aspecto crítico de la Fundación SCP, y cómo se refleja en las acciones de los miembros?"),
                Question("¿Cuál es la importancia de las investigaciones de los SCP dentro de la fundación?")
            ],
            Enum.Roles.Nivel2,
            [Role("WebMNG", 1146208459579215912, 0), Enum.Roles.Nivel1],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetEtica(self):
        return Application(
            3,
            "Interes en el Comite de Etica",
            [
                Question("Esta aplicacion cumple solo con el proposito de mostrar tu interes en unirte al comite.", isShort=True),
                Question("¿Por que te gustaria unirte al comite de etica?"),
                Question("Describe tus conocimientos acerca de comite de etica.")
            ],
            None,
            [Enum.Roles.Nivel0, Enum.Roles.Nivel1, Enum.Roles.Nivel2, Enum.Roles.Nivel3, Enum.Roles.Nivel4, Enum.Roles.Nivel5],
            [Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetSeguridad(self):
        return Application(
            4,
            "Departamento de Seguridad",
            [
                Question("¿Cual es la funcion del Departamento de Seguridad?"),
                Question("¿Si encuentras un SCP como recluta que harias?"),
                Question("¿Cual es el procedimiento si un Clase D cruza la linea?"),
                Question("¿Que acciones deberia tomar el personal de seguridad para un test?"),
                Question("Redacta el brief dado a los Clase D para los tests.")
            ],
            None,
            [Enum.Roles.Nivel0, Enum.Roles.Nivel1, Enum.Roles.Nivel2, Enum.Roles.Nivel3, Enum.Roles.Nivel4, Enum.Roles.Nivel5],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetCiencia(self):
        return Application(
            5,
            "Departamento Cientifico",
            [
                Question("¿Cual es la funcion del Departamento Cientifico?"),
                Question("¿Por qué quiere unirse a este departamento?"),
                Question("Como aprendíz ¿Tiene el permiso de realizar un test clase Euclid/Keter?", isShort=True),
                Question("Si en un test un SCP logra escapar ¿Que procedimiento crees que deberías de seguir?"),
                Question("Nombre y describa un SCP Euclid.")
            ],
            None,
            [Enum.Roles.Nivel1, Enum.Roles.Nivel2, Enum.Roles.Nivel3, Enum.Roles.Nivel4, Enum.Roles.Nivel5],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetIngenieria(self):
        return Application(
            6,
            "Ingenieria & Servicio Tecnico",
            [
                Question("¿Por qué quieres unirte al departamento de Ingeniería y Servicio Técnico?"),
                Question("En términos simples, ¿Qué es un servidor y que funciones cumple?"),
                Question("Alguien esta abusando del sistema de luces y alarmas ¿Qué es lo que harías?"),
                Question("Hay una brecha de contención y estás haciendo una prueba de luces ¿Qué harías?"),
                Question("¿En que situaciones en necesario el uso de cámaras?")
            ],
            None,
            [Enum.Roles.Nivel0, Enum.Roles.Nivel1, Enum.Roles.Nivel2, Enum.Roles.Nivel3, Enum.Roles.Nivel4, Enum.Roles.Nivel5],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
    def GetMedicina(self):
        return Application(
            7,
            "Departamento Medico",
            [
                Question("¿De que se encarga el departamento Médico?."),
                Question("Explica que es lo que mas te gusta del departamento."),
                Question("¿Qué procedimiento se llevaría acabo en caso de una infección/contagios en el sitio o sea como debería actuar el departamento médico?"),
                Question("Explique con sus palabras como curaria a las siguientes personas con las siguientes enfermedades/heridas. Una tiene una herida de bala en el pecho y otra tiene congelación."),
                Question("¿Que es la bronquitis?")
            ],
            None,
            [Enum.Roles.Nivel1, Enum.Roles.Nivel2, Enum.Roles.Nivel3, Enum.Roles.Nivel4, Enum.Roles.Nivel5],
            [Enum.Roles.Nivel4, Enum.Roles.Nivel5, Enum.Roles.O5, Enum.Roles.O5X, Enum.Roles.O5Y, Enum.Roles.Admin],
            3
        )
        
RobloxSession = requests.Session()
RobloxSession.cookies[".ROBLOSECURITY"] = os.environ["ROBLOXSECURITY"]

def rbx_request(method, url, **kwargs):
    request = RobloxSession.request(method, url, **kwargs)
    print(request.headers)
    method = method.lower()
    if (method == "post") or (method == "put") or (method == "patch") or (method == "delete"):
        if "X-CSRF-TOKEN" in request.headers:
            RobloxSession.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
            if request.status_code == 401:  # Request failed, send it again
                request = RobloxSession.request(method, url, **kwargs)
                print(request.content)
                print(request.status_code)
                print(request.headers)
    return request
        
class User:
    def __init__(self, DiscordUser:discord.User, RobloxID:int):
        self.DiscordUser = DiscordUser
        self.RobloxID = RobloxID
    def InitFromDiscordUser(DiscordUser:discord.User):
        print(DiscordUser.id)
        if foundids.get(DiscordUser.id):
            return User(DiscordUser, foundids.get(DiscordUser.id))
        else:
            rq = requests.get(f"https://api.blox.link/v4/public/guilds/1070754678247280640/discord-to-roblox/{DiscordUser.id}",
                              headers={"Authorization" : os.environ["BLOXLINK_PROD_API_KEY"]})
            match rq.status_code:
                case 200:
                    foundids[DiscordUser.id] = rq.json()["robloxID"]
                    print(foundids[DiscordUser.id])
                    return User(DiscordUser, foundids[DiscordUser.id])
                case _:
                    raise Exception("User not found")
    def UpdateRank(self, Role:Role):
        rq = rbx_request("patch", f"https://groups.roblox.com/v1/groups/6059381/users/{self.RobloxID}", json={"roleId" : Role.RobloxID})
        print(rq.status_code)
        print(rq.content)

Enum.Applications = ApplicationsTem()
            
class EmbedLibrary:
    def getCancelEmbed():
        embed = discord.Embed(
            title="La operacion se ha cancelado",
            timestamp = datetime.datetime.now(),
            color=9705753
        )
        embed.set_footer(text="Fundacion SCP",icon_url="https://tr.rbxcdn.com/ca679fbc7704077a5831a7dedd98a014/150/150/Image/Png")
        return embed

    def getErrorEmbed(e:str):
        if e != "":
            message = e
        else:
            message = "Un error desconocido ha ocurrido"
        embed = discord.Embed(
            title=message,
            timestamp = datetime.datetime.now(),
            description="Contactar <@986737559705124884>" if message == "Un error desconocido ha ocurrido" else "",
            color=9705753
        )
        embed.set_footer(text="Fundacion SCP",icon_url="https://tr.rbxcdn.com/ca679fbc7704077a5831a7dedd98a014/150/150/Image/Png")
        return embed

    def getWaitEmbed():
        embed = discord.Embed(
            title="Por favor espere...",
            description="Si este proceso tarda mas de 60 segundos contactar <@986737559705124884>",
            timestamp = datetime.datetime.now(),
            color=16765440
        )
        embed.set_footer(text="Fundacion SCP",icon_url="https://tr.rbxcdn.com/ca679fbc7704077a5831a7dedd98a014/150/150/Image/Png")
        return embed
    
    def getGeneralEmbed(title:str, description:str, color=0):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp = datetime.datetime.now(),
        )
        embed.set_footer(text="Fundacion SCP",icon_url="https://tr.rbxcdn.com/ca679fbc7704077a5831a7dedd98a014/150/150/Image/Png")
        return embed    
    
    def getAppEmbed(user:discord.User, app:Application):
        embed = discord.Embed(
            title=user.display_name+ f" (@{user.name})",
            timestamp = datetime.datetime.now(),
        )
        embed.set_author(name=app.Title, icon_url=user.avatar.url)
        embed.set_footer(text="Fundacion SCP",icon_url="https://tr.rbxcdn.com/ca679fbc7704077a5831a7dedd98a014/150/150/Image/Png")
        for Question in app.Questions:
            embed.add_field(name=Question.Question, value=Question.Answer, inline=False)
        return embed
    
runningApps = EmbedLibrary.getGeneralEmbed("Aplicaciones Pendientes", "")
runningAppsMessage = None

deleteOnShutdown = []

@BOT.event
async def on_ready():
    global runningAppsMessage
    print(f"discord bot online as {BOT.user}")  
    print(runningApps)
    try:
        synced = await BOT.tree.sync()
        print(f"Synced {len(synced)} commands")
        
        runningAppsMessage = await BOT.get_channel(canal_de_info).send(embed=runningApps)
        deleteOnShutdown.append(runningAppsMessage)
        
        options = []
        
        for Application in [method for method in dir(Enum.Applications) if callable(getattr(Enum.Applications, method)) if not method.startswith('_')]:
            Application = getattr(Enum.Applications, Application)()
            for _ in Application.ApplicableRoles:
                    options.append(discord.SelectOption(label=Application.Title, value=Application.ID))
                    break
            del Application
        
        select = discord.ui.Select(options=options)
        
        async def select_callback(interaction:discord.Interaction):
            for Application in [method for method in dir(Enum.Applications) if callable(getattr(Enum.Applications, method)) if not method.startswith('_')]:
                Application = getattr(Enum.Applications, Application)()
                if Application.ID == int(interaction.data["values"][0]):
                    Application = Application
                    print(f"{interaction.user.name} ha iniciado una aplicacion para {Application.Title}")
                    found = False
                    for Role in Application.ApplicableRoles:
                        if interaction.user.get_role(Role.DiscordID):
                            found = True
                    if not found:
                        await interaction.response.send_message(embed=EmbedLibrary.getErrorEmbed("Usted no tiene permiso para realizar esta aplicacion"), ephemeral=True, delete_after=5)
                        return
                    if doneapps.get(interaction.user.id):
                        if Application.ID in doneapps[interaction.user.id]:
                            await interaction.response.send_message(embed=EmbedLibrary.getErrorEmbed("Ya has aplicado a esta aplicacion"), ephemeral=True, delete_after=5)
                            return
                    break
            
            async def cancel_cb(interaction:discord.Interaction):
                global runningApps, runningAppsMessage
                try:
                    del activedms[interaction.user.dm_channel.id]
                except:
                    await interaction.user.dm_channel.send(embed=EmbedLibrary.getErrorEmbed("Esta app ya ha sido enviada o cancelada"))
                else:
                    await interaction.user.dm_channel.send(embed=EmbedLibrary.getCancelEmbed())
                    await runningAppsMessage.edit(embed=runningApps)
                finally:
                    await interaction.message.edit(view=None)
                
                
            cancel_button = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.red)
            cancel_button.callback = cancel_cb
            
            view = discord.ui.View(timeout=None)
            view.add_item(cancel_button)
            
            await interaction.user.send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", Application.Questions[0].Question), view=view)
            
            activedms[interaction.user.dm_channel.id] = Application
            
            await interaction.response.send_message(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", "Revisa tus mensajes privados"), ephemeral=True, delete_after=5)
        
        select.callback = select_callback
        
        view = discord.ui.View(timeout=None)
        view.add_item(select)
        
        mes1 = await BOT.get_channel(canal_de_info).send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", "Seleccione que aplicacion desea:"), view=view)
        deleteOnShutdown.append(mes1)
        
        asyncio.get_event_loop().add_signal_handler(signal.SIGTERM, sigtermHandler)
    except Exception as e:
        print(e)
        
def checkuser(interaction:discord.Interaction) -> bool:
    return interaction.user.id in (
        986737559705124884, #yo
        511732131928473603, #alaska
        511732131928473603, #yaku
        754491675102937098 #max
    )
        
@BOT.event
async def on_message(message:discord.Message):
    if message.channel.id in activedms and message.author.id != BOT.user.id:
        Application = activedms[message.channel.id]
        respond = True
        for Question in Application.Questions:
            if Question.Answer == "":
                if len(message.content) > 1024:
                    await message.channel.send(embed=EmbedLibrary.getErrorEmbed("La respuesta no puede tener mas de 1024 caracteres"))
                    await message.channel.send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", Application.Questions[Application.Questions.index(Question)].Question))
                    respond = False
                    break
                elif len(message.content) < 100 and not Question.isShort:
                    await message.channel.send(embed=EmbedLibrary.getErrorEmbed("La respuesta no puede tener menos de 100 caracteres"))
                    await message.channel.send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", Application.Questions[Application.Questions.index(Question)].Question))
                    respond = False
                    break
                else:
                    Question.Answer = message.content
                    break
        if Application.Questions[-1].Answer != "":
            
            async def accept_callback(interaction:discord.Interaction):
                global runningApps, runningAppsMessage
                for Field in runningApps.fields:
                    if Field.value == f"<@{message.author.id}>":
                        runningApps.remove_field(runningApps.fields.index(Field))
                        break
                await runningAppsMessage.edit(embed=runningApps)
                await interaction.message.edit(view=None, content=f"{interaction.message.content} ha sido aceptado por <@{interaction.user.id}>")
                if Application.NextRank != None:
                    ruser = User.InitFromDiscordUser(message.author)
                    ruser.UpdateRank(Application.NextRank)
                await BOT.get_channel(canal_de_resultados).send(f"La aplicacion de {interaction.message.content} para **`{Application.Title}`** ha sido aprobada por <@{interaction.user.id}> ({interaction.message.to_reference().jump_url})", silent=True)
                await BOT.get_user(int(interaction.message.content.removeprefix("<@").removesuffix(">"))).send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", f"Felicitaciones! Has aprobado tu aplicacion para **`{Application.Title}`**", color=4385571))
                
            async def deny_callback(interaction:discord.Interaction):
                global runningApps, runningAppsMessage
                for Field in runningApps.fields:
                    if Field.value == f"<@{message.author.id}>":
                        runningApps.remove_field(runningApps.fields.index(Field))
                        break
                await runningAppsMessage.edit(embed=runningApps)
                await interaction.message.edit(view=None, content=f"{interaction.message.content} ha sido denegada por <@{interaction.user.id}>")
                await BOT.get_channel(canal_de_resultados).send(f"La aplicacion de {interaction.message.content} para **`{Application.Title}`** ha sido denegada por <@{interaction.user.id}> ({interaction.message.to_reference().jump_url})", silent=True)
                await BOT.get_user(int(interaction.message.content.removeprefix("<@").removesuffix(">"))).send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", f"Lamentablemente, has reprobado tu aplicacion para **`{Application.Title}`**", color=9705753))
        
            accept_button = discord.ui.Button(label="Aceptar", style=discord.ButtonStyle.green)
            accept_button.callback = accept_callback
            
            deny_button = discord.ui.Button(label="Denegar", style=discord.ButtonStyle.red)
            deny_button.callback = deny_callback
            
            view = discord.ui.View(timeout=None)
            view.add_item(accept_button)
            view.add_item(deny_button)
            
            async def send_cb(interaction:discord.Interaction):
                global runningAppsMessage, runningApps
                runningApps = runningApps.add_field(name=Application.Title, value=f"<@{interaction.user.id}>", inline=False)
                if doneapps.get(message.author.id):
                    doneapps[message.author.id].append(Application.ID)
                else:
                    doneapps[message.author.id] = [Application.ID]
                await runningAppsMessage.edit(embed=runningApps)
                await BOT.get_channel(canal_de_apps).send(content=f"<@{message.author.id}>", embed=EmbedLibrary.getAppEmbed(message.author, Application), view=view)
                await interaction.message.edit(view=None)
                await message.channel.send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", "Gracias por aplicar!"))
                
            async def cancel_cb(interaction:discord.Interaction):
                await interaction.edit_original_response(view=None)
                await message.channel.send(embed=EmbedLibrary.getCancelEmbed())
                del activedms[message.channel.id]
            
            sendbutton = discord.ui.Button(label="Enviar", style=discord.ButtonStyle.green)
            sendbutton.callback = send_cb
            
            cancelbutton = discord.ui.Button(label="Cancelar", style=discord.ButtonStyle.red)
            cancelbutton.callback = cancel_cb
            
            view2 = discord.ui.View(timeout=None)
            view2.add_item(sendbutton)
            view2.add_item(cancelbutton)
            
            try:
                del activedms[message.channel.id]
            except:
                pass
            finally:
                await message.channel.send(content=f"<@{message.author.id}>", embed=EmbedLibrary.getAppEmbed(message.author, Application), view=view2)
        elif respond:
            await message.channel.send(embed=EmbedLibrary.getGeneralEmbed("Aplicacion", Application.Questions[Application.Questions.index(Question)+1].Question))
                       

async def onfailcheck(interaction:discord.Interaction, error=None):
    await interaction.response.send_message(embed=EmbedLibrary.getErrorEmbed("No tienes permitido usar este comando"), ephemeral=True, delete_after=5)
    
@BOT.tree.error(onfailcheck)    
async def pas(*args, **kwargs):
    pass

def sigtermHandler():
    for message in deleteOnShutdown:
        message.delete()



BOT.run(os.environ["FUNDACION_PROD_BOT_TOKEN"])

