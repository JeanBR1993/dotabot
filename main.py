#Versão 1.0 Bot de Discord para o grupo de Dota
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('Logado como {0.user}'.format(client), "LOGIN:OK")




@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$dotabot'):
        await message.channel.send("Dae mamacos, eu sou um bot em desenvolvimento, num futuro próximo darei estatísticas sobre os jogadores daqui como MMR ganho na semana, vitórias/derrotas e etc...")
        await message.channel.send("Por enquanto estou em teste e só respondo com um toque de humor duvidoso de acordo com comandos iniciados com '$'")
        await message.channel.send("Os comandos disponíveis são: $ladeia, $carlostaco, $rayfeed, $caio, $dudjack, $zedare, $massuke, $afini, $rapp, $lusvarghi, $marcim, $dutakaki, $miltu, $jean")
        await message.channel.send("As opiniões não são do programador, são do BOT, confiem.")


    if message.content.startswith('$ladeia'):
        await message.channel.send('Melhor supp do romários, exemplo de superação saiu dos haroldos. NEAAAHH!')

    if message.content.startswith('$carlostaco'):
        await message.channel.send('Intolerante com quem picka Crystal Maiden e não pega Ult mas boa pessoa.')

    if message.content.startswith('$rayfeed'):
        await message.channel.send('Eterno lendinha com jogadas duvidosas e entregantes.')

    if message.content.startswith('$caio'):
        await message.channel.send('Melhor pudge do Brasil, ainda deu MMR gratuito e dois rampages pro Jean em ranked.')

    if message.content.startswith('$dudjack'):
        await message.channel.send('Um dos melhores supp do grupo quando não tem ideia de fazer morphiling supp4.')

    if message.content.startswith('$zedare'):
        await message.channel.send('Ele faz warlock mid mas a gente gosta dele, melhor barathrum do centroeste brasileiro')

    if message.content.startswith('$massuke'):
        await message.channel.send('Seria o melhor Skywrath Mage do mundo se pegasse a ult no lvl 6.')

    if message.content.startswith('$afini'):
        await message.channel.send('Provavelmente o único do grupo com dedo suficiente pra jogar de injoker.')

    if message.content.startswith('$rapp'):
        await message.channel.send('Se perder a lane com ele de duo é porque você é ruim, supp de respeito.')

    if message.content.startswith('$lusvarghi'):
        await message.channel.send('Maior MMR do grupo, adiquiriu escoliose de carregar tanto ruim junto nas PTs.')

    if message.content.startswith('$marcim'):
        await message.channel.send('Dono de opiniões controversas como: "Runa illusion é a melhor runa que tem", "Necro off é bom" e "PERDEMO" depois de um FB.')

    if message.content.startswith('$dutakaki'):
        await message.channel.send('HC que faz BKB como último item mas já carregou várias vezes, jogador tranquilão')

    if message.content.startswith('$miltu'):
        await message.channel.send('Jogador com a maior versatilidade do grupo, off, hc, mid, supp, faz qualquer coisa; só não faz bem mas aí seria pedir de mais.')

    if message.content.startswith('$jean'):
        await message.channel.send('Terror dos lobbys, time inimigo sempre bane PA, jugg em respeito à essa lenda (literalmente, sdds ancient e divine)')



client.run('OTMyNjgyODE0MDQ5MDk5ODg2.YeWijw.Xl9ITs8zXdUvrp-lhCqNH9mZpys')
