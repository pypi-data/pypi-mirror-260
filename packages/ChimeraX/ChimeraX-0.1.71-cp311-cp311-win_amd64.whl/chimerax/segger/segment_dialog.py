
# Copyright (c) 2009 Greg Pintilie - pintilie@mit.edu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import os.path
import numpy
from sys import stderr
from time import time as clock

from .axes import prAxes
from . import regions
from . import graph
from . import dev_menus, timing, seggerVersion

showDevTools = False


REG_OPACITY = 0.45

def debug(*args, **kw):
    from . import debug
    if debug:
        print(*args, **kw)


from chimerax.core.tools import ToolInstance
class VolumeSegmentationDialog ( ToolInstance ):

    title = "Segment Map (Segger v" + seggerVersion + ")"
    name = "segment map"
    help = 'help:user/tools/segment.html'
    SESSION_SAVE = True

    def __init__(self, session, tool_name):
        self.cur_seg = None

        ToolInstance.__init__(self, session, tool_name)
        from chimerax.ui import MainToolWindow
        tw = MainToolWindow(self, close_destroys = False)
        self.tool_window = tw
        parent = tw.ui_area

        from Qt.QtWidgets import QVBoxLayout, QLabel
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        parent.setLayout(layout)

        # File and Regions pull-down menus
        mbar = self._create_menubar(parent)
        layout.addWidget(mbar)
        
        # Map menu
        mf = self._create_map_menu(parent)
        layout.addWidget(mf)

        # Segmentation menu
        sf = self._create_segmentation_menu(parent)
        layout.addWidget(sf)

        # Options panel
        options = self._create_options_gui(parent)
        layout.addWidget(options)

        # Shortcuts panel
        shortcuts = self._create_shortcuts_gui(parent)
        layout.addWidget(shortcuts)

        # Segment, Group, Ungroup, ... buttons
        bf = self._create_action_buttons(parent)
        layout.addWidget(bf)

        # Status line
        self._status_label = sl = QLabel(parent)
        layout.addWidget(sl)
        
        tw.manage(placement="side", fixed_size = True)

        self._model_close_handler = session.triggers.add_handler('remove models', self.model_closed_cb)

        from Qt.QtCore import QTimer
        QTimer.singleShot(1000, self._help_line)

    def delete(self):
        self.session.triggers.remove_handler(self._model_close_handler)
        ToolInstance.delete(self)
        
    def _create_map_menu(self, parent):
        from Qt.QtWidgets import QFrame, QHBoxLayout, QLabel
        
        mf = QFrame(parent)
        mlayout = QHBoxLayout(mf)
        mlayout.setContentsMargins(0,0,0,0)
        mlayout.setSpacing(10)
        
        sm = QLabel('Segment map', mf)
        mlayout.addWidget(sm)
        from chimerax.ui.widgets import ModelMenuButton
        from chimerax.map import Volume
        self._map_menu = mm = ModelMenuButton(self.session, class_filter = Volume)
        # mm.value_changed.connect(self._map_chosen_cb)
        mlayout.addWidget(mm)
        mlayout.addStretch(1)    # Extra space at end

        return mf

    def _create_segmentation_menu(self, parent):
        from Qt.QtWidgets import QFrame, QHBoxLayout, QLabel
        
        sf = QFrame(parent)
        slayout = QHBoxLayout(sf)
        slayout.setContentsMargins(0,0,0,0)
        slayout.setSpacing(10)
        
        cs = QLabel('Current segmentation', sf)
        slayout.addWidget(cs)
        from chimerax.ui.widgets import ModelMenuButton
        from .regions import Segmentation
        self._segmentation_menu = sm = ModelMenuButton(self.session, class_filter = Segmentation)
        sm.value_changed.connect(self._segmentation_menu_cb)
        slayout.addWidget(sm)
        self._region_count = rc = QLabel('', sf)
        slayout.addWidget(rc)

        slayout.addStretch(1)    # Extra space at end

        return sf
    
    def _create_menubar(self, parent):

# Can't use QMenuBar since this takes over main window menu on Mac.
#        from Qt.QtWidgets import QMenuBar
#        mbar = QMenuBar(parent)
#        mbar.setNativeMenuBar(False)	# On Mac keep menu in window, not top of screen.

        from Qt.QtWidgets import QFrame, QHBoxLayout, QPushButton, QMenu
        
        mbar = QFrame(parent)
        mbar.setFrameStyle(QFrame.Box | QFrame.Raised)
        layout = QHBoxLayout(mbar)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(10)

        file_menu_entries = (
            ('Open segmentation...', self.OpenSegmentation),
            ('Save segmentation', self.SaveSegmentation),
            ('Save segmentation as...', self.SaveSegmentationAs),
            ("Save selected regions to .mrc file...", self.WriteSelRegionsMRCFile),
            ("Save all regions to .mrc file...", self.WriteAllRegionsMRCFile),
            ("Save each region to .mrc file...", self.WriteEachRegionMRCFile),
            ("Close segmentation", self.CloseSeg),
            ("Close all segmentations except displayed", self.CloseHiddenSeg),
            ("Close all segmentations", self.CloseAll),
            ("Associate Selected", self.Associate),
            )

        fb = QPushButton('File', mbar)
        button_style = 'QPushButton { border: none; } QPushButton::menu-indicator { image: none; }'
        from sys import platform
        if platform == 'darwin':
            # Specify exact width and height to work around Qt 6.2.3 bug where text is clipped.
            button_style += ' QPushButton { width: 40px; height: 25px; }'
        fb.setStyleSheet(button_style)
        layout.addWidget(fb)
        fmenu = QMenu(fb)
        fb.setMenu(fmenu)
        for text, func in file_menu_entries:
            fmenu.addAction(text, func)

        from . import attributes
        regions_menu_entries = (
            ('separator', None),
            ("Show all", self.RegSurfsShowAll),
            ("Show only selected", self.RegSurfsShowOnlySelected),
            ("Show adjacent", self.RegSurfsShowAdjacent),
            ('Show grouping', self.ShowUngroupedSurfaces),
            ('Unshow grouping', self.ShowGroupSurfaces),
            ("Hide", self.RegSurfsHide),
            ("Make transparent", self.RegSurfsTransparent),
            ("Make opaque", self.RegSurfsOpaque),
            ('Color density map', self.ColorDensity),
            ('separator', None),
            ('Select groups', self.SelectGroups),
            ('Select boundary regions', self.SelectBoundaryRegions),
            ("Invert selection", self.Invert),
            ("Regions overlapping current selection", self.Overlapping),
            ('separator', None),
            #("Group selected", self.JoinSelRegs),
            #("Ungroup selected", self.UngroupSelRegs),
            #("Smooth and group", self.SmoothAndGroupOneStep),
            ("Delete selected regions", self.DelSelRegs),
            ("Delete all except selected", self.DelExcSelRegs),
            ("separator", None),
            ("Enclosed volume", self.RegionsVolume),
            ("Mean and SD", self.RegionMeanAndSD),
            #("Mask map with selected", self.MaskMapWRegions),
            #("Mask another map with selected (shrink map)", self.MaskAnotherMapWRegionsShrink),
            #("Mask another map with selected (keep map dimensions)", self.MaskAnotherMapWRegions),
            ("Extract densities...", self.ExtractDensities),
            ("Subtract selected from map", self.SubtractRegionsFromMap),
            ("Show axes for selected", self.ShowRegionAxesSelected),
            ("Hide all axes", self.HideRegionAxes),
            ("separator", None),
            ("Attributes table...", attributes.show_region_attributes_dialog),
            ("How many sub-regions", self.ShowNumSubRegs)
            )

        rb = QPushButton('Regions', mbar)
        if platform == 'darwin':
            button_style += ' QPushButton { width: 65px; height: 25px; }'
        rb.setStyleSheet(button_style)
        layout.addWidget(rb)
        rmenu = QMenu(rb)
        rb.setMenu(rmenu)
        for text, func in regions_menu_entries:
            if text == 'separator':
                rmenu.addSeparator()
            else:
                a = rmenu.addAction(text, func)
                if text in ('Extract densities...', 'Attributes table...'):
                    a.setEnabled(False)	# These are not ported to ChimeraX yet.

        if dev_menus:
            rmenu.add_separator()
            for lbl, var, val, cmd in (
                ("Surfaces around voxels", self.regsVisMode,
                 'Voxel_Surfaces', self.RegsDispUpdate),
                ("Map iso-surfaces", self.regsVisMode,
                 'Iso_Surfaces', self.RegsDispUpdate),
                #(" - delete files", self.deleteCloseFiles, 1, None),
                ):
                rmenu.add_radiobutton(label = lbl, variable = var, value = val,
                                      command = cmd)
            #rmenu.add_separator()
            #for lbl, cmd in (#("Adjacency graph",self.RegionsAdjGraph),
                #("Group connected", self.GroupConnectedRegs),
                #("Select non-placed", self.SelectNonPlacedRegions),
                #("Apply threshold", self.RegsDispThr),
                #("Group connected", self.GroupConnectedRegs),
                #("Group by contacts", self.GroupByContacts),
                #("Group using all fits", self.GroupUsingFits),
                #("Ungroup ALL", self.UngroupAllRegs),
                #("Reduce map", self.ReduceMap),
                #("Close", self.CloseRegions),
                #):
                #rmenu.add_command(label = lbl, command = cmd)
            #self.deleteCloseFiles = Tkinter.IntVar()
            #self.deleteCloseFiles.set ( 1 )

            #rmenu.add_separator()
            #for lbl, cmd in (
            #    ("Mask map with selected (Cube Result)", self.MaskMapWRegionsCube),
            #    ("Extract map cube around selected", self.ExtractMapWRegionsCube),
            #    ):
            #    rmenu.add_command(label = lbl, command = cmd)

        if dev_menus:
            graph_menu_entries = (
                #('Save graph', self.SaveGraph),
                #('Load graph', self.LoadGraph),
                #'separator',
                ('Create graph with uniform link radii', self.Graph),
                #(' - Use maximum density between regions', self.GraphMaxD),
                #(' - Use average density between regions', self.GraphAvgD),
                (' - Use number of contacting voxel pairs', self.GraphN),
                'separator',
                ('Close graph', self.CloseGraph),
                #('Break selected links', graph.break_selected_links),
                #('Link selected', graph.link_selected),
                #('Group regions using skeleton', self.GroupBySkeleton),
                #('Join selected', self.GroupBySkeleton)
                )
            smenu = Hybrid.cascade_menu(menubar, 'Graph',
                                        graph_menu_entries)

        layout.addStretch(1)
        
        return mbar
    
    def _create_options_gui(self, parent):

        from chimerax.ui.widgets import CollapsiblePanel, EntriesRow, radio_buttons
        p = CollapsiblePanel(parent, 'Segmenting Options')
        f = p.content_area

        nrer = EntriesRow(f, 'Display at most', 60, 'regions, granularity', 1, 'voxels')
        self._max_num_regions, self._surface_granularity = nrer.values

        krer = EntriesRow(f, 'Keep regions having at least', 1, 'voxels,', 0, 'contact voxels')
        self._min_region_size, self._min_contact_size = krer.values
        
        gser = EntriesRow(f, True, 'Group by smoothing', 4, 'steps of size', 1.0, ', stop at', 1, 'regions')
        self._group_smooth, self._num_steps, self._step_size, self._target_num_regions = gser.values

        gcer = EntriesRow(f, False, 'Group by connectivity', 20, 'steps, stop at', 1, 'regions', False, 'only visible')
        self._group_con, self._num_steps_con, self._target_num_regions_con, self._group_by_con_only_visible = gcer.values

        radio_buttons(self._group_smooth, self._group_con)
        
        return p
    
    def _create_shortcuts_gui(self, parent):

        from chimerax.ui.widgets import CollapsiblePanel, button_row
        p = CollapsiblePanel(parent, 'Shortcuts Options')
        f = p.content_area
        layout = f.layout()

        rows = [('Select regions:', (('All', self.SelectAllRegions),
                                     ("Over Sel. Atoms", self.Overlapping),
                                     ("Invert", self.Invert),
                                     ("Not-Grp", self.SelectNotGrouped),
                                     ("Grouped", self.SelectGrouped))),
                ('Selected regions:', (#("Group", self.Group),
                                       #("Ungroup", self.Ungroup),
                                       ("Hide", self.RegSurfsHide),
                                       ("Show", self.RegSurfsShow),
                                       ("Delete", self.DelSelRegs),
                                       ("Tr.", self.RegSurfsTransparent),
                                       ("Opaque", self.RegSurfsOpaque),
                                       ("Mesh", self.RegSurfsMesh))),
                ('Show regions: ', (("None", self.RegSurfsShowNone),
                                    ("All", self.RegSurfsShowAll),
                                    ("Only Sel.", self.RegSurfsShowOnlySelected),
                                    ("Adj.", self.RegSurfsShowAdjacent),
                                    ("Not-Grp", self.RegSurfsShowNotGrouped),
                                    ("Grouped", self.RegSurfsShowGrouped))),

                ('Other tools: ', (("Fit", self.FitDialog),
                                   ("Extract", None), #self.ExtractDensities),
                                   ("iSeg", None), #self.ISeg),
                                   #("SegLoop", self.SegLoop),
                                   ("ProMod", None), #self.ProMod),
                                   ("ModelZ", None), #self.ModelZ),
                )),
                ]
        for title, buttons in rows:
            r = button_row(f, buttons, label=title, margins = (0,0,0,0))
            layout.addWidget(r)
        layout.addStretch(1)
        
        return p

    def _create_action_buttons(self, parent):
        from Qt.QtWidgets import QFrame, QHBoxLayout, QPushButton
        bf = QFrame(parent)
        blayout = QHBoxLayout(bf)
        blayout.setContentsMargins(0,0,0,0)
        blayout.setSpacing(10)

        buttons = [('Segment', self._segment),
                   ('Group', self._group),
                   ('Ungroup', self._ungroup),
                   ('Fit', self.FitDialog),
                   ('Help', self._help)]
        for name, callback in buttons:
            b = QPushButton(name, bf)
            b.clicked.connect(callback)
            blayout.addWidget(b)

        blayout.addStretch(1)    # Extra space at end

        return bf

        
    @classmethod
    def get_singleton(self, session, create=True):
        from chimerax.core import tools
        return tools.get_singleton(session, VolumeSegmentationDialog, 'Segment Map', create=create)

    def status(self, message, log = True):
        self._status_label.setText(message)
        if log:
            self.session.logger.info(message)
        
    def _segment(self):
        self.Segment()

    def _group(self):
        self.Group()

    def _ungroup(self):
        self.Ungroup()

    def _help(self):
        from chimerax.help_viewer import show_url
        show_url(self.session, self.help)

    def _help_line(self):
        self.status('<font color=blue>To cite Segger or learn more about it press the Help button</font>', log = False)
            
    @property
    def map_name(self):
        v = self._map_menu.value
        return v.name if v else ''

    def _get_chosen_map(self):
        return self._map_menu.value
    def _set_chosen_map(self, map):
        self._map_menu.value = map
    chosen_map = property(_get_chosen_map, _set_chosen_map)
    
    def _get_chosen_segmentation(self):
        return self._segmentation_menu.value
    def _set_chosen_segmentation(self, seg):
        self._segmentation_menu.value = seg
    chosen_segmentation = property(_get_chosen_segmentation, _set_chosen_segmentation)

    @property
    def group_mode(self):
        if self._group_smooth.enabled:
            return 'smooth'
        if self._group_con.enabled:
            return 'connected'
        return None
    
    def fillInUI(self, parent):

        self.group_mouse_mode = None

        self.regsVisMode = tkinter.StringVar()
        self.regsVisMode.set ( 'Voxel_Surfaces' )

        rmenu = Hybrid.cascade_menu(menubar, 'Regions', regions_menu_entries)

        if dev_menus:
            rmenu.add_separator()
            for lbl, var, val, cmd in (
                ("Surfaces around voxels", self.regsVisMode,
                 'Voxel_Surfaces', self.RegsDispUpdate),
                ("Map iso-surfaces", self.regsVisMode,
                 'Iso_Surfaces', self.RegsDispUpdate),
                #(" - delete files", self.deleteCloseFiles, 1, None),
                ):
                rmenu.add_radiobutton(label = lbl, variable = var, value = val,
                                      command = cmd)
            #rmenu.add_separator()
            #for lbl, cmd in (#("Adjacency graph",self.RegionsAdjGraph),
                #("Group connected", self.GroupConnectedRegs),
                #("Select non-placed", self.SelectNonPlacedRegions),
                #("Apply threshold", self.RegsDispThr),
                #("Group connected", self.GroupConnectedRegs),
                #("Group by contacts", self.GroupByContacts),
                #("Group using all fits", self.GroupUsingFits),
                #("Ungroup ALL", self.UngroupAllRegs),
                #("Reduce map", self.ReduceMap),
                #("Close", self.CloseRegions),
                #):
                #rmenu.add_command(label = lbl, command = cmd)
            #self.deleteCloseFiles = Tkinter.IntVar()
            #self.deleteCloseFiles.set ( 1 )

            #rmenu.add_separator()
            #for lbl, cmd in (
            #    ("Mask map with selected (Cube Result)", self.MaskMapWRegionsCube),
            #    ("Extract map cube around selected", self.ExtractMapWRegionsCube),
            #    ):
            #    rmenu.add_command(label = lbl, command = cmd)

        if dev_menus:
            graph_menu_entries = (
                #('Save graph', self.SaveGraph),
                #('Load graph', self.LoadGraph),
                #'separator',
                ('Create graph with uniform link radii', self.Graph),
                #(' - Use maximum density between regions', self.GraphMaxD),
                #(' - Use average density between regions', self.GraphAvgD),
                (' - Use number of contacting voxel pairs', self.GraphN),
                'separator',
                ('Close graph', self.CloseGraph),
                #('Break selected links', graph.break_selected_links),
                #('Link selected', graph.link_selected),
                #('Group regions using skeleton', self.GroupBySkeleton),
                #('Join selected', self.GroupBySkeleton)
                )
            smenu = Hybrid.cascade_menu(menubar, 'Graph',
                                        graph_menu_entries)

        self.UseAllMods = tkinter.IntVar()
        self.UseAllMods.set ( 0 )

        if dev_menus:
            b = tkinter.Button(f, text="Ctr Rot", command=self.MapCOM)
            b.grid (column=6, row=0, sticky='w', padx=5)


        if dev_menus:
            cp = Hybrid.Popup_Panel(parent)
            cpf = cp.frame
            cpf.grid(row = row, column = 0, sticky = 'news')
            cpf.grid_remove()
            cpf.columnconfigure(0, weight=1)
            self.contactsPanel = cp.panel_shown_variable
            row += 1
            orow = 0

            cb = cp.make_close_button(cpf)
            cb.grid(row = orow, column = 0, sticky = 'e')

            l = tkinter.Label(cpf, text='Contact Grouping', font = 'TkCaptionFont')
            l.grid(column=0, row=orow, sticky='w', pady=5)
            orow += 1

            s = Hybrid.Scale(cpf, 'Coloring level ', 1, 100, 1, 100)
            s.frame.grid(row = orow, column = 0, sticky = 'ew')
            orow += 1
            self.colorLevel = s
            s.callback(self.SetColorLevel)

            b = tkinter.Button(cpf, text = 'Set Grouping',
                               command = self.SetContactGrouping)
            b.grid(row = orow, column = 0, sticky = 'w')
            orow += 1


        # --- Options Frame ----------------------------------------------------------------------

        oft = Hybrid.Checkbutton(f, 'Use symmetry:', False )
        #oft.button.grid(row = 0, column = 0, sticky = 'w')
        self.useSymmetry = oft.variable

        if 0 :
            f = tkinter.Frame(sopt)
            #f.grid(column=0, row=sorow, sticky='w')

            #self.symmetryString = Tkinter.StringVar(f)
            #e = Tkinter.Entry(f, width=10, textvariable=self.symmetryString)
            #e.grid(column=1, row=0, sticky='w', padx=5)

            #b = Tkinter.Button(f, text="Detect", command=self.DetectSym)
            #b.grid (column=2, row=0, sticky='w', padx=5)

            #b = Tkinter.Button(f, text="Show", command=self.PlaceSym)
            #b.grid (column=3, row=0, sticky='w', padx=5)

            #sorow += 1



        if 0:
            f = tkinter.Frame(sopt)
            f.grid(column=0, row=sorow, sticky='w')
            sorow += 1

            l = tkinter.Label(f, text='Minimum connecting voxels ')
            l.grid(column=0, row=0, sticky='w')

            self.minConnection = tkinter.StringVar(sopt)
            self.minConnection.set ( '0' )
            e = tkinter.Entry(f, width=5, textvariable=self.minConnection)
            e.grid(column=1, row=0, sticky='w', padx=5)


            mmf = tkinter.Frame(sopt)
            mmf.grid(row = sorow, column = 0, sticky = 'ew')
            sorow += 1

            mg = Hybrid.Checkbutton(mmf, 'Group with mouse ', False)
            mg.button.grid(row = 0, column = 0, sticky = 'w')
            self.mouse_group = mg.variable
            mg.callback(self.mouse_group_cb)

            mgb = Hybrid.Option_Menu(mmf, '', 'button 1', 'button 2',
                                     'button 3', 'ctrl button 1',
                                     'ctrl button 2', 'ctrl button 3')
            mgb.variable.set('button 3')
            mgb.frame.grid(row = 0, column = 1, sticky = 'w')
            mgb.add_callback(self.mouse_group_button_cb)
            self.mouse_group_button = mgb


        # --- Shortcuts Frame ----------------------------------------------------------------------

        sc = Hybrid.Popup_Panel(parent)
        scf = sc.frame
        scf.grid(row = row, column = 0, sticky = 'news')
        scf.grid_remove()
        scf.columnconfigure(0, weight=1)
        self.shortcutsPanelShownVar = sc.panel_shown_variable
        row += 1
        orow = 0

        dummyFrame = tkinter.Frame(scf, relief='groove', borderwidth=1)
        tkinter.Frame(dummyFrame).pack()
        dummyFrame.grid(row=orow,column=0,columnspan=7, pady=1, sticky='we')
        orow += 1

        cb = sc.make_close_button(scf)
        cb.grid(row = orow, column = 1, sticky = 'e')

        l = tkinter.Label(scf, text='Shortcuts', font = 'TkCaptionFont')
        l.grid(column=0, row=orow, sticky='w', pady=5)
        orow += 1

        sopt = tkinter.Frame(scf)
        sopt.grid(column=0, row=orow, sticky='ew', padx=10)
        orow += 1
        sorow = 0


        f = tkinter.Frame(sopt)
        f.grid(column=0, row=sorow, sticky='w')
        sorow += 1
        if 1 :
            b = tkinter.Label(f, text="Select regions: ", width=15, anchor=tkinter.E)
            b.grid (column=0, row=0, sticky='w', padx=0)

            self.overlappingPercentage = tkinter.StringVar(f)
            self.overlappingPercentage.set ( "50" )
            #e = Tkinter.Entry(f, width=4, textvariable=self.overlappingPercentage)
            #e.grid(column=1, row=0, sticky='w', padx=5)
            #l = Tkinter.Label(f, text="%")
            #l.grid(column=2, row=0, sticky='w')


            b = tkinter.Button(f, text="All", command=self.SelectAllRegions)
            b.grid (column=1, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Over Sel. Atoms", command=self.Overlapping)
            b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Invert", command=self.Invert)
            b.grid (column=3, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Not-", command=self.SelectNotGrouped)
            b.grid (column=4, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Grouped", command=self.SelectGrouped)
            b.grid (column=5, row=0, sticky='w', padx=5)


        f = tkinter.Frame(sopt)
        f.grid(column=0, row=sorow, sticky='w')
        sorow += 1
        if 1 :
            l = tkinter.Label(f, text='Selected regions: ', width=15, anchor=tkinter.E)
            l.grid(column=0, row=0)

            #b = Tkinter.Button(f, text="Group", command=self.Group)
            #b.grid (column=1, row=0, sticky='w', padx=5)

            #b = Tkinter.Button(f, text="Ungroup", command=self.Ungroup)
            #b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Hide", command=self.RegSurfsHide)
            b.grid (column=1, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Show", command=self.RegSurfsShow)
            b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Delete", command=self.DelSelRegs)
            b.grid (column=3, row=0, sticky='w', padx=5)


        #f = Tkinter.Frame(sopt)
        #f.grid(column=0, row=sorow, sticky='w')
        #sorow += 1
        #if 1 :
            #l = Tkinter.Label(f, text=' ', width=15)
            #l.grid(column=0, row=0, sticky='w')

            b = tkinter.Button(f, text="Tr.", command=self.RegSurfsTransparent)
            b.grid (column=4, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Opaque", command=self.RegSurfsOpaque)
            b.grid (column=5, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Mesh", command=self.RegSurfsMesh)
            b.grid (column=6, row=0, sticky='w', padx=5)


            #b = Tkinter.Button(f, text="Invert Selection", command=self.Invert)
            #b.grid (column=3, row=0, sticky='w', padx=5)


        f = tkinter.Frame(sopt)
        f.grid(column=0, row=sorow, sticky='w')
        sorow += 1
        if 1 :
            l = tkinter.Label(f, text='Show regions: ', width=15, anchor=tkinter.E)
            l.grid(column=0, row=0, sticky='w')

            b = tkinter.Button(f, text="None", command=self.RegSurfsShowNone)
            b.grid (column=1, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="All", command=self.RegSurfsShowAll)
            b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Only Sel.", command=self.RegSurfsShowOnlySelected)
            b.grid (column=3, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Adj.", command=self.RegSurfsShowAdjacent)
            b.grid (column=4, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Not-", command=self.RegSurfsShowNotGrouped)
            b.grid (column=5, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Grouped", command=self.RegSurfsShowGrouped)
            b.grid (column=6, row=0, sticky='w', padx=5)


            if 0 :
                b = tkinter.Button(f, text="Axes", command=self.ShowRegionAxesSelected)
                b.grid (column=4, row=0, sticky='w', padx=5)

                self.axesFactor = tkinter.StringVar(f)
                self.axesFactor.set ( "3" )
                e = tkinter.Entry(f, width=4, textvariable=self.axesFactor)
                e.grid(column=5, row=0, sticky='w', padx=5)



        if 1 :
            # flat, groove, raised, ridge, solid, or sunken
            dummyFrame = tkinter.Frame(sopt, relief='flat', borderwidth=1)
            tkinter.Frame(dummyFrame).pack()
            dummyFrame.grid(row=sorow,column=0,columnspan=7, pady=3, sticky='we')
            sorow += 1

            f = tkinter.Frame(sopt)
            f.grid(column=0, row=sorow, sticky='w')
            sorow += 1

            l = tkinter.Label(f, text='Other tools: ', width=15, anchor=tkinter.E)
            l.grid(column=0, row=0)

            b = tkinter.Button(f, text="Fit", command=self.FitDialog)
            b.grid (column=1, row=0, sticky='w', padx=2)

            b = tkinter.Button(f, text="Extract", command=self.ExtractDensities)
            b.grid (column=2, row=0, sticky='w', padx=2)

            b = tkinter.Button(f, text="iSeg", command=self.ISeg)
            b.grid (column=3, row=0, sticky='w', padx=2)

            #b = Tkinter.Button(f, text="SegLoop", command=self.SegLoop)
            #b.grid (column=5, row=0, sticky='w', padx=2)

            b = tkinter.Button(f, text="ProMod", command=self.ProMod)
            b.grid (column=6, row=0, sticky='w', padx=2)

            b = tkinter.Button(f, text="ModelZ", command=self.ModelZ)
            b.grid (column=7, row=0, sticky='w', padx=2)


        if showDevTools or dev_menus :
            f = tkinter.Frame(sopt)
            f.grid(column=0, row=sorow, sticky='w')
            sorow += 1

            l = tkinter.Label(f, text=' ', width=15, anchor=tkinter.E)
            l.grid(column=0, row=0)

            #b = Tkinter.Button(f, text="GeoSeg", command=self.GeoSegDialog)
            #b.grid (column=1, row=0, sticky='w', padx=5)

            #b = Tkinter.Button(f, text="SSE", command=self.SSE)
            #b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Animate", command=self.Animate)
            b.grid (column=3, row=0, sticky='w', padx=5)

            if showDevTools or dev_menus :
                b = tkinter.Button(f, text="iSeg", command=self.ISeg)
                b.grid (column=4, row=0, sticky='w', padx=2)


            b = tkinter.Button(f, text="FlexFit", command=self.FlexFit)
            b.grid (column=5, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="GeoSeg", command=self.GeoSeg)
            b.grid (column=6, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="MapQ", command=self.MapQ)
            b.grid (column=7, row=0, sticky='w', padx=2)



            f = tkinter.Frame(sopt)
            f.grid(column=0, row=sorow, sticky='w')
            sorow += 1

            l = tkinter.Label(f, text=' ', width=15, anchor=tkinter.E)
            l.grid(column=0, row=0)

            b = tkinter.Button(f, text="SegMod", command=self.SegMod)
            b.grid (column=1, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="SegNA", command=self.SegNA)
            b.grid (column=2, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Ar", command=self.Ar)
            b.grid (column=3, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="VR", command=self.Vr)
            b.grid (column=4, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="Mono", command=self.CamMono)
            b.grid (column=5, row=0, sticky='w', padx=5)

            b = tkinter.Button(f, text="SBS", command=self.CamSBS)
            b.grid (column=6, row=0, sticky='w', padx=5)



        # ---------- end of shortcuts frame  ------------------------------------------------------


        dummyFrame = tkinter.Frame(parent, relief='groove', borderwidth=1)
        tkinter.Frame(dummyFrame).pack()
        dummyFrame.grid(row=row,column=0,columnspan=7, pady=7, sticky='we')


        row += 1

        f = tkinter.Frame(parent)
        f.grid(column=0, row=row, sticky='ew')
        row += 1

        l = tkinter.Label(f, text='To cite Segger or learn more about it press the Help button', fg="blue")
        l.grid(column=0, row=0, sticky='w')

        dummyFrame = tkinter.Frame(parent, relief='groove', borderwidth=1)
        tkinter.Frame(dummyFrame).pack()
        dummyFrame.grid(row=row,column=0,columnspan=7, pady=3, sticky='we')
        row += 1

        global msg
        msg = tkinter.Label(parent, width = 60, anchor = 'w', justify = 'left', fg="red")
        msg.grid(column=0, row=row, sticky='ew')
        self.msg = msg

        self.status ( 'Select an open density map in the field above and press Segment!' )
        row += 1

        vlist = VolumeViewer.volume_list()
        if vlist:
            self.SetMapMenu(vlist[0])

        for m in regions.segmentations(self.session) :

            v = m.volume_data()
            if v and m.display :
                self.SetCurrentSegmentation ( m )
                try : self.SetMapMenu ( v )
                except : pass

        chimera.openModels.addRemoveHandler(self.ModelClosed, None)

        if dev_menus :
            self.optionsPanel.set(True)
            self.shortcutsPanelShownVar.set(True)


    def SetColorLevel(self):

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        s = self.colorLevel
        lev = int(s.value())

        regions = [r for r in smod.all_regions()
                   if hasattr(r, 'color_level') and r.color_level >= lev and
                   (r.preg is None or r.preg.color_level < lev)]
        smod.color_density(regions)
        return

        # TODO: Unused code adjusts region surface colors.

        if not hasattr(smod, 'contact_grouping'):
            cg = smod.contact_grouping = regions.contact_grouping(smod)
            smod.region_count = len(smod.childless_regions())
        cg = smod.contact_grouping
        range = (smod.region_count - len(cg), smod.region_count)
        if s.range() != range:
            s.set_range(range[0], range[1], step = 1)
        p = max(0, smod.region_count - int(s.value()))

        cs, pairs = regions.connected_subsets(cg[:p])

        # Reset colors
        from .regions import float_to_8bit_color
        for r in smod.regions:
            sp = r.surface_piece
            if sp:
                sp.color = float_to_8bit_color(r.color)

        # Color groups
        for rlist in cs:
            r0 = rlist[0]
            sp0 = r0.surface_piece
            if sp0:
                c = sp0.color
                for r in rlist[1:]:
                    sp = r.surface_piece
                    if sp:
                        sp.color = c

    def SetColorLevelRange(self):

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        clevels = [r.color_level for r in smod.all_regions()
                   if hasattr(r, 'color_level')]
        clmin = min(clevels)
        clmax = max(clevels)
        cl = self.colorLevel
        cl.set_range(clmin, clmax, step = 1)
        cl.set_value(clmin)

    def SetContactGrouping(self):

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        s = self.colorLevel
        lev = int(s.value())

        regions = [r for r in smod.all_regions()
                   if hasattr(r, 'color_level') and r.color_level < lev]
        smod.remove_regions(regions, update_surfaces = True)
        self.RegsDispUpdate()


    def ColorDensity(self):

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        smod.color_density()




    def Options(self) :

        self.optionsPanel.set (not self.optionsPanel.get())



    def Shortcuts (self) :

        debug("shortcuts")
        self.shortcutsPanelShownVar.set ( not self.shortcutsPanelShownVar.get() )

    def RSeg ( self ) :
        from . import rseg_dialog
        rseg_dialog.show_dialog()

    def ISeg ( self ) :
        from . import iseg_dialog
        iseg_dialog.show_dialog()

    def SSE ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import sse_dialog
        sse_dialog.show_sse_dialog()

    def SegLoop ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import segloop_dialog
        segloop_dialog.show_dialog()

    def SegMod ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import segmod_dialog
        segmod_dialog.show_dialog()

    def SegNA ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import segna_dialog
        segna_dialog.show_dialog()


    def Ar ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import ar_dialog
        ar_dialog.show_dialog()


    def Vr ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import vr_dialog
        vr_dialog.show_dialog()


    def CamMono ( self ) :
        chimera.viewer.camera.setMode ( "mono" )

    def CamSBS ( self ) :
        chimera.viewer.camera.setMode ( "DTI side-by-side stereo" )


    def ProMod ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import promod_dialog
        promod_dialog.show_dialog()


    def ModelZ ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import modelz
        modelz.show_dialog()

    def MapQ ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import mapq
        mapq.show_dialog()


    def Animate ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import animate_dialog
        animate_dialog.close_animate_dialog ()
        animate_dialog.show_dialog()

    def FlexFit ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import flexfit_dialog
        flexfit_dialog.show_dialog()


    def Tomolog ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import tomolog_dialog
        tomolog_dialog.show_dialog()

    def GeoSeg ( self ) :
        # self.ssePanelShownVar.set ( not self.ssePanelShownVar.get() )
        from . import geoseg_dialog
        geoseg_dialog.show_dialog()

    def MapCOM ( self ) :

        dmap = self.SegmentationMap()

        from . import axes
        pts, weights = axes.map_points ( dmap )
        if len(pts) == 0 :
            debug(" - no pts at this threshold?")
            return

        COM, U, S, V = axes.prAxes ( pts )
        debug("com:", COM)


        #chimera.viewer.camera.center = chimera.Point ( COM[0], COM[1], COM[2] )
        #xf = chimera.Xform.translation ( chimera.Vector( -COM[0], -COM[1], -COM[2] ) )
        #dmap.openState.xform = xf

        p = chimera.Point ( COM[0], COM[1], COM[2] )
        chimera.openModels.cofr = dmap.openState.xform.apply ( p )



    def OpenSegmentation(self):

        dmap = self.SegmentationMap()
        dir = os.path.dirname(dmap.data.path) if dmap else None
        from . import segfile
        segfile.show_open_dialog(self.session, dir)



    def OpenSegFiles(self, paths_and_types, open = True):

        smods = []
        from . import segfile
        for path, ftype in paths_and_types:
            if ftype == 'Segmentation':
                smod = segfile.read_segmentation(self.session, path, open)
            elif ftype == 'Old regions file':
                dmap = self.SegmentationMap()
                if dmap is None:
                    from os.path import basename
                    self.session.logger.error(
                        'Segmentation map must be open before opening old-style segmentation file\n\n\t%s\n\nbecause file does not contain grid size and spacing.' % basename(path))
                    return
                from . import regionsfile
                smod = regionsfile.ReadRegionsFile ( path, dmap )
            smods.append(smod)

        if len(smods) == 0:
            self.status ( "No segmentation was loaded." )
            return

        for smod in smods:
            smod.open_map()

        # TODO: Can't control whether marker model is opened.
        smod = smods[-1]
        self.show_segmentation(smod)

        for s in smods:
            mname = os.path.basename(getattr(s, 'map_path', 'unknown'))
            self.status('Opened segmentation %s of map %s, grid size (%d,%d,%d)'
                 % ((s.name, mname) + tuple(s.grid_size())))


        return smods

    def show_segmentation(self, smod):
        self.SetCurrentSegmentation(smod)
        v = smod.volume_data()
        if v:
            self.SetMapMenu(v)
        else :
            self.status ( "Volume data not found" )
        self.RegsDispUpdate ()


    def SaveSegmentation(self):

        smod = self.CurrentSegmentation()
        if smod:

            map = smod.volume_data()
            if map == None :
                self.status ( "Map not found - please associate a map first" )
                return

            if hasattr(smod, 'path') and smod.path:
                from . import segfile
                segfile.write_segmentation(smod, smod.path)
                self.status ( "Saved" )

            else:
                self.SaveSegmentationAs()
        else :
            self.status ( "No segmentation selected" )



    def SaveSegmentationAs(self):

        smod = self.CurrentSegmentation()
        if smod:
            from . import segfile
            segfile.show_save_dialog(smod, self.path_changed_cb)

    def path_changed_cb(self, seg):

        if seg is self.CurrentSegmentation():
            seg.name = os.path.basename(seg.path)
            self.chosen_segmentation.value = seg

    def model_closed_cb(self, trigger, mlist):

        if self.cur_seg in mlist:
            self.cur_seg = None
            self.chosen_segmentation = None

    def MapMenu ( self ) :

        self.mb.menu.delete ( 0, 'end' )        # Clear menu
        from chimerax.map import Volume
        mlist = self.session.models.list(type = Volume)
        for m in mlist :
            self.mb.menu.add_radiobutton ( label=m.name, variable=self.dmap,
                                           command=lambda m=m: self.MapSelected(m) )

    def SetMapMenu (self, dmap):

        self.chosen_map = dmap
        self.cur_dmap = dmap
        #print "Set map menu to ", dmap.name

    def MapSelected ( self, dmap ) :

        self.cur_dmap = dmap
        #if dmap:
        #    dmap.display = True

    def SegmentationMap(self):

        return self.chosen_map

    def FillSegmentationMenu ( self ) :

        menu = self.mbSegmentationMenu
        menu.delete ( 0, 'end' )      # Clear menu

        open_names = [(m.name, m) for m in regions.segmentations(self.session)]
        if len(open_names ) > 0 :
            menu.add_radiobutton ( label="Open regions files:" )
            menu.add_separator()
            open_names.sort()
            for name, smod in open_names:
                menu.add_radiobutton (label=name, variable=self.regions_file,
                          command=lambda smod=smod: self.RFileSelected(smod) )

        smm = self.SegmentationMap()
        if smm == None :
            self.SetCurrentSegmentation(None)
            self.SetMapMenu(None)
            return

        path = os.path.dirname ( smm.data.path ) + os.path.sep
        bname = os.path.splitext ( smm.name ) [0]

        files = os.listdir ( path );
        names_in_path = []
        for f in files :
            if f.find ( bname ) < 0 or f.find('.seg') < 0 : continue
            if f.find ( ".txt" ) >= 0 : continue
            if f.find ( ".mrc" ) >= 0 : continue
            if not f in open_names :
                names_in_path.append ( f )

        if len ( names_in_path ) == 0 : return

        if len(open_names ) > 0 :
            menu.add_separator()

        menu.add_radiobutton ( label="In %s:" % path )
        menu.add_separator()

        for f in names_in_path :
            menu.add_radiobutton (
                label=f, variable=self.regions_file, command=self.RFileSelected )

    def _segmentation_menu_cb(self):

        seg = self.chosen_segmentation
        if seg:
            self.RFileSelected(seg)

    def RFileSelected ( self, rmod = None ) :

        if rmod is None:
            mm = self.SegmentationMap()
            if mm == None :
                debug(self.map_name, "not open");
                return
            path = os.path.dirname(mm.data.path) + os.path.sep
            seg = self.chosen_segmentation
            rfile = seg.name
            debug(" - opening seg file " + rfile + " for map " + mm.name)
            rmod = self.OpenSegFiles ( [(path + rfile, 'Segmentation')] )[-1]
        else:
            rmod.display = True
            if rmod.adj_graph : rmod.adj_graph.show_model(True)
            self.ReportRegionCount(rmod)
                        # hiding all other segmentations can be annoying sometimes
            if 0 :
                for m in regions.segmentations(self.session):
                    if m != rmod:
                        m.display = False
                        if m.adj_graph : m.adj_graph.show_model(False)
            rfile = rmod.name

        self.cur_seg = rmod
        self.SetMapMenu(rmod.volume_data())

        self.status ( "Showing %s - %d regions, %d surfaces" %
               (rfile, len(rmod.regions), len(rmod.region_surfaces)) )


    def CurrentSegmentation ( self, warn = True ):

        if warn and self.cur_seg is None:
            self.status ( "No segmentation chosen" )
        return self.cur_seg

    def SetCurrentSegmentation ( self, smod ):

        self.cur_seg = smod
        self.chose_segmentation = smod
        if smod:
            self.SetMapMenu(smod.volume_data())

    def NewSurfaceResolution( self, event = None ):

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        self.SetSurfaceGranularity(smod)

    def SetSurfaceGranularity ( self, smod ):

        res = self._surface_granularity.value

        if res <= 0:
            return

        smod.change_surface_resolution(res)


    def NewMaxRegions ( self, event = None ):

        self.RegsDispUpdate ()

    def CloseHiddenSeg ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        for m in regions.segmentations (self.session) :
            if not m.display:
                self.status ( "Closed %s" % m.name )
                m.close()



    def SaveRegsToMRC ( self, regs, dmap, path = None ) :

        segs = set([r.segmentation for r in regs])
        for s in segs:
            if tuple(s.grid_size()) != tuple(dmap.data.size):
                msg = ('Cannot mask map.\n\n'
                       'Map %s grid size (%d,%d,%d) does not match '
                       'segmentation %s grid size (%d,%d,%d).'
                       % ((dmap.name,) + tuple(dmap.data.size) +
                          (s.name,) + tuple(s.grid_size())))
                self.session.logger.error(msg)
                return

        if path is None:
            # Show file chooser dialog.
            fprefix = os.path.splitext(dmap.name)[0]
            if len(regs) == 1 :
                fname = fprefix + "_region_%d.mrc" % regs[0].rid
            else :
                fname = fprefix + "_%d_regions.mrc" % len(regs)
            dir = os.path.dirname ( dmap.data.path )
            ipath = os.path.join(dir, fname)
            from Qt.QtWidgets import QFileDialog
            path, type = QFileDialog.getSaveFileName(caption = "Save Masked Map",
                                                     directory = ipath,
                                                     filter = 'MRC map (*.mrc)')
            if not path:
                return

        (li,lj,lk), (hi,hj,hk) = regions.region_bounds(regs)

        bound = 2
        li = li - bound; lj = lj - bound; lk = lk - bound
        hi = hi + bound; hj = hj + bound; hk = hk + bound

        n1 = hi - li + 1
        n2 = hj - lj + 1
        n3 = hk - lk + 1

        debug("Bounds - %d %d %d --> %d %d %d --> %d %d %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3 ))

        self.status ( "Saving %d regions to mrc file..." % len(regs) )

        nmat = numpy.zeros ( (n3,n2,n1), numpy.float32 )
        dmat = dmap.full_matrix()

        #regs_name = ""
        for reg in regs :
            p = reg.points()
            i,j,k = p[:,0],p[:,1],p[:,2]
            nmat[k-lk,j-lj,i-li] = dmat[k,j,i]

        O = dmap.data.origin
        debug("origin:", O)
        nO = ( O[0] + float(li) * dmap.data.step[0],
               O[1] + float(lj) * dmap.data.step[1],
               O[2] + float(lk) * dmap.data.step[2] )

        debug("new origin:", nO)

        name = os.path.basename ( path )
        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, step = dmap.data.step,
                                cell_angles = dmap.data.cell_angles, name = name )
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, dmap.session )


        nv.position = dmap.scene_position

        nv.write_file ( path, "mrc" )

        if [s.volume_data() for s in segs] == [dmap]:
            self.status ( "Wrote %s" % ( nv.name, ) )
        else:
            self.status ( "Masked map %s, wrote %s" % ( dmap.name, nv.name ) )



    def WriteSelRegionsMRCFile ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod == None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions to save to .mrc file" )
            return

        self.SaveRegsToMRC ( regs, dmap )


    def WriteAllRegionsMRCFile ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod == None : return

        regs = [ sp.region for sp in smod.region_surfaces ]

        self.SaveRegsToMRC ( regs, dmap )




    def WriteEachRegionMRCFile ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            regs = smod.regions

        # Choose file path.
        dir = os.path.dirname ( dmap.data.path )
        fprefix = os.path.splitext ( dmap.name ) [0]
        fname = fprefix + "_region_%d.mrc"
        ipath = os.path.join(dir, fname)
        from Qt.QtWidgets import QFileDialog
        path, type = QFileDialog.getSaveFileName(caption = "Save Masked Maps",
                                                 directory = ipath,
                                                 filter = 'MRC map (*.mrc)')
        if not path:
            return
        if not '%d' in path:
            self.status ( "Must include '%d' in map file name for region number" )
            return

        debug("Saving each of %d regions to .mrc files" % len(regs))

        for reg in regs :
            self.SaveRegsToMRC ( [reg], dmap, path % (reg.rid,) )



    def MaskMapWRegions ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        nv = regions.mask_volume(regs, dmap)
        if nv is None:
            self.status ('Map size %d,%d,%d is incompatible with mask size %d,%d,%d'
                  % (tuple(dmap.data.size) + tuple(smod.grid_size())))
            return

        return nv


    def MaskAnotherMapWRegions ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        points = regs[0].points().astype ( numpy.float32 )
        for r in regs[1:] :
            npoints = r.points().astype ( numpy.float32 )
            points = numpy.concatenate ( [points, npoints], axis=0 )

        tf = (dmap.scene_position.inverse() *
              smod.scene_position *
              smod.seg_map.data.ijk_to_xyz_transform)
        tf.transform_points ( points, in_place = True )

        from chimerax.map_data import zone_masked_grid_data
        sg = zone_masked_grid_data ( dmap.data, points, smod.seg_map.data.step[0] )

        from chimerax.map import volume_from_grid_data
        gv = volume_from_grid_data ( sg, dmap.session )
        gv.openState.xform = dmap.openState.xform
        #chimera.openModels.add ( [gv] )
        gv.name = "Masked"


    def ExtractDensities ( self ) :

        from . import extract_region_dialog
        extract_region_dialog.show_extract_region_dialog()


    def FitDialog ( self ) :

        from .fit_dialog import show_fit_segments_dialog
        show_fit_segments_dialog( self.session )

    def GeoSegDialog ( self ) :

        from . import geoseg;
        geoseg.show_dialog();


    def MaskAnotherMapWRegionsShrink ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        points = regs[0].points().astype ( numpy.float32 )
        for r in regs[1:] :
            npoints = r.points().astype ( numpy.float32 )
            points = numpy.concatenate ( [points, npoints], axis=0 )

        tf = (dmap.scene_position.inverse() *
              smod.scene_position *
              smod.seg_map.data.ijk_to_xyz_transform)
        tf.transform_points ( points, in_place = True )

        sg = VolumeData.zone_masked_grid_data ( dmap.data, points, smod.seg_map.data.step[0] )
        regsm = sg.matrix()

        nze = numpy.nonzero ( regsm )

        debug(nze)

        li = numpy.min ( nze[0] )
        lj = numpy.min ( nze[1] )
        lk = numpy.min ( nze[2] )

        hi = numpy.max ( nze[0] )
        hj = numpy.max ( nze[1] )
        hk = numpy.max ( nze[2] )

        bound = 2
        li = li - bound; lj = lj - bound; lk = lk - bound
        hi = hi + bound; hj = hj + bound; hk = hk + bound

        n1 = hi - li + 1
        n2 = hj - lj + 1
        n3 = hk - lk + 1

        debug("Bounds - %d %d %d --> %d %d %d --> %d %d %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3 ))

        self.status ( "Saving %d regions to mrc file..." % len(regs) )

        nmat = numpy.zeros ( (n1,n2,n3), numpy.float32 )
        #dmat = dmap.full_matrix()

        debug("map grid dim: ", numpy.shape ( dmap.full_matrix() ))
        debug("masked grid dim: ", numpy.shape ( regsm ))
        debug("new map grid dim: ", numpy.shape ( nmat ))


        #regs_name = ""
        for ii in range ( len(nze[0]) ) :
            i,j,k = nze[0][ii], nze[1][ii], nze[2][ii]
            #nmat[k-lk,j-lj,i-li] = regsm[k,j,i]
            nmat[i-li,j-lj,k-lk] = regsm[i,j,k]

        O = dmap.data.origin
        debug("origin:", O)
        nO = ( O[0] + float(lk) * dmap.data.step[0],
               O[1] + float(lj) * dmap.data.step[1],
               O[2] + float(li) * dmap.data.step[2] )

        debug("new origin:", nO)

        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, dmap.data.step, dmap.data.cell_angles )
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, dmap.session )

        nv.name = "Masked"

        nv.openState.xform = dmap.openState.xform


    def MaskMapWRegionsCube ( self ) :

        # thsi is useful for input to EMAN fitting procedures which
        # requires a cube map

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        if 0 :
            points = regs[0].points().astype ( numpy.float32 )
            for r in regs[1:] :
                npoints = r.points().astype ( numpy.float32 )
                points = numpy.concatenate ( [points, npoints], axis=0 )

        for rri, reg in enumerate ( regs ) :

            debug(" ---- Region %d/%d ---- " % (rri+1, len(regs)))

            points = reg.points().astype ( numpy.float32 )

            tf = (dmap.scene_position.inverse() *
                  smod.scene_position *
                  smod.seg_map.data.ijk_to_xyz_transform)
            tf.transform_points ( points, in_place = True )

            sg = VolumeData.zone_masked_grid_data ( dmap.data, points, smod.seg_map.data.step[0] )
            regsm = sg.matrix()

            nze = numpy.nonzero ( regsm )

            # print nze

            li = numpy.min ( nze[0] )
            lj = numpy.min ( nze[1] )
            lk = numpy.min ( nze[2] )

            hi = numpy.max ( nze[0] )
            hj = numpy.max ( nze[1] )
            hk = numpy.max ( nze[2] )

            ci = int ( numpy.ceil ( (hi + li) / 2 ) )
            cj = int ( numpy.ceil ( (hj + lj) / 2 ) )
            ck = int ( numpy.ceil ( (hk + lk) / 2 ) )

            n1 = hi - li + 1
            n2 = hj - lj + 1
            n3 = hk - lk + 1

            n = 120 # max ( n1, n2, n3 ) + 4
            n2 = int ( numpy.ceil ( n / 2 ) )

            li = ci - n2; lj = cj - n2; lk = ck - n2
            hi = ci + n2; hj = cj + n2; hk = ck + n2

            debug("Bounds - %d %d %d --> %d %d %d --> %d %d %d (%d)" % ( li, lj, lk, hi, hj, hk, n1, n2, n3, n ))

            self.status ( "Saving %d regions to mrc file..." % len(regs) )

            nmat = numpy.zeros ( (n,n,n), numpy.float32 )
            #dmat = dmap.full_matrix()

            debug("map grid dim: ", numpy.shape ( dmap.full_matrix() ))
            debug("masked grid dim: ", numpy.shape ( regsm ))
            debug("new map grid dim: ", numpy.shape ( nmat ))


            #regs_name = ""
            for ii in range ( len(nze[0]) ) :
                i,j,k = nze[0][ii], nze[1][ii], nze[2][ii]
                mapVal = regsm[i,j,k]
                nmat[i-li,j-lj,k-lk] = mapVal

            O = dmap.data.origin
            debug("origin:", O)
            if 1 :
                nO = ( O[0] + float(lk) * dmap.data.step[0],
                       O[1] + float(lj) * dmap.data.step[1],
                       O[2] + float(li) * dmap.data.step[2] )
                debug("new origin:", nO)
            else :
                nO = ( -float(n2) * dmap.data.step[0],
                       -float(n2) * dmap.data.step[1],
                       -float(n2) * dmap.data.step[2] )
                debug("new origin:", nO)


            from chimerax.map_data import ArrayGridData
            ndata = ArrayGridData ( nmat, nO, dmap.data.step, dmap.data.cell_angles )
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( ndata, dmap.session )

            suff = "_CubeRid%d.mrc" % reg.rid

            import os.path
            nv.name = os.path.splitext (dmap.name) [0] + suff
            nv.openState.xform = dmap.openState.xform

            path = os.path.splitext (dmap.data.path) [0] + suff
            nv.write_file ( path, "mrc" )


    def ExtractMapWRegionsCube ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        if 0 :
            points = regs[0].points().astype ( numpy.float32 )
            for r in regs[1:] :
                npoints = r.points().astype ( numpy.float32 )
                points = numpy.concatenate ( [points, npoints], axis=0 )

        for rri, reg in enumerate ( regs ) :

            (li,lj,lk), (hi,hj,hk) = regions.region_bounds( [reg] )

            ci = int ( numpy.ceil ( (hi + li) / 2 ) )
            cj = int ( numpy.ceil ( (hj + lj) / 2 ) )
            ck = int ( numpy.ceil ( (hk + lk) / 2 ) )

            n1 = hi - li + 1
            n2 = hj - lj + 1
            n3 = hk - lk + 1

            n = 62 # max ( n1, n2, n3 ) + 4
            n2 = int ( numpy.ceil ( n / 2 ) )

            li = ci - n2; lj = cj - n2; lk = ck - n2
            hi = ci + n2; hj = cj + n2; hk = ck + n2

            #bound = 2
            #li = li - bound; lj = lj - bound; lk = lk - bound
            #hi = hi + bound; hj = hj + bound; hk = hk + bound

            debug("Bounds - %d %d %d --> %d %d %d --> %d %d %d, %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3, n ))

            self.status ( "Saving %d regions to mrc file..." % len(regs) )

            #nmat = numpy.zeros ( (n3,n2,n1), numpy.float32 )
            nmat = numpy.zeros ( (n,n,n), numpy.float32 )
            dmat = dmap.full_matrix()

            #regs_name = ""
            for i in range ( li, hi ) :
                for j in range ( lj, hj ) :
                    for k in range ( lk, hk ) :
                        try :
                            nmat[k-lk,j-lj,i-li] = dmat[k,j,i]
                        except :
                            pass

            O = dmap.data.origin
            debug("origin:", O)
            nO = O
            if 1 :
                nO = ( O[0] + float(li) * dmap.data.step[0],
                       O[1] + float(lj) * dmap.data.step[1],
                       O[2] + float(lk) * dmap.data.step[2] )
            else :
                nO = ( -float(n2) * dmap.data.step[0],
                       -float(n2) * dmap.data.step[1],
                       -float(n2) * dmap.data.step[2] )
                debug("new origin:", nO)

            from chimerax.map_data import ArrayGridData
            ndata = ArrayGridData ( nmat, nO, dmap.data.step, dmap.data.cell_angles )
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( ndata, dmap.session )

            suff = "_MC_%d_%d_%d_%d.mrc" % (li, lj, lk, n)

            import os.path
            nv.name = os.path.splitext (dmap.name) [0] + suff
            nv.openState.xform = dmap.openState.xform

            path = os.path.splitext (dmap.data.path) [0] + suff
            nv.write_file ( path, "mrc" )


    def SubtractRegionsFromMap ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map from which density will be taken" ); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Please select one ore more regions" )
            return

        nv = regions.remove_mask_volume(regs, dmap)
        if nv is None:
            self.status ('Map size %d,%d,%d is incompatible with mask size %d,%d,%d'
                  % (tuple(dmap.data.size) + tuple(smod.grid_size())))
            return

        return nv



    def DetectSym ( self ) :

        dmap = segmentation_map()

        if dmap == None:
            self.status ( "Please select a map in the Segment Map dialog" )
            return []

        debug("Symmetry for", dmap.name)

        from Measure.symmetry import find_point_symmetry

        syms, msg = find_point_symmetry ( dmap, nMax=8 )

        if syms is None :
            self.status ( "No symmetry detected for %s" % dmap.name )
            self.symmetryString.set ( "No symmetry detected" )
            return []

        self.status ( msg )
        start = msg.find(': ')+2
        end = msg.find (', center')
        self.symmetryString.set ( msg [start : end] )

        for i, sym in enumerate ( syms ) :
            #print i, " -> ", sym
            pass

        return syms


    def PlaceSym ( self ) :

        dmap = segmentation_map()

        if dmap == None:
            self.status ( "Please select a map..." )
            return

        smod = self.CurrentSegmentation()
        if smod is None :
            self.status ( "Select a segmentation..." )
            return

        regions = smod.selected_regions()
        if len(regions)==0 :
            self.status ( "Select one or more regions..." )
            return

        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return

        if csyms == None :
            self.status ( 'Select "Use symmetry" to use this function...' )
            return

        centers, syms = csyms

        debug("Showing %d symmetric copies..." % len(syms))
        debug("Centers:", centers)

        com = centers[0]
        t_0_com = ( (1.0,0.0,0.0,-com[0]),
                    (0.0,1.0,0.0,-com[1]),
                    (0.0,0.0,1.0,-com[2]) )
        t_to_com = ( (1.0,0.0,0.0,com[0]),
                    (0.0,1.0,0.0,com[1]),
                    (0.0,0.0,1.0,com[2]) )

        ptf = smod.point_transform()
        #print ptf


        surf = _surface.SurfaceModel ()

        for i, reg in enumerate (regions) :

            for si, smat in enumerate ( syms [1 : ] ) :

                tf = Matrix.multiply_matrices( t_to_com, smat, t_0_com )

                points = numpy.array ( reg.points(), numpy.float32 )
                tf.transform_points ( points, in_place = True )
                #print points

                from MultiScale.surface import surface_points
                vertices, triangles, normals = \
                    surface_points ( points,
                                     resolution = smod.surface_resolution,
                                     density_threshold = 0.1,
                                     smoothing_factor = .25,
                                     smoothing_iterations = 5 )

                ptf.transform_points ( vertices, in_place = True )

                nsp = surf.addPiece ( vertices, triangles, reg.color )
                nsp.oslName = "Reg_%d_sym_%d" % (reg.rid, si)




        surf.name = "SymmetryRegionSurfs"
        self.session.models.add ( [surf] )



    def RegsDispUpdate ( self, task = None ) :

        smod = self.CurrentSegmentation()
        if smod is None :
            debug(" - regs disp update - no smod")
            return

        if smod.volume_data() is None:
            debug(" - regs disp update - no smod")
            smod.set_volume_data(self.SegmentationMap())

        maxnr = self.MaximumRegionsToDisplay()

        if maxnr > 0 and len(smod.regions) >= maxnr  :
            self.status('Only showing %d of %d regions.' % (maxnr, len(smod.regions)))

        #vis_mode = self.regsVisMode.get()
        vis_mode = 'Voxel_Surfaces'
        smod.display_regions(vis_mode, maxnr, task)

        if maxnr >= len(smod.regions):
            self.status ( "Showing %d region surfaces" % len(smod.regions) )
        else:
            self.status ( "Showing %d of %d region surfaces" %
                   (maxnr, len(smod.regions)) )

        self.ReportRegionCount(smod)

    def MaximumRegionsToDisplay ( self ) :

        maxnr = self._max_num_regions.value
        return maxnr

    def ReportRegionCount ( self, smod ):

        if smod is None:
            s = ''
        else:
            s = "%s regions" % "{:,}".format( len(smod.regions) )
        self._region_count.setText(s)


    def RegsDispThr ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        debug("%s - thresholding %d regions" % ( smod.name, len(smod.regions) ))

        dmap = self.SegmentationMap()
        if dmap == None : debug("Map %s not open" % self.map_name); return
        debug(" - using map:", dmap.name)
        dthr = dmap.minimum_surface_level

        for r in smod.regions : r.remove_surface()

        maxnr = self.MaximumRegionsToDisplay()
        for reg in smod.regions :

            if maxnr > 0 and len(smod.region_surfaces) >= maxnr  :
                self.status('Only showing %d of %d regions.' %
                     (len(smod.region_surfaces), len(smod.regions)))
                break
            reg.make_surface()


    def RegsPrint ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        for reg in smod.regions :

            debug("%d - %d %d %d" % ( reg.rid, reg.max_point[0], reg.max_point[1], reg.map_point[2] ))


    def ReduceMap ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a map first" ); return
        mm = self.SegmentationMap()
        if mm == None : self.status ( "%s is not open" % self.map_name ); return

        path = os.path.dirname ( mm.data.path ) + os.path.sep
        mname = os.path.splitext ( mm.name )[0]

        d = mm.data
        m2 = d.matrix ( ijk_step=(2,2,2) )
        step2 = ( d.step[0]*2.0, d.step[1]*2.0, d.step[2]*2.0 )
        ld = VolumeData.Array_Grid_Data(m2, d.origin, step2, d.cell_angles, d.rotation,
                           name = mname + '_s2.mrc')

        gv = VolumeViewer.volume.add_data_set ( ld, None )
        gv.name = mname + '_s2.mrc'

        debug("writing", path + gv.name)
        mod.write_file ( path + gv.name, "mrc" )


    def GetUseSymmetry ( self ) :

        csyms = None
        err_msg = None

        #use_sym = self.useSymmetry.get ()
        use_sym = False
        if use_sym :

            sstring = self.symmetryString.get ()
            if len ( sstring ) == 0 :
                self.status ("Detecting symmetry...")
                self.DetectSym ()
                sstring = self.symmetryString.get ()

            if len ( sstring ) == 0 :
                self.status ( "Enter a symmetry string, e.g. D8" )
                return [None, "No symmetry specified or found"]

            debug("Using symmetry:", sstring)

            from Measure.symmetry import centers_and_points

            dmap = segmentation_map()
            centers, xyz, w = centers_and_points(dmap)
            #print "Centers: ", centers
            tcenters = numpy.array(centers, numpy.float32)
            Matrix.transform_points ( tcenters, dmap.data.xyz_to_ijk_transform )
            #print "Centers in ijk coords: ", tcenters

            import Symmetry

            if sstring[0] == "D" :
                debug("Dihedral syms")
                syms = Symmetry.dihedral_symmetry_matrices ( int(sstring[1]) )
                csyms = [tcenters, syms]

            elif sstring[0] == "C" :
                debug("Cyclic syms")
                syms = Symmetry.cyclic_symmetry_matrices ( int(sstring[1]) )
                csyms = [tcenters, syms]

            else :
                err_msg = "Symmetry string not recognized"


        return [ csyms, err_msg ]



    def Segment ( self, show = True, group = True ) :

        smod = self.CurrentSegmentation(warn = False)
        if smod :
            self.session.models.close ( [smod] )

        if self.chosen_map :
            from os.path import splitext
            mname, mext = splitext ( self.chosen_map.name )
            debug(" - current map: %s" % self.chosen_map.name)
            remm = []
            for m in self.session.models.list() :
                if ".seg" in m.name and mname in m.name :
                    debug(" - closing %s" % m.name)
                    remm.append ( m )
            if len(remm) > 0 :
                self.session.models.close ( remm )

        smod = self.SegmentAndGroup(show, group)
        return smod



    def SegmentAndGroup ( self, show = True, group = True, task = None ) :

        if len(self.map_name) == 0 :
            self.status ("Select a density map in the Segment map field" );
            return

        mm = self.SegmentationMap()
        if mm == None : self.status ( "%s is not open" % self.map_name ); return

        thrD = mm.minimum_surface_level
        if thrD is None:
            self.status ("Must show map in surface style, surface threshold level is needed to segment")
            return
                
        debug("\n___________________________")
        self.status ( "Segmenting %s, density threshold %f" % (mm.name, thrD) )

        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return

        smod = self.CurrentSegmentation(warn = False)
        if smod is None or smod.volume_data() != mm:
            mbase, msuf = os.path.splitext ( mm.name )
            msp = msuf.find(' ')
            mend = '' if msp == -1 else msuf[msp:]
            segname = mbase + mend + '.seg'
            smod = regions.Segmentation(segname, mm.session, mm)
            self.session.models.add([smod])
            self.SetSurfaceGranularity(smod)
            self.SetCurrentSegmentation(smod)

        if timing: t0 = clock()
        smod.calculate_watershed_regions ( mm, thrD, csyms, task )

        if timing: t1 = clock()
        self.RemoveSmallRegions(smod, task)
        self.RemoveContactRegions(smod, task)
        nwr = len(smod.regions)

        if timing: t2 = clock()

        if group:
            if self.group_mode == 'smooth' :
                self.SmoothAndGroup ( smod, task )
            else :
                self.GroupByCons ( smod, task )


        # Undisplay other segmentations
        if timing: t3 = clock()
        for m in regions.segmentations(self.session) :
            if m != smod:
                m.display = False

        self.RegsDispUpdate ( task )     # Display region surfaces
#        mm.display = False              # Undisplay map

        if timing :
            t4 = clock()
            debug("Time %.2f sec: watershed %.2f sec, small %.2f, group %.2f sec, display %.2f sec" % (t4-t0, t1-t0, t2-t1, t3-t2, t4-t3))

        self.status ( '%d watershed regions, grouped to %d regions' % ( nwr, len(smod.regions)) )

        return smod



    def RemoveSmallRegions(self, smod = None, task = None):

        if smod is None:
            smod = self.CurrentSegmentation()
            if smod is None:
                return

        minsize = self._min_region_size.value
        if minsize <= 1:
            return

        if task is None:
            smod.remove_small_regions(minsize)
            self.RegsDispUpdate()
        else:
            smod.remove_small_regions(minsize, task)
            self.RegsDispUpdate(task)

        self.ReportRegionCount(smod)


    def RemoveContactRegions(self, smod = None, task = None):

        if smod is None:
            smod = self.CurrentSegmentation()
            if smod is None:
                return

        minsize = self._min_contact_size.value
        if minsize <= 0:
            return

        smod.remove_contact_regions(minsize)
        self.RegsDispUpdate()

        self.ReportRegionCount(smod)



    def GroupConnectedRegs ( self ) :

        if 0 :
            min_contact = int(self.minConnection.get())

            smod = self.CurrentSegmentation()
            if smod == None : return

            regions = smod.selected_regions()
            if len(regions)==0 :
                regions = smod.regions

            smod.group_connected ( regions, min_contact)

            self.RegsDispUpdate()
            self.ReportRegionCount(smod)
            if regions:
                from .regions import TopParentRegions
                smod.select_regions(TopParentRegions(regions))

        else :

            debug(" - connection grouping step")


    def GroupByContacts ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        regions.group_by_contacts(smod)
        self.RegsDispUpdate()

        self.SetColorLevelRange()
        self.ReportRegionCount(smod)

        self.contactsPanel.set(True)

    def CloseAll ( self ) :

        self.status ( "Closing all segmentations." )

        dmap = self.SegmentationMap()
        if dmap != None :
            dmap.display = True

        for m in regions.segmentations (self.session):
            debug('Closed', m.name)
            m.close()

        self.SetCurrentSegmentation ( None )
        self.ReportRegionCount(None)


    def Associate ( self ) :

        seg = self.CurrentSegmentation ()
        if seg :
            debug(" - seg: ", seg.name)

            if self.chosen_map :
                debug(" - map: " + self.chosen_map.name)
                seg.set_volume_data ( self.chosen_map )
                self.status ( "Map %s is now associated with %s" % (self.chosen_map.name, seg.name) )
            else :
                self.status ( "No map selected" )


    def SmoothAndGroup ( self, smod, task = None ) :

        numit = self._num_steps.value
        sdev =  self._step_size.value
        targNRegs = self._target_num_regions.value

        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return


        if targNRegs <= 0 :
            self.status ( "# of regions" )
            return

        smod.smooth_and_group(numit, sdev, targNRegs, csyms, task)

        self.ReportRegionCount(smod)




    def GroupByCons ( self, smod, task = None ) :

        numit = self._num_steps_con.value

        targNRegs = self._target_num_regions_con.value

        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return


        if targNRegs <= 0 :
            self.status ( "Enter an integer > 0 for target # of regions" )
            return

        debug(" - grouping %d steps, target %d" % (numit, targNRegs))

        #smod.smooth_and_group(numit, sdev, targNRegs, csyms, task)
        smod.group_connected_n ( numit, targNRegs, None, csyms, task )



        self.ReportRegionCount(smod)



    def GroupByConsOneStep ( self, task = None  ) :

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        if smod.volume_data() is None:
            self.status ('Segmentation map not opened')
            return

        if len(smod.regions) <= 1:
            self.status ('%s has %d regions' % (smod.name, len(smod.regions)))
            return


        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return

        regions = None
        if  self._group_by_con_only_visible.enabled :
            regions = smod.visible_regions()
            if len(regions) == 0 :
                self.status ("Grouping by connections: no visible regions found or they are from a different model" )
                return

            self.status ("Grouping by connections: applying only to %d regions visible" % len(regions) )


        newRegs, removedRegs = smod.group_connected_n ( 1, 1, regions, csyms )
        #self.RegsDispUpdate ( )        # Display region surfaces

        for r in newRegs : r.make_surface (None, None, smod.regions_scale)
        for r in removedRegs : r.remove_surface()

        self.ReportRegionCount(smod)

        if smod.adj_graph :
            graph.create_graph ( smod, smod.graph_links )

        self.status ( "Got %d regions after grouping by connections" % (len(smod.regions)) )


    def SmoothAndGroupOneStep ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None:
            return

        if smod.volume_data() is None:
            self.status ('Segmentation map not opened')
            return

        if len(smod.regions) <= 1:
            self.status ('%s has %d regions' % (smod.name, len(smod.regions)))
            return

        step = self._step_size.value

        sdev = step + smod.smoothing_level


        self.status ( "Smoothing and grouping, standard deviation %.3g voxels" % sdev)


        csyms, sym_err = self.GetUseSymmetry ()
        if sym_err :
            self.status ( sym_err )
            return


        while 1:
            new_regs = len(smod.smooth_and_group(1, sdev, 1, csyms))

            # if symmetry is being used we should stop after one step
            # since symmetry can block regions from joining indefinitely
            if csyms or new_regs > 0 : break

            self.status ('No new groups smoothing %.3g voxels' % sdev)
            sdev += step
        self.RegsDispUpdate ( )         # Display region surfaces

        self.ReportRegionCount(smod)

        if smod.adj_graph :
            graph.create_graph ( smod, smod.graph_links )

        self.status ( "Got %d regions after smoothing %.3g voxels." %
               (len(smod.regions), sdev) )


    def Overlapping ( self ) :

        dmap = self.SegmentationMap()
        if dmap == None :
            self.status ( "No map selected" )
            return

        smod = self.CurrentSegmentation()
        if smod == None :
            self.status ( "No segmentation selected" )
            return

        if len(smod.regions) == 0 :
            self.status ( "No regions found in %s" % smod.name )
            return

        from chimerax.atomic import selected_atoms
        selatoms = selected_atoms(self.session)
        spoints = None

        if len ( selatoms ) > 0 :
            spoints = selatoms.scene_coords

        else :
            
            from chimerax.map import Volume
            mods = [v for v in self.session.selection.models() if isinstance(v, Volume)]
            if len(mods) == 1 :
                mod = mods[0]
                debug("Using for selection:", mod.name)

                from . import axes
                spoints, weights = axes.map_points ( mod, True )
                debug(" - map - got %d points in contour" % len (spoints))
                mod.scene_position.transform_points( spoints, in_place = True )
            else :
                self.status ("0 or more than 1 volume model selected")
                return


        simap = self.PointIndexesInMap ( spoints, dmap )

        self.status ( "Overlapping %d atoms with %d regions" % (
            len(selatoms), len(smod.regions) ) )

        #ovp = float ( self.overlappingPercentage.get() )
        ovp = 50.0
        ovRatio = ovp / 100.0
        debug(" - overlap ratio: %f" % ovRatio)

        oregs = []
        for ri, r in enumerate ( smod.regions ) :
            ipoints = r.points()
            noverlap = 0
            for i,j,k in ipoints :
                try : simap[i][j][k]
                except: continue
                noverlap += 1
            ov = float ( noverlap ) / float ( len(ipoints) )
            if ov > ovRatio : oregs.append ( r )
            #if noverlap > 0 : oregs.append ( r )
        regions.select_regions ( oregs )

        self.status ( "Selected %d regions" % ( len(oregs) ) )




    def GroupUsingFits ( self ) :

        dmap = self.SegmentationMap()
        if dmap == None : debug("Map %s not open" % self.map_name); return

        smod = self.CurrentSegmentation()
        if smod == None : return

        if len(smod.regions) == 0 : debug("No regions in", smod.name); return
        try : dmap.fitted_mols
        except : dmap.fitted_mols = []
        if len(dmap.fitted_mols) == 0 : debug("No fits found for", dmap.name); return

        debug("Grouping %d regions by overlap to %d fitted structures" % (
            len(smod.regions), len(dmap.fitted_mols) ))

        dmap.chain_maps = []

        for mol in dmap.fitted_mols :
            try : mol.fmap.imap
            except : mol.fmap.imap = self.MapIndexesInMap ( dmap, mol.fmap )
            from random import random as rand
            mol.fmap.surf_color = ( rand(), rand(), rand(), 1 )
            dmap.chain_maps.append ( mol.fmap )

#        self.SegAccuracy ( "_fits_acc", True )



    def RegSurfsShowNone ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        for reg in smod.regions :
            if reg.surface_piece:
                reg.surface_piece.display = False


    def RegSurfsShowAll ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        self.RegsDispUpdate()


    def RegSurfsShowOnlySelected ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        regions.show_only_regions(smod.selected_regions())


    def RegSurfsHide ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        #if len(sregs) == 0 : sregs = smod.all_regions()

        for r in sregs : r.hide_surface()


    def RegSurfsShow ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        #if len(sregs) == 0 : sregs = smod.all_regions()

        for r in sregs : r.show_surface()



    def RegSurfsShowAdjacent ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 :
            return

        cr = set()
        for r in sregs :
            cr.update(r.contacting_regions())

        self.status ( "Region has %d adjacent regions" % len(cr) )
        for r in cr :
            r.show_surface()






    def RegSurfsShowNotGrouped ( self ) :

        debug("Showing not-grouped regions...")

        smod = self.CurrentSegmentation()
        if smod == None : return

        for reg in smod.regions :
            if len(reg.cregs) == 0 :
                if reg.surface_piece:
                    reg.surface_piece.display = True
            else :
                if reg.surface_piece:
                    reg.surface_piece.display = False



    def SelectGrouped ( self ) :

        debug("Selecting grouped regions...")

        smod = self.CurrentSegmentation()
        if smod == None : return

        smod.select_regions([reg for reg in smod.regions if len(reg.cregs) > 0], only = True)


    def SelectNotGrouped ( self ) :

        debug("Showing not-grouped regions...")

        smod = self.CurrentSegmentation()
        if smod == None : return

        smod.select_regions([reg for reg in smod.regions if len(reg.cregs) == 0], only = True)



    def RegSurfsShowGrouped ( self ) :

        debug("Showing grouped regions...")

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.grouped_regions()
        if len(sregs) == 0 :
            self.status ( "No grouped regions" )
            return

        self.status ( "Showing %d grouped regions" % len(sregs) )

        regions.show_only_regions(sregs)



    def RegSurfsTransparent ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 : sregs = smod.all_regions()

        for r in sregs :
            if r.has_surface():
                cr,cg,cb = r.surface_piece.color[:3] #r.color[:3]
                r.surface_piece.color = ( cr, cg, cb, int(255*REG_OPACITY) )
                r.surface_piece.display_style = r.surface_piece.Solid


    def RegSurfsOpaque ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 : sregs = smod.all_regions()

        for r in sregs :
            if r.has_surface():
                cr,cg,cb = r.surface_piece.color[:3] #r.color[:3]
                r.surface_piece.color = ( cr, cg, cb, 255 )
                r.surface_piece.display_style = r.surface_piece.Solid


    def RegSurfsMesh ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 : sregs = smod.all_regions()

        for r in sregs :
            if r.has_surface():
                cr,cg,cb = r.surface_piece.color[:3] #r.color[:3]
                r.surface_piece.color = ( cr, cg, cb, 255 )
                r.surface_piece.display_style = r.surface_piece.Mesh
                #r.surface_piece.lineThickness = 1.0



    def SelectAllRegions ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        smod.select_regions(smod.regions)


    def Invert ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sel_regs = set ( smod.selected_regions() )

        smod.select_regions([r for r in smod.regions if not r in sel_regs], only = True)


    def Group ( self ):


        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs) == 0:

            if self.group_mode == 'smooth' :
                self.SmoothAndGroupOneStep()
            else :
                self.GroupByConsOneStep()

        else:
            self.JoinSelRegs()


    def JoinSelRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "No regions selected" )
            return
        regs = regions.TopParentRegions(regs)

        jreg = smod.join_regions ( regs )
        jreg.make_surface(None, None, smod.regions_scale)

        if smod.adj_graph :
            graph.create_graph ( smod, smod.graph_links )

        smod.select_regions([jreg], only = True)

        self.ReportRegionCount(smod)
        self.status ( "Grouped %d regions" % len(regs) )




    def DelSelRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None :
            self.status ( "No segmentation selected..." )
            return

        regs = smod.selected_regions()
        if len(regs)==0 :
            self.status ( "Select one or more regions to delete" )
            return

        smod.remove_regions ( regs, update_surfaces = True, remove_children = True )

        self.ReportRegionCount(smod)
        self.status ( "Deleted %d regions" % len(regs) )


    def DelExcSelRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None :
            self.status ( "No segmentation selected..." )
            return

        sel_regs = smod.selected_regions()
        if len(sel_regs)==0 :
            self.status ( "No regions selected..." )
            return

        dregs = [r for r in smod.regions
                 if not r in sel_regs]

        smod.remove_regions ( dregs, update_surfaces = True, remove_children = True )

        self.ReportRegionCount(smod)
        self.status ( "Deleted %d regions" % len(dregs) )


    def Ungroup ( self ):

        smod = self.CurrentSegmentation()
        if smod and smod.selected_regions():
            self.UngroupSelRegs()
        else:
            self.UngroupLastSmoothing()


    def SafeCreateSurfsForRegs ( self, smod, rlist, rregs ) :

        maxnr = self.MaximumRegionsToDisplay()

        nsurfs = 0
        for r in smod.regions :
            if r.has_surface() :
                nsurfs += 1

        debug(" - %d surfs have pieces before" % nsurfs)

        # surfs that will go away...
        for r in rregs :
            if r.has_surface() :
                nsurfs -= 1

        debug(" - %d surfs will have pieces after removing selected" % nsurfs)


        if nsurfs >= maxnr :
            self.status('Ungrouped to %d regions, but did not show their surfaces, see Options' % len(rlist) )

        else :
            canshow = maxnr - nsurfs

            if canshow < len(rlist) :
                self.status('Ungrouped to %d regions, but did not show all surfaces, see Options' % len(rlist) )
            else :
                self.status('Ungrouped to %d regions' % len(rlist) )

            for ri, reg in enumerate ( rlist ) :
                if ri >= canshow :
                    break
                reg.make_surface(None, None, smod.regions_scale)



    def ShowNumSubRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 :
            self.status ( "No regions selected" )
            return
        sregs = regions.TopParentRegions(sregs)

        num = 0
        for r in sregs :
            if len(r.cregs) == 0 :
                pass
            else :
                num += len(r.cregs)

        self.status ( "selected regions have %d total sub regions" % num )



    def UngroupSelRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 :
            self.status ( "No regions selected" )
            return
        sregs = regions.TopParentRegions(sregs)

        smod.clear_selected_regions()

        [rlist, removedRegs] = smod.ungroup_regions ( sregs )
        self.SafeCreateSurfsForRegs ( smod, rlist, removedRegs )
        for r in removedRegs : r.remove_surface()

        debug(" - now %d regions" % len(smod.regions))

        if smod.adj_graph :
            graph.create_graph ( smod, smod.graph_links )

        smod.select_regions ( rlist )

        self.ReportRegionCount(smod)



    def UngroupAllRegs ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        rlist = list(smod.regions)
        [rlist2, removedRegs] = smod.ungroup_regions(rlist)

        self.SafeCreateSurfsForRegs ( smod, rlist2, removedRegs )
        for r in removedRegs : r.remove_surface()

        self.ReportRegionCount(smod)



    def UngroupLastSmoothing ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        levels = [r.smoothing_level for r in smod.regions]
        if len(levels) == 0:
            return
        slev = max(levels)

        rlev = [r for r in smod.regions if r.smoothing_level == slev]
        rlist2 = []
        removedRegs = []

        [rlist2, removedRegs] = smod.ungroup_regions(rlev)

        self.SafeCreateSurfsForRegs ( smod, rlist2, removedRegs )
        for r in removedRegs : r.remove_surface()

        levels = [r.smoothing_level for r in smod.regions]
        smod.smoothing_level = max(levels)

        if smod.adj_graph :
            graph.create_graph ( smod, smod.graph_links )

        #self.status ( "Ungrouped to %.3g voxel smoothing, %d regions" % (smod.smoothing_level, len(smod.regions)) )
        self.ReportRegionCount(smod)


    def CloseRegions ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        self.session.models.close ( [smod] )
        self.SetCurrentSegmentation(None)
        self.ReportRegionCount(None)

        if smod.adj_graph : smod.adj_graph.close()


    def CloseSeg ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        smod.close()
        self.SetCurrentSegmentation(None)



    def RegionsVolume ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        debug("%d selected regions" % len(sregs))

        if len(sregs) == 0 :
            sregs = smod.regions

        if len(sregs) == 0 :
            self.status ( "No regions found in %s" % smod.name )
            return

        tvol = sum([reg.enclosed_volume() for reg in sregs])
        pcount = sum([reg.point_count() for reg in sregs])

        rw = "region"
        if len(sregs) > 1 : rw = "regions"
        self.status ( "Volume of %d %s: %.3g Angstroms^3, %d points" % ( len(sregs), rw, tvol, pcount ) )

    def RegionMeanAndSD ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs) == 0 :
            self.status ( "No regions selected in %s" % smod.name )
            return

        v = self.SegmentationMap()
        if v is None:
            v = smod.volume_data()
            if v is None:
                self.status ( 'No map specified' )
                return

        means, sdevs = regions.mean_and_sd(sregs, v)
        for r, m, sd in zip(sregs, means, sdevs):
            self.status ( 'Region %d mean %.5g, SD %.5g' % (r.rid, m, sd) )


    def Graph ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.create_graph(smod,"uniform")

    def GraphAvgD ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.create_graph(smod,"avgd")

    def GraphMaxD ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.create_graph(smod,"maxd")

    def GraphN ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.create_graph(smod,"N")


    def LoadGraph ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None:
            graph.open_skeleton(smod)

    def SaveGraph ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.read_graph(smod)

    def CloseGraph ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            graph.close(smod)
            smod.display = True

    def GroupBySkeleton ( self ) :

        smod = self.CurrentSegmentation()
        if smod:
            skeleton.group_by_skeleton(smod)
            smod.display = True
            smod.display_regions()
            self.ReportRegionCount(smod)

    def RemoveGraphLinks ( self ) :

        graph.remove_graph_links()


    def ShowRegionsAxes ( self, regs ) :

        smod = self.CurrentSegmentation()
        if smod is None: return

        for r in regs :

            sp = r.surface_piece
            try :
                sp.axes.display = True
                self.session.models.close ( [sp.axes] )
            except :
                pass

            tpoints = r.map_points()
            sp.COM, sp.U, sp.S, sp.V = prAxes ( tpoints )

            com = numpy.sum(tpoints, axis=0) / len(tpoints)
            comv = numpy.ones_like ( tpoints ) * com
            points = tpoints - comv

            ppoints = points * sp.U
            sp.Extents = numpy.asarray ( numpy.max ( numpy.abs ( ppoints ), 0 ) )[0]

            sp.Extents[0] += 5.0
            sp.Extents[1] += 5.0
            sp.Extents[2] += 5.0

            from . import axes

            if 0 :
            # for ribosome direction
                sp.Extents[1] = sp.Extents[1] * float(self.axesFactor.get())

                sp.axes = axes.AxesMod ( self.session, sp.COM, sp.U, sp.Extents, 6, 1.0, alignTo = sp )
            else :
                sp.axes = axes.AxesMod ( self.session, sp.COM, sp.U, sp.Extents, 1.0, 1.1, alignTo = sp )

            sp.axes.name = "region_%d_axes" % r.rid



    def ShowRegionAxesSelected ( self ) :

        smod = self.CurrentSegmentation()
        if smod == None : return

        sregs = smod.selected_regions()
        if len(sregs)==0 : debug("no selected regions found"); return

        self.ShowRegionsAxes ( sregs )


    def HideRegionAxes ( self ) :

        debug("hiding axes")
        mclose = []
        for m in self.session.models:
            t = m.name.split ("_")
            if t[0] == "region" and t[2] == "axes" :
                debug("- removing", m.name)
                mclose.append(m)
                
        self.session.models.close( mclose )




    def PointIndexesInMap ( self, points, ref_map ) :

        debug("Making map indices for %d points in %s" % ( len(points), ref_map.name ))

        tf = ref_map.data.xyz_to_ijk_transform * ref_map.scene_position.inverse()
        tf.transform_points ( points, in_place = True )

        imap = {}
        for fi, fj, fk in points :
            if 0 :
                i, j, k = int(numpy.round(fi)), int(numpy.round(fj)), int(numpy.round(fk))
                try : mi = imap[i]
                except : mi = {}; imap[i] = mi
                try : mij = mi[j]
                except : mij = {}; mi[j] = mij
                mij[k] = 1
                continue
            for i in [ int(numpy.floor(fi)), int(numpy.ceil(fi)) ] :
                for j in [ int(numpy.floor(fj)), int(numpy.ceil(fj)) ] :
                    for k in [ int(numpy.floor(fk)), int(numpy.ceil(fk)) ] :
                        try : mi = imap[i]
                        except : mi = {}; imap[i] = mi
                        try : mij = mi[j]
                        except : mij = {}; mi[j] = mij
                        mij[k] = 1


        return imap #, C, bRad


    def MapIndexesInMap ( self, ref_map, mask_map ) :

        thr = mask_map.minimum_surface_level
        mm = mask_map.data.matrix()
        mm = numpy.where ( mm > thr, mm, numpy.zeros_like(mm) )

        nze = numpy.nonzero ( mm )
        nzs = numpy.array ( [nze[2], nze[1], nze[0]] )

        # the copy is needed! otherwise the _contour.afine_transform does not work for some reason
        points =  numpy.transpose ( nzs ).astype(numpy.float32)

        #points = numpy.zeros ( ( len(nze[0]), 3 ), numpy.float32 )
        #for ei, i in enumerate ( nze[0] ) :
        #    j = nze[1][ei]
        #    k = nze[2][ei]
        #    points[ei][0], points[ei][1], points[ei][2] = float (k), float(j), float(i)

        #print points[0]

        debug("Making map indices for %s in %s" % ( mask_map.name, ref_map.name ))
        debug(" - %d points above %.3f" % ( len(points), thr ))

        # transform to index reference frame of ref_map
        f1 = mask_map.data.ijk_to_xyz_transform
        f2 = mask_map.scene_position
        f3 = ref_map.scene_position.inverse()
        f4 = ref_map.data.xyz_to_ijk_transform

        tf = f4 * f3 * f2 * f1
        tf.transform_points ( points, in_place = True )

        #_contour.affine_transform_vertices ( points, f1 )
        #_contour.affine_transform_vertices ( points, f2 )
        #_contour.affine_transform_vertices ( points, f3 )

        #print points[0]

        #com = numpy.sum (points, axis=0) / len(points)
        #C = chimera.Vector ( com[0], com[1], com[2] )
        #comv = numpy.ones_like ( points ) * com
        #points_v = points - comv
        #bRad = numpy.sqrt ( numpy.max ( numpy.sum ( numpy.square (points_v), 1 ) ) )

        # transform points to indexes in reference map
        # _contour.affine_transform_vertices ( points, ref_map.data.xyz_to_ijk_transform )

        imap = {}
        for fk, fj, fi in points :

            for i in [ int(numpy.floor(fi)), int(numpy.ceil(fi)) ] :
                for j in [ int(numpy.floor(fj)), int(numpy.ceil(fj)) ] :
                    for k in [ int(numpy.floor(fk)), int(numpy.ceil(fk)) ] :

                        try : mi = imap[i]
                        except : mi = {}; imap[i] = mi
                        try : mij = mi[j]
                        except : mij = {}; mi[j] = mij
                        mij[k] = 1


        return imap #, C, bRad


    def ShowGroupSurfaces ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        sregs = smod.selected_regions()
        regs = set([r.top_parent() for r in sregs])
        if len(regs)==0 :
            regs = smod.regions

        for r in regs:
            for c in r.all_children():
                c.remove_surface()
            r.make_surface()

        if sregs:
            surfs = [r.surface() for r in regs if r.has_surface()]
            for s in surfs:
                s.highlighted = True


    def ShowUngroupedSurfaces ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        sregs = smod.selected_regions()
        regs = set([r.top_parent() for r in sregs])
        if len(regs)==0 :
            regs = smod.regions

        for i, r in enumerate(regs):
            if r.has_children():
                r.remove_surface()
                for c in r.childless_regions():
                    c.make_surface()
            else:
                r.make_surface()

        if sregs:
            from .regions import all_regions
            surfs = [r.surface() for r in all_regions(regs) if r.has_surface()]
            for s in surfs:
                s.highlighted = True


    def SelectGroups ( self ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        rlist = [r for r in smod.regions if r.has_children()]
        from .regions import all_regions
        surfs = [r.surface() for r in all_regions(rlist) if r.has_surface()]
        for s in surfs:
            s.highlighted = True


    # Regions that have voxels on the mask boundary.
    def SelectBoundaryRegions ( self, pad = 3 ) :

        smod = self.CurrentSegmentation()
        if smod is None : return

        m = smod.mask
        if m is None:
            return

        from chimerax.segment import region_bounds
        b = region_bounds(m)

        rset = set()
        kmax, jmax, imax = [(s-1)-pad for s in m.shape]
        for r in smod.childless_regions():
            i = r.rid
            if (i < len(b) and b[i,6] > 0 and
                (b[i,0] <= pad or b[i,1] <= pad or b[i,2] <= pad or
                 b[i,3] >= kmax or b[i,4] >= jmax or b[i,5] >= imax)):
                rset.add(r.top_parent())
        from .regions import all_regions, select_regions
        select_regions(all_regions(rset))


    def SelectNonPlacedRegions ( self ) :

        if len(self.map_name) == 0 : self.status ("Please select a density map"); return
        dmap = self.SegmentationMap()
        if dmap == None : self.status ( "%s is not open" % self.map_name ); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        rlist = []
        for sp in smod.region_surfaces :
            try :
                sp.region.placed
            except :
                rlist.append(sp.region)
        smod.select_regions(rlist, only = True)

        debug("%d non-placed regions" % len(rlist))


    def mouse_group_cb(self):

        gmm = self.group_mouse_mode
        if self.mouse_group.get():
            if gmm is None:
                from . import mousemode
                gmm = mousemode.Group_Connected_Mouse_Mode()
                self.group_mouse_mode = gmm
            button, modifiers = self.mouse_button_spec()
            gmm.bind_mouse_button(button, modifiers)
        elif gmm:
            gmm.unbind_mouse_button()

    def mouse_group_button_cb(self):

        if self.mouse_group.get() and self.group_mouse_mode:
            button, modifiers = self.mouse_button_spec()
            self.group_mouse_mode.bind_mouse_button(button, modifiers)

    def mouse_button_spec(self):

        name = self.mouse_group_button.variable.get()
        name_to_bspec = {'button 1':('1', []), 'ctrl button 1':('1', ['Ctrl']),
                         'button 2':('2', []), 'ctrl button 2':('2', ['Ctrl']),
                         'button 3':('3', []), 'ctrl button 3':('3', ['Ctrl'])}
        bspec = name_to_bspec[name]
        return bspec


    # State save/restore in ChimeraX
    _save_attrs = ['_map_menu', '_segmentation_menu',
                   '_max_num_regions', '_surface_granularity',
                   '_min_region_size', '_min_contact_size',
                   '_group_smooth', '_num_steps', '_step_size', '_target_num_regions',
                   '_group_con', '_num_steps_con', '_target_num_regions_con', '_group_by_con_only_visible']
  
    def take_snapshot(self, session, flags):
        data = { 'version': 1 }
        for attr in VolumeSegmentationDialog._save_attrs:
            try:
                data[attr] = getattr(self, attr).value
            except Exception:
                msg = 'Did not save Segment Map setting "%s" in session because it has an invalid value.' % attr
                session.logger.warning(msg)
        return data

    @staticmethod
    def restore_snapshot(session, data):
        d = VolumeSegmentationDialog.get_singleton(session)
        for attr in VolumeSegmentationDialog._save_attrs:
            if attr in data:
                getattr(d, attr).value = data[attr]
        return d
    

def volume_segmentation_dialog ( session, create=False ) :

    return VolumeSegmentationDialog.get_singleton(session, create=create)


def current_segmentation( session, warn = True ):

    d = volume_segmentation_dialog( session )
    if d:
        return d.CurrentSegmentation(warn)
    elif warn:
        d.status ( "No segmentation opened" )
    return None

def segmentation_map( session ):

    d = volume_segmentation_dialog( session )
    if d:
        return d.SegmentationMap()
    return None
