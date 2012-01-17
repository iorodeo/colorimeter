from py2scad import *

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
        params = {
                'size' : (inner_y+0*wall_thickness, inner_z, wall_thickness),
                'xz+'  : xz_pos,
                'xz-'  : xz_neg,
                'yz+'  : yz_pos,
                'yz-'  : yz_neg,
                }

        plate_maker = Plate_W_Tabs(params)
        self.inner_panel= plate_maker.make()


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
            self.holder_standoff_hole_xy.append((hole_x, hole_y))
            standoff_hole = {
                    'panel': 'holder',
                    'type': 'round',
                    'location': (0, hole_y),
                    'size': standoff_hole_diam,
                    }
            standoff_floor_hole = {
                    'panel': 'bottom',
                    'type': 'round',
                    'location': (0, hole_y),
                    'size': standoff_hole_diam,
                    }

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
        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        x, y = self.params['second_top_dimensions']
        x_overhang = self.params['top_x_overhang']
        y_overhang = self.params['top_y_overhang']
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
        x_shift = -0.5*holder_x + self.params['inner_panel_offset']  
        z_shift = 0.5*wall_thickness - 0.5*inner_z + holder_standoff_height
        holder = Translate(self.holder,v=(x_shift,0,z_shift))

        # Position holder standoffs
        shift_z = 0.5*holder_standoff_height - 0.5*inner_z 
        for pos, standoff in zip(self.holder_standoff_hole_xy, self.holder_standoffs):
            shift_x, shift_y = pos
            standoff = Translate(standoff,v=(shift_x, shift_y,shift_z))
            if show_holder_standoffs:
                part_list.append(standoff)

        if show_holder:
            part_list.append(holder)

        # Position second top
        second_top = Translate(self.second_top, v = (0,0,30))
        if show_second_top:
            part_list.append(second_top)

        return part_list

    def get_projection(self,**kwargs):

        part_list = super(Colorimeter_Enclosure,self).get_projection(**kwargs)

        inner_x, inner_y, inner_z = self.params['inner_dimensions']
        wall_thickness = self.params['wall_thickness']
        top_x_overhang = self.params['top_x_overhang']
        top_y_overhang = self.params['top_y_overhang']
        bottom_x_overhang = self.params['bottom_x_overhang']
        bottom_y_overhang = self.params['bottom_y_overhang']
        spacing = 4*wall_thickness

        # Position second bottom
        x_shift = -(1.0*self.bottom_x + wall_thickness + spacing) 

        # Position inner panel
        y_shift = -(0.5*self.bottom_y + 0.5*inner_z + wall_thickness + spacing)
        inner_panel = Translate(self.inner_panel, v=(x_shift,y_shift,0))
        inner_panel = Projection(inner_panel)
        part_list.append(inner_panel)

        return part_list


