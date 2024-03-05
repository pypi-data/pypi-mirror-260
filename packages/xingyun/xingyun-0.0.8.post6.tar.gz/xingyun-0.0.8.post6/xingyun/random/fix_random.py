import time
import copy
import random
from typing import Any
from xingyun.universal.import_module import my_import_module

from .set_random_seed import RandomAllowedModule

def get_random_state(module: RandomAllowedModule) -> Any:
    if module == "random":
        return random.getstate()
    
    if module == "numpy":
        np = my_import_module("numpy")
        if np is None:
            return None
        return np.random.get_state()
    
    if module == "torch":
        torch = my_import_module("torch")
        cuda = my_import_module("torch.cuda")

        if (torch is None) or (cuda is None):
            return None

        return {
            "torch": torch.random.get_rng_state(),
            "cuda" : cuda .random.get_rng_state(),
        }

def set_random_state(state: Any, module: RandomAllowedModule) -> bool:
    flag = True
    if module == "random":

        try:
            random.setstate(state)
        except:
            flag = False
    
    if module == "numpy":

        np = my_import_module("numpy")
        if (np is None) or (state is None):
            return False
        
        try:
            np.random.set_state(state)
        except:
            flag = False
    
    if module == "torch":
        torch = my_import_module("torch")
        cuda = my_import_module("torch.cuda")

        if (torch is None) or (cuda is None):
            return False
        try:
            torch.random.set_rng_state(state["torch"])
            cuda.random.set_rng_state(state["cuda"])
        except:
            flag = False
            
    
    if not flag:
        raise RuntimeError(f"set random state of module {module} bad.")

    return flag

class FixRandom:
    def __init__(self, random_seed: int | None = None, modules:  list[RandomAllowedModule] = ["random" , "torch" , "numpy"]):
        '''This class create a temporary environment, inside which the random seed 
        is set to a given value while not affecting the global random seed.

        Notice that, to make this class work, the global random seed must be also managed by `xingyun`.
        '''
        if random_seed is None:
            random_seed = int( time.time() )
    
        self.random_seed = random_seed
        self.modules = modules

        self.entering_state = {}

    def __enter__(self):
        for m in self.modules:
            self.entering_state[m] = get_random_state(m)
    
    def __exit__(self, *args, **kwargs):
        for m in self.modules:
            set_random_state(self.entering_state[m],m)
            


        



