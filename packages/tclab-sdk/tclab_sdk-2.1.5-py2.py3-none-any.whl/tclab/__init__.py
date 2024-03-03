import base64 as _base64
import hashlib as _hashlib
import json as _json
import os as _os
import string as _string
import subprocess as _subprocess
import threading as _threading
import time as _time
from Crypto.Cipher import AES as _AES
from Crypto.Util.Padding import pad as _pad, unpad as _unpad
import psutil as _psutil
import requests as _requests
import platform as _platform
import sys as _sys
import inspect as _inspect

class base:
    def __init__(self, key: str=False, **kwargs):
        """初始化

        Args:
            host (str): CMS服务器地址
            port (int): 端口
            key (str): 密钥
            key_file (str): 密钥文件路径
            try_times (int): 尝试次数
        """
        self._lab_server_host="https://cms.yht.life" if 'host' not in kwargs or not kwargs['host'] else kwargs['host']
        self._lab_server_port=False if 'port' not in kwargs or not kwargs['port'] else int(kwargs['port'])
        if not self._lab_server_port:
            self._lab_server_port=443 if self._lab_server_host.startswith("https://") else 80
        self._lab_server = f'{self._lab_server_host}:{self._lab_server_port}'
        self._try_times=10 if 'try_times' not in kwargs else int(kwargs['try_times'])
        key=(False if 'key' not in kwargs else kwargs['key']) if not key else key 
        if not key:
            key=self._import_key_from_file(False if 'key_file' not in kwargs else kwargs['key_file'])
        self._key = key
        
        self._check_connection(True)
        self._check_key(True)
        self._map_func()
        
    def _check_connection(self,excp:bool=False):
        """检查连接函数
        """
        times=0
        while True:
            try:
                res = _requests.post(f'{self._lab_server}/',timeout=10).text
                break
            except Exception as e:
                times+=1
                if times==self._try_times:
                    if excp:
                        raise Exception('[Module] Connection Failure.') 
                    return False
                
        if 'TC Laboratory Central Management System' not in res:
            if excp:
                raise Exception('[Module] Server Invalid.')
            return False
        return True

    def _check_key(self,excp:bool=False):
        """检查密钥函数
        """
        if not self._encrypt_data(_json.dumps({}, ensure_ascii=False), self._key):
            if excp:
                raise Exception('[Module] Key Invalid.')
            return False
        return True
        
    def _import_key_from_file(self,path:str=False):
        """导入密钥函数

        Args:
            path (str): 密钥路径

        Returns:
            str: 密钥
        """
        # 如果没有密钥路径
        if not path:
            for part in _psutil.disk_partitions():
                p=f"{part.device}.lab/key"
                if _os.path.exists(p):
                    f=open(p,'r',encoding='utf-8')
                    d=f.read()
                    f.close()
                    return d
            raise Exception('[Module] Key File Not Found.')
        try:
            f=open(path,'r',encoding='utf-8')
            d=f.read()
            f.close()
        except:
            raise Exception('[Module] Cannot Read Key File.')
        return d
    
    def _encrypt_data(self,data: str, key: str):
        """加密函数

        Args:
            data (str): 待加密的数据
            key (str): 加密密钥

        Returns:
            str: base64格式的加密数据
        """
        try:
            key = key.encode()
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.encrypt(_pad(data.encode('utf-8'), _AES.block_size))
            return _base64.b64encode(text).decode()
        except:
            return False


    def _decrypt_data(self,data: str, key: str):
        """解密函数

        Args:
            data (str): 加密的数据
            key (str): 密钥

        Returns:
            str: 解密的数据
        """
        try:
            key = key.encode()
            data = _base64.b64decode(data)
            cryptor = _AES.new(key, _AES.MODE_ECB)
            text = cryptor.decrypt(data)
            text = _unpad(text, _AES.block_size).decode()
            data=_json.loads(text)
            return data['data']
        except:
            return False
    
    def _request(self, data: dict={}):
        """向CMS发送数据

        Args:
            data (dict): 数据

        """
        data = {
            "key_md5": _hashlib.md5(self._key.encode(encoding='utf-8')).hexdigest(),
            "timestamp": _time.time(),
            "data": data
        }
        data = self._encrypt_data(_json.dumps(data, ensure_ascii=False), self._key)

        times=0
        while True:
            try:
                res = _requests.post(self._lab_server,json={'data': data},timeout=10).text
                break
            except Exception as e:
                times+=1
                if times==self._try_times:
                    raise Exception('[Module] Connection Failure.') 

        r = self._decrypt_data(res, self._key)
        res=r if r else _json.loads(res)
        if res and int(res['status_code']) == 1:
            return res['data']
        if res['status_code'] == 0:
            raise Exception(f"[CMS] {res['data']}")

    def _generate_execute(self,name):
        """生成执行函数
        """
        def execute(kw=False,**kwargs):
            data={}
            for i in self._func[name]["PARAMS"]:
                data[i["NAME"]]=i["DEFAULT"]
            if kw:
                kwargs=kw
            for i in kwargs:
                _in=False
                for j in data:
                    if i.upper()==j.upper():
                        data[j]=kwargs[i]
                        _in=True
                if not _in:
                    data[i]=kwargs[i]
                
            for i in data:
                if data[i]==None:
                    raise Exception(f'[CMS] Params Invalid.({i})')
            return self._request({'command': name, 'data': data})

        return execute
        
    def _deep_copy(self,data):
        """深拷贝函数
        """
        if type(data) in [int, float, str, bool, type(None)]:
            return data
        if type(data)==list:
            return [self._deep_copy(i) for i in data]
        if type(data)==dict:
            return {i:self._deep_copy(data[i]) for i in data}
        return data
    
    def _map_func(self):
        self._func={
            'create': {
                'ID': '4fbfc5e509114a5fa69aa09f8af4fb81',
                'NAME': 'create',
                'DESCRIPTION': '创建一个对象',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'NAME',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'TYPE',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'DESCRIPTION',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': '',
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'MINIMUM_LEVEL',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': 4,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'PARENT_NODE',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': 1,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'PROPERTIES',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': {},
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'EXECUTABLE',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': True,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'PARAMS',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': [],
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'CALLBACK_TYPE',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': '[]',
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'CHILDREN',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': [],
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'delete': {
                'ID': '8932f85b072648c28bfed56fbe2e605a',
                'NAME': 'delete',
                'DESCRIPTION': '删除对象',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'only_child',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': False,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'execute': {
                'ID': '5ae6f65e39db4252b067497fefe684e7',
                'NAME': 'execute',
                'DESCRIPTION': '执行对象',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'params',
                        'TYPE': 'str',
                        'OPTIONAL': True,
                        'DEFAULT': [],
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'heartbeat': {
                'ID': '57bf0a2d7bae47f8a2eb6f8a53cfb014',
                'NAME': 'heartbeat',
                'DESCRIPTION': '发送心跳包并请求任务',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'query': {
                'ID': '551fd28b8a2c47f7969ccfe7fc97d7cc',
                'NAME': 'query',
                'DESCRIPTION': '查询任务状态',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'task_id',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'update': {
                'ID': 'ad3d03676bb743c0ab3f4ec7fa0e9811',
                'NAME': 'update',
                'DESCRIPTION': '更新任务状态',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    },
                    {
                        'NAME': 'task_id',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'get_obj_path': {
                'ID': 'ea5a5a69a0ac43e8870bf1f0fafaaded',
                'NAME': 'get_obj_path',
                'DESCRIPTION': '获取对象路径',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'get_path_obj': {
                'ID': 'fd98aa74fa804f3fa0066dac8e57ca14',
                'NAME': 'get_path_obj',
                'DESCRIPTION': '获取路径ID',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'path',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'get': {
                'ID': '511487ca4611496b9b726fa9eff36081',
                'NAME': 'get',
                'DESCRIPTION': '获取对象全部信息',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'exist': {
                'ID': '70dd7c07ba814f34870d575e853d856f',
                'NAME': 'exist',
                'DESCRIPTION': '获取是否存在',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            },
            'tree': {
                'ID': 'a876cfdd9dd84ddea3c25605878e52ed',
                'NAME': 'tree',
                'DESCRIPTION': '列出对象子节点',
                'TYPE': 'FUNCTION',
                'MINIMUM_LEVEL': 4,
                'PARENT_NODE': 2,
                'PARAMS': [
                    {
                        'NAME': 'ID',
                        'TYPE': 'str',
                        'OPTIONAL': False,
                        'DEFAULT': None,
                        'DESCRIPTION': ''
                    }
                ],
                'CALLBACK_TYPE': [
                    {'TYPE': 'str', 'DESCRIPTION': ''}
                ],
                'EXECUTABLE': True,
                'PROPERTIES': {},
                'CHILDREN': []
            }
        }
        for i in self._func:
            exec(f"self.{i}=self._generate_execute(i)")
            for j in self._func[i]:
                exec(f"self.{i}._{j}=self._func[i][j]")
    
    def _textualize(self,name,data):
        """文本对象化

        Args:
            name (str): 对象名称
            data: 任意对象

        Returns:
            dict: 对象
        """
        if type(data)==tuple:
            data=list(data)
        if type(data) in [int, float, str, bool, type(None)]:
            return {"NAME":name,"TYPE":"VALUE","DATA":data}
        if type(data) in [list, dict]:
            return {"NAME":name,"TYPE":"OBJECT","DATA":data}
        
    def _substantialize(self,p):
        """对象实体化

        Args:
            p (dict): 对象

        Returns:
            _type_: 对应对象
        """
        if p["TYPE"] in ["VALUE","OBJECT"]:
            return p["DATA"]
            

class client:
    def __init__(self,**kwargs):
        # 初始化
        self._base=base(**kwargs)
        # 挂载对象
        self._mount_point_id=kwargs['mount_point'] if 'mount_point' in kwargs else '1'
        self._mount_point_id=self._trans2id(self._mount_point_id)
        self._mount(self,self._mount_point_id)
        # 刷新间隔
        self._refresh_interval=kwargs['refresh_interval'] if 'refresh_interval' in kwargs else 5
        self._query_refresh_interval=kwargs['query_refresh_interval'] if 'query_refresh_interval' in kwargs else 0.5
        # 挂载CMS操作
        self.CMS=self._base
        self.CMS._DESCRIPTION="管理CMS"
        # 定时重新挂载
        self._refresh_thread=_threading.Thread(target=self._refresh)
        self._refresh_thread.daemon=True
        self._refresh_thread.start()
    
    def _refresh(self):
        """定时重新挂载
        """
        while True:
            self._mount(self,self._mount_point_id)
            _time.sleep(self._refresh_interval)
    
    def _trans2id(self,p):
        """转换为id并检测是否合法

        Args:
            p (str): 路径或id
            
        Returns:
            str: id
        """
        if self._base.exist(id=p):
            return p
        return self._base.get_path_obj(path=p)
        
        
    def _mount(self,mount_point,mount_point_id,root_path='',_mount_data=False):
        """挂载对象
        """
        if _mount_data==False:
            self._mount_data=self._base.tree(id=mount_point_id)
            _mount_data=self._mount_data
        for obj in _mount_data:
            exec(f"mount_point.{obj['NAME'].replace('-','_')}=self._generate_execute(obj)")
            # 挂载属性
            for attr in obj:
                exec(f"mount_point.{obj['NAME'].replace('-','_')}._{attr}=obj[attr]")
            # 刷新函数
            exec(f"mount_point.{obj['NAME'].replace('-','_')}._refresh=self._generate_refresh(mount_point,mount_point_id)")
            # 节点状态检测
            exec(f"mount_point.{obj['NAME'].replace('-','_')}._status=self._generate_status(mount_point.{obj['NAME'].replace('-','_')})")
            # 自身路径
            exec(f"mount_point.{obj['NAME'].replace('-','_')}._path='{root_path+obj['NAME']}'")
            self._mount(eval(f"mount_point.{obj['NAME'].replace('-','_')}"),obj['ID'],root_path+obj['NAME']+'.',obj["CHILDREN"])
            
    def _generate_refresh(self,mount_point,mount_point_id):
        """生成刷新函数
        """
        def refresh():
            self._mount(mount_point,mount_point_id)
                
        return refresh
    
    def _generate_status(self,obj):
        """生成状态函数
        """
        def status():
            # 刷新数据
            obj._refresh()
            # 检测状态
            status_map={"Online":[0,5],"Slow":[5,20],"Offline":[20,999999999]}
            for i in status_map:
                if status_map[i][0]<_time.time()-obj._REFRESH_TIMESTAMP<status_map[i][1]:
                    return i  
        return status
    
    def _generate_execute(self,obj):
        """生成执行函数
        """
        def execute(**params):
            return self._execute(obj["ID"],params)
        return execute
    
    def _execute(self,id,params):
        """执行命令
        """
        # 解析参数
        # 回调
        _progress_callback=False
        if '_progress_callback' in params:
            _progress_callback=params['_progress_callback']
            del params['_progress_callback']
        # 超时时间
        _timeout=False
        if '_timeout' in params:
            _timeout=params['_timeout']
            del params['_timeout']
        
        # 对象化
        ps=[]
        for p in params:
            ps.append(self._base._textualize(p,params[p]))
        kwargs={"ID":id,"params":ps}
        # 创建任务
        task=self._base.execute(kwargs)
        # 查询任务
        start_time=_time.time()
        res=self._base.query(task)
        while res["status"] in ["created","processing"]:
            res=self._base.query(task)
            # 回报进度
            if _progress_callback:
                _progress_callback(res["progress"],res["progress_text"])
            _time.sleep(self._query_refresh_interval)
            if _timeout and _time.time()-start_time>_timeout:
                raise Exception('[Task] Timeout.')
        
        # 返回结果
        if res["status"]=="failed":# 如果失败
            raise Exception('[Task] '+ res["progress_text"])
        elif res["status"]=="finished":# 成功返回结果
            data=[]
            for r in res["result"]:
                data.append(self._base._substantialize(r))
            return tuple(data)
        else:
            raise Exception(f'[Task] Unknown Error.(res["status"]="{res["status"]}")')
    
    
class device:
    def __init__(self,device_id=False,**kwargs):
        # 映射表
        self._map={}
        # 处理中的和已完成的任务
        self._tasks=[]
        # 刷新间隔
        self._refresh_interval=kwargs['refresh_interval'] if 'refresh_interval' in kwargs else 0.5
        # 挂载点
        self._mount_point_id=kwargs['mount_point'] if 'mount_point' in kwargs else device_id
        self._kwargs=kwargs
        # 开发模式
        if 'develop' in kwargs:
            if kwargs['develop']:
                print('[Module] Develop Mode.Do Not Use In Production.')
                self._develop=True
                return
        self._develop=False
        # 初始化
        if not device_id and 'device_id' not in kwargs:
            raise Exception('[Module] Device ID Required.')
        self.device_id=device_id if device_id else kwargs['device_id']
        self._base=base(**kwargs)
        # 挂载函数
        self._mount_point_id=self._trans2id(self._mount_point_id)
        self._mount_point_path=self._base.get_obj_path(id=self._mount_point_id)
        
    def run(self,silent=False,block=True):
        if not block:
            self.run_thread=_threading.Thread(target=self.run,args=(silent,))
            self.run_thread.daemon=True
            self.run_thread.start()
            return
        if self._develop:
            self.build()
            return
        _print=print
        if silent:
            _print=lambda x:x
        _print("[INFO] Checking...")
        try:
            e,m,t=self.statistics()
            _print(t)
        except Exception as e:
            _print(f"[WARNING] No Permission To Access Tree.")
        _print("[INFO] Started.")
        while True:
            try:
                self._check()
            except Exception as e:
                print(f"[WARNING] Could Not Refresh Tasks.({str(e)})")
            _time.sleep(self._refresh_interval)
    
    def _trans2id(self,p):
        """转换为id并检测是否合法

        Args:
            p (str): 路径或id
            
        Returns:
            str: id
        """
        if self._base.exist(id=p):
            return p
        return self._base.get_path_obj(path=p)
    
    def _trans2path(self,p):
        """转换为完整path

        Args:
            p (str): 路径或id
            
        Returns:
            str: path
        """
        if self._base.exist(id=p):
            return self._base.get_obj_path(id=p)
        p=self._mount_point_path+'.'+p if p else self._mount_point_path
        if not self._base.get_path_obj(path=p):
            raise Exception(f'[Module] Path Invalid.({p})')
        return p
    
    def mount(self,path,mode='direct'):
        """挂载函数到对象路径

        Args:
            path (str): 路径或id
            mode (str): 传参方式(direct/packed)
        """
        id=path
        if not self._develop:
            path=self._trans2path(path)
            id=self._trans2id(path)
        def outwrapper(func):
            self._map[id]={"func":func,"mode":mode}
            return func
        return outwrapper
    
    def _check(self):
        """检查并执行命令
        """
        res=self._base.heartbeat(id=self.device_id,status=["created","processing"])
        for r in res:
            if r['status']=='created':  
                self._tasks.append(r["task_id"])
                # 标记为进行中
                self._base.update(id=r["ID"],task_id=r['task_id'],status='processing')
                t=_threading.Thread(target=self._execute,args=(r,))
                t.daemon=True
                t.start()
            # 未完成的任务
            if r['status']=='processing' and r["task_id"] not in self._tasks:
                self._base.update(id=r["ID"],task_id=r['task_id'],status='created',progress_text='',progress=0)
            
    def _execute(self,task):
        """执行命令
        """
        # 如果未连接到此对象
        if not task["ID"] in self._map:
            self._tasks.remove(task["task_id"])
            return
        # 执行命令
        try:
            # 解析参数
            params={}
            for p in task["params"]:
                params[p['NAME']]=self._base._substantialize(p)
            if self._map[task["ID"]]["mode"]=='packed':
                # 注册进度函数
                params["_progress_callback"]=self.generate_progress_callback(task)
                self._finish(self._map[task["ID"]]["func"](params),task)
            elif self._map[task["ID"]]["mode"]=='direct':
                p_str=""
                for i in params:
                    p_str+=f"{i}=params['{i}'],"
                p_str=p_str[:-1]
                p_str=p_str+",_progress_callback=self.generate_progress_callback(task)" if '_progress_callback' in _inspect.getargspec(self._map[task["ID"]]["func"]).args else p_str
                p_str=p_str[1:] if len(p_str) and p_str[0]==',' else p_str
                self._finish(eval(f'self._map[task["ID"]]["func"]({p_str})'),task)
            else:
                raise Exception('[Module] Mode Invalid.')
        except Exception as e:
            self._fail(str(e),task)
    
    def generate_progress_callback(self,task):
        """生成进度回调函数

        Args:
            task (dict): 任务
        """
        def progress_callback(progress=False,progress_text=False):
            """上传进度

            Args:
                progress (float): 进度(可选)
                progress_text (bool, optional): 进度信息(可选)
            """
            if progress_text:
                self._base.update(id=task["ID"],task_id=task['task_id'],progress=progress,progress_text=progress_text)
            else:
                self._base.update(id=task["ID"],task_id=task['task_id'],progress=progress)
        return progress_callback
        
    def _finish(self,res,task):
        params=[]
        if type(res) == tuple:
            for i in res:
                params.append(self._base._textualize('',i))
        else:
            params.append(self._base._textualize('',res))
        self._base.update(id=task["ID"],task_id=task['task_id'],status='finished',result=params,progress=100)
        
    def _fail(self,res,task):
        self._base.update(id=task["ID"],task_id=task['task_id'],status='failed',progress_text=res,progress=100)
        
    def statistics(self,id=None):
        """统计挂载情况
        """
        recursion=True
        if not id:
            id=self.device_id
            recursion=False
        executable=0
        mounted=0
        for i in self._base.tree(id=id):
            if i["EXECUTABLE"]:
                executable+=1
            if self._map.get(i["ID"]):
                mounted+=1
            exec,moun=self.statistics(i['ID'])
            executable+=exec
            moun+=moun
        if not recursion:
            mounted=len(self._map)
            if self._map.get(id):
                executable+=1
            t=f"[INFO] Mounted:{mounted} Executable:{executable}"
            if executable:
                t+=f" Percent:{round(mounted/executable*100,2)}%"
            return executable,mounted,t
        return executable,mounted
    
    def build(self):
        """构建设备(开发模式下)
        """
        if not self._develop:
            raise Exception('[Module] Develop Mode Required.')
        def get_indent(text):
            """获取缩进数
            """
            return text.index(text.replace(" ",'')[0])
        def parse_annotation(doc,target):
            """解析注释
            """
            if not doc:
                doc=""
            doc=doc.replace("\t","    ")
            lines=doc.splitlines()
            target=target.upper()
            if target=="FUNC":
                t=doc.splitlines()
                if not t:
                    return ''
                return t[0]
            if target=="PARAMS":
                args_lines=[]
                r=False
                indent=0
                args=[]
                for line in lines:
                    if line.replace(" ",'')=='' or get_indent(line)==indent:
                        r=False
                        continue
                    # 若在Args内
                    if r:
                        # 获取参数名和类型
                        arg=line.split(":")[0]
                        arg_name=arg.split(" (")[0].replace(" ",'')
                        arg_type=arg.split(" (")[1].split(")")[0]
                        arg_optional=False
                        if ',' in arg_type:
                            arg_type=arg_type.split(",")[0].replace(" ",'')
                            arg_optional=True
                        # 获取参数注释
                        arg_description=line.split(":")[1][1:]
                        # 获取参数默认值
                        arg_default=False
                        if arg_optional:
                            arg_default=line.split("Defaults to ")[1][:-1]
                        args.append({"NAME":arg_name,"TYPE":arg_type,"OPTIONAL":arg_optional,"DEFAULT":arg_default,"DESCRIPTION":arg_description})
                    if line.replace(" ",'').startswith("Args:"):
                        r=True
                        indent=get_indent(line)
                        continue
                return args
            if target=="CALLBACK_TYPE":
                r=False
                indent=0
                returns=[]
                for line in lines:
                    if line.replace(" ",'')=='' or get_indent(line)==indent:
                        r=False
                        continue
                    # 若在Returns内
                    if r:
                        # 获取参数类型
                        arg=line.split(":")[0]
                        arg_type=arg.replace(" ",'')
                        # 获取参数注释
                        arg_description=line.split(":")[1][1:]
                        returns.append({"TYPE":arg_type,"DESCRIPTION":arg_description})
                    if line.replace(" ",'').startswith("Returns:"):
                        r=True
                        indent=get_indent(line)
                        continue
                return returns
            if target=="LEVEL":
                for line in lines:
                    if line.replace(" ",'').startswith("Level:"):
                        return int(line.split("Level: ")[1].replace(" ",''))
                return False
            if target=="PROPERTIES":
                r=False
                indent=0
                properties={}
                for line in lines:
                    if line.replace(" ",'')=='' or get_indent(line)==indent:
                        r=False
                        continue
                    # 若在Properties内
                    if r:
                        # 获取参数名称
                        arg_name=line.split(":")[0].replace(" ",'')
                        # 获取参数值
                        arg_value=eval(line.split(":")[1])
                        properties[arg_name]=arg_value
                    if line.replace(" ",'').startswith("Properties:"):
                        r=True
                        indent=get_indent(line)
                        continue
                return properties
            return ''
        def build_func_data(i,inherit_level=4):
            """构建函数信息
            """
            doc=self._map[i]["func"].__doc__
            if i!='':
                NAME=i.split('.')[-1]
            else:
                NAME=self._map[i]["func"].__name__
            DESCRIPTION=parse_annotation(doc,"func")
            EXECUTABLE=True
            TYPE="FUNCTION"
            if i=='':
                TYPE="DEVICE"
            PROPERTIES=parse_annotation(doc,"properties")
            PARAMS=parse_annotation(doc,"params")
            CALLBACK_TYPE=parse_annotation(doc,"callback_type")
            LEVEL=parse_annotation(doc,"level") if parse_annotation(doc,"level") else inherit_level
            CHILDREN=[]
            for j in self._map:
                if ((i=="" and j.count(".")==0) or (i!="" and j.startswith(i+'.'))) and i!=j:
                    CHILDREN.append(build_func_data(j,LEVEL))
            return {
                "NAME":NAME,
                "TYPE":TYPE,
                "DESCRIPTION":DESCRIPTION,
                "MINIMUM_LEVEL":LEVEL,
                "PROPERTIES":PROPERTIES,
                "EXECUTABLE":EXECUTABLE,
                "PARAMS":PARAMS,
                "CALLBACK_TYPE":CALLBACK_TYPE,
                "CHILDREN":CHILDREN
            }
        
        
        # 请求整体设备信息
        if "" not in self._map:
            NAME=input("Enter Device Name:")
            DESCRIPTION=input("Enter Device Description:")
            LEVEL=input("Enter Device Minimum Level(Default 4):")
            if not LEVEL:
                LEVEL=4
            LEVEL=int(LEVEL)
            DATA={
                "NAME":NAME,
                "TYPE":"DEVICE",
                "DESCRIPTION":DESCRIPTION,
                "MINIMUM_LEVEL":LEVEL,
                "PROPERTIES":{},
                "EXECUTABLE":False,
                "PARAMS":[],
                "CALLBACK_TYPE":[],
                "CHILDREN":[]
            }
            for j in self._map:
                if j.count('.')==0:
                    try:
                        DATA["CHILDREN"].append(build_func_data(j))
                    except:
                        print(f"[ERROR] Build Function Data Failed.({j})")
                        _sys.exit()
        else:
            try:
                DATA=build_func_data("")
            except Exception as e:
                print(f"[ERROR] Build Function Data Failed.(ROOT)")
                _sys.exit()
        print("[INFO] Build Success.")
        if not input("Mount Now?(Enter To Exit)"):
            print(DATA)
            print("Done.")
            return
        secret=input("Enter Tclab Secret To Mount:")
        self._kwargs["key"]=secret
        self._base=base(**self._kwargs)
        path=input("Where To Mount?(Enter Path Or ID):")
        DATA["PARENT_NODE"]=self._trans2id(path)
        res=self._base._request({'command': "create", 'data': DATA})
        print(f"Copy: device=lab.device(device_id=\"{res['ID']}\",key=\"{res['AUTHORIZATION_CODE']}\")")
        print("Done.")
        return