#-----------------------------------------------------------------------------------------------
#   rubiks_cube_execution.py
#   created on: 23-Dez-2025
#-----------------------------------------------------------------------------------------------
from enum import Enum, auto
from solver.GetCubeOrientation import *

#--- definitions -------------------------------------------------------------------------------
class state(Enum):
    STATE_IDLE                  = auto()
    SATE_SHOOT_PIC              = auto()
    STATE_RECONSTRUCTION_CUBE   = auto()
    STATE_CALC_SOLUTION         = auto()
    STATE_CONVERT_STR           = auto()
    STATE_IMPELEMENT_SOLUTION   = auto()
    STATE_ERROR                 = auto()
#--- local variables ---------------------------------------------------------------------------
_robot3 = None
_robot4 = None
_stateHandler = None
_state = None
_running = False

    
#--- private functions -------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_idle():
    
    return state.SATE_SHOOT_PIC
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_shootPic():
    pass
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_reconstructionCube():
    pass
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_calculateSolution():
    pass
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_convertString():
    pass
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_implementSolution():
    pass
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def _statemachine_error():
    pass
#--- public functions --------------------------------------------------------------------------    
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def rubiksCubeExe_start():
    _stateHandler.get(_state, _statemachine_error)
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def rubiksCubeExe_getColorString():
    
    
    string = get_final_color_string()
    return string
#-----------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------
def rubiksCubeExe_init(robot3, robot4):
    global _robot3, _robot4, _stateHandler

    _robot3 = robot3
    _robot4 = robot4

    _stateHandler = {
        state.STATE_IDLE:                   _statemachine_idle,
        state.STATE_ERROR:                  _statemachine_error,          
        state.SATE_SHOOT_PIC:               _statemachine_shootPic,      
        state.STATE_RECONSTRUCTION_CUBE:    _statemachine_reconstructionCube,
        state.STATE_CALC_SOLUTION:          _statemachine_calculateSolution,    
        state.STATE_CONVERT_STR:            _statemachine_convertString,     
        state.STATE_IMPELEMENT_SOLUTION:    _statemachine_implementSolution,   
        state.STATE_ERROR:                  _statemachine_error      
    }







