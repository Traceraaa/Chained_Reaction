import maya.cmds as cmds
import time

# Global Variables
global isFirstTime
global ChainCount
global selected_curve_name
global curve_type

isFirstTime = True
ChainCount = 22
selected_curve_name = ""
curve_type = 3


def find_object_in_scene():
    all_curves = cmds.ls(type="nurbsCurve")
    all_transform_node = []
    number_of_curves = 0
    for curve_shape in all_curves:
        transform_node = cmds.listRelatives(curve_shape, parent=True, fullPath=True)[0]
        transform_node = transform_node.split("|")[-1]
        all_transform_node.append(transform_node)
    number_of_curves = len(all_transform_node)
    return all_transform_node, number_of_curves


def enable_reconstruct():
    cmds.radioButtonGrp(make_window.curvetype, e=True, en=True)


def make_window():
    # let's create a windo and UI
    winName = "Rebuilder"
    if cmds.window(winName, q=True, ex=True):
        cmds.deleteUI(winName)

    cmds.window(winName, t="CurveRiggr", w=700, h=450, s=False)

    cmds.columnLayout(margins=5)
    master_layout = cmds.columnLayout(mar=5)
    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.text("Curve Rigger Tool", font="boldLabelFont")
    cmds.separator(w=700, h=10)
    cmds.setParent(master_layout)
    # *****************************************************************************************************************
    make_window.ui_curve_frame = cmds.frameLayout(l="Curve Settings", w=700, cll=True, cl=False)
    make_window.ui_curve_layout = cmds.columnLayout()
    cmds.text("Before anything, ensure you have a curve selected to restructure the curve use this slider")
    cmds.setParent(make_window.ui_curve_layout)
    scroll_layout = cmds.rowLayout(numberOfColumns=2)
    text_scroll_layout = cmds.scrollLayout(w=250, h=50, hst=0, vst=16)

    if find_object_in_scene()[0]:
        make_window.curve_scroll_list = cmds.textScrollList(parent=text_scroll_layout,
                                                            numberOfRows=find_object_in_scene()[1],
                                                            allowMultiSelection=True,
                                                            append=find_object_in_scene()[0],
                                                            sc="enable_reconstruct()"
                                                            )
        cmds.setParent(scroll_layout)
        make_window.btn_refresh = cmds.iconTextButton(style='iconAndTextVertical',
                                                      image1='refresh.xpm',
                                                      label='refresh',
                                                      al="right",
                                                      c="refresh_list()"
                                                      )
        cmds.setParent(scroll_layout)

        cmds.setParent(make_window.ui_curve_layout)

        make_window.curvetype = cmds.radioButtonGrp(label='Type of Curve',
                                                    labelArray4=['Linear-1', 'Quadratic-2', 'Cubic-3', 'Quintic-5'],
                                                    numberOfRadioButtons=4,
                                                    cc1='curvetype()', cc2='curvetype()', cc3='curvetype()',
                                                    cc4='curvetype()', en=False)

        cmds.rowLayout(numberOfColumns=2)
        make_window.SpanCount = cmds.intSliderGrp(min=3, max=100, v=3, cc="SpanMod()", f=True, en=False)
        make_window.cb_use_smooth = cmds.checkBox(l="Adjust Smoothness", cc="NextStep()", en=False)
        cmds.setParent(make_window.ui_curve_layout)
        cmds.separator(w=700)
        cmds.text("now if you want to smooth it, use this slider to smooth")
        make_window.SmoothNess = cmds.floatSliderGrp(min=0, max=10, v=0, cc="SmoothChange()", f=True, en=False)
        make_window.btn_next_to_make_controllers = cmds.button(l="Next", c="expand_controller_section()", en=False)
        cmds.separator(w=700)
        cmds.setParent(master_layout)

        # *****************************************************************************************************************
        make_window.ui_controller_frame = cmds.frameLayout(l="Make Controllers", w=700, cll=True, cl=True)
        make_window.ui_controller_layout = cmds.columnLayout()
        cmds.text("now if you are done with the curve, use this button to create controllers")
        make_window.RedoCTRL = cmds.intSliderGrp(min=3, max=100, v=3, cc="CTRLRedo()", f=True, en=False)
        cmds.rowLayout(numberOfColumns=2)
        make_window.btn_cmaker = cmds.button(l="CTRL maker", c="CMaker()", en=False)
        make_window.btn_to_final_step = cmds.button(l="Next", c="make_chain_section()", en=False)
        cmds.setParent(make_window.ui_controller_layout)
        cmds.separator(w=700)
        cmds.setParent(master_layout)

        # *****************************************************************************************************************
        make_window.ui_chain_frame = cmds.frameLayout(l="Make Chains", w=700, cll=True, cl=True)
        make_window.ui_chain_layout = cmds.columnLayout()
        cmds.text("now if you are done, select your desired object and click next")
        cmds.rowLayout(numberOfColumns=3)
        make_window.btn_make_chain_from_selected_obj = cmds.button(l="Make Chain", c="FinalStep()", en=False)
        make_window.btn_make_chain = cmds.button(l="MakeChain Only", c="MakeChain()", en=False)
        make_window.cb_make_proxy = cmds.checkBox(l="Use Proxy Geo", cc="make_proxy_geo()", en=False)
        cmds.setParent(make_window.ui_chain_layout)
        cmds.setParent(master_layout)

        # *****************************************************************************************************************

        cmds.showWindow()
    else:
        cmds.confirmDialog(title='Error', message='You need to create a curve first.', icon='critical')


# confirm = cmds.confirmDialog(t="Warning",
#                              m="Ensure your curve is created and selected before moving on",
#                              b=['Yes', 'No'],
#                              cb='No'
#                              )
# if confirm == "No":
#     cmds.confirmDialog(m="Check if you have curve created and selected before moving on")
# else:
make_window()


# start of the functions
def curvetype():
    global curve_type
    cmds.intSliderGrp(make_window.SpanCount, e=True, en=True)
    cmds.floatSliderGrp(make_window.SmoothNess, e=True, en=False)
    cmds.checkBox(make_window.cb_use_smooth, e=True, v=False )
    curve_type = cmds.radioButtonGrp(make_window.curvetype, q=True, sl=True)
    if curve_type == 1:
        cmds.confirmDialog(m="Linear curves can not be smoothened.")
    print(curve_type)


def SpanMod():
    global isFirstTime
    global selected_curve_name
    global curve_type
    if curve_type == 4:
        curve_type = 5
    if curve_type == 1:
        cmds.checkBox(make_window.cb_use_smooth, e=True, en=False)
    else:
        cmds.checkBox(make_window.cb_use_smooth, e=True, en=True)

    if not isFirstTime:
        cmds.undo()

    cmds.radioButtonGrp(make_window.curvetype, e=True, en=False)
    cmds.textScrollList(make_window.curve_scroll_list, e=True, en=False)
    cmds.button(make_window.btn_next_to_make_controllers, e=True, en=True)
    spanValue = cmds.intSliderGrp(make_window.SpanCount, q=True, v=True)
    selected_curve_name = cmds.textScrollList(make_window.curve_scroll_list, q=True, si=True)

    cmds.select(selected_curve_name)
    selectedCurve = cmds.ls(sl=True)
    cmds.rebuildCurve(selectedCurve, rpo=True, kep=True, rt=0, s=spanValue, d=curve_type)
    cmds.select(selectedCurve)
    isFirstTime = False


def NextStep():
    global isFirstTime
    isFirstTime = True

    cmds.intSliderGrp(make_window.SpanCount, e=True, en=False)
    cmds.floatSliderGrp(make_window.SmoothNess, e=True, en=True)
    


def expand_controller_section():
    # Expand toggles
    cmds.frameLayout(make_window.ui_curve_frame, e=True, cl=True)
    cmds.frameLayout(make_window.ui_controller_frame, e=True, cl=False)
    # Button enable/disable
    cmds.button(make_window.btn_next_to_make_controllers, e=True, en=False)
    cmds.button(make_window.btn_cmaker, e=True, en=True)
    # Checkbox disabled
    cmds.checkBox(make_window.cb_use_smooth, e=True, en=False)
    # sliders disabled
    cmds.floatSliderGrp(make_window.SmoothNess, e=True, en=False)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=False)


def make_chain_section():
    # Expand toggles
    cmds.frameLayout(make_window.ui_controller_frame, e=True, cl=True)
    cmds.frameLayout(make_window.ui_chain_frame, e=True, cl=False)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=False)
    cmds.button(make_window.btn_to_final_step, e=True, en=False)
    cmds.button(make_window.btn_make_chain_from_selected_obj, e=True, en=True)
    cmds.button(make_window.btn_make_chain, e=True, en=True)
    cmds.checkBox(make_window.cb_make_proxy, e=True, en=True)


def SmoothChange():
    global isFirstTime
    if not isFirstTime:
        cmds.undo()

    cmds.button(make_window.btn_next_to_make_controllers, e=True, en=True)
    selected_curve_name = cmds.textScrollList(make_window.curve_scroll_list, q=True, si=True)
    newSmooth = cmds.floatSliderGrp(make_window.SmoothNess, q=True, v=True)
    selectedCurve = cmds.ls(selected_curve_name, sl=True)
    cmds.smoothCurve(selectedCurve[0] + ".cv[*]", s=newSmooth)
    cmds.select(selectedCurve)
    isFirstTime = False


def CMaker():
    cmds.floatSliderGrp(make_window.SmoothNess, e=True, en=False)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=False)

    selectedCRV = cmds.ls(sl=True)
    EPlist = cmds.ls(selectedCRV[0] + ".ep[*]", fl=True)
    locList = []
    # now with having those two lists we can create locators and dump them on each point in order
    for EPi in EPlist:
        cmds.select(EPi, r=True)
        cmds.pointCurveConstraint()
        cmds.CenterPivot()
        locList.append(cmds.rename("EPCTRL1"))
    cmds.select(locList)
    cmds.group(n="AllLocators")
    cmds.select(selectedCRV)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=True)
    cmds.button(make_window.btn_cmaker, e=True, en=False)


def CTRLRedo():
    cmds.button(make_window.btn_to_final_step, e=True, en=True)
    cmds.delete("AllLocators")
    newRespan = cmds.intSliderGrp(make_window.RedoCTRL, q=True, v=True)
    selectedcurve = cmds.ls(sl=True)
    cmds.rebuildCurve(selectedcurve, rpo=True, kep=True, rt=0, s=newRespan)
    cmds.select(selectedcurve)
    CMaker()


def FinalStep():

    global ChainCount
    global selected_curve_name

    cmds.button(make_window.btn_make_chain, e=True, en=True)
    cmds.button(make_window.btn_cmaker, e=True, en=False)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=False)

    startTime = 1
    AnimCTList = cmds.ls("EPCTRL*", tr=True)
    endTime = len(AnimCTList)

    chainLinks = []

    selectedOBJ = cmds.ls(sl=True)
    for CurKey in range(startTime, endTime + 1):
        myTime = cmds.currentTime(query=True)
        cmds.select(selectedOBJ, r=True)
        cmds.FreezeTransformations()
        cmds.duplicate()
        cmds.select(AnimCTList[CurKey - 1], add=True)
        cmds.matchTransform()
        cmds.parentConstraint(w=1.0)
        cmds.currentTime(myTime + 1, e=True)
        cmds.playbackOptions(by=1)
        chainLinks.append(cmds.rename("CLink1"))
    
    cmds.select(chainLinks)
    cmds.group(n="AllLinks")
    cmds.currentTime(startTime)

def MakeChain():

    global ChainCount
    global selected_curve_name

    cmds.button(make_window.btn_make_chain, e=True, en=True)
    cmds.button(make_window.btn_cmaker, e=True, en=False)
    cmds.intSliderGrp(make_window.RedoCTRL, e=True, en=False)

    startTime = 1
    AnimCTList = cmds.ls("EPCTRL*", tr=True)
    endTime = len(AnimCTList)

    chainLinks = []

    selectedOBJ = cmds.ls(sl=True)
    for CurKey in range(startTime, endTime + 1):
        myTime = cmds.currentTime(query=True)
        cmds.select(selectedOBJ, r=True)
        cmds.FreezeTransformations()
        cmds.duplicate()
        cmds.select(AnimCTList[CurKey - 1], add=True)
        cmds.matchTransform()
        cmds.parentConstraint(w=1.0)
        cmds.currentTime(myTime + 1, e=True)
        cmds.playbackOptions(by=1)
        chainLinks.append(cmds.rename("CLink1"))
    
    cmds.select(chainLinks)
    cmds.group(n="AllLinks")
    cmds.currentTime(startTime)

    linksCount = len(chainLinks)
    for i in range(1, linksCount, 2):
        cmds.currentTime(i)
        cmds.select(chainLinks[i])
        cmds.setAttr(chainLinks[i] + ".rx", 90)



# def MakeChain():
#     global ChainCount
#     global selected_curve_name

#     selected_curve_name = cmds.textScrollList(make_window.curve_scroll_list, q=True, si=True)
#     selectedOBJ = cmds.ls(sl=True)
#     cmds.select(selectedOBJ, r=True)
#     cmds.select(selected_curve_name, add=True)
#     cmds.pathAnimation(fm=True, f=True, fa="x", ua="y", wut="vector", wu=(0, 1, 0), inverseFront=False, iu=False,
#                        b=False, stu=1, etu=ChainCount)
#     cmds.select(selectedOBJ, r=True)
#     cmds.selectKey('motionPath1_uValue', time=(1, ChainCount))
#     cmds.keyTangent(itt="linear", ott="linear")
#     chainLinks = []
#     for curkey in range(1, ChainCount + 1):
#         cmds.currentTime(curkey)
#         cmds.select(selectedOBJ, r=True)
#         cmds.duplicate()
#         chainLinks.append(cmds.rename("CLink1"))
#     cmds.select(chainLinks)

#     cmds.group(n="AllLinks")
#     linksCount = len(chainLinks)
#     for i in range(1, linksCount, 2):
#         cmds.currentTime(i)
#         time.sleep(.2)
#         cmds.select(chainLinks[i])
#         time.sleep(.2)
#         cmds.setAttr(chainLinks[i] + ".rx", 90)
#     # cmds.snapshot(n="TreadSS",i=1,ch=False,st=1,et=ChainCount,u="animCurve")
#     cmds.DeleteMotionPaths()


def make_proxy_geo():
    proxy_geo = cmds.polyTorus(n="ProxyGeo", sa=10, sh=10, sr=0.3)
    edges_to_scale = []
    edges_template = ["pTorus1.e[109]", "pTorus1.e[119]", "pTorus1.e[129]", "pTorus1.e[139]", "pTorus1.e[149]",
                      "pTorus1.e[159]", "pTorus1.e[169]", "pTorus1.e[179]", "pTorus1.e[189]", "pTorus1.e[199]",
                      "pTorus1.e[104]", "pTorus1.e[114]", "pTorus1.e[124]", "pTorus1.e[134]", "pTorus1.e[144]",
                      "pTorus1.e[154]", "pTorus1.e[164]", "pTorus1.e[174]", "pTorus1.e[184]", "pTorus1.e[194]"]
    for edge in edges_template:
        suffix_name = edge.split(".")[-1]
        new_edge_name = "ProxyGeo." + str(suffix_name)
        edges_to_scale.append(new_edge_name)

    cmds.select(cl=True)
    cmds.select(edges_to_scale)
    cmds.scale(0.828, 1, 1, )
    cmds.select(proxy_geo)


def refresh_list():
    make_window()