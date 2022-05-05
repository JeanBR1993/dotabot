# Versão 2.0 do Bot Discord de dota
# Esse bot foi criado com o intuíto de melhorar a conveniência e convivência de usuários de canais do jogo DOTA 2 no
# Discord
# Eu, Jean, criador do robô permito o uso do mesmo para fins não lucrativos à partir da licença GPL (Licença Pública Geral)
# Não haverá mais atualizações, melhorias ou debugging do código por minha parte, é permitido no entanto que haja fork
# se alguém quiser continuar o trabalho nele.

import requests
import re
from discord.ext import commands

# Lista que guardará todos players cadastrados no bot
playerslist = []

# URL usada para puxar os dados dos jogadores
playerinfo = "https://api.opendota.com/api/players/"


# Objeto principal, cada jogador será construído usando-o e guardado na playerlist
class Player:

    # Função de construção
    def __init__(self, nome, profile_id):

        # Construção da URL final de cada usuário para extração de dados
        response = requests.get(playerinfo + profile_id)
        # Rotina pra controle de erros da API de extração
        if response.status_code != 200:
            print("API de output com problemas, chame o 'programador'", response.status_code)
            return
        else:
            list = response.text.split(",")

        # Atributos do objeto junto com os métodos de tratamento dos dados extraídos
        self.nome = nome
        self.profileid = profile_id
        self.mmr = get_mmr(list)
        self.nickname = get_nickname(list)
        self.avatar = get_avatar(list)

    #Único método do objeto, é usado para atualizar as estátísticas do mesmo
    def update(self):

        response = requests.get(playerinfo + self.profileid)
        if response.status_code > 200 or response.status_code < 200:
            print("API de output com problemas, chame o 'programador'", response.status_code)
            return
        else:
            list = response.text.split(",")

        self.mmr = get_mmr(list)
        self.nickname = get_nickname(list)
        self.avatar = get_avatar(list)


# Método de tratamento dos dados obtidos na API, extrai o MMR do jogador.
def get_mmr(data):

    mmrdirty = []
    mmrclean = ""

    for x in data:
        mmrdirty.append(re.findall('estimate":[0-9]+', x))

    mmrdirty.sort(reverse=True)
    mmrdirty = mmrdirty[0]
    for x in mmrdirty:
        for y in x:
            if y.isdigit():
                    mmrclean += y
    return int(mmrclean)

# Método de tratamento dos dados obtidos na API, extrai o nickname atual do jogador.
def get_nickname(data):

    dirtynick = []
    cleannick = ""

    for x in data:
        dirtynick.append(re.findall('personaname":".+', x))

    dirtynick.sort(reverse=True)
    dirtynick = dirtynick[0]
    for x in dirtynick:
        dirtynick = x

    counter = 0
    for x in dirtynick:

        if counter > 13:
            cleannick += x
        counter += 1
    return cleannick.rstrip('"')

# Método de tratamento dos dados obtidos na API, extrai o avatar atual do jogador.
# O avatar não está sendo mostrado na atual versão do bot por um bug de alguns canais do discord.
def get_avatar(data):

    dirtyavatar = []
    cleanavatar = ""

    for x in data:
        dirtyavatar.append(re.findall('avatarmedium":".+', x))

    dirtyavatar.sort(reverse=True)
    dirtyavatar = dirtyavatar[0]
    for x in dirtyavatar:
        dirtyavatar = x

    counter = 0
    for x in dirtyavatar:

        if counter > 14:
            cleanavatar += x
        counter += 1
    return cleanavatar.rstrip('"')
#-----------------------------------------------------------------------------------------------------------------------
# Término da definiação do objeto e dos métodos de tratamento de dados, começo da programação do bot
#-----------------------------------------------------------------------------------------------------------------------

# Definição do símbolo de texto usado para chamar o bot no chat do discord
bot = commands.Bot(command_prefix="$")

# Decorador de comandos do bot
@bot.command()
# Comando de ajuda com o qual o usuário obtém mais informações sobre cada comando
async def ajuda(ctx, arg):
    if arg == "criar":
        await ctx.send("Adiciona o jogador à lista de dados, é invocado com dois argumentos, nome e profileID, exemplo: '$criar Jean 51348142'")
    elif arg == "deletar":
        await ctx.send("Deleta o jogador da lista de dados, é invocado com um argumento: profileID, exemplo:'$deletar 51348142'")
    elif arg == "leaderboard":
        await ctx.send("Retorna a lista em ordem descrescente de MMR dos jogadores cadastrados, é invocado sem argumentos, exemplo:'$leaderboard'")
    elif arg == "mmr":
        await ctx.send("Retorna o MMR de um único jogador, é invocado com o nome de argumento, exemplo: '$mmr Jean'")
    elif arg == "jogadores":
        await ctx.send("Retorna a lista de jogadores cadastrados no bot com nome, nick e mmr, é invocado sem argumentos, exemplo: '$players'")
    elif arg == "atualizar":
        await ctx.send("Atualiza os dados de todos jogadores cadastrados na lista, retorna nenhum dado, é invocado sem argumentos, exemplo:'$atualizar'")
    else:
        await ctx.send("Não foi providenciado ou não existe o argumento dado, invoque '$comandos' para saber os disponíveis.")

@bot.command()
# Exibe todos comandos disponíveis para uso do Bot
async def comandos(ctx):
    await ctx.send("Comandos disponíveis: '$comandos', '$ajuda', '$criar', '$deletar', '$leaderboard', '$mmr', '$jogadores' e '$atualizar'; acesse ajuda com o nome do comando para saber como cada um funciona, exemplo: '$ajuda criar'")

@bot.command()
# Adiciona o jogador à lista de dados, é invocado com dois argumentos, nome e profileID, exemplo: '$criar Jean 51348142'
async def criar(ctx, name, steamid):
    for x in playerslist:
        if x.nome.lower() == name.lower():
            await ctx.send("Esse nome já é cadastrado na lista, escolha outro")
            return
        if x.profileid == steamid:
            await ctx.send("Esse profileID já está cadastrado na lista")
            return
    try:
        Player(name, steamid)
        playerslist.append(Player(name, steamid))
        await ctx.send("O player foi criado com sucesso")
    except:
        await ctx.send("Teve algum problema na criação do player, este não foi adicionado")

@bot.command()
# Deleta o jogador da lista de dados, é invocado com um argumento: profileID, exemplo:'$deletar 51348142'
async def deletar(ctx, steamid):
    for x in playerslist:
        if x.profileid == steamid:
            playerslist.remove(x)
            del x
            await ctx.send("O player foi deletado com sucesso")
            return
    await ctx.send("Essa SteamId não é vinculada à nenhum player cadastrado ou foi dado outro argumento")

@bot.command()
# Retorna a lista de jogadores cadastrados no bot com nome, nick e mmr, é invocado sem argumentos, exemplo: '$players'
async def jogadores(ctx):
    strfinal = "Os jogadores cadastrados são: "
    for x in playerslist:
        temp = x.nome + " com nick: " + x.nickname + " / "
        strfinal += temp
    await ctx.send(strfinal)


@bot.command()
# Atualiza os dados de todos jogadores cadastrados na lista, é invocado sem argumentos, exemplo:'$atualizar'
async def atualizar(ctx):
    for x in playerslist:
        try:
            x.update()
        except:
            await ctx.send("As informações de {jogador} não foram atualizadas, contate o programador".format(jogador=x.nome))
    await ctx.send("As informações de todos players foram atualizadas.")


@bot.command()
# Retorna lista em ordem descrescente de MMR dos jogadores cadastrados, é invocado sem argumentos, exemplo:'$leaderboard'
async def leaderboard(ctx):
    organizada = sorted(playerslist, key=lambda x: x.mmr, reverse=True)
    counter = 1
    for x in organizada:
        await ctx.send("{contador} - {nome} / nick: {nick} / MMR: {mmr}".format(contador=counter, nome=x.nome, nick=x.nickname, mmr=x.mmr))
        counter +=1
    del organizada

@bot.command()
# Retorna o MMR de um único jogador, é invocado com o nome de argumento, exemplo: '$mmr Jean'
async def mmr(ctx, nome):
   for x in playerslist:
       if x.nome.lower() == nome.lower():
           await ctx.send("{jogador}, com nick de '{nick}' tem MMR estimado de {mmr}".format(jogador=x.nome, nick=x.nickname, mmr=x.mmr))
           return
   await ctx.send("Jogador não cadastrado")



# Esse é o local onde você cola a chave que o discord providencia para que você consiga comunicar com a API deles.
# ----- SEM ESSA CHAVE O BOT NÃO FUNCIONA -----
bot.run("XXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXX")
# ----- SEM ESSA CHAVE O BOT NÃO FUNCIONA -----
