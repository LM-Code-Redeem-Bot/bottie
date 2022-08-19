import discord
import os
import requests
import time
from threading import Thread
import pandas as pd

codes = []
thread_count=0

admins = list(str(os.getenv('admin')).split(","))

client = discord.Client()

def sub_redeem(i, temp, code):
    global thread_count
    response = requests.get("https://lmbot-" + str(thread_count) + ".vercel.app/" +
                            str(temp[i - 1]) + "/" + str(code))
    print("Bot-", i, response.status_code, time.ctime())
    if (response.status_code == 504):
        time.sleep(2)
        response = requests.get("https://lmbot-" + str(thread_count) + ".vercel.app/" +
                                str(temp[i - 1]) + "/" + str(code))
        print("Bot-", i, response.status_code, time.ctime())
    thread_count=thread_count-1

def redeem(code):
    global thread_count
    codes.append(code)
    print(time.ctime())
    data = pd.read_csv(os.getenv('data_sheet'))
    temp = list(data['ID'])
    c = len(temp)
    for j in range(5):
        for i in range(1, c + 1):
            # sub_redeem(i,temp,code):
            thread_count=thread_count+1
            background_thread = Thread(target=sub_redeem,
                                       args=(
                                           i,
                                           temp,
                                           code,
                                       ))
            background_thread.start()
            # response = requests.get("https://lmcrbot-" + str(i) +
            #                         ".vercel.app/" + str(temp[i - 1]) + "/" +
            #                         str(code))
            # print("Bot-", i, response.status_code, time.ctime())
            # if (response.status_code == 504):
            #     time.sleep(2)
            #     response = requests.get("https://lmcrbot-" + str(i) +
            #                             ".vercel.app/" + str(temp[i - 1]) +
            #                             "/" + str(code))
            #     print("Bot-", i, response.status_code, time.ctime())
        time.sleep(12)
    print(time.ctime())
    print("🚀", code, "Redemeed Successfully...!!!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(('$help', '$Help')):
        msg1 = '🚀 Hey Dude, Here are bot commands for you !!! {0.author.mention}'.format(
            message)
        await message.channel.send('==================================')
        await message.channel.send(msg1)
        await message.channel.send('==================================')
        await message.channel.send(
            '✅ Bot Commands :-\n1)  $help\n2) $hi\n3) $code LM_Code')
        await message.channel.send('==================================')

    if message.content.startswith(('$$help', '$$Help')):
        if str(message.author.name) in admins:
            msg1 = '☯ Hey Dude, Here are bot Admin commands for you !!! {0.author.mention}'.format(
                message)
            await message.channel.send('==================================')
            await message.channel.send(msg1)
            await message.channel.send('==================================')
            await message.channel.send(
                '🎉 Bot Commands :-\n1)  $$help\n2) $code@history\n3) $data@history\n4) $code@reset '
            )
            await message.channel.send('==================================')
        else:
            msg1 = '🧐 {0.author.mention} Warning Its Only For Admins...!!!'.format(
                message)
            await message.channel.send('==================================')
            await message.channel.send(msg1)
            await message.channel.send('==================================')

    if message.content.startswith(('$hi', '$Hi', '$Hii', '$hii')):
        msg1 = '✨ Hey Dude, Welcome Here !!! {0.author.mention}'.format(
            message)
        await message.channel.send('==================================')
        await message.channel.send(msg1)
        await message.channel.send('==================================')

    if message.content.startswith(('$code', '$Code')):
        l = str(message.content)
        li = l.split()
        if (len(li) == 1):
            await message.channel.send("👀 No Code Entered...!!!")
        elif str(li[1].upper()) in codes:
            await message.channel.send(
                "🙄 Duplication Of Code Is Not Allowed...!!!")
        else:
            li[1] = li[1].upper()
            old_code = pd.read_csv('code_history.csv')
            new_code = pd.DataFrame({"Codes History": [li[1]]})
            old_code = pd.concat([old_code, new_code])
            # old_code.append(new_code)
            old_code.to_csv('code_history.csv', index=False)
            await message.channel.send('==================================')
            await message.channel.send(
                '🔰 Code :- {}, Added For Redeemption'.format(li[1]))
            await message.channel.send('==================================')
            await message.channel.send(
                '⛄ Please Wait For a Minute Untill You Enter Another...!!!')
            await message.channel.send('==================================')
            # redeem(li[1])
            background_thread = Thread(target=redeem, args=(li[1], ))
            background_thread.start()
            await message.channel.send("🚀" + str(li[1]) +
                                       " ,Redemeed Successfully...!!!")
        await message.channel.send('==================================')

client.run(os.getenv('TOKEN'))
