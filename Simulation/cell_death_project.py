
from cc3d import CompuCellSetup
        

from cell_death_projectSteppables import cell_death_projectSteppable

CompuCellSetup.register_steppable(steppable=cell_death_projectSteppable(frequency=1))


CompuCellSetup.run()
