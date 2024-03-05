"""Pythagoras aims to democratize access to distributed serverless compute.

We make it simple and inexpensive to create, deploy and run planet-scale
massively parallel algorithms from within local Python scripts and notebooks.
Pythagoras makes data scientists' lives easier, while allowing them to
solve more complex problems in a shorter time with smaller budgets.
"""
from typing import Optional, Callable, Dict
from random import Random
from persidict import PersiDict

from pythagoras._99_misc_utils import *
from pythagoras._01_foundational_objects import *
from pythagoras._02_ordinary_functions import *
from pythagoras._03_autonomous_functions import *
from pythagoras._04_idempotent_functions import *
from pythagoras._05_events_and_exceptions import *
from pythagoras._06_mission_control import *


global_value_store:Optional[PersiDict] = None
global_crash_history: Optional[PersiDict] = None
global_event_log: Optional[PersiDict] = None

function_output_store:Optional[PersiDict] = None
function_execution_requests:Optional[PersiDict] = None
function_execution_attempts:Optional[PersiDict] = None
function_crash_history:Optional[PersiDict] = None
function_event_log:Optional[PersiDict] = None


# ??????????????????????????????????????
function_garage:Optional[PersiDict] = None # ????
function_source_repository:Optional[PersiDict] = None # ????
# ??????????????????????????????????????


all_autonomous_functions:Optional[Dict[str|None,Dict[str,AutonomousFunction]]] = None
default_island_name: Optional[str] = None
entropy_infuser: Optional[Random] = None
initialization_parameters: Optional[dict] = None

primary_decorators = {d.__name__:d for d in [
    idempotent, autonomous, strictly_autonomous]}
all_decorators = {d.__name__:d for d in [
    idempotent, autonomous, strictly_autonomous, ordinary]}


