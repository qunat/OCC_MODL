#旋转拉伸
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeRevol
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Dir

E11 = BRepBuilderAPI_MakeEdge(gp_Pnt(40.,0.,0.), gp_Pnt(82.5,25.,0.)).Edge()
E12 = BRepBuilderAPI_MakeEdge(gp_Pnt(82.5,25.,0.), gp_Pnt(42.5,93.,0.)).Edge()
E13 = BRepBuilderAPI_MakeEdge(gp_Pnt(42.5,93.,0.), gp_Pnt(0.,68.,0.)).Edge()
E14 = BRepBuilderAPI_MakeEdge(gp_Pnt(0.,68.,0.), gp_Pnt(40.,0.,0.)).Edge()
W1 = BRepBuilderAPI_MakeWire(E11,E12,E13,E14)

A=BRepPrimAPI_MakeRevol(BRepBuilderAPI_MakeFace(W1.Wire()).Face(),gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,1,0) ))
if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(W1.Shape(), update=True)
    display.DisplayShape(A.Shape(), update=True)
    start_display()
