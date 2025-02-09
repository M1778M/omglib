from threading import Thread,Timer
import random as _random
import time
_PUBLIC_EVENTS = []
EPublic = 1
EPrivate= 2

def _event_thread_call(call,args,kwargs):
    t=Thread(target=call,args=args,kwargs=kwargs,daemon=True)
    t.start()
    return t

def new(event):
    if event == Event:
        return Event(hash(str(_random.randint(1e10,9e10))))
    else:
        return event()

class Event:
    def __init__(self,event_id:int,event_:int=EPublic,event_handler_func=_event_thread_call):
        self.event_alive = True
        self.event_id = event_id
        self.event_functions = []
        self.alive_threads=[]
        self.thread_collector_active = False
        self.event_handler_func=event_handler_func
        self.loop_fires = []
        self.loop_fire_collector_active = False
        if event_ == EPublic:
            self.public = True
        else:
            self.public = False
        if self.public:
            _PUBLIC_EVENTS.append(self)
    def __call__(self):
        return self
    def clear_event_functions(self):
        self.event_functions=[]
    def thread_collector(self):
        self.thread_collector_active = True
        while self.event_alive:
            time.sleep(.1)
            for i,t in enumerate(self.alive_threads):
                if not t.is_alive():
                    self.alive_threads.pop(i)
                    continue
            time.sleep(.1)
    def disconnect(self,func):
        self.event_functions.remove(func)
        return 1
    def connect(self,func):
        self.event_functions.append(func)
        return 1
    def clear_threads(self):
        for t in self.alive_threads:
            t._stop()
            self.alive_threads.remove(t)
        return True
    def clear_loop_fires(self):
        for r in self.loop_fires:
            r.disconnect()
            self.loop_fires.remove(r)
        return True
    def WaitFire(self,ms,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()
        t=Timer(ms/1000,self.event_handler_func,args=(self.event_functions[-1],args_,data))
        t.start()
        self.alive_threads.append(t)
    def WaitFireAll(self,ms,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()
        for i,func in enumerate(self.event_functions):
            t=Timer(ms/1000,self.event_handler_func,args=(self.event_functions[i],args_,data))
            t.start()
            self.alive_threads.append(t)
    def Fire(self,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()
        self.alive_threads.append(self.event_handler_func(self.event_functions[-1],args_,data))
    def FireAll(self,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()
        for i,func in enumerate(self.event_functions):
            self.alive_threads.append(self.event_handler_func(self.event_functions[i],args_,data))
    @staticmethod
    def _loop_fire_func(sleep_ms:float,func,args,kwargs):
        r=_Runner(func,args,kwargs)
        t=Thread(target=r.run,args=(sleep_ms,))
        t.start()
        return r
    def LoopFire(self,every_ms:float,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()

        if not self.loop_fire_collector_active:
            Thread(target=self._loop_fire_collector,args=(),daemon=True).start()
        self.loop_fires.append(self._loop_fire_func(every_ms/1000,self.event_functions[-1],args_,data))
       
    def LoopFireAll(self,every_ms:float,args_:tuple=(),**data):
        if not self.thread_collector_active:
            Thread(target=self.thread_collector,args=(),daemon=True).start()

        if not self.loop_fire_collector_active:
            Thread(target=self._loop_fire_collector,args=(),daemon=True).start()
        for i,func in enumerate(self.event_functions):
            self.loop_fires.append(self._loop_fire_func(every_ms/1000,self.event_functions[i],args_,data))
    def _loop_fire_collector(self):
        self.loop_fire_collector_active = True
        while True:
            time.sleep(0.1)
            for i, r in enumerate(self.loop_fires):
                if not r.active:
                    self.loop_fires.pop(i)
                    continue
            time.sleep(0.1)
    def StopLastLoopFire(self,index=-1):
        self.loop_fires[index].disconnect()
    def StopAllLoopFires(self):
        for runner in self.loop_fires:
            runner.disconnect()
class _Runner:
    def __init__(self,func,args,kwargs):
        self.active = True
        self.func = func
        self.args=args
        self.kwargs=kwargs
    def disconnect(self):
        self.active = False
    def run(self,ms:float):
        while self.active:
            time.sleep(ms)
            Thread(target=self.func,args=self.args,kwargs=self.kwargs).start()
        return True

