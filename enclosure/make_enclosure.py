"""
Creates an enclosure for the colorimeter
"""
from py2scad import *
from colorimeter_enclosure_v2 import Colorimeter_Enclosure

INCH2MM = 25.4

# Inside dimensions
x,y,z = 2.5*INCH2MM, 3.0*INCH2MM, 1.75*INCH2MM
wall_thickness = 3.0 
cuvette_size = 12.35,12.35

hole_list = []

# Create enclosure parameters
params = {
        'inner_dimensions'        : (x,y,z), 
        'wall_thickness'          : wall_thickness, 
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.2*INCH2MM,
        'top_y_overhang'          : 0.2*INCH2MM,
        'bottom_x_overhang'       : 0.2*INCH2MM,
        'bottom_y_overhang'       : 0.2*INCH2MM, 
        'lid2front_tabs'          : (0.25,0.75),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'inner_panel_side_tabs'   : (0.5,),
        'inner_panel_bottom_tabs' : (0.25, 0.75),
        'lid2front_tab_width'     : 0.5*INCH2MM,
        'lid2side_tab_width'      : 0.5*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'inner_panel_tab_width'   : 0.3*INCH2MM, 
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM,
        'standoff_hole_diameter'  : 0.116*INCH2MM, 
        'inner_panel_offset'      : 0.5*cuvette_size[0] + wall_thickness,
        'led_cable_hole_position' : (-1.0*INCH2MM, -0.45*INCH2MM),
        'led_cable_hole_size'     : 2.5,
        'cuvette_slot_size'       : (3.0,5.0),
        'cuvette_slot_position'   : (0.0, -6.55),
        'pcb_position'            : (0,-0.15*INCH2MM),
        'pcb_hole_spacing'        : (1.6*INCH2MM, 0.8*INCH2MM),
        'pcb_mount_hole_diam'     : 0.12* INCH2MM,
        'shrouded_hole_position'  : (0.5*INCH2MM, -0.15*INCH2MM),
        'shrouded_hole_size'      : (9.5, 20.5, 1),
        'top_hole_size'           : (x-0.8*INCH2MM, y-0.8*INCH2MM, 1),
        'top_hole_position'       : (0,0),
        'holder_size'             : (20.0,40.0),
        'cuvette_size'            : cuvette_size,
        'holder_standoff_height'  : 1*INCH2MM,
        'holder_standoff_inset'   : 2.0,
        'hole_list'               : [],
        'second_top_dimensions'   : (x + wall_thickness, y + wall_thickness),
        'slider_hole_1_dimensions': (x-0.6*INCH2MM, y-0.6*INCH2MM),
        'slider_hole_2_dimensions': (x*0.5, y -19),
        'slider_hole_2_position'  : (-0.5*x - wall_thickness,0),
        }

enclosure = Colorimeter_Enclosure(params)
enclosure.make()
enclosure.add_holes(hole_list)

part_assembly = enclosure.get_assembly(
        explode=(0,0,0),
        show_top=True,
        show_bottom=True,
        show_left=True,
        show_right=True,
        show_front=True,
        show_back=True,
        show_holder=True,
        show_holder_standoffs=True,
        show_inner_panel=True,
        show_second_top=False,
        show_outer_slider=True,
        )

part_projection = enclosure.get_projection(project=True)

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly_2.0.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
prog_projection.write('enclosure_projection.scad')

