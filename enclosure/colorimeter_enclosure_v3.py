from py2scad import *
import subprocess

class Colorimeter_Enclosure(Basic_Enclosure):

    def __init__(self,params):
        super(Colorimeter_Enclosure,self).__init__(params) 

    def make(self):
        super(Colorimeter_Enclosure,self).make()

        # Make inner panel, custom cutouts, holder and second top
        self.make_inner_panel()
        self.make_inner_panel_tab_holes()
        self.make_cuvette_slot()
        self.make_pcb_holes()
        self.make_shrouded_header_hole()
        self.make_top_hole()
        self.make_led_cable_hole()
        self.make_holder()
        self.make_holder_standoffs()
        self.make_second_top()
        self.make_second_top_hole()
        self.make_outer_slider()
        self.make_outer_slider_holes()
        self.make_slider()

    def make_inner_panel(self):
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        inner_panel_tab_width = self.params['inner_panel_tab_width']
        try:
            depth_adjust = self.params['tab_depth_adjust']
        except KeyError:
            depth_adjust = 0.0
        tab_depth = wall_thickness + depth_adjust 

        # Create tab data top and bottom tabs
        xz_pos = []
        xz_neg = []
        for loc in self.params['inner_panel_bottom_tabs']:
            tab_data = (loc, inner_panel_tab_width, tab_depth, '+')
            xz_neg.append(tab_data)

        # Create tab data for front and back tabs 
        yz_pos = []
        yz_neg = []
        for loc in self.params['inner_panel_side_tabs']:
            tab_data = (loc, inner_panel_tab_width, tab_depth, '+')
            yz_pos.append(tab_data)
            yz_neg.append(tab_data)

        # Pack panel data into parameters structure
        panel_x = inner_y+0*wall_thickness
        panel_y = inner_z
        panel_z = wall_thickness
        params = {
                'size' : (panel_x, panel_y, panel_z),
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        plate_maker = Plate_W_Tabs(params)
        self.inner_panel= plate_maker.make()

        # Extend inner pannel to block any light
        top_hole_x, top_hole_y, radius = self.params['top_hole_size']
        tol = self.params['inner_panel_vert_tol']

        block_y = 2*wall_thickness - 2*tol
        block_x = top_hole_y
        block_z = wall_thickness

        light_block = Cube(size=(block_x, block_y, block_z))
        light_block = Translate(light_block,v=(0,0.5*panel_y,0))

        self.inner_panel = Union([self.inner_panel, light_block])
        


    def make_inner_panel_tab_holes(self):
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        inner_panel_tab_width = self.params['inner_panel_tab_width']
        inner_panel_offset = self.params['inner_panel_offset']
        hole_list = []

        # create top and bottom holes
        for loc in self.params['inner_panel_bottom_tabs']:
            for panel in ('bottom',):
                x = inner_panel_offset
                y = -0.5*inner_y + inner_y*loc
                hole = {
                        'panel'    : panel,
                        'type'     : 'square',
                        'location' : (x, y),
                        'size'     : (wall_thickness,inner_panel_tab_width),
                        }
                hole_list.append(hole)

        # create front and back holes
        for loc in self.params['inner_panel_side_tabs']:
            for panel in ('front', 'back'):
                x = inner_panel_offset
                z = -0.5*inner_z + inner_z*loc
                hole = {
                        'panel'    : panel,
                        'type'     : 'square',
                        'location' : (x,z),
                        'size'     : (wall_thickness, inner_panel_tab_width),
                        }
                hole_list.append(hole)

        self.add_holes(hole_list)

    def make_cuvette_slot(self):
        hole = {
                'panel' : 'inner_panel',
                'type'  : 'square',
                'location' : self.params['cuvette_slot_position'],
                'size'     : self.params['cuvette_slot_size'],
                }
        self.add_holes([hole])

    def make_pcb_holes(self): 
        pcb_center_x, pcb_center_y = self.params['pcb_position']
        pcb_hole_spacing_x, pcb_hole_spacing_y = self.params['pcb_hole_spacing']
        pcb_mount_hole_diam = self.params['pcb_mount_hole_diam']
        hole_list = []
        # Create PCB holes
        for i in (-1,1):
            for j in (-1,1):
                for panel in ('left', 'right'):
                    hole_x = pcb_center_x + i*0.5*pcb_hole_spacing_x
                    hole_z = pcb_center_y + j*0.5*pcb_hole_spacing_y
                    hole = { 
                            'panel'     : panel,
                            'type'      : 'round',
                            'location'  : (hole_x, hole_z),
                            'size'      : pcb_mount_hole_diam, 
                            }
                    hole_list.append(hole)
        self.add_holes(hole_list)

    def make_shrouded_header_hole(self):
        shrouded_hole_x,shrouded_hole_z = self.params['shrouded_hole_position']
        shrouded_hole_size = self.params['shrouded_hole_size']
        hole = {
                'panel'    : 'right',
                'type'     : 'rounded_square',
                'location' : (shrouded_hole_x,shrouded_hole_z),
                'size'     : shrouded_hole_size,
                }
        self.add_holes([hole])

    def make_top_hole(self):
        top_hole_size = self.params['top_hole_size']
        top_hole_position = self.params['top_hole_position']

        hole_top = {
                'panel'    : 'top',
                'type'     : 'rounded_square',
                'location' : top_hole_position,
                'size'     : top_hole_size,
                }
        
        self.add_holes([hole_top])

    def make_led_cable_hole(self):
        led_cable_hole_position = self.params['led_cable_hole_position']
        led_cable_hole_size = self.params['led_cable_hole_size']
        hole = {
                'panel'    : 'inner_panel',
                'type'     : 'round',
                'location' : led_cable_hole_position,
                'size'     : led_cable_hole_size,
                }
        self.add_holes([hole])

    def make_holder(self):
        holder_size = self.params['holder_size']
        holder_x, holder_y = holder_size
        thickness = self.params['wall_thickness']
        cuvette_size = self.params['cuvette_size']
        cuvette_x, cuvette_y = cuvette_size
        standoff_hole_diam = self.params['standoff_hole_diameter']
        standoff_diam = self.params['standoff_diameter']
        holder_standoff_inset = self.params['holder_standoff_inset']
        inner_panel_offset = self.params['inner_panel_offset'] 

        self.holder = Cube(size=(holder_x, holder_y,thickness))
        hole_list = []

        cuvette_hole = {
                'panel': 'holder',
                'type' : 'square',
                'location': (0.5*holder_x,0),
                'size' : (2*cuvette_x, cuvette_y),
                }

        self.holder_standoff_hole_xy = []

        for i in (-1,1):
            hole_x = 0
            hole_y = i*(0.5*holder_y - 0.5*standoff_diam - holder_standoff_inset)
            standoff_hole = {
                    'panel': 'holder',
                    'type': 'round',
                    'location': (hole_x, hole_y),
                    'size': standoff_hole_diam,
                    }

            hole_x = -0.5*holder_x + inner_panel_offset - 0.5*thickness  

            standoff_floor_hole = {
                    'panel': 'bottom',
                    'type': 'round',
                    'location': (hole_x, hole_y),
                    'size': standoff_hole_diam,
                    }

            self.holder_standoff_hole_xy.append((hole_x, hole_y))
            hole_list.append(standoff_hole)
            hole_list.append(standoff_floor_hole)

        hole_list.append(cuvette_hole)
        self.add_holes(hole_list)

    def make_holder_standoffs(self):
        standoff_diam = self.params['standoff_diameter']
        r = 0.5*standoff_diam
        h = self.params['holder_standoff_height']
        standoff = Cylinder(h=h,r1=r,r2=r)
        self.holder_standoffs = [standoff, standoff]

    def make_second_top(self):
        lid_radius = self.params['lid_radius']
        thickness = self.params['wall_thickness']
        standoff_hole_diam = self.params['standoff_hole_diameter']
        hole_list = []
        for x,y in self.standoff_xy_pos:
            hole = (x,y,standoff_hole_diam)
            hole_list.append(hole)
        self.second_top = plate_w_holes(self.top_x, self.top_y, thickness, hole_list, radius = lid_radius)
    
    def make_second_top_hole(self):
        top_hole_size = self.params['top_hole_size']
        top_hole_position = self.params['top_hole_position']
        second_top_hole = {
                'panel'    : 'second_top',
                'type'     : 'rounded_square',
                'location' : top_hole_position,
                'size'     : top_hole_size,
                }
        self.add_holes([second_top_hole])

    def make_outer_slider(self):
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        lid_radius = self.params['lid_radius']
        thickness = self.params['wall_thickness']
        standoff_hole_diam = self.params['standoff_hole_diameter']
        hole_list = []
        for x,y in self.standoff_xy_pos:
            hole = (x,y,standoff_hole_diam)
            hole_list.append(hole)
        self.outer_slider = plate_w_holes(self.top_x, self.top_y, thickness, hole_list, radius = lid_radius)

    def make_outer_slider_holes(self):
        
        # Create central hole
        slider_hole_size = self.params['slider_hole_size']
        slider_hole_position = self.params['top_hole_position']
        slider_tab_length_y = self.params['slider_tab_length_y']
        thickness = self.params['wall_thickness']

        outer_slider_hole = {
                'panel'    : 'outer_slider',
                'type'     : 'square',
                'location' : slider_hole_position,
                'size'     : slider_hole_size,
                }
        
        self.add_holes([outer_slider_hole])

        # Cut gap for slider
        slider_hole_x, slider_hole_y = slider_hole_size
        gap_cut_pos_x = -0.5*self.top_x + 0.25*(self.top_x - slider_hole_x)
        gap_cut_pos_y = 0
        gap_cut_size_x = 0.5*(self.top_x - slider_hole_x) + 2*thickness
        gap_cut_size_y = slider_hole_y - 2*slider_tab_length_y
        self.slider_gap_size_y = gap_cut_size_y

        slider_gap_hole = {
                'panel'    : 'outer_slider',
                'type'     : 'square',
                'location' : (gap_cut_pos_x, gap_cut_pos_y),
                'size'     : (gap_cut_size_x, gap_cut_size_y),
                }
        
        self.add_holes([slider_gap_hole])

    def make_slider(self):
        slider_hole_size = self.params['slider_hole_size']
        slider_overhang = self.params['slider_overhang']
        slider_tolerance = self.params['slider_tolerance']
        thickness = self.params['wall_thickness']
        lid_radius = self.params['lid_radius']
        slider_hole_x, slider_hole_y = slider_hole_size

        # Create base cube for slider
        slider_base_x = slider_hole_x + 0.5*(self.top_x - slider_hole_x)
        slider_base_x += slider_overhang
        slider_base_y = self.slider_gap_size_y - 2.0*slider_tolerance
        slider_base_z = thickness
        slider_base_size = slider_base_x, slider_base_y, slider_base_z
        self.slider_base_size = slider_base_size
        slider_base = plate_w_holes(
                slider_base_x,
                slider_base_y,
                slider_base_z,
                [],
                radius = lid_radius,
                )
        # Fix issue with removed material due to lid radius
        slider_base_fixup = Cube(size=(0.5*slider_base_x, slider_base_y, slider_base_z))
        slider_base_fixup = Translate(slider_base_fixup,v=(0.25*slider_base_x,0,0))
        slider_base = Union([slider_base,slider_base_fixup])

        # Create blocking tabs for slider
        slider_tab_x = self.params['slider_tab_length_x']
        slider_tab_y = slider_hole_y - 2.0*slider_tolerance
        slider_tab_z = thickness
        slider_tab_size = slider_tab_x, slider_tab_y, slider_tab_z
        slider_tab = Cube(size=slider_tab_size)

        # Positoin slider tab
        x_shift = 0.5*slider_base_x - 0.5*slider_tab_x
        slider_tab = Translate(slider_tab,v=(x_shift,0,0))

        # Create slider through union
        self.slider = Union([slider_base,slider_tab])

        
    def get_assembly(self,**kwargs):
        try:
            show_inner_panel = kwargs.pop('show_inner_panel')
        except KeyError:
            show_inner_panel = True
        try:
            show_holder = kwargs.pop('show_holder')
        except KeyError:
            show_holder = True
        try:
            show_holder_standoffs = kwargs.pop('show_holder_standoffs')
        except KeyError:
            show_holder_standoffs = True
        try:
            show_second_top = kwargs.pop('show_second_top')
        except KeyError:
            show_second_top = True
        try:
            show_outer_slider = kwargs.pop('show_outer_slider')
        except KeyError:
            show_second_top = True
        try:
            show_slider = kwargs.pop('show_slider')
        except KeyError:
            show_slider = True

        part_list = super(Colorimeter_Enclosure,self).get_assembly(**kwargs)

        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        explode_x, explode_y, explode_z = kwargs['explode']

        # Position inner panel
        x_shift = self.params['inner_panel_offset']
        inner_panel = Rotate(self.inner_panel, a=90, v=(0,0,1))
        inner_panel = Rotate(inner_panel, a=90, v=(0,1,0))
        inner_panel = Translate(inner_panel,v=(x_shift,0,0))
        if show_inner_panel:
            part_list.append(inner_panel)

        # Position holder
        holder_x, holder_y = self.params['holder_size']
        holder_standoff_height = self.params['holder_standoff_height']
        x_shift = -0.5*holder_x + self.params['inner_panel_offset'] - 0.5*wall_thickness  
        z_shift = 0.5*wall_thickness - 0.5*inner_z + holder_standoff_height
        holder = Translate(self.holder,v=(x_shift,0,z_shift))

        # Position holder standoffs
        z_shift = 0.5*holder_standoff_height - 0.5*inner_z 
        for pos, standoff in zip(self.holder_standoff_hole_xy, self.holder_standoffs):
            x_shift, y_shift = pos
            standoff = Translate(standoff,v=(x_shift, y_shift,z_shift))
            if show_holder_standoffs:
                part_list.append(standoff)

        if show_holder:
            part_list.append(holder)

        # Position outer slider
        z_shift = 0.5*inner_z + 1.5*wall_thickness + 2*explode_z
        outer_slider = Translate(self.outer_slider, v = (0,0,z_shift))
        if show_outer_slider:
            part_list.append(outer_slider)

        # Position slider
        slider_tolerance = self.params['slider_tolerance']
        slider_base_x, slider_base_y, slider_base_z = self.slider_base_size
        slider_hole_x, slider_hole_y = self.params['slider_hole_size']
        x_shift = -0.5*slider_base_x  + 0.5*slider_hole_x - slider_tolerance 
        slider = Translate(self.slider,v=(4*x_shift,0,z_shift))
        if show_slider:
            part_list.append(slider)

        # Position second top
        z_shift += wall_thickness + explode_z
        second_top = Translate(self.second_top, v = (0,0,z_shift))
        if show_second_top:
            part_list.append(second_top)
        return part_list

    def write_projections(self,prefix='projection', create_dxf=True):
        self.ref_cube = Cube(size=[INCH2MM,INCH2MM,INCH2MM])
        parts_list = [
                'top',
                'bottom',
                'left',
                'right',
                'front',
                'back',
                'inner_panel',
                'second_top',
                'slider',
                'outer_slider',
                'holder',
                'ref_cube',
                ]
        for part_name in parts_list:
            part = getattr(self,part_name)
            filename_base = '{0}_{1}'.format(prefix,part_name)
            filename_scad = '{0}.scad'.format(filename_base) 
            print 'writing: {0}'.format(filename_scad)

            # Create openscad projections
            prog = SCAD_Prog()
            prog.fn = 50
            part_projection = Projection(part)
            prog.add(part_projection)
            prog.write(filename_scad)
            del prog

            # Write dxf files
            filename_dxf = '{0}.dxf'.format(filename_base)
            print 'writing: {0}'.format(filename_dxf)
            subprocess.call(['openscad', '-x', filename_dxf, filename_scad])



