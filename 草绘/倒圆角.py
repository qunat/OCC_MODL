#二维倒圆：
from OCC.Core.gp import gp_Pnt, gp_Pln
from OCC.Core.ChFi2d import ChFi2d_AnaFilletAlgo
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Extend.ShapeFactory import make_wire
from OCC.Display.SimpleGui import init_display
display,start_display, add_menu,add_functionto_menu = init_display()
# Defining the points
p1 = gp_Pnt(0, 0, 0)
p2 = gp_Pnt(5, 5, 0)
p3 = gp_Pnt(-5,5, 0)
# Making the edges
ed1 = BRepBuilderAPI_MakeEdge(p3, p2).Edge()
ed2 = BRepBuilderAPI_MakeEdge(p2, p1).Edge()
#Making the 2dFillet
f = ChFi2d_AnaFilletAlgo()
f.Init(ed1, ed2, gp_Pln())
radius = 1.0
f.Perform(radius)
fillet2d = f.Result(ed1, ed2)
# Create and display a wire
w = make_wire([ed1, fillet2d, ed2])
display.DisplayShape(w)
start_display()