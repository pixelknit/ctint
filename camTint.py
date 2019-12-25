import hou

import os

def camTint():
    try:
        node = hou.selectedNodes()[0]
        values=node.parm('numobj').eval()
        path = node.parent().path()
        #print path
        allsub = []
        bnull = hou.node(path).createNode('null', 'GEO_IN')
        bnull.moveToGoodPosition()
        
        for i in range(values):
            
            vol=hou.node(path).createNode('volume', 'vdb{}'.format(i))
            parm = vol.parm('dimensionsource1')
            parm.set(1)
            vol.setParms({'camera':'../../cam{}'.format(i+1),'zmax':200, 'name': 'cam{}'.format(i), 'initialval1': 1, 'samplediv': 100})
            vol.moveToGoodPosition()
            innull = bnull.createOutputNode('null', 'IN')
            innull.moveToGoodPosition()
            solver = hou.node(path).createNode('solver')
            solver.allowEditingOfContents(True)
            solver.moveToGoodPosition()
            solver.setInput(0, innull)
            solver.setInput(1, vol)

            kpath = solver.path() + '/d/s/'
            input1 = hou.node(kpath + 'Input_1')
            input2 = hou.node(kpath + 'Input_2')
            prevframe = hou.node(kpath + 'Prev_Frame')
            aw = hou.node(kpath).createNode('attribwrangle','test')
            aw.moveToGoodPosition()
            aw.setInput(0, input1)
            aw.setInput(1, input2)
            aw.setInput(2, prevframe)
            aw.parm('snippet').set('@sample += point(2,"sample",@ptnum) + volumesample(1, 0 ,@P);')
            aw.createOutputNode('output')

            cl = solver.createOutputNode('color')
            cl.moveToGoodPosition()
            cl.parm('colortype').set(3)
            cl.parm('rampattribute').set('sample')
            cl.setParms({'ramp1cr': 1, 'ramp1cg': 1, 'ramp1cb': 1})
            cl.setParms({'ramp2cr': 0, 'ramp2cg': 1, 'ramp2cb': 0})
            cl.setColor(hou.Color((1.0,0.23,0.13)))

            #break
            
        cl_mix = hou.node(path).createNode('attribwrangle', 'color_mix')
        cl_mix.moveToGoodPosition()
        cl_mix.parm('snippet').set('@Cd *= point(1,"Cd",@ptnum);')
    except:
        hou.ui.displayMessage('Please select the camera object merge node')
#camtint()