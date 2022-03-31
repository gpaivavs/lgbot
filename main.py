import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import roller
import scryfall_getter
import json

load_dotenv()
lgbot_token = os.getenv('discord_token')
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    with open('rolagens.json', 'r') as arquivo:
        roller.rolagens_dict = json.load(arquivo)
        print(roller.rolagens_dict)


@client.command()
async def scryfall(ctx, *args):
    carta = ' '.join(args)
    busca_carta = scryfall_getter.get_card(str(carta))
    await ctx.send(busca_carta)


@client.command()
async def r(ctx, conteudo, nome=None):
    try:
        a, b, c, d = roller.limpar_string(conteudo)
        rolagem = roller.Rolagem(a, b, c, d)
        rolagem.rolar()
        if nome:
            roller.rolagem_dict[nome] = rolagem
            roller.rolagens_dict[nome] = rolagem.to_dict()
            await ctx.send(f'{ctx.message.author.mention} rolou:\n'
                           f'```'
                           f'{conteudo}:\n'
                           f'Rolagens {rolagem.resultados}\n'
                           f'Total: {rolagem.total}'
                           f'```')
        else:
            await ctx.send(f'{ctx.message.author.mention} rolou:\n'
                           f'```'
                           f'{conteudo}:\n'
                           f'Rolagens {rolagem.resultados}\n'
                           f'Total: {rolagem.total}'
                           f'```')
    except:
        await ctx.send(f'Deu ruim amigo, checa a sintaxe do comando pfv.')


@client.command()
async def rh(ctx, nome_rolada):
    #rolagem = roller.rolagem_dict[nome_rolada]
    rolagem_dict = roller.rolagens_dict[nome_rolada]
    rolagem = roller.Rolagem(rolagem_dict["quantidade"], rolagem_dict["face"], rolagem_dict["vantagem"],
                              rolagem_dict["modificador"])
    rolagem.rolar()
    await ctx.send(f'{ctx.message.author.mention} rolou:\n'
                   f'```{nome_rolada}:\n'
                   f'{rolagem_dict["quantidade"]}d{rolagem_dict["face"]}h{rolagem_dict["vantagem"]}'
                   f'+{rolagem_dict["modificador"]}:\n'
                   f'Rolagens {rolagem.resultados}\n'
                   f'Total: {rolagem.total}```')


@client.command()
async def rsave(ctx):
    rolagens_json = json.dumps(roller.rolagens_dict, indent=4)
    print(rolagens_json)
    with open('rolagens.json','w') as arquivo:
        json.dump(roller.rolagens_dict,arquivo,indent=4)
    await ctx.send(f'```Rolagens salvas.```')


@client.command()
async def helpme(ctx):
    help_text = "```" \
                "!scryfall to lookup magic cards by name.\n" \
                "!r to roll dice (!r 2d20h1+10 rolls 2 twenty-sided dice, keeps the highest one, adds 10 to result)." \
                "You can write anything after a roll to save the roll under that name.\n" \
                "!rh <saved roll name> to roll saved rolls.\n" \
                "!rsave will commit all saved rolls to a file for posterity.\n" \
                "```"
    await ctx.send(help_text)


client.run(lgbot_token)
