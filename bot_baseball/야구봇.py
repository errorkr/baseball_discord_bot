#필요한 기능,파일 불러오기
import os
import sys
import asyncio
import discord
from discord.ext import commands
import random
import re




client = commands.Bot(command_prefix='~')


token = "token입력해주세요"


@client.event
async def on_ready():
    print("Logged in as ") 
    print(client.user.name)
    print(client.user.id)
    print("===========")

    while True:
        game2 = discord.Game("야구게임한판 ㄱ?")
        await client.change_presence(status=discord.Status.online, activity=game2)
        await asyncio.sleep(10)
        game3 = discord.Game("야구봇이랑 디스코드")
        await client.change_presence(status=discord.Status.online, activity=game3)
        await asyncio.sleep(10)
        game4 = discord.Game("도움말은 ~도움")
        await client.change_presence(status=discord.Status.online, activity=game4)
        await asyncio.sleep(10)




@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot: 
        return None 

    id = message.author.id 
    channel = message.channel 

    def check3(m):
        return lambda m: m.author == message.author and m.channel == message.channel
    
    async def get_input_of_type4(func,message):
        while True:
            try:
                msg = await client.wait_for('message', timeout=20 ,check=check3(message))
                if msg.content == "가위" or msg.content == "바위" or msg.content == "보" or msg.content == "그만":
                    return func(msg.content)
                else:
                    continue
            except ValueError:
                continue
            
    member = message.author
    member = str(member)
    member = member[:-5]
            

    
    if message.content.startswith('~도움'):
        embed = discord.Embed(
            title='**야구봇 등장!**',
            description='커맨드 리스트',
            colour=discord.Colour.green()
        )
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name='~골라줘,', value='랜덤으로 하나 골라줌.')
        embed.add_field(name='~말해', value='똑같이 말해준다.')
        embed.add_field(name='~주사위 number' , value='1부터 number까지 랜덤으로 값줌.')
        embed.add_field(name='~야구노말,~야구이지,~야구하드', value='4자리수를 입력하여 야구게임 할수 있음 그만할려면 0입력')
        embed.add_field(name='~가위바위보,~갈바', value='연승 가위바위보 그만할려면 "그만" 입력')
        embed.set_footer(text='문의사항 디스코드 프로핏일걸요#1495')
        await channel.send(embed=embed)
        


    
    elif message.content.startswith('~말해'):
        mes = message.content
        mes = mes[4:]
        await channel.send(mes)
    elif message.content.startswith('~야구 룰'):
        await channel.send('1. 1000~9999사이 숫자 중 중복되는 숫자가 없는 숫자를 입력한다. ex) 9981 x, 1235 o\n\n2.정해져 있는 숫자에서 숫자가 포함만 되있으면 볼, 숫자위치가 같으면 스트라이크. 단,스트라이크 볼 중복카운트아님\n3.4스트라이크 => 게임 승리.\n4.처음에는 0이 올 수 없고, 이지모드에는 0이없다.\n5.0을 치면 다시 시작')


        
    
    
    elif message.content.startswith("~가위바위보") or message.content.startswith("~갈바"):
        await channel.send(f"{member}, 가위바위보 시작!! 제한시간은 20초! 가위, 바위, 보중 하나를 말해주세요")
        tal=True
        k=0
        while (tal==True):
            try:
                rcp = await get_input_of_type4(str,message)
                if rcp == "그만":
                    tal=False
                    await channel.send(f'{member} 게임을 중단합니다. {k}연승에서 마무리')
                    break
            except asyncio.TimeoutError:
                await channel.send(f'{member}, 시간 초과 ㅠㅠ...... ')
                tal=False
                break
            except ValueError:
                continue      
            bot_response = random.randint(1, 3)
            if bot_response == 1: 
                if rcp == "가위": 
                    await channel.send(f"✌ {member}, 비겼어~ 계속 하자!")
                    continue
                elif rcp == "바위": 
                    k=k+1
                    await channel.send(f"✌ {member} {k}연승 중, 내가 졌어....")                        
                    continue
                elif rcp == "보":
                    await channel.send(f"✌ {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                else:
                    continue
            if bot_response == 2: 
                if rcp == "가위": 
                    await channel.send(f"✊ {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                elif rcp == "바위": 
                    await channel.send(f"✊ {member}, 비겼어~ 계속 하자!")
                    continue
                elif rcp == "보": 
                    k=k+1
                    await channel.send(f"✊ {member} {k}연승 중, 내가 졌어..")
                    continue
                else:
                    continue
            if bot_response == 3:
                if rcp == "가위": 
                    k=k+1
                    await channel.send(f"🖐 {member} {k}연승 중, 내가 졌어..")
                    continue
                elif rcp == "바위":                        
                    await channel.send(f"🖐 {member}, 내가 이겼어!")
                    tal=False
                    await channel.send(f"{member} {k}연승에서 마무리!")
                    break
                elif rcp == "보": 
                    await channel.send(f"🖐 {member}, 비겼어~ 계속 하자!")
                    continue
                else:
                    continue
    
    else: #위의 if에 해당되지 않는 경우
        return None #동작하지 않고 무시한다.




@client.command(pass_context=True)
async def 주사위(ctx, num1):
    picked = random.randint(1, int(num1))
    if picked%2==0: 
        if picked > int(num1)//2:
            if picked==int(num1):
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n와 대박🎰!!, 제일 높은 숫자네요")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n오늘 운이 좀 괜찮은데요??!")
        if picked <= int(num1)//2:
            if picked==1:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n헐😱.. 제일 낮은 숫자네요..")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"오늘 운이 좀 별로네요 ㅠㅠ")
    if picked%2==1: 
        if picked >= int(num1)//2+1:
            if picked==int(num1):
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n와 대박🎰!!, 제일 높은 숫자네요")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n오늘 운이 좀 괜찮은데요??!")
        if picked <= int(num1)//2:
            if picked==1:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"\n헐😱.. 제일 낮은 숫자네요..")
            else:
                await ctx.send('주사위🎲 숫자는 '+str(picked)+"오늘 운이 좀 별로네요 ㅠㅠ")




@client.command(pass_context=True) 
async def 골라줘(ctx, *args):
    choice=random.choice(args)
    await ctx.send(f"난 {choice}")
    




    
    
  

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

async def get_input_of_type(func, ctx):
    while True:
        try:
            msg = await client.wait_for('message', check=check(ctx))
            return func(msg.content)
        except ValueError:
            continue
            
async def get_input_of_type2(func,ctx):
        while True:
            try:
                msg = await client.wait_for('message', timeout=20 ,check=check(ctx))
                return func(msg.content)
            except ValueError:
                continue
#실험용
@client.command()
async def 더하기(ctx):
    await ctx.send("첫번째 숫자는 뭘로?")
    firstnum = await get_input_of_type(int, ctx)
    await ctx.send("두번째 숫자는 뭘로?")
    secondnum = await get_input_of_type(int, ctx)
    await ctx.send(f"{firstnum} + {secondnum} = {firstnum+secondnum}")
    
#야구 난이도별 코드
@client.command()
async def 야구이지(ctx):
    a=[]
    for i in range(100,999):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        if (b1=="0" or b2=="0" or b0==b1 or b0==b2 or b1==b2):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 이지모드 시작! 0은 포함되지않아. 100~999사이 숫자만 입력해줘")
    while(k<7):
        await ctx.send(f"{member}, 숫자를 입력해~ 기회는 {7-k}번 남았어!")
        num2 = await get_input_of_type(int,ctx)
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
                break
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,3):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,3):
            for j in range(0,3):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count
        if(num==num2):
            if k==1:
                await ctx.send(f"{member}, 당신은 1/648 확률을 뚫어낸 찍신??! 대박! 정답이야!!")
                break
            else:
                await ctx.send(f"{member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==7:
                await ctx.send(f"{member}, 7번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"{member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"{member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼!")
                    continue

@client.command(aliases=["야구노말","야구노멀"])
async def 야구게임(ctx):
    a=[]
    for i in range(1000,10000):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        b3=p[3]
        if (b0==b1 or b0==b2 or b0==b3 or b1==b2 or b1==b3 or b2==b3):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 시작!")
    while(k<10):
        await ctx.send(f"@{member}, 숫자를 입력해~ 기회는 {10-k}번 남았어!")
        num2 = await get_input_of_type(int,ctx)
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,4):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,4):
            for j in range(0,4):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count
        if(num==num2):
            if k==1:
                await ctx.send(f"??? {member}, 당신은 찍신??! 한번 만에 바로 맞췄어 대박!")
                break
            else:
                await ctx.send(f"와우! {member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==10:
                await ctx.send(f"ㅠㅠㅠ {member}, 10번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"나가세요~ {member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"내가 말할차례! {member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼이야!")
                    continue

@client.command()
async def 야구하드(ctx):
    a=[]
    for i in range(1000,10000):
        a.append(i)
    b=[]
    for j in a:
        p=str(j)
        b0=p[0]
        b1=p[1]
        b2=p[2]
        b3=p[3]
        if (b0==b1 or b0==b2 or b0==b3 or b1==b2 or b1==b3 or b2==b3):
            continue
        b.append(j)
    num=random.choice(b)
    k=0
    member = ctx.author
    member = str(member)
    member = member[:-5]
    await ctx.send("야구게임 하드모드 시작!")
    tal=True
    while(k<8 and tal==True):
        await ctx.send(f"@{member}, 숫자를 입력해~ 기회는 {8-k}번, 제한시간은 20초 남았어!")
        try:
            num2 = await get_input_of_type2(int,ctx)
        except asyncio.TimeoutError:
            await ctx.send(f'시간 초과 ㅠㅠ.. 다시 시작해 주세요! 정답은 {num}')
            tal=False
            break
        except ValueError:
            continue
        if num2 not in b:
            if num2 == 0:
                await ctx.send("야구게임을 종료합니다.")
                tal=False
                break
            else:
                await ctx.send("룰에 어긋나는 숫자를 입력했어. 다시 입력해~")
                continue
        k=k+1
        strike_count=0
        for i in range(0,4):
            if(str(num)[i]==str(num2)[i]):
                strike_count=strike_count+1
        ball_count=0
        for i in range(0,4):
            for j in range(0,4):
                if(str(num)[i]==str(num2)[j]):
                    ball_count=ball_count+1
        ball_count=ball_count-strike_count            
        if(num==num2):
            if k==1:
                await ctx.send(f"{member}, 당신은 1/4536 확률을 뚫어낸 찍신??! 대박! 정답이야!!")
                break
            else:
                await ctx.send(f"{member}, {k}번만에 정답을 맞췄어. 정답은 {num}야!")
                break
        else:
            if k==8:
                await ctx.send(f"{member}, 8번 실패해서 게임 오버 ㅠㅠ 정답은 {num}야!")
                break
            else:
                if strike_count==0 and ball_count==0:
                    await ctx.send(f"{member}, {k}번째 시도 out!!")
                    continue
                else:
                    await ctx.send(f"{member}, {k}번째 시도 {strike_count}스트라이크 {ball_count}볼!")
                    continue




        


        
client.run(token)


