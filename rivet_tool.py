'''
////////////////////////////////////////////////////////////////
----------------------------------------------------------------
This tool allow you to create a bounch of rivets over a surface
----------------------------------------------------------------
                        Run the code
////////////////////////////////////////////////////////////////
'''
import maya.cmds as cmds

#Proc to lock and hide Attributes
def locknHide(obj):
      st_attrs = ['tx', 'ty', 'tz','rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
      for attr in st_attrs:
            cmds.setAttr('{}.{}'.format(obj, attr), l=1, k=0, cb=0)

#Proc to create a single rivet in a surface
def createRivet(n, grp, srfc, v = .5, u = .5, maxU=1, maxV=1):
      loc = cmds.spaceLocator(n='{}_Loc'.format(n))[0]
      pos = cmds.createNode('pointOnSurfaceInfo', n = '{}_Pos'.format(n))
      fbfMtx = cmds.createNode('fourByFourMatrix', n = '{}_Fbf'.format(n))
      mMtx = cmds.createNode('multMatrix', n = '{}_mMtx'.format(n))     
      dMtx = cmds.createNode('decomposeMatrix', n = '{}_dMtx'.format(n))
      #Sets
      cmds.setAttr('{}.parameterV'.format(pos), v)
      cmds.setAttr('{}.parameterU'.format(pos), u)
      cmds.addAttr(loc, ln='paramU', at='double', min=0, max=maxU, dv=u, k=1)
      cmds.addAttr(loc, ln='paramV', at='double', min=0, max=maxV, dv=v, k=1)
      #Connections
      cmds.connectAttr('{}.worldSpace[0]'.format(srfc), '{}.inputSurface'.format(pos))
      cmds.connectAttr('{}.positionX'.format(pos), '{}.in30'.format(fbfMtx))
      cmds.connectAttr('{}.positionY'.format(pos), '{}.in31'.format(fbfMtx))
      cmds.connectAttr('{}.positionZ'.format(pos), '{}.in32'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedNormalX'.format(pos), '{}.in00'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedNormalY'.format(pos), '{}.in01'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedNormalZ'.format(pos), '{}.in02'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentUX'.format(pos), '{}.in10'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentUY'.format(pos), '{}.in11'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentUZ'.format(pos), '{}.in12'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentVX'.format(pos), '{}.in20'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentVY'.format(pos), '{}.in21'.format(fbfMtx))
      cmds.connectAttr('{}.normalizedTangentVZ'.format(pos), '{}.in22'.format(fbfMtx))
      cmds.connectAttr('{}.output'.format(fbfMtx), '{}.matrixIn[0]'.format(mMtx))
      cmds.connectAttr('{}.worldInverseMatrix'.format(grp), '{}.matrixIn[1]'.format(mMtx))
      cmds.connectAttr('{}.matrixSum'.format(mMtx), '{}.inputMatrix'.format(dMtx))
      cmds.connectAttr('{}.outputTranslate'.format(dMtx), '{}.translate'.format(loc))
      cmds.connectAttr('{}.outputRotate'.format(dMtx), '{}.rotate'.format(loc))
      #cmds.connectAttr('{}.outputShear'.format(dMtx), '{}.shear'.format(loc))
      cmds.connectAttr('{}.paramU'.format(loc), '{}.parameterU'.format(pos))
      cmds.connectAttr('{}.paramV'.format(loc), '{}.parameterV'.format(pos))
      #xtra
      cmds.parent(loc, grp)
      locknHide(loc)

#Proc build rivets along a surface
#This proc makes the while loop V and for loop U on a single surface
#########################################################
def buildRiv(int_rivU, int_rivV, name, sel):  
    if cmds.objExists('{}_Grp'.format(name)):
        name = '{}_1'.format(name)
    if int_rivU and int_rivV > 1:  
        #print(int_rivU, int_rivV)
        mgrp = cmds.group(n='{}_Grp'.format(name), em=1)
    degree = cmds.getAttr('{}.degreeUV'.format(sel))[0]
    int_maxU = cmds.getAttr('{}.minMaxRangeU'.format(sel))[0][1]
    int_maxV = cmds.getAttr('{}.minMaxRangeV'.format(sel))[0][1]
    #print (int_maxU)
    #print (int_maxV)

    setU = int_maxU/int_rivU
    setV = int_maxV/int_rivV
    #print(setU)
    #print(setV)
    '''
    if ends:
        u_ = 0
    else:
        u_ = setU
    '''
    #Matrix generator
    vCons = setV
    vCount = 0

    while(vCount < int_rivV-1):
        uCons = setU
        #print uCons    
        for uCount in range(0, int_rivU-1):
           
            createRivet(n = '{}_U{}_V{}'.format(name, uCount, vCount), grp=mgrp, srfc=sel, v = setV, u = uCons, maxU = int_maxU, maxV = int_maxV)
            uCons += setU
        vCount += 1
        setV = setV + vCons
##############################################
########   Main Window start   ###############
def showRivUI():
       
    def click(value):
        ##### INPUTS ###########
        name = cmds.textField('nameTxt', text=1, q=1)
        int_rivU = cmds.intFieldGrp('uvCount', value1=1, q=1)
        int_rivV = cmds.intFieldGrp('uvCount', value2=1, q=1)
        lst_sel = cmds.ls(sl=1, dag=1, ni=1, s=1)
        sfx = ''
        nameExists = name
        endU = False
        endV = False  
        abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'ab', 'bc', 'cd', 'de', 'ef', 'fg', 'gh', 'hi', 'ij', 'jk', 'kl', 'lm', 'mn', 'no', 'op', 'pq', 'qr', 'rs', 'st', 'tu', 'uv', 'vw', 'wx', 'xy', 'yz']  
        #print(lst_sel, name, int_rivU, int_rivV)
        ########## Main Porcces ########
        int_rivU = int_rivU + 1
        int_rivV = int_rivV + 1
           
        if not lst_sel:
            cmds.warning("Select at least one surface")
        else:
            for iCount in range(0, len(lst_sel)):
                if cmds.objectType(lst_sel[iCount]) == 'nurbsSurface':
                    if not nameExists:
                        name = '{}_Rvt'.format(cmds.listRelatives(lst_sel[iCount], p=1)[0].replace('_Srfc', ''))
                    else:
                        sfx = '_' + abc[iCount]
                    buildRiv(int_rivU, int_rivV, name+sfx, lst_sel[iCount])
                else:
                    cmds.warning('Objects must be type "nurbsSurface"')    
        ###################
    if cmds.window('rivetCreator', exists = 1):
        cmds.deleteUI('rivetCreator')
   
    rivWindow = cmds.window( 'rivetCreator', title="Rivets Generator", iconName='Short Name', wh=(400, 200), sizeable=1)
    #############################################################################################################
    layTop = cmds.columnLayout( adjustableColumn=1,  columnOffset=['both', 10], rowSpacing=15, columnWidth=200, bgc=[.2, .2, .2], parent=rivWindow)
    cmds.separator(style='none', height=10, parent=layTop)
    infoDesc = cmds.text('Select one or more Surfaces', align='center', font='boldLabelFont', bgc = [.2, .2, .5], parent=layTop)
    ##########################################################################
    cmds.separator(style='none', height=5, parent=layTop)
    countUV = cmds.intFieldGrp('uvCount', label='Count  U - V', extraLabel='Rivets', adjustableColumn=1, columnAlign=[1, 'center'], numberOfFields=2, value1=1, value2=1, parent=layTop)
   
    rowLay = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'right', 0), adjustableColumn=2, columnWidth=[(1, 100), (2, 250)] )
    name = cmds.text('Name   ', align='right', parent=rowLay)
    flTxt = cmds.textField('nameTxt', placeholderText='Without a name rivets will take the objects name', parent=rowLay)
     
    btn_create = cmds.button( 'create', label='Create', align='center', parent=layTop, bgc= [.5, .2, .2], command = click)
    btn_close = cmds.button( 'close', label='Close', command=('cmds.deleteUI(\"' + rivWindow + '\", window=True)'), bgc= [.3, .3, .3], parent=layTop)    
    # Set its parent to the Maya window (denoted by '..')
    cmds.setParent( '..' )
    # Show the window that we created (window)
    cmds.showWindow( rivWindow )

showRivUI()    
########   Main Window end     ###############
##############################################

#### COMING FEATURES ####
#########################
# Permite realizar rivets en poligono
# Permite decidir si los locators empiezan en 0 o terminan en el nivel mas alto
# Permite decidir si se quiere un grupo como Offset o simple