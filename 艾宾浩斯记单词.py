#-*- coding=utf-8 -*-#
import datetime,re,random,time,os
from threading import Thread
from os import system as sy
from sys import path
nowpath=os.getcwd()+'/.DANCIsave'#藏起来hhh
if not os.path.exists(nowpath):
    os.makedirs(nowpath)
path.append(nowpath)#将存档位置加入模块导入默认目录
k=0
try:
    from wordslist import wordslist,daka,Map,Map0
except:
    #不存在则新建存档
    k=25
    with open('%s/wordslist.py'%nowpath,'w') as f:
        temp=[['2019-01-01',0,0]]*7
        f.write("wordslist={}\ndaka={'L_D':'2019-1-1','CON':0,'TOT':0}\nMap=%s\nMap0=0"%temp)
#尽力导入模块...
while k>1:
    print('\r新建存档中',end='')
    k-=1
    if k%4==0:
        print('   ',end='')
    elif k%4==1:
        print('.  ',end='')
    elif k%4==2:
        print('.. ',end='')
    else:
        print('...',end='')
    try:
        from wordslist import wordslist,daka,Map,Map0
        print('')
        break
    except:
        time.sleep(0.4)
if k==1:
    print('\n新建存档失败,3秒后关闭程序')
    time.sleep(3)
    exit()

def main():
    sy('clear')
    global DATE
    global Map
    global Map0
    print('图表状态:%s'%('关' if not Map0 else '开'))
    if input('如需切换请输入1:(默认请直接回车)'):
        Map0=int(not Map0)
    save()
    sy('clear')
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
    elif not print(f"你已连续复习{daka['CON']}天,累计{daka['TOT']}天啦") and daka['CON']==0:
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
            sy('clear')
            print('请输入数字!')
            continue
        if n == 1:
            Ch={}#重复列表
            print('新增内容:(q/结束)(格式:A  B)(2个空格)')
            x=input('1.批量导入 2.文件导入:')
            if x=='2':
                print('文件内容格式:\nA  B\nA  B\n...')
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
                        Ch.update(learn(i))
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
                        temp=learn(x)
                        if temp:
                            Ch.update(temp)
            if Ch:#有重复
                Change(Ch)
        elif n == 2:
            print('复习:(q/退出;y/已会(不再出现);n/不记得(刷新复习频率))')
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
        sy('clear')

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
            return {xen:(i,wordslist[i][xen],xch)}
    wordslist[date1][xen] = xch
    Map[-1][2]=len(wordslist[date1])
    save()
    return 0

def Change(Ch):#Ch={xen:(Date_index,oldxch,newxch)}
    print('已存在词汇,是否修改: %s'%(' '.join([i for i in Ch])))
    k=1
    for i in Ch:
        if k:
            print(f"{i}: {Ch[i][1]} --> {Ch[i][2]}")
            tag=input('?Y/y/N/n ')
        if tag=='y':
            wordslist[Ch[i][0]][i]=Ch[i][2]
            print('✓')
        elif tag=='n':
            pass
        elif tag=='Y':
            wordslist[Ch[i][0]][i]=Ch[i][2]
            if k:
                print('✓')
            k=0
        else:
            k=0
    save()

def save():
    global Map0
    data = 'wordslist=%s\ndaka=%s\nMap=%s\nMap0=%d'%(wordslist,daka,Map,Map0)
    with open('%s/wordslist.py'%nowpath,'w') as f:#保存存档
        f.write(data)

#背单词时的倒计时,改为多线程,在回车后不会继续倒数
def Sleep(text1,text2):
    global T
    k=0
    for i in range(500):
        if T:
            break
        if k%100==0:
            print('\r'+str(5-k//100),end='')
        k+=1
        time.sleep(0.01)
    print('\r'+text1+'\n'+text2,end='')#意译+剩余数量
    if k!=500:#提前结束则多换一行
        print()

def check(x):#x=日期
    global Map
    global T
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
        k+=1
        T=0
        Count=Thread(target=Sleep,args=(i[1],f'{len(l)-k}/{len(l)}'))
        Count.start()
        tag=input()
        T=1
        Count.join()
        if tag=='q':
            print('还没背完就退出无法打卡哦,确定退出吗?y/n')
            if input()=='y':
                if Map[-1][1]<k:
                    Map[-1][1]=k
                    save()
                print(':P')
                return
        #会了
        elif tag=='y':
            if 'knowwell' not in wordslist:
                wordslist['knowwell']={}
            dele(i[0])
            wordslist['knowwell'][i[0]] = i[1]
            save()
        #完全不记得了,移动至今天的记录
        elif tag=='n':
            dele(i[0])
            learn('%s  %s'%(i[0],i[1]))
    if Map[-1][1]<len(l):
        Map[-1][1]=len(l)
    print('背完啦,给自己点个赞吧^_^')
    if not l:
        print('不要自己骗自己哦...')
    if Map0:
        Histo(Map)
    if daka['L_D']!=str(datetime.date.today()):
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
    temp={}
    for i in wordslist:
        temp.update(wordslist[i])
    temp=[(i,temp[i]) for i in temp]#方便查意思
    print('输入要查询的单词(退出->q):')
    while 1:
        k=0
        x=input()
        if not x:
            continue
        if x=='q':
            return
        #有中文则从意译中查找
        ch=has_ch(x)
        temp0=[]
        temp0=[i for i in temp if x==i[ch]]
        if temp0:
            k=1
            print('\n'.join(['%s  %s'%(i[0],i[1]) for i in set(temp0)]))
        else:
            temp0=[]
            #模糊查找...
            for j in range(3):
                for i in temp:
                    temp0+=[i for i in temp if x in i[ch]]
                    if temp0:
                        k=1
                    #若输入空格则查询所有带空格的词组
                    if len(temp0)>5 and x!=' ':
                        temp0=temp0[:6]
                        break
                if len(x)<=2:
                    break
                x=x[:-1]
                if len(temp0)>5:
                    break
            if temp0:
                print('你要找的是不是:\n%s'%('\n'.join(['%s  %s'%(i[0],i[1]) for i in set(temp0)])))
        if k==0:
            print('单词不在库中')

def has_ch(x):
    for i in x:
        if '\u4e00'<=i<='\u9fcf':
            return 1
    return 0

def Histo(data0):#柱状图,精度10,data0=[listY1,...];listY=[date,r_num,l_num]
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
    Dia=('▒','█')
    Map=('┃','━','┻','┗','▶','▲')
    print('      %s:复习数量    %s:新增数量'%(Dia[0],Dia[1]))
    temp=''.join([f'{i[0][-5:]:>6}' for i in data])
    X0='       '+temp
    X1='   0'+Map[3]+(Map[1]*5+Map[2])*7+Map[1]*5+Map[4]
    temp=[f'{i:>4}' for i in range(100,0,-10)]
    for i in range(len(temp)):
        if i%2==1:
            temp[i]='    '
    Y=['    ']*2+temp+['    ']
    temp=[Map[5]+'    ']+[Map[0]+'    ']*11
    Y=[Y[i]+temp[i] for i in range(12)]
    #以上框架
    H=[0,0]
    for k in (0,1):
        Ht=[0]*39
        for i in range(7):
            Ht[i*6+k*2]=data[i][k+1]//10+(0 if data[i][k+1]%10<5 else 1)
        H[k]=Ht
    for i in range(39):
        Dl=(Dia[0],H[0][i])
        Dr=(Dia[1],H[1][i])
        temp=[' ']*(12-Dl[1]-Dr[1])+[Dl[0]]*(Dl[1])+[Dr[0]]*(Dr[1])
        Y=[Y[i]+temp[i] for i in range(12)]
    print('\n'.join(Y)+'\n'+X1+'\n'+X0)

if __name__=='__main__':
    main()
