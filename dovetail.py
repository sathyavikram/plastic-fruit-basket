import FreeCAD as App
import Part
import params

def make_dovetail_peg(is_left):
    """
    Creates a male dovetail peg (for the slat ends).
    If is_left=True, this is for the left end of the slat (at X = -span/2).
    It sticks out in the -X direction by depth.
    Neck is at X=0, wide part is at X = -depth.
    """
    neck  = params.SLAT_DOVETAIL_NECK
    width = params.SLAT_DOVETAIL_WIDTH
    depth = params.SLAT_DOVETAIL_DEPTH
    height = params.SLAT_DIAMETER

    dx = -depth if is_left else depth
    
    # Profile in XY plane
    p1 = App.Vector(0, -neck / 2.0, -height / 2.0)
    p2 = App.Vector(0, neck / 2.0, -height / 2.0)
    p3 = App.Vector(dx, width / 2.0, -height / 2.0)
    p4 = App.Vector(dx, -width / 2.0, -height / 2.0)

    wire_bottom = Part.makePolygon([p1, p2, p3, p4, p1])
    face_bottom = Part.Face(wire_bottom)

    # Extrude up by height
    peg = face_bottom.extrude(App.Vector(0, 0, height))
    return peg

def make_dovetail_slot(extra_z_top=50.0):
    """
    Creates a female dovetail cut tool for side face entry.
    """
    neck  = params.SLAT_DOVETAIL_NECK + 2 * params.DOVETAIL_CLEARANCE
    width = params.SLAT_DOVETAIL_WIDTH + 2 * params.DOVETAIL_CLEARANCE
    depth = params.SLAT_DOVETAIL_DEPTH + params.DOVETAIL_CLEARANCE
    height = params.SLAT_DIAMETER + 0.5 * params.SCALE

    base_x = params.FRAME_THICKNESS
    dx = -depth
    
    p1 = App.Vector(base_x, -neck / 2.0, -height / 2.0)
    p2 = App.Vector(base_x, neck / 2.0, -height / 2.0)
    p3 = App.Vector(base_x + dx, width / 2.0, -height / 2.0)
    p4 = App.Vector(base_x + dx, -width / 2.0, -height / 2.0)

    wire_bottom = Part.makePolygon([p1, p2, p3, p4, p1])
    face_bottom = Part.Face(wire_bottom)

    cut_tool = face_bottom.extrude(App.Vector(0, 0, height + extra_z_top))
    return cut_tool


def make_top_dovetail_slot(extra_z_top=5.0):
    """
    Creates a female dovetail cut tool for top-surface entry on cradle arms.
    Neck is at top (Z=0), wide base is below (Z=-height).
    Extruded in X across frame thickness (X=0 to X=thickness).
    """
    neck  = params.SLAT_DOVETAIL_NECK + 2 * params.DOVETAIL_CLEARANCE
    width = params.SLAT_DOVETAIL_WIDTH + 2 * params.DOVETAIL_CLEARANCE
    depth = params.FRAME_THICKNESS + 2.0 * params.SCALE
    height = params.SLAT_DIAMETER + 0.5 * params.SCALE

    # YZ profile
    p1 = App.Vector(-1.0 * params.SCALE, -neck / 2.0, extra_z_top)
    p2 = App.Vector(-1.0 * params.SCALE, neck / 2.0, extra_z_top)
    p3 = App.Vector(-1.0 * params.SCALE, width / 2.0, -height)
    p4 = App.Vector(-1.0 * params.SCALE, -width / 2.0, -height)

    wire_yz = Part.makePolygon([p1, p2, p3, p4, p1])
    face_yz = Part.Face(wire_yz)

    # Extrude along +X across the frame thickness
    cut_tool = face_yz.extrude(App.Vector(depth, 0, 0))
    return cut_tool


def make_top_dovetail_peg(is_left=True):
    """
    Creates a male top-surface dovetail peg for slat ends.
    Neck is at top (Z=0), wide base is below (Z=-height).
    Extrudes along X (length = depth).
    """
    neck   = params.SLAT_DOVETAIL_NECK
    width  = params.SLAT_DOVETAIL_WIDTH
    height = params.SLAT_DIAMETER
    depth  = params.FRAME_THICKNESS

    dx = -depth if is_left else depth

    p1 = App.Vector(0, -neck / 2.0, 0)
    p2 = App.Vector(0, neck / 2.0, 0)
    p3 = App.Vector(0, width / 2.0, -height)
    p4 = App.Vector(0, -width / 2.0, -height)

    wire_yz = Part.makePolygon([p1, p2, p3, p4, p1])
    face_yz = Part.Face(wire_yz)

    peg = face_yz.extrude(App.Vector(dx, 0, 0))
    return peg

