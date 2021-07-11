from math import atan, cos, sin, pi

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse,BRepAlgoAPI_Common
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_Transform, BRepBuilderAPI_MakeWire,
                                BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace)
from OCC.Core.BRepFeat import BRepFeat_MakeCylindricalHole
from OCC.Core.BRepPrimAPI import (BRepPrimAPI_MakeSphere, BRepPrimAPI_MakeCylinder,
                             BRepPrimAPI_MakeTorus, BRepPrimAPI_MakeRevol)
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir, gp_Ax1, gp_Trsf, gp_Vec

def generate_shape():
    """Create a sphere with faces top and bottom"""
    sphere_radius = 1.0
    sphere_angle = atan(0.5)
    sphere_origin = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    sphere = BRepPrimAPI_MakeSphere(sphere_origin, sphere_radius,
                                    -sphere_angle, sphere_angle).Shape()
    return sphere


def add_feature(base):
    """Add a "feature" to a shape. In this case we drill a hole through it."""
    feature_diameter = 0.8
    feature_origin = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    feature_maker = BRepFeat_MakeCylindricalHole()
    feature_maker.Init(base, feature_origin)
    feature_maker.Build()
    feature_maker.Perform(feature_diameter / 2.0)
    shape = feature_maker.Shape()
    return shape


def boolean_cut(base):
    # Create a cylinder
    cylinder_radius = 0.25
    cylinder_height = 2.0
    cylinder_origin = gp_Ax2(gp_Pnt(0.0, 0.0, - cylinder_height / 2.0), gp_Dir(0.0, 0.0, 1.0))
    cylinder = BRepPrimAPI_MakeCylinder(cylinder_origin, cylinder_radius, cylinder_height)

    # Repeatedly move and subtract it from the input shape
    move = gp_Trsf()
    boolean_result = base
    clone_radius = 1.0

    for clone in range(8):
        angle = clone *  pi / 4.0
        # Move the cylinder
        move.SetTranslation(gp_Vec(cos(angle) * clone_radius, sin(angle) * clone_radius, 0.0))
        moved_cylinder = BRepBuilderAPI_Transform(cylinder.Shape(), move, True).Shape()
        # Subtract the moved cylinder from the drilled sphere
        boolean_result = BRepAlgoAPI_Cut(boolean_result, moved_cylinder).Shape()
    return boolean_result


def boolean_fuse(base):
    ring_radius = 0.25
    torus_radius = 1.0 - ring_radius
    torus = BRepPrimAPI_MakeTorus(torus_radius, ring_radius).Shape()
    fuse = BRepAlgoAPI_Fuse(base, torus).Shape()
    return fuse


def revolved_cut(base):
    # Define 7 points
    face_points = TColgp_Array1OfPnt(1, 7)
    face_inner_radius = 0.6

    pts = [
        gp_Pnt(face_inner_radius - 0.05, 0.0, -0.05),
        gp_Pnt(face_inner_radius - 0.10, 0.0, -0.025),
        gp_Pnt(face_inner_radius - 0.10, 0.0, 0.025),
        gp_Pnt(face_inner_radius + 0.10, 0.0, 0.025),
        gp_Pnt(face_inner_radius + 0.10, 0.0, -0.025),
        gp_Pnt(face_inner_radius + 0.05, 0.0, -0.05),
        gp_Pnt(face_inner_radius - 0.05, 0.0, -0.05),
    ]

    for n, i in enumerate(pts):
        face_points.SetValue(n + 1, i)

    # Use these points to create edges and add these edges to a wire
    hexwire = BRepBuilderAPI_MakeWire()

    for i in range(1, 7):
        hexedge = BRepBuilderAPI_MakeEdge(face_points.Value(i), face_points.Value(i + 1)).Edge()
        hexwire.Add(hexedge)

    # Turn the wire into a 6 sided face
    hexface = BRepBuilderAPI_MakeFace(hexwire.Wire()).Face()

    # Revolve the face around an axis
    revolve_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    revolved_shape = BRepPrimAPI_MakeRevol(hexface, revolve_axis).Shape()

    # Move the generated shape
    move = gp_Trsf()
    move.SetTranslation(gp_Pnt(0, 0, 0), gp_Pnt(0, 0, sin(0.5)))
    moved_shape = BRepBuilderAPI_Transform(revolved_shape, move, False).Shape()

    # Remove the revolved shape
    cut = BRepAlgoAPI_Cut(base, moved_shape).Shape()
    return cut


def generate_demo():
    basic_shape = generate_shape()
    featured_shape = add_feature(basic_shape)
    cut_shape = boolean_cut(featured_shape)
    fused_shape = boolean_fuse(cut_shape)
    revolved_shape = revolved_cut(fused_shape)
    return revolved_shape


demo = generate_demo()