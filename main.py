
#------------------------------------------------------------------------------
#from __future__ import division  
#python_version = 3.7           
from crudleEngine import *
#------------------------------------------------------------------------------
def main():

    state_machine.setState(State("main_menu"))
    clock = sf.Clock()
    while window.is_open:
        state_machine.eventHandle()
        state_machine.update()
        state_machine.draw()
main()

#------------------------------------------------------------------------------
