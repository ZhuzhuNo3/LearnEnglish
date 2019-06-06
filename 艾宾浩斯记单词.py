#-*- coding=utf-8 -*-#
import datetime,re,random,time
from os import system as sy
try:
    from wordslist import wordslist,daka,Map
except ModuleNotFoundError:#不存在则新建存档
    with open('wordslist.py','w') as f:
        temp=[['2019-01-01',0,0]]*7
        f.write("wordslist={}\ndaka={'L_D':'2019-1-1','CON':0,'TOT':0}\nMap=%s"%temp)
    from wordslist import wordslist,daka,Map

def main():
    global DATE
    global Map
    timelist = (1,2,4,7,15,31,36,41)
    DATE = []
    now = datetime.date.today()#今天的日期
    if Map[-1][0]!=str(now):
        Map=Map[1:]+[[str(now),0,0]]
    DATE.append(str(now))
    for i in timelist:#计算需要复习的日期
        delta = datetime.timedelta(days=i)
        DATE.append(str(now + delta))
    L_D=[int(i) for i in daka['L_D'].split('-')]
    LD=datetime.date(L_D[0],L_D[1],L_D[2])
    if (LD+datetime.timedelta(1))!=now and LD!=now:
        daka['CON']=0#没有连续复习
    if daka['TOT']==0:
        pass
    elif not print(f"你已连续复习{daka['CON']}天,累计天{daka['TOT']}啦") and daka['CON']==0:
        print('不积跬步,无以至千里!')
    elif daka['CON']<6:
        print('继续加油哦!')
    elif daka['CON']<50:
        print('Whatever is worth doing is worth doing well!')
    else:
        print('Great minds have purpose, others have wishes.')
    #以上初始化结束
    while 1:
        print('\n1.新增 2.复习 3.删除 4.查询 5.退出')
        try:
            n = int(input())
        except:
            continue
        if n == 1:
            Ch=[]#重复列表
            print('新增内容:(q/结束)(格式:A  B)(2个空格)')
            x=input('1.批量导入 2.文件导入:')
            if x=='2':
                print('文件内容格式:\nA  B(换行,括号里的不需要哦)\nA  B\n...')
                data=input('输入文件详细地址:\n')
                try:
                    while data[-1]==' ':#去除多余空格
                        data=data[:-1]
                    with open(data,'r') as f:
                        words=f.read().split('\n')
                    while words[-1]=='':#去除空元素
                        words=words[:-1]
                    for i in words:
                        print(i)
                        Ch.append(learn(i))
                except:
                    print('无法读取文件')
            elif x=='1':
                while True:
                    x = input()
                    if x == 'q':
                        break
                    elif x == '':
                        print('无效内容')
                    else:
                        Ch.append(learn(x))
            Ch=[i for i in Ch if i]#去除0
            if Ch:#有重复
                Change(Ch)
        elif n == 2:
            print('复习:(q/退出;y/已会(不再出现))')
            check(str(now))
        elif n == 3:
            for i in wordslist:
                for k in wordslist[i]:
                    print(k+' ',end='')
            print('\n删除:')
            dele(input())
        elif n == 4:
            seekword()
        elif n == 5:
            break
        input('回车结束...')
        try:
            sy('clear')
        except:
            sy('clr')

def learn(x):
    global DATE
    global Map
    xen = re.findall(r'(.+?)\s\s',x)
    xch = re.findall(r'.+?\s\s(.+)',x)
    if not xch:
        print('输入格式:hello  你好,哈啰')
        return 0
    else:
        xen = xen[0]
        xch = xch[0]
    date1 = ','.join(DATE)
    #需要记忆的日期存储为key
    #输入内容存储为dict
    if date1 not in wordslist:
        wordslist[date1]={}
    for i in wordslist:
        if xen in wordslist[i]:#如果输入内容已存在
            return (xen,i,wordslist[i][xen],xch)
    wordslist[date1][xen] = xch
    Map[-1][2]=len(wordslist[date1])
    save()
    return 0

def Change(Ch):#Ch=[(xen,Date_index,oldxch,newxch),]
    print('已存在词汇,是否修改: %s'%(' '.join([i[0] for i in Ch])))
    k=1
    for i in Ch:
        if k:
            print(f"{i[0]}: {i[2]} --> {i[3]}")
            tag=input('?Y/y/N/n ')
        if tag=='y':
            wordslist[i[1]][i[0]]=i[3]
            print('✓')
        elif tag=='n':
            pass
        elif tag=='Y':
            wordslist[i[1]][i[0]]=i[3]
            if k:
                print('✓')
            k=0
        else:
            k=0
    save()

def save():
    data = 'wordslist=%s\ndaka=%s\nMap=%s'%(wordslist,daka,Map)
    with open('wordslist.py','w') as f:#保存存档
        f.write(data)

def check(x):#x=日期
    global Map
    print('= = 今日份复习开始 = =')
    value = [i for i in wordslist if x in i]
    l=[]
    for i in value:
        l += [(k,'%s'%wordslist[i][k]) for k in wordslist[i]]
    random.shuffle(l)
    l=l[:151]#设置上限
    k=0
    for i in l:
        print(i[0])
        for j in range(5):
            print('\r'+str(5-j),end='')
            time.sleep(1)
        print('\r'+i[1])
        k+=1
        tag=input(f'{len(l)-k}/{len(l)}')
        if tag=='q':
            print('还没背完就退出无法打卡哦,确定退出吗?y/n')
            if input()=='y':
                Map[-1][1]=k
                save()
                print(':P')
                return
        elif tag=='y':
            if 'knowwell' not in wordslist:
                wordslist['knowwell']={}
            wordslist['knowwell'][i[0]] = i[1]
            dele(i[0])
    print('背完啦,给自己点个赞吧^_^')
    if not l:
        print('不要自己骗自己哦...')
    WaveMap(Map)
    if daka['L_D']!=datetime.date.today():
        daka['CON']+=1
        daka['TOT']+=1
        daka['L_D']=str(datetime.date.today())
        save()

def dele(x):
    for i in wordslist:
        if x in wordslist[i]:
            del wordslist[i][x]
            print('✓')
            save()
            return
    print('不存在')

def seekword():
    print('输入要查询的单词(退出->q):')
    while 1:
        k=0
        x=input()
        for i in wordslist:
            if x in wordslist[i]:
                print(wordslist[i][x])
                k=1
            elif x == 'q':
                return
        if k==0:
            print('单词不在库中')

def WaveMap(data0):#极其简陋的图data0=[listY1,...];listY=[date,r_num,l_num]
    temp=data0[-1][0].split('-')
    data=[data0[-1]]
    for i in range(1,7):
        delta=datetime.timedelta(days=i)
        k=datetime.date(int(temp[0]),int(temp[1]),int(temp[2]))-delta
        t=1
        for j in range(7):
            if str(k)==data0[j][0]:
                data=[data0[j]]+data
                t=0
                break
        if t:
            data=[[str(k),0,0]]+data
    Dia=('▒','█','░')
    Map=('┃','━','┻','┗','▶','▲')
    print('      %s:复习数量    %s:学习数量'%(Dia[0],Dia[2]))
    temp=''.join([f'{i[0][-5:]:>6}' for i in data])
    X0='       '+temp
    X1='   0'+Map[3]+(Map[1]*5+Map[2])*7+Map[1]*5+Map[4]
    temp=[f'{i:>4}' for i in range(100,0,-10)]
    for i in range(len(temp)):
        if i%2==1:
            temp[i]='    '
    Y=['    ']*2+temp+['    ']
    temp=[Map[5]+'     ']+[Map[0]+'     ']*11
    Y=[Y[i]+temp[i] for i in range(12)]
    #以上框架
    H=[0,0]
    for k in (0,1):
        Ht=[0]*37
        for i in range(7):
            Ht[i*6]=data[i][k+1]
        for i in range(0,36,6):
           a=Ht[i]
           b=Ht[i+6]
           Ht[i+3]=(a+b)//2
           Ht[i+2]=(Ht[i+3]+a)//2
           Ht[i+4]=(Ht[i+3]+b)//2
           Ht[i+1]=(Ht[i+2]+a)//2
           Ht[i+5]=(Ht[i+4]+b)//2
        for i in range(37):
            add=0 if Ht[i]%10<5 else 1
            if add>12:
                add=12
            Ht[i]=Ht[i]//10+add
        H[k]=Ht
    for i in range(37):
        Dh=(Dia[0],H[0][i])
        Dl=(Dia[2],H[1][i])
        if H[0][i]<H[1][i]:
            temp=Dl
            Dl=Dh
            Dh=temp
        temp=[' ']*(12-Dh[1])+[Dh[0]]*(Dh[1]-Dl[1])+[Dia[1]]*(Dl[1])
        Y=[Y[i]+temp[i] for i in range(12)]
    print('\n'.join(Y)+'\n'+X1+'\n'+X0)

if __name__=='__main__':
    main()
