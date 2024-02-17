import maya.cmds as cmds
import time

global isFirstTime
global ChainCount
isFirstTime=True
ChainCount=22   
#let's create a windo and UI
winName="Rebuilder"
if cmds.window(winName,q=True,ex=True):
    cmds.deleteUI(winName)

cmds.window(winName,t="CurveRigegr",w=500,h=400,s=False)
cmds.columnLayout()
cmds.text("before anything, ensure you have a curve selected")
cmds.text("to restructure the curve use this slider")
SpanCount=cmds.intSliderGrp(min=3,max=100,v=3,cc="SpanMod()",f=True)
cmds.separator(w=500)
cmds.text("now if you want to smooth it, use this slider to smooth")
SmoothNess=cmds.floatSliderGrp(min=0,max=10,v=0,cc="SmoothChange()",f=True,en=False)
cmds.separator(w=500)
cmds.button(l="Next Step",c="NextStep()")
cmds.separator(w=500)
cmds.text("now if you are done with the curve, use this button to create controllers")
cmds.button(l="CTRL maker",c="CMaker()")
RedoCTRL=cmds.intSliderGrp(min=3,max=100,v=3,cc="CTRLRedo()",f=True,en=False)
cmds.separator(w=500)
cmds.text("now if you are done, select your desired object and click next")
cmds.button(l="!!NEXT!!",c="FinalStep()")
cmds.button(l="MakeChain Only",c="MakeChain()")
cmds.showWindow()

#start of the functions
def SpanMod():
    global isFirstTime
    if not isFirstTime:
        cmds.undo()
    spanValue=cmds.intSliderGrp(SpanCount,q=True,v=True)
    selectedCurve=cmds.ls(sl=True)
    cmds.rebuildCurve(selectedCurve,rpo=True,kep=True,rt=0,s=spanValue)
    cmds.select(selectedCurve)
    isFirstTime=False

def NextStep():
    global isFirstTime
    isFirstTime=True
    cmds.intSliderGrp(SpanCount,e=True,en=False)
    cmds.floatSliderGrp(SmoothNess,e=True,en=True)
    
def SmoothChange():
    global isFirstTime
    if not isFirstTime:
        cmds.undo()
    newSmooth=cmds.floatSliderGrp(SmoothNess,q=True,v=True)
    selectedCurve=cmds.ls(sl=True)
    cmds.smoothCurve(selectedCurve[0]+".cv[*]",s=newSmooth)
    cmds.select(selectedCurve)
    isFirstTime=False

def CMaker():
    selectedCRV=cmds.ls(sl=True)
    EPlist=cmds.ls(selectedCRV[0]+".ep[*]",fl=True)
    locList=[]
    #now with having those two lists we can create locators and dump them on each point in order
    for EPi in EPlist:
        cmds.select(EPi,r=True)
        cmds.pointCurveConstraint()
        cmds.CenterPivot()
        locList.append(cmds.rename("EPCTRL1"))
    cmds.select(locList)
    cmds.group(n="AllLocators")
    cmds.select(selectedCRV)
    cmds.intSliderGrp(RedoCTRL,e=True,en=True)
    
def CTRLRedo():

    cmds.delete("AllLocators")
    newRespan=cmds.intSliderGrp(RedoCTRL,q=True,v=True)
    selectedcurve=cmds.ls(sl=True)
    cmds.rebuildCurve(selectedcurve,rpo=True,kep=True,rt=0,s=newRespan)
    cmds.select(selectedcurve)
    CMaker()

def FinalStep():
    startTime=1
    AnimCTList=cmds.ls("EPCTRL*",tr=True)
    endTime=len(AnimCTList)
    selectedOBJ=cmds.ls(sl=True)
    for CurKey in range(startTime,endTime+1):
        myTime=cmds.currentTime(query=True)
        cmds.select(selectedOBJ,r=True)
        cmds.FreezeTransformations()
        cmds.duplicate()
        cmds.select(AnimCTList[CurKey-1],add=True)
        cmds.matchTransform()
        cmds.parentConstraint(w=1.0)
        cmds.currentTime(myTime+1,e=True)
        cmds.playbackOptions(by=1)
    cmds.currentTime(startTime)
    

def MakeChain():
    global ChainCount
    selectedOBJ=cmds.ls(sl=True)
    cmds.select(selectedOBJ,r=True)
    cmds.select("curve1",add=True)
    cmds.pathAnimation(fm=True,f=True,fa="x",ua="y",wut="vector",wu=(0,1,0),inverseFront=False,iu=False,b=False,stu=1,etu=ChainCount)
    cmds.select(selectedOBJ,r=True)
    cmds.selectKey('motionPath1_uValue',time=(1,ChainCount))
    cmds.keyTangent(itt="linear",ott="linear")
    chainLinks=[]
    for curkey in range(1,ChainCount+1):
        cmds.currentTime(curkey)
        #time.sleep(.5)
        cmds.select(selectedOBJ,r=True)
        cmds.duplicate()
        #time.sleep(.5)
        chainLinks.append(cmds.rename("CLink1"))
        #cmds.rotate(0,90,0)
    cmds.select(chainLinks)
    cmds.group(n="AllLinks")
    linksCount=len(chainLinks)
    for i in range(1,linksCount,2):
        cmds.currentTime(i)
        time.sleep(.2)
        cmds.select(chainLinks[i])
        time.sleep(.2)
        cmds.setAttr(chainLinks[i]+".rx",90)
    #cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=ChainCount,u="animCurve")
    cmds.DeleteMotionPaths()






