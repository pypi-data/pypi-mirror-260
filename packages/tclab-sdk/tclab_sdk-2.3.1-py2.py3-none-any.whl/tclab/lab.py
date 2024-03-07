import time
import uuid
import tclab as lab
import os
import sys
from rich import print
from rich.progress import Progress
from rich.console import Console
import threading
from blessed import Terminal

def get_environment(name,default=None):
    """获取实验环境信息
    """
    res=os.environ.get(name)
    if not res:
        if default:
            return False
        print(f"[red]环境变量{name}不存在.[/red]")
        sys.exit()
        # res=input("请输入:")
        # save=input(f"是否保存为环境变量{name}?(y/n)")
        # if save.lower()=='y':
        #     os.environ.setdefault(name,res)
        #     print(f"[green]环境变量{name}已保存.[/green]")
    return res

def render(data,select=0):
    """渲染列表

    Args:
        data (list): 列表文件
    """
    global Select,History
    History.append([data,select])
    console = Console(color_system='256', style=None)
    console.clear()
    height=console.height
    console.rule("[bold red]LABORATORY TERMINAL", align='left')
    height-=1
    if len(data)<Select+1:
        if len(data)>1:
            Select=len(data)-1
        else:
            Select=0
        select=Select
    fr=(select-select%(console.height-2))
    if fr<0:
        fr=0
    to=fr+console.height-2
    for i in range(fr,to):
        width=console.width
        if len(data)<i+1:
            break
        if i==select:
            style_add=" on blue"
        else:
            style_add=""
        console.print(f"{i+1}.",style="white"+style_add,end='')
        console.print(data[i]["name"],style="white"+style_add,end='')
        width-=len(data[i]["name"])+len(str(i+1))+1
        if "status" in data[i] and data[i]["status"]:
            status=data[i]["status"]
            width-=len(status)
            if status=='Online':
                console.print(' '*width+status,style="bold green"+style_add,end='')
            elif status=="Slow":
                console.print(' '*width+status,style="bold yellow"+style_add,end='')
            else:
                console.print(' '*width+status,style="bold red"+style_add,end='')
        else:
            console.print(' '*width,style="white"+style_add,end='')
        height-=1
    console.print("\n"*(height-1))
    console.print(f'[{Selecting.upper()}] ',style="bold white",end='')
    if Select<len(Data) and "func" in Data[Select] and "_DESCRIPTION" in dir(Data[Select]["func"]):
        console.print(Data[Select]["func"]._DESCRIPTION,style="bold white",end='')


def callback(x):
    global Data,Select,Selecting,Result,History
    if not Selecting:
        return
    
    try:
        if str(x)=="KEY_UP":
            if Select>0:
                Select-=1
            render(Data,Select)
        if str(x)=="KEY_DOWN":
            Select+=1
            render(Data,Select)
        if len(Data) and str(x)=="KEY_ENTER":
            if Selecting=="func":
                Result=Data[Select]['func']
                Selecting=False
            elif Selecting=="attr":
                if 'func' in Data[Select]:
                    Data=eval(Data[Select]['enter'])
                    Select=0
                    render(Data,Select)
                else:
                    Result=Data[Select]['data']
                    Selecting=False
        if str(x)=="KEY_ESCAPE":
            while len(History)>1 and History[-2][0]==Data:
                Data,Select=History[-2]
                History=History[:-2]
            if len(History)>1:
                Data,Select=History[-2]
                History=History[:-2]
            render(Data,Select)
        if str(x)=="KEY_RIGHT":
            if len(Data) and "children" in Data[Select]:
                Data=eval(Data[Select]['children'])
                Select=0
                render(Data,Select)
    except:
        pass
    
def tree_func(parent):
    """获取树形子函数结构

    Args:
        parent (str): 父函数
    """
    global Status_Map
    data=[]
    for i in remove_prefix(dir(parent)):
        data.append({"name":i,"func":eval(f"parent.{i}"),"enter":"tree_attr(Data[Select]['func'])","children":f"tree_func(Data[Select]['func'])"})
        if '_status' in dir(eval(f"parent.{i}")) and "__status" not in dir(eval(f"parent.{i}")):
            if i in Status_Map:
                data[-1]["status"]=Status_Map[i]
            else:
                data[-1]["status"]=eval(f"parent.{i}._status(refresh=False)")
                eval(f"parent.{i}").__status=data[-1]["status"]
                Status_Map[i]=data[-1]["status"]
    return data

def tree_attr(parent):
    """获取树形参数结构

    Args:
        parent (str): 父函数
    """
    data=[]
    for i in dir(parent):
        if i.startswith("_") and not i.startswith("__"):
            data.append({"name":i,"data":getattr(parent,i)})
    return data

def remove_prefix(arr):
    """移除带前缀的文本

    Args:
        arr (list): 文本列表
    """
    res=[]
    for a in arr:
        if not a.replace(" ","")[0]=="_":
            res.append(a)
    return res

cons=None
eclient=None
Data=None
Select=0
Selecting="func"
Result=None
History=[]
Status_Map={}
def get_result(mode="func"):
    global Selecting,Result,Data,Select,History
    Data=tree_func(client)
    Select=0
    Selecting=mode
    Result=None
    History=[]
    render(Data,Select)
    while Selecting:
        time.sleep(0.1)
    return Result

def Input(text):
    console.print(text,end="")
    t=time.time()
    r=input()
    while time.time()-t<0.2:
        t=time.time()
        r=input()
    return r

def register_keyboard(callback):
    t=threading.Thread(target=register_keyboard_thread,args=(callback,))
    t.daemon=True
    t.start()
    
def register_keyboard_thread(callback):
    global term
    term=Terminal()
    while True:
        with term.cbreak():
            val = term.inkey(timeout=0.1)
        if val and val.name and len(val.name):
            callback(val.name)
        while not Selecting:
            time.sleep(0.1)

def run():
    global console,client
    os.system("mode con cols=60 lines=20")
    console = Console(color_system='256', style=None)
    console.clear()
    console.rule("[bold blue]Initializing...", align='center')
    console.print("Connecting...")
    console.print("Server:",get_environment("lab_host",True)+":"+get_environment("lab_port",True))

    client=lab.client(key=get_environment("lab_secret"),host=get_environment("lab_host",True),port=get_environment("lab_port",True))

    register_keyboard(callback)

    while True:
        # 获取一个函数
        func=get_result()
        # 参数
        params={}
        console = Console(color_system='256', style=None)
        console.clear()
        # Input(f"按任意键继续...")
        console.clear()
        console.rule("[bold red]LABORATORY TERMINAL", align='left')
        if "_PARAMS" not in dir(func) or not func._EXECUTABLE or "__name__" not in dir(func):
            console.print(f"[red]函数不可执行![/red]")
            time.sleep(1)
            continue
        try:
            path=func._path
        except:
            path="CMS."+func.__name__
        console.print(f"目标函数:{path}(ID:{func._ID})")
        # 获取参数
        n=1
        for param in func._PARAMS:
            if param['OPTIONAL']:
                console.print(f"参数{n}.{param['NAME']} ({param['TYPE']},optional): {param['DESCRIPTION']}")
                if Input("是否需要此参数?(y/n)")=='n':
                    n+=1
                    continue
            else:
                console.print(f"参数{n}.{param['NAME']} ({param['TYPE']}): {param['DESCRIPTION']}")
            r=Input("从键盘输入参数值(空跳过):")
            if r=="":
                params[param['NAME']]=get_result("attr")
                console.clear()
                # Input(f"按任意键继续...")
                console.clear()
                console.rule("[bold red]LABORATORY TERMINAL", align='left')
                console.print(f"目标函数:{path}(ID:{func._ID})")
            else:
                try:
                    params[param['NAME']]=eval(r)
                except:
                    params[param['NAME']]=r
            n+=1
        r=Input("是否执行?(y/n) ")
        if r.lower()=='y':
            p_str=""
            for i in params:
                p_str+=f"{i}=params['{i}'],"
            p_str=p_str[:-1]
            if not path.startswith("CMS."):
                p_str=p_str+",_progress_callback=progress_callback"
            p_str=p_str[1:] if len(p_str) and p_str[0]==',' else p_str
            with Progress() as progress:
        
                task = progress.add_task('[green]Started.', total=100)
                def progress_callback(pro,progress_text):
                    progress.update(task, completed=pro,description=progress_text if progress_text else "[green]Processing...")
                try:
                    res=eval(f'func({p_str})')
                    res2=f"[green]执行成功,返回:[/green]"
                    console.print(res2)
                    console.print(res)
                    progress.update(task, advance=100,description="[blue]Finished.")
                except Exception as e:
                    res=f"[red]执行错误:{str(e)}[/red]"
                    progress.update(task, advance=100,description="[red]ERROR.")
                    console.print(res)
            Input("按任意键继续...")
        if r.lower()=='n':
            console.print("已取消执行.")
            
