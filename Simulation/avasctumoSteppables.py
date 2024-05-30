
from cc3d.core.PySteppables import *



class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        for cell in self.cell_list:

            cell.targetVolume = 25
            cell.lambdaVolume = 2.0
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
    
        secretor = self.get_field_secretor("Nutrients")
        field = self.field.Nutrients
        
        for cell in self.cell_list_by_type(self.PROL):
            cell_secr = secretor.uptakeInsideCellTotalCount(cell, 2.0, 0.01)
            cell.targetVolume += -cell_secr.tot_amount/50
            
            if field[cell.xCOM,cell.yCOM,0]<66:
                cell.type=self.QUIE
            
        
        for cell in self.cell_list_by_type(self.QUIE): 
            secretor.uptakeInsideCell(cell, 2.0, 0.01) 
            
            if field[cell.xCOM,cell.yCOM,0]>66:
                cell.type=self.PROL
            if mcs<1000:
                if field[cell.xCOM,cell.yCOM,0]<23:
                    cell.type=self.NECR
         
        for cell in self.cell_list_by_type(self.NECR):
            cell.targetVolume -= 1

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        # field = self.field.CHEMICAL_FIELD_NAME
        
        # for cell in self.cell_list:
            # concentrationAtCOM = field[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]

            # # you can use here any fcn of concentrationAtCOM
            # cell.targetVolume += 0.01 * concentrationAtCOM       

        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>50:
                cells_to_divide.append(cell)

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=2
        # else:
            # self.child_cell.type=1

        