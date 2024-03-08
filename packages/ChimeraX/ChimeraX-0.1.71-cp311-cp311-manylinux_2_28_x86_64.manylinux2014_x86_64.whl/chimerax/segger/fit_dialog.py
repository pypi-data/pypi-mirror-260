
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

from time import time as clock
from random import random as rand

from .axes import prAxes
from .regions import mask_volume, regions_radius

from . import dev_menus, timing, seggerVersion

from .segment_dialog import debug

SAF_DVOL = 0.75
SAF_DBRAD = 0.3
SAF_LS_DEPTH = 4
SAF_LS_NGROUPS = 1000

REG_OPACITY = 0.45
MAX_NUM_GROUPS = 1000


from .fit_devel import Fit_Devel

from chimerax.core.tools import ToolInstance
class FitSegmentsDialog ( ToolInstance, Fit_Devel ):

    help = 'help:user/tools/fitsegments.html'
    SESSION_SAVE = True

    def __init__(self, session, tool_name):

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

        # Fit pull-down menus
        mbar = self._create_menubar(parent)
        layout.addWidget(mbar)
        
        # Fit model menu
        mf = self._create_fit_model_menu(parent)
        layout.addWidget(mf)

        # Fit list
        fl = self._create_fit_list(parent)
        layout.addWidget(fl)
        
        # Options panel
        options = self._create_options_gui(parent)
        layout.addWidget(options)

        # Fit, Help buttons
        bf = self._create_action_buttons(parent)
        layout.addWidget(bf)

        # Status line
        self._status_label = sl = QLabel(parent)
        layout.addWidget(sl)
        
        tw.manage(placement="side")

#        session.triggers.add_handler('remove models', self.model_closed_cb)

        from Qt.QtCore import QTimer
        QTimer.singleShot(1000, self._help_line)
    
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

        fit_menu_entries = [
            ('Delete selected fits from list', self.delete_fit_cb),
            ('Delete ALL fits from list', self.delete_all_fit_cb),

            ('separator', None),
            ('Place molecule copies', self.place_copies_cb),
            ('Place map copies', self.place_map_copies_cb),
            #('Cube map', self.extractCubeMap),
            ('Close placed copies', self.close_copies_cb),

            ('separator', None),
            ("Save chosen fit molecules", self.SaveStrucFit),

            ('separator', None),
            ('Copy fit map on segmented map grid', self.copy_fit_map),

            ('separator', None),
            ('Group regions by visible (Molecule) models', self.GroupRegionsByMols),
            ('Group regions by chains in visible (Molecule) models', self.GroupRegionsByChains),

            ('separator', None),
            ("Show molecule axes", self.StrucShowAxes),
            ("Hide molecule axes", self.StrucHideAxes),
            ("Show overlapping regions", self.ShowOverlappingRegions),

            ('separator', None),
            ("Export fit scores", self.ExportFitScores),
            ("Plot fit scores", self.PlotFitScores),
            ("Inter-molecule clash scores", self.VisiScores )
            ]

        fb = QPushButton('Fit', mbar)
        button_style = 'QPushButton { border: none; } QPushButton::menu-indicator { image: none; }'
        fb.setStyleSheet(button_style)
        layout.addWidget(fb)
        fmenu = QMenu(fb)
        fb.setMenu(fmenu)
        for text, func in fit_menu_entries:
            if text == 'separator':
                fmenu.addSeparator()
            else:
                fmenu.addAction(text, func)

        layout.addStretch(1)
                
        return mbar
    
    def _create_fit_model_menu(self, parent):
        from Qt.QtWidgets import QFrame, QHBoxLayout, QLabel
        
        mf = QFrame(parent)
        mlayout = QHBoxLayout(mf)
        mlayout.setContentsMargins(0,0,0,0)
        mlayout.setSpacing(10)
        
        sm = QLabel('Structure or map to fit', mf)
        mlayout.addWidget(sm)
        from chimerax.ui.widgets import ModelMenuButton
        from chimerax.map import Volume
        from chimerax.atomic import Structure
        self._fit_model_menu = mm = ModelMenuButton(self.session, class_filter = (Volume, Structure))
        slist = self.session.models.list(type = Structure)
        mlist = self.session.models.list(type = Volume)
        if slist or mlist:
            mm.value = slist[0] if slist else mlist[0]
        # mm.value_changed.connect(self._map_chosen_cb)
        mlayout.addWidget(mm)
        mlayout.addStretch(1)    # Extra space at end

        return mf
    
    def _create_options_gui(self, parent):

        from chimerax.ui.widgets import CollapsiblePanel
        p = CollapsiblePanel(parent, 'Options')
        f = p.content_area

        from chimerax.ui.widgets import EntriesRow, radio_buttons

        ler = EntriesRow(f, False, 'Treat all sub-models as one structure')
        self._lump_subids = ler.values[0]

        smer = EntriesRow(f, 'Density map resolution:', 4, 'grid spacing:', 2, ('Calculate Map', self.GenStrucMap))
        self._sim_res, self._sim_grid_sp = smer.values

        wer = EntriesRow(f, 'Which regions to use for fitting:\n',
                         '    ', True, 'Combined selected regions\n',
                         '    ', False, 'Each selected region\n',
                         '    ', False, 'Groups of regions inculding selected region(s)\n',
                         '    ', False, 'Groups of regions including all regions')
        radio_buttons(*tuple(wer.values))
        self._combined_selected_regions, self._each_selected_region, self._around_selected, self._all_groups = wer.values
        
        amer = EntriesRow(f, 'Alignment method:\n',
                          '    ', True, "Align principal axes (faster - only 4 fits will be tried)\n",
                          '    ', False, "Rotational search (try", 100, 'evenly rotated fits)')
        self._prin_axes_search, self._rota_search, self._rota_search_num =  amer.values
        radio_buttons(self._prin_axes_search, self._rota_search)

        mmer = EntriesRow(f, False, 'Mask map with region(s) to prevent large drifts')
        self._mask_map_when_fitting = mmer.values[0]

        ler = EntriesRow(f, False, 'Use Laplacian filter')
        self._use_laplace = ler.values[0]

        ofer = EntriesRow(f, True, 'Optimize fits')
        self._optimize_fits = ofer.values[0]
        
        cver = EntriesRow(f, True, 'Cluster fits that are <', 5.0, 'Angstroms and <', 3.0, 'degrees apart')
        self._do_cluster_fits, self._position_tol, self._angle_tol = cver.values

        nfer = EntriesRow(f, 'Add top', 1, 'fit(s) to list (empty to add all fits to list)')
        self._num_fits_to_add = nfer.values[0]

        cler = EntriesRow(f, False, 'Clashes with copies from symmetry:', '',
                          ('Detect', self.DetectSym), ('Show', self.PlaceSym))
        self._calc_symmetry_clashes, self._symmetry = cler.values
        
        return p

    def _create_fit_list(self, parent):
        
        self.list_fits = []	# List of Fit instances

        from Qt.QtWidgets import QFrame, QVBoxLayout, QLabel, QListWidget

        f = QFrame(parent)
        layout = QVBoxLayout(f)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Use a fixed width font so columns line up.
        from Qt.QtGui import QFontDatabase
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        h = ('%8s %8s %8s %8s %8s %15s %15s %10s'
             % ('Corr', 'Atoms', 'Backbone', 'Clash', 'Occupied', 'Molecule', 'Map', 'Region'))
        ll = QLabel(h, f)
        ll.setFont(font)
        layout.addWidget(ll)
        class FitList(QListWidget):
            def keyPressEvent(self, event):
                from Qt.QtCore import Qt
                if event.key() == Qt.Key_Delete:
                    self.delete_fit()
                else:
                    QListWidget.keyPressEvent(self, event)
        self._fit_listbox = lb = FitList(f)
        lb.setFont(font)
        lb.setSelectionMode(lb.ExtendedSelection)
        lb.delete_fit = self.delete_fit_cb
        lb.itemSelectionChanged.connect(self.fit_selection_cb)
        layout.addWidget(lb)

        return f

    def _create_action_buttons(self, parent):
        from Qt.QtWidgets import QFrame, QHBoxLayout, QPushButton
        bf = QFrame(parent)
        blayout = QHBoxLayout(bf)
        blayout.setContentsMargins(0,0,0,0)
        blayout.setSpacing(10)

        sb = QPushButton('Fit', bf)
        sb.clicked.connect(self._fit)
        blayout.addWidget(sb)
        
        hb = QPushButton('Help', bf)
        hb.clicked.connect(self._help)
        blayout.addWidget(hb)

        blayout.addStretch(1)    # Extra space at end

        return bf
        
    def _fit(self):
        self.Fit()

    def _help(self):
        from chimerax.help_viewer import show_url
        show_url(self.session, self.help)

    def _help_line(self):
        self.status('<font color=blue>To cite Segger or learn more about it press the Help button</font>', log = False)

    @classmethod
    def get_singleton(self, session, create=True):
        from chimerax.core import tools
        d = tools.get_singleton(session, FitSegmentsDialog, 'Fit to Segments', create=create)
        return d

    def status(self, message, log = True):
        self._status_label.setText(message)
        if log:
            self.session.logger.info(message)

    def fillInUI(self, parent):

        import tkinter
        from CGLtk import Hybrid

        tw = parent.winfo_toplevel()
        self.toplevel_widget = tw
        tw.withdraw()

        parent.columnconfigure(0, weight = 1)

        row = 1

        menubar = tkinter.Menu(parent, type = 'menubar', tearoff = False)
        tw.config(menu = menubar)

        self.UseAllMods = tkinter.IntVar()
        self.UseAllMods.set ( 0 )

        fit_menu_entries = [
            ('Delete selected fits from list', self.delete_fit_cb),
            ('Delete ALL fits from list', self.delete_all_fit_cb),
            'separator',
            ('Place molecule copies', self.place_copies_cb),
            ('Place map copies', self.place_map_copies_cb),
            #('Cube map', self.extractCubeMap),
            ('Close placed copies', self.close_copies_cb),

            'separator',
            ("Save chosen fit molecules", self.SaveStrucFit),

            'separator',
            ('Place selected map relative to segmented map', self.save_map_resample),

            'separator']

        if dev_menus :
            fit_menu_entries = fit_menu_entries + [
                ('Group regions by SS in visible (Molecule) models', self.GroupRegionsBySS),
                ('Mask map with selection', self.MaskWithSel)
            ]

        fit_menu_entries = fit_menu_entries + [
            ('Group regions by visible (Molecule) models', self.GroupRegionsByMols),
            ('Group regions by chains in visible (Molecule) models', self.GroupRegionsByChains),

            'separator',
            ("Show molecule axes", self.StrucShowAxes),
            ("Hide molecule axes", self.StrucHideAxes),
            ("Show overlapping regions", self.ShowOverlappingRegions),

            'separator',
            ("Export fit scores", self.ExportFitScores),
            ("Plot fit scores", self.PlotFitScores),
            ( "Score Visible", self.VisiScores )
            ]

        if dev_menus :
            fit_menu_entries = fit_menu_entries + [
                'separator',
                ('Difference map', self.DifferenceMap),
                ('Intersection map', self.IntersectionMap),
                ('Shape match', self.ShapeMatch),

                'separator',
                ('Fit all visible maps to selected', self.FitAllVisMaps),
                ('Make average map of visible fitted maps', self.AvgFMaps2),
                ('Make difference map of visible fitted maps', self.DifFMaps2),
                ('Take fitted map densities into segmented map', self.TakeFMap_with_DMap0),
                ('Take fitted map densities into segmented map + noise', self.TakeFMap_with_DMapN),
                ('Take fitted map densities into segmented map (Shrink/grow)', self.TakeFMap_with_DMap),
                ('Save visible fitted maps in segmented map grid', self.TakeFMapsVis),
                ('Take segmented map densities into fitted map', self.TakeDMap_with_FMap),
                'separator',
                ('Group regions by chains in visible molecules', self.GroupRegionsByChains),
                ('Group regions by visible molecules', self.GroupRegionsByMols),
                ('Group regions by selected fitted molecules', self.GroupRegionsByFittedMols),
                ('Group regions by visible maps', self.GroupRegionsByVisiMaps),
                'separator',
                #('0 map with selection', self.ZeroMapBySel),
                #('0 map with visible molecules', self.ZeroMapByMols),
                ('0 map with selected fitted molecules', self.ZeroMapFittedMols),
                ('Values in map', self.ValuesInMap),
                ('Mask with selected map/model', self.MaskMapWithSel)
                 ]


        fmenu = Hybrid.cascade_menu(menubar, 'Fit', fit_menu_entries)
        #self.add_devel_menus(fmenu)

        from chimera.tkgui import aquaMenuBar
        aquaMenuBar(menubar, parent, row = 0, columnspan=3)


        f = tkinter.Frame(parent)
        f.grid(column=0, row=row, sticky='ew')
        row += 1

        l = tkinter.Label(f, text='Structure or Map to fit')
        l.grid(column=0, row=0, sticky='w')

        self.struc = tkinter.StringVar(parent)
        self.strucMB  = tkinter.Menubutton ( f, textvariable=self.struc, relief=tkinter.RAISED )
        self.strucMB.grid (column=1, row=0, sticky='we', padx=5)
        self.strucMB.menu  =  tkinter.Menu ( self.strucMB, tearoff=0, postcommand=self.StrucMenu )
        self.strucMB["menu"]  =  self.strucMB.menu


        h = '%10s %10s %10s %10s %10s %20s %20s %20s' % ('Corr.', 'At. Incl.', 'BB Incl.', 'Clashes', 'Dens. Occ.', 'Molecule', 'Map', 'Region')
        fl = Hybrid.Scrollable_List(parent, h, 8, self.fit_selection_cb)
        self.fit_listbox = fl.listbox
        self.list_fits = []
        fl.frame.grid(row = row, column = 0, sticky = 'news')
        parent.rowconfigure(row, weight = 1)
        row += 1
        self.fit_listbox.bind('<KeyPress-Delete>', self.delete_fit_cb)


        op = Hybrid.Popup_Panel(parent)
        opf = op.frame
        opf.grid(row = row, column = 0, sticky = 'news')
        opf.grid_remove()
        opf.columnconfigure(0, weight=1)
        self.optionsPanel = op.panel_shown_variable
        row += 1
        orow = 0

        cb = op.make_close_button(opf)
        cb.grid(row = orow, column = 0, sticky = 'e')

        l = tkinter.Label(opf, text='Fitting Options', font = 'TkCaptionFont')
        l.grid(column=0, row=orow, sticky='w', pady=5)
        orow += 1

        fopt = tkinter.Frame(opf)
        fopt.grid(column=0, row=orow, sticky='ew', padx=10)
        orow += 1
        forow = 0


        oft = Hybrid.Checkbutton(fopt, 'Treat all sub-models as one structure', False)
        oft.button.grid(row = forow, column = 0, sticky = 'w')
        self.lump_subids = oft.variable

        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        l = tkinter.Label(f, text='Density map resolution:')
        l.grid(column=0, row=0, sticky='w')

        self.simRes = tkinter.StringVar(fopt)
        e = tkinter.Entry(f, width=4, textvariable=self.simRes)
        e.grid(column=1, row=0, sticky='w', padx=5)

        l = tkinter.Label(f, text='grid spacing:')
        l.grid(column=2, row=0, sticky='w')

        self.simGridSp = tkinter.StringVar(fopt)
        e = tkinter.Entry(f, width=4, textvariable=self.simGridSp)
        e.grid(column=3, row=0, sticky='w', padx=5)

        b = tkinter.Button(f, text="Calculate Map", command=self.GenStrucMap)
        b.grid (column=4, row=0, sticky='w', padx=5)


        forow += 1

        l = tkinter.Label(fopt, text='Which regions to use for fitting:')
        l.grid(column=0, row=forow, sticky='w')

        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        self.alignTo = tkinter.StringVar()
        self.alignTo.set ( 'combined_selected_regions' )

        l = tkinter.Label(f, text=' ', width=5)
        l.grid(column=0, row=0, sticky='w')

        c = tkinter.Radiobutton(f, text="Combined selected regions", variable=self.alignTo, value = 'combined_selected_regions')
        c.grid (column=1, row=0, sticky='w')

        c = tkinter.Radiobutton(f, text="Each selected region", variable=self.alignTo, value = 'each_selected_region')
        c.grid (column=1, row=1, sticky='w')

        c = tkinter.Radiobutton(f, text="Groups of regions including selected region(s)", variable=self.alignTo, value = 'around_selected')
        c.grid (column=1, row=2, sticky='w')

        c = tkinter.Radiobutton(f, text="Groups of regions including all regions", variable=self.alignTo, value = 'all_groups')
        c.grid (column=1, row=3, sticky='w')

        forow += 1

        l = tkinter.Label(fopt, text='Alignment method:')
        l.grid(column=0, row=forow, sticky='w')

        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        self.rotaSearch = tkinter.IntVar()
        self.rotaSearch.set ( 0 )

        l = tkinter.Label(f, text=' ', width=5)
        l.grid(column=0, row=0, sticky='w')

        c = tkinter.Radiobutton(f, text="Align principal axes (faster - only 4 fits will be tried)", variable=self.rotaSearch, value = 0)
        c.grid (column=1, row = 0, sticky='w')

        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        l = tkinter.Label(f, text=' ', width=5)
        l.grid(column=0, row=0, sticky='w')

        c = tkinter.Radiobutton(f, text="Rotational search (try", variable=self.rotaSearch, value = 1)
        c.grid (column=1, row = 0, sticky='w')

        self.rotaSearchNum = tkinter.StringVar(f, "100")
        e = tkinter.Entry(f, width=5, textvariable=self.rotaSearchNum)
        e.grid(column=2, row=0, sticky='w', padx=5)

        l = tkinter.Label(f, text='evenly rotated fits)')
        l.grid(column=3, row=0, sticky='w')


        forow += 1

        oft = Hybrid.Checkbutton(fopt, 'Mask map with region(s) to prevent large drifts', False)
        oft.button.grid(row = forow, column = 0, sticky = 'w')
        self.mask_map_when_fitting = oft.variable


        forow += 1

        oft = Hybrid.Checkbutton(fopt, 'Use Laplacian filter', False)
        oft.button.grid(row = forow, column = 0, sticky = 'w')
        self.useLaplace = oft.variable


        forow += 1

        oft = Hybrid.Checkbutton(fopt, 'Optimize fits', True)
        oft.button.grid(row = forow, column = 0, sticky = 'w')
        self.optimize_fits = oft.variable


        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        oft = Hybrid.Checkbutton(f, 'Cluster fits that are <', True)
        oft.button.grid(row = 0, column = 0, sticky = 'w')
        self.doClusterFits = oft.variable

        self.positionTolString = tkinter.StringVar(f, "5.0")
        e = tkinter.Entry(f, width=5, textvariable=self.positionTolString)
        e.grid(column=1, row=0, sticky='w', padx=5)

        l = tkinter.Label(f, text='Angstroms and <')
        l.grid(column=2, row=0, sticky='w')

        self.angleTolString = tkinter.StringVar(f, "3.0")
        e = tkinter.Entry(f, width=5, textvariable=self.angleTolString)
        e.grid(column=3, row=0, sticky='w', padx=5)

        l = tkinter.Label(f, text='degrees apart' )
        l.grid(column=4, row=0, sticky='w')


        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        l = tkinter.Label(f, text='Add top')
        l.grid(column=0, row=0, sticky='w')

        self.numFitsToAdd = tkinter.StringVar(f, "1")
        e = tkinter.Entry(f, width=5, textvariable=self.numFitsToAdd)
        e.grid(column=1, row=0, sticky='w', padx=5)

        l = tkinter.Label(f, text='fit(s) to list (empty to add all fits to list)')
        l.grid(column=2, row=0, sticky='w')


        forow += 1

        f = tkinter.Frame(fopt)
        f.grid(column=0, row=forow, sticky='w')

        oft = Hybrid.Checkbutton(f, 'Clashes with copies from symmetry:', False)
        oft.button.grid(row = 0, column = 0, sticky = 'w')
        self.calcSymmetryClashes = oft.variable

        self.symmetryString = tkinter.StringVar(f)
        e = tkinter.Entry(f, width=10, textvariable=self.symmetryString)
        e.grid(column=1, row=0, sticky='w', padx=5)

        b = tkinter.Button(f, text="Detect", command=self.DetectSym)
        b.grid (column=2, row=0, sticky='w', padx=5)

        b = tkinter.Button(f, text="Show", command=self.PlaceSym)
        b.grid (column=3, row=0, sticky='w', padx=5)



        dummyFrame = tkinter.Frame(parent, relief='groove', borderwidth=1)
        tkinter.Frame(dummyFrame).pack()
        dummyFrame.grid(row=row,column=0,columnspan=7, pady=7, sticky='we')

        row = row + 1

        global msg
        msg = tkinter.Label(parent, width = 60, anchor = 'w', justify = 'left', fg="red")
        msg.grid(column=0, row=row, sticky='ew')
        self.msg = msg
        row += 1

        self.SetResolution()

        chimera.openModels.addRemoveHandler(self.ModelClosed, None)

        mlist = OML(modelTypes = [chimera.Molecule])
        if mlist:
            self.struc.set(self.menu_name(mlist[0]))

        if dev_menus :
            self.optionsPanel.set(True)


        self.saveFrames = False
        self.frameAt = 0




    def PlotFitScores ( self ) :


        # self.list_fits.append((fmap, dmap, fmap.M, corr, atomI, bbI, bbC, hdo, regions))

        debug("Plotting %d fits:" % len ( self.list_fits ))

        if len ( self.list_fits ) == 0 :
            self.status ( "No fits in list to plot" )
            return


        minCorr = 1e9
        maxCorr = 0
        for fit in self.list_fits :
            corr = fit.correlation
            if maxCorr < corr : maxCorr = corr
            if minCorr > corr : minCorr = corr

        debug(" - maxCorr: %.3f minCorr: %.3f" % (maxCorr, minCorr))

        minCorr, maxCorr = 0, 1

        w = 600
        h = 400
        import PIL
        from PIL import Image, ImageDraw

        im = PIL.Image.new ( 'RGB', (w,h), (255,255,255) )

        #im.putpixel ( (i,j), (fclr[0], fclr[1], fclr[2]) )

        chartW = w - 40
        chartH = h - 40
        chartX = 20
        chartY = 20

        draw = ImageDraw.Draw(im) # Create a draw object

        lineClr = (120,120,120)
        draw.rectangle((10, h-10, w-10, h-10), fill=lineClr, outline=lineClr)
        draw.rectangle((10, 10, 10, h-10), fill=lineClr, outline=lineClr)

        xAt = chartX
        for fit in self.list_fits :
            barWidth = int ( float(chartW) / float(len(self.list_fits)) )
            xPos = int ( xAt + barWidth/2 )

            x1 = xAt
            x2 = xAt + barWidth
            if ( barWidth > 3 ) :
                x1 = x1 + 1
                x2 = x2 - 2

            yTop = int ( h - ( chartY + (fit.correlation - minCorr) * chartH / (maxCorr - minCorr) ) )
            yBot = int ( h - chartY )

            lineClr = ( int(rand()*255.0), int(rand()*255.0), int(rand()*255.0) )
            draw.rectangle((x1, yTop, x2, yBot), fill=lineClr, outline=lineClr)

            debug("x:%d barW %.2f cor %.2f height %.3f yTop %d yBot %d" % ( xAt, barWidth, fit.correlation, chartH, yTop, yBot ))

            xAt = xAt + barWidth


        #im.save ( "plot.png", 'PNG' )

        def save ( path ):
            self.status ( "Saved to " + path )
            im.save ( path, 'PNG' )

        idir = None
        ifile = None

        from .opensave import SaveFileDialog
        SaveFileDialog ( title = 'Save Plot',
                       filters = [('PNG', '*.png', '.png')],
                       initialdir = idir, initialfile = ifile, command = save )






    def PlotFitScores_Experimental ( self ) :

        debug("Plotting fits:")

        N = self._num_fits_to_add.value

        totAngles = 0
        minCorr = 1e9
        maxCorr = 0
        for corr, M, regions, stats in self.cfits [0 : N-1] :
            debug(" - #fits:%d maxAngle:%.1f maxShift:%.2f maxHeight:%.2f" % ( stats['numFits'], stats['maxAngle'], stats['maxShift'], stats['maxHeight'] ))
            totAngles = totAngles + stats['maxAngle']
            if maxCorr < corr : maxCorr = corr
            if minCorr > corr-stats['maxHeight'] : minCorr = corr-stats['maxHeight']

        minCorr, maxCorr = 0, 1

        debug(" - totAngles: %.2f, maxCorr: %.3f minCorr: %.3f" % (totAngles, maxCorr, minCorr))

        w = 600
        h = 400
        import PIL
        from PIL import Image, ImageDraw

        im = PIL.Image.new ( 'RGB', (w,h), (255,255,255) )

        #im.putpixel ( (i,j), (fclr[0], fclr[1], fclr[2]) )

        chartW = w - 40
        chartH = h - 40
        chartX = 20
        chartY = 20

        draw = ImageDraw.Draw(im) # Create a draw object

        lineClr = (120,120,120)
        draw.rectangle((10, h-10, w-10, h-10), fill=lineClr, outline=lineClr)
        draw.rectangle((10, 10, 10, h-10), fill=lineClr, outline=lineClr)

        xAt = chartX
        for corr, M, regions, stats in self.cfits [0 : N-1] :

            barWidth = int ( max ( 1, numpy.floor ( stats['maxAngle']  * float(chartW) / totAngles ) ) )
            xPos = int ( xAt + barWidth/2 )

            x1 = xAt
            x2 = xAt + barWidth
            if ( barWidth > 3 ) :
                x1 = x1 + 1
                x2 = x2 - 2

            yTop = int ( h - ( chartY + (corr - minCorr) * chartH / (maxCorr - minCorr) ) )
            yBot = int ( h - ( chartY + (corr - stats['maxHeight'] - minCorr) * chartH / (maxCorr - minCorr) ) )

            lineClr = ( int(rand()*255.0), int(rand()*255.0), int(rand()*255.0) )
            draw.rectangle((x1, yTop, x2, yBot), fill=lineClr, outline=lineClr)

            debug("maxA %.2f x:%d barW %.2f cor %.2f height %.3f yTop %d yBot %d" % ( stats['maxAngle'], xAt, barWidth, corr, stats['maxHeight'], yTop, yBot ))

            xAt = xAt + barWidth


        #im.save ( "plot.png", 'PNG' )

        def save ( path, lfits = lfits ):
            self.status ( "Saved to " + path )
            im.save ( path, 'PNG' )

        idir = None
        ifile = None

        from .opensave import SaveFileDialog
        SaveFileDialog ( title = 'Save Plot',
                       filters = [('PNG', '*.png', '.png')],
                       initialdir = idir, initialfile = ifile, command = save )




    def ExportFitScores ( self ) :

        num = len(self.list_fits)
        if num == 0 :
            self.status ( "No fits to export" )
            return

        scores = []

        # (fmap, dmap, fmap.M, corr, atomI, bbI, regions)

        for fit in self.list_fits :
            scores.append ( [ fit.correlation, fit.atom_inclusion, fit.backbone_inclusion,
                              fit.backbone_clash, fit.high_density_occupancy ] )

        def ZZ ( scs ) :
            if len(scs) < 3 :
                return (0.0, 0, 0, 0)

            best_score = scs[0]
            other_scores = scs[1:14]
            avg = numpy.average ( other_scores )
            stdev = numpy.std ( other_scores )
            return [(best_score - avg) / stdev, best_score, avg, stdev]

        def save ( path, scores = scores ):
            f = open ( path, "a" )

            f.write ( "%s\t%s\t%s\t%s\t%s\n" % (
                "Cross-correlation",
                "Atom Inclusion",
                "Backbone-Atom Inclusion",
                "Clash score",
                "Density occupancy" ) )

            s1, s2, s3, s4, s5 = [], [], [], [], []
            for s in scores :
                f.write ( "%f\t%f\t%f\t%f\t%f\n" % (s[0], s[1], s[2], s[3], s[4]) )
                s1.append ( s[0] )
                s2.append ( s[1] )
                s3.append ( s[2] )
                s4.append ( s[3] )
                s5.append ( s[4] )

            Z1, Z2, Z3, Z4, Z5 = ZZ(s1), ZZ(s2), ZZ(s3), ZZ(s4), ZZ(s5)
            #f.write ( "Zscores: %f\t%f\t%f\t%f\t%f\n" % (Z1[0], Z2[0], Z3[0], Z4[0], Z5[0]) )
            f.write ( "Score\tZ-score\tTop score\tMean\tSTDev\n" )
            f.write ( "Cross-correlation:\t%f\t%f\t%f\t%f\n" % (Z1[0], Z1[1], Z1[2], Z1[3]) )
            f.write ( "Atom Inclusion:\t%f\t%f\t%f\t%f\n" % (Z2[0], Z2[1], Z2[2], Z2[3]) )
            f.write ( "Density occupancy:\t%f\t%f\t%f\t%f\n" % (Z5[0], Z5[1], Z5[2], Z5[3]) )
            f.write ( "Clash score:\t%f\t%f\t%f\t%f\n" % (Z4[0], Z4[1], Z4[2], Z4[3]) )


            f.close ()
            self.status ( "Wrote %d fits to %s" % ( len(scores), path ) )


        idir = None
        ifile = None

        first_fit = self.list_fits[0]
        fit_map = first_fit.fit_map
        ref_map = first_fit.target_map
        regions = first_fit.regions

        fit_path = ""
        try : fit_path = fit_map.mols[0].openedAs[0]
        except : fit_path = fit_map.data.path

        import os.path
        idir, ifile = os.path.split(fit_path)
        base, suf = os.path.splitext(ifile)
        map_base, map_suf = os.path.splitext( ref_map.name )
        ifile = base + "_fits_in_%s_regs" % map_base

        for r in regions :
            ifile = ifile + ("_%d" % r.rid)

        from .opensave import SaveFileDialog
        SaveFileDialog ( title = 'Save Fit Scores',
                       filters = [('TXT', '*.txt', '.txt')],
                       initialdir = idir, initialfile = ifile, command = save )


    def add_fit (self, fmap, dmap):

        corr = fmap.fit_score
        regions = fmap.fit_regions
        atomI = fmap.atomInclusion
        bbI = fmap.bbAtomInclusion
        bbC = fmap.bbClashes
        hdo = fmap.hdoScore

        fit = Fit(fmap, dmap, fmap.M, corr, atomI, bbI, bbC, hdo, regions)
        self.list_fits.append(fit)

        self._add_fit_to_listbox(fit)

    def _add_fit_to_listbox(self, fit):

        ids = ','.join(['%d' % r.rid for r in fit.regions])
        line = ('%8.4f %8.4f %8.4f %8.4f %8.4f %15s %15s %10s'
                % (fit.correlation, fit.atom_inclusion, fit.backbone_inclusion,
                   fit.backbone_clash, fit.high_density_occupancy,
                   fit.fit_map.struc_name, fit.target_map.name, ids))
        self._fit_listbox.addItem(line)

    def fit_selection_cb (self) :

        lfits = self.selected_listbox_fits()
        if len(lfits) == 0:
            return

        fit = lfits[0]
        for mol in fit.fit_map.mols :
            if mol.deleted:
                self.status('Fit molecule was closed')
        else:
            self.place_molecule(fit.fit_map, fit.position, fit.target_map)
        self.make_regions_transparent(fit.regions)


    def place_molecule(self, fmap, mat, dmap):

        if dmap.deleted:
            debug("Reference map no longer open")
            return

        if fmap.deleted:
            debug("Fitted map no longer open")
            return

#        com = mat.origin()
#        q = Segger.quaternion.Quaternion()
#        q.fromXform ( mat )
#        debug("COM: ", com, "Q: %.6f" % q.s, q.v)

        xf = dmap.scene_position * mat
        fmap.scene_position = xf
        fmap.M = mat

        for mol in fmap.mols :
            if not mol.deleted:
                mol.scene_position = xf

    def make_regions_transparent(self, regions):

        for r in regions:
            r.show_transparent( REG_OPACITY )

    def selected_listbox_rows(self):

        lb = self._fit_listbox
        return [lb.row(i) for i in lb.selectedItems()]
    
    def selected_listbox_fits(self):

        lf = self.list_fits
        return [lf[r] for r in self.selected_listbox_rows()]

    def delete_all_fit_cb ( self ) :

        self._fit_listbox.clear()
        self.list_fits = []

    def delete_fit_cb(self):

        rows = self.selected_listbox_rows()
        if len(rows) == 0:
            self.status('No fits chosen from list')
            return
        rows.sort(reverse = True)
        lb = self._fit_listbox
        for r in rows:
            lb.takeItem(r)
            del self.list_fits[r]

        self.status('Deleted %d fits' % len(rows))


    def place_copies_cb(self):

        lfits = self.selected_listbox_fits()
        if len(lfits) == 0:
            self.status('No fits chosen from list')
            return

        nPlaced = 0
        for fit in lfits:
            if len ( fit.fit_map.mols ) > 0 :
                self.PlaceCopy(fit.fit_map.mols, fit.position, fit.target_map, (rand(),rand(),rand(),1) )
                nPlaced += 1

        self.status('Placed %d models' % nPlaced)




    def place_map_copies_cb ( self ) :

        lfits = self.selected_listbox_fits()
        if len(lfits) == 0 :
            self.status('No fits chosen from list')
            return

        for fit in lfits:
            self.place_molecule(fit.fit_map, fit.position, fit.target_map)
            sf = "_F2Rid%d.mrc" % regions[0].rid
            pmap = place_map_resample ( fit.fit_map, fit.target_map, sf )

            try :
                self.fitted_mols = self.fitted_mols + [pmap]
            except :
                self.fitted_mols = [pmap]


        self.status('Placed %d models' % len(lfits))


    def copy_fit_map ( self ) :

        dmap = self.segmentation_map
        if dmap is None :
            self.status ('No segmentation map is chosen in Segment Map panel')
            return

        fmap = self.StructuresToFit ()
        if len(fmap) == 0 :
            debug("Select the map to save")
            return

        fmap = fmap[0]

        from chimerax.map import Volume
        if not isinstance(fmap, Volume) :
            self.status ("Require map chosen in fit menu, got %s which is not a map."
                         % self._fit_model_menu.text())
        else :
            place_map_resample ( fmap, dmap, "_F2Rid.mrc" )


    def extractCubeMap ( self ) :

        dmap = self.segmentation_map
        if dmap is None :
            self.status ( "No segmentation map is chosen in Segment Map panel" )
            return

        fmap = self.StructuresToFit ()

        if len(fmap) == 0 :
            debug("Select the map to save")
            return

        fmap = fmap[0]
        debug("Saving ", fmap.name)

        from chimerax.map_data import grid_indices
        npoints = grid_indices ( dmap.data.size, numpy.single)  # i,j,k indices
        dmap.data.ijk_to_xyz_transform.transform_points ( npoints, in_place = True )

        dvals = fmap.interpolated_values ( npoints, dmap.scene_position )
        #dvals = numpy.where ( dvals > threshold, dvals, numpy.zeros_like(dvals) )
        #nze = numpy.nonzero ( dvals )

        nmat = dvals.reshape( dmap.data.size )
        #f_mat = fmap.data.full_matrix()
        #f_mask = numpy.where ( f_mat > fmap.minimum_surface_level, numpy.ones_like(f_mat), numpy.zeros_like(f_mat) )
        #df_mat = df_mat * f_mask

        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, self.session )

        fmap_base = os.path.splitext (fmap.name)[0]
        dmap_base = os.path.splitext (dmap.name)[0]
        fmap_path = os.path.splitext (fmap.data.path)[0]
        dmap_path = os.path.splitext (dmap.data.path)[0]

        nv.name = "emd_1093_62.mrc"
        nv.scene_position = dmap.scene_position




    def close_copies_cb ( self ) :

        fmols = getattr(self, 'fitted_mols', [])
        if len(fmols) == 0:
            self.status ( "No fitted molecule copies found" )
            return

        self.fitted_mols = []
        self.session.models.close ( fmols )


    def Options(self):

        self.optionsPanel.set(not self.optionsPanel.get())


    def SetResolution ( self ):

        dmap = self.segmentation_map
        if dmap == None : return

        if self._sim_res.value == 0:
            res = min(dmap.data.step) * 3
            self._sim_res.value = res
            self._sim_grid_sp.value = res/3.0

    @property
    def _sim_res_and_grid(self):
        res, grid = self._sim_res.value, self._sim_grid_sp.value
        if res == 0:
            self.SetResolution()
            res, grid = self._sim_res.value, self._sim_grid_sp.value
        return res, grid


    def CurrentSegmentation ( self, warn = True ):

        from .segment_dialog import current_segmentation
        return current_segmentation(self.session, warn)


    def StrucMenu ( self ) :

        self.strucMB.menu.delete ( 0, 'end' )   # Clear menu

        self.strucMB.menu.add_radiobutton ( label="Open structures:" )
        self.strucMB.menu.add_separator()

        id_struc = {}
        open_mols = {}
        from chimerax.map import Volume
        from chimerax.atomic import Structure
        for m in OML() :
            if isinstance(m, (Volume, Structure)):
                try : id_struc [ m.id ].append ( m )
                except : id_struc [ m.id ] = [m]
                open_mols[m.name] = True
            else :
                #debug type(m)
                pass

        cur_sel_found = False
        for mid, mols in id_struc.items() :

            if len(mols) == 1 or self._lump_subids.enabled :
                mol = mols[0]
                label = self.menu_name(mol)
                self.strucMB.menu.add_radiobutton ( label= label,
                                                    variable=self.struc,
                                                    command = self.StrucSelected )
                if label == self.struc.get() :
                    cur_sel_found = True

            else :
                for mol in mols :
                    label = self.menu_name(mol)
                    self.strucMB.menu.add_radiobutton ( label=label,
                                                        variable=self.struc,
                                                        command = self.StrucSelected )
                    if label == self.struc.get() :
                        cur_sel_found = True


        if not cur_sel_found :
            self.struc.set ( "" )

        dmap = self.segmentation_map
        if dmap == None : return

        path = os.path.dirname ( dmap.data.path ) + os.path.sep
        files = os.listdir ( path );
        mols_in_path = []
        for f in files :
            if f.find ( ".pdb" ) >= 0 and (f in open_mols) == False :
                mols_in_path.append ( f )

        if len ( mols_in_path ) == 0 : return

        self.strucMB.menu.add_separator()
        self.strucMB.menu.add_radiobutton ( label="In %s:" % path )
        self.strucMB.menu.add_separator()

        for fm in mols_in_path :
            self.strucMB.menu.add_radiobutton ( label=fm, variable=self.struc,
                                                command = self.StrucSelected )


    def StrucSelected ( self ) :

        # Check if selected entry is an existing open molecule.
        mlist = self.StructuresToFit()
        if mlist:
            debug("selected structure found:", mlist[0].name)

            try :
                natoms = sum([len(m.atoms) for m in mlist])
                debug("%d molecules, %d atoms" % (len(mlist), natoms))
            except :
                debug("%d map" % (len(mlist)))
            return

        # otherwise look for selection as a pdb file to be loaded...

        dmap = self.segmentation_map
        if dmap == None : debug(" - no map selected"); return

        path = os.path.dirname(dmap.data.path) + os.path.sep

        label = self.struc.get()
        fmol = chimera.openModels.open ( path + label )[0]
        debug(" - opened")

        sel_str = "#%s" % fmol.id_string
        try : mols = chimera.selection.OSLSelection ( sel_str ).molecules()
        except : self.status ("Structure not opened sucessfully"); return

        mol = mols[0]
        label = self.menu_name(mol)

        self.struc.set(label)


    def StructuresToFit ( self ) :

        return [self._struct_to_fit]

    @property
    def segmentation_map(self):

        from . import segment_dialog
        return segment_dialog.segmentation_map( self.session )
    
    def menu_name(self, mol):

        show_subid = not self._lump_subids.enabled and mol.subid != 0
        id =  '%s' % mol.id_string if show_subid else '%d' % mol.id[0]
        mname = "%s (%s)" % (mol.name, id)
        return mname


    @property
    def _struct_to_fit(self):

        return self._fit_model_menu.value

    def Fit ( self ) :

        self.doStop = False

        dmap = self.segmentation_map
        if dmap == None :
            self.status ( "Density map not found or not selected" )
            return

        fmol = self._struct_to_fit
        if fmol is None:
            return


        from chimerax.map import Volume
        from chimerax.atomic import Structure
        if isinstance(fmol, Structure):
            # this property added to self will indicate to functions called
            # below whether we are fitting a map instead of a molecule
            self.map_to_fit = None

            #if fmol.openState is dmap.openState :
            #    self.status('Molecule cannot be moved relative to map\nbecause they have the same model id number.')
            #    return
        elif isinstance(fmol, Volume):
            
            fmap = fmol
            self.map_to_fit = fmap
            fmap.mols = []
            fmap.struc_name = fmap.name

            points, weights = fit_points ( fmap )
            # debug "Points : ", points

            fmap.COM, fmap.U, fmap.S, fmap.V = prAxes ( points )
            debug("COM : ", fmap.COM)
            debug("U : ", fmap.U)

            from chimerax.geometry import Place
            toCOM = Place ( [
                [ 1, 0, 0, -fmap.COM[0] ],
                [ 0, 1, 0, -fmap.COM[1] ],
                [ 0, 0, 1, -fmap.COM[2] ] ] )

            mR = Place ( [
                [ fmap.V[0,0], fmap.V[0,1], fmap.V[0,2], 0 ],
                [ fmap.V[1,0], fmap.V[1,1], fmap.V[1,2], 0 ],
                [ fmap.V[2,0], fmap.V[2,1], fmap.V[2,2], 0 ] ] )

            # this matrix centers the map and aligns its principal axes
            # to the x-y-z axes
            fmap.preM = mR * toCOM


        if self._combined_selected_regions.enabled :
            descrip, func = ("Fitting to combined selected regions...", self.FitMapToSelRGroup)
        elif self._each_selected_region.enabled :
            descrip, func = ("Fitting to each selected region...", self.FitToEachRegion)
        elif self._around_selected.enabled :
            descrip, func = ("Fitting groups around selected...", self.FitMapToRegionsAroundSel)
        elif self._all_groups.enabled :
            descrip, func = ( "Fitting to all groups...", self.FitMapToRGroups)
        else:
            self.status('No alignment method chosen')
            return

        debug(descrip)
        func()
        dmap = self.segmentation_map
        if dmap:
            dmap.display = False


    def Stop (self) :
        debug("will stop...")
        self.doStop = True



    def DetectSym ( self ) :

        dmap = self.segmentation_map

        if dmap == None:
            self.status ( "Please select a map in the Segment Map dialog" )
            return []

        debug("Symmetry for", dmap.name)

        from chimerax.std_commands.measure_symmetry import find_point_symmetry

        syms, msg = find_point_symmetry ( dmap, n_max=8 )

        if syms is None :
            self.status ( "No symmetry detected for %s" % dmap.name )
            self._symmetry.value =  "No symmetry detected" 
            return []

        self.status ( msg )
        start = msg.find(': ')+2
        end = msg.find (', center')
        self._symmetry.value = msg [start : end]

        for i, sym in enumerate ( syms ) :
            #debug i, " -> ", sym
            pass

        return syms


    def PlaceSym ( self ) :

        fmap = self.MoleculeMap()
        dmap = self.segmentation_map

        if fmap == None or dmap == None:
            self.status ( "Please select an open structure to fit" )
            return

        from chimerax.std_commands.measure_symmetry import centers_and_points

        syms = []
        esym = self._symmetry.value
        if 1 or len (esym) == 0 :
            syms = self.DetectSym ()
        else :
            debug("Custom sym:", esym)
            if ( esym == "C3" ) :

                debug(" - dmap: ", dmap.name)
                mpoints, mpoint_weights = fit_points(dmap)
                COM, U, S, V = prAxes ( mpoints )
                debug("COM: ", COM)
                debug("U: ", U)
                debug("S: ", S)

                ax = ( 0, 1, 0 )
                #ax = dmap.scene_position.inverse().apply ( ax )

                from chimerax.geometry import Place, rotation
                syms.append ( Place () )
                rm1 = rotation ( (ax.x,ax.y,ax.z), 360.0/3.0, COM )
                debug(rm1)
                syms.append ( rm1 )
                #syms.append ( Matrix.rotation_transform ( (1.0,0.0,0.0), 2.0*360.0/3.0 ) )

                #centers, xyz, w = centers_and_points(dmap)
                #debug " - center:", centers
                #ctf = Matrix.translation_matrix([-x for x in COM[0]])
                #syms = Matrix.coordinate_transform_list(syms, ctf)


        smols = []

        for sym in syms [1 : ] :

            #mols = self.PlaceCopy (fmap.mols, sym*fmap.M, dmap, (0,0,0,1) )
            mols = self.PlaceCopy (fmap.mols, sym*fmap.scene_position, dmap, (.4, .8, .4, 1) )
#            for m in mols : m.scene_position = dmap.scene_position
            smols.extend(mols)

        return smols


    def PlaceSymOld ( self ) :

        fmap = self.MoleculeMap()
        dmap = self.segmentation_map

        if fmap == None or dmap == None:
            debug("Fit or segmentation map not found")
            return

        from chimerax.map_data import grid_indices
        fpoints = grid_indices(dmap.data.size, numpy.single)  # i,j,k indices
        dmap.data.ijk_to_xyz_transform.transform_points( fpoints, in_place = True )
        mat = dmap.data.full_matrix()
        fpoint_weights = numpy.ravel(mat).astype(numpy.single)

        threshold = dmap.minimum_surface_level
        ge = numpy.greater_equal(fpoint_weights, threshold)
        fpoints = numpy.compress(ge, fpoints, 0)
        fpoint_weights = numpy.compress(ge, fpoint_weights)
        nz = numpy.nonzero( fpoint_weights )[0]

        debug("%d above %f in %s\n" % (len(nz), threshold, dmap.name))

        COM, U, S, V = prAxes ( fpoints )

        debug("COM: ", COM)
        debug("U: ", U)
        debug("S: ", S)

        from chimerax.geometry import Place
        T0 = Place ( [
            [ 1, 0, 0, -COM[0] ],
            [ 0, 1, 0, -COM[1] ],
            [ 0, 0, 1, -COM[2] ] ] )

        T = Place ( [
            [ 1, 0, 0, COM[0] ],
            [ 0, 1, 0, COM[1] ],
            [ 0, 0, 1, COM[2] ] ] )


        fmapM = fmap.scene_position
        dmapM = dmap.scene_position


        smols = []

        if 0 :
            from chimerax.geometry import rotation
            M = rotation( (0, 0, 1), 360.0/7.0 )
            mols = self.PlaceCopy (fmap.mols, M*fmap.M, dmap, (0,0,0,1) )
            for m in mols : m.scene_position = dmap.scene_position
            smols = smols + mols

            M = rotation( (0, 0, 1), -360.0/7.0 )
            mols = self.PlaceCopy (fmap.mols, M*fmap.M, dmap, (0,0,0,1))
            for m in mols : m.scene_position = dmap.scene_position
            smols = smols + mols

            M1 = rotation( (1, 0, 0), 180.0 )
            M =  rotation( (0, 0, 1), 2.0*360.0/7.0 )
            mols = self.PlaceCopy (fmap.mols, M*M1*fmap.M, dmap, (0,0,0,1))
            for m in mols : m.scene_position = dmap.scene_position
            smols = smols + mols

            M1 = rotation( (0, 0, 1), 180.0 )
            M = rotation( (0, 0, 1), 3.0*360.0/7.0 )
            mols = self.PlaceCopy (fmap.mols, M*M1*fmap.M, dmap, (0,0,0,1) )
            for m in mols : m.scene_position = dmap.scene_position
            smols = smols + mols


        from chimerax.geometry import rotation
        M = rotation( (U[0,2], U[1,2], U[2,2]), 360.0/7.0 )
        mols = self.PlaceCopy (fmap.mols, T*M*T0*fmap.M, dmap, (0,0,0,1) )
        for m in mols : m.scene_position = dmap.scene_position
        smols = smols + mols

        M = rotation( (U[0,2], U[1,2], U[2,2]), -360.0/7.0 )
        mols = self.PlaceCopy (fmap.mols, T*M*T0*fmap.M, dmap, (0,0,0,1) )
        for m in mols : m.scene_position = dmap.scene_position
        smols = smols + mols

        return smols


    def StrucCenter ( self ) :

        mols = [self._struct_to_fit]
        centerMol ( mols )

        mm = self.segmentation_map
        if mm :
            for mol in mols :
                mol.scene_position = mm.scene_position



    def StrucShowAxes ( self ) :

        mols = [self._struct_to_fit]        
        centerMol ( mols )

        fmol = mols[0]
        debug("Showing axes for", fmol.name)
        debug(" - COM:", fmol.COM)
        debug(" - extents:", fmol.Extents)

        try :
            self.session.models.close ( [fmol.axes] )
            fmol.axes = None
        except :
            pass

        from . import axes
        fmol.axes =  axes.AxesMod ( fmol.session, Extents = fmol.Extents, rad = 1.0,
                                    alignTo = fmol )
        fmol.axes.name = os.path.splitext (fmol.name)[0] + "_axes"



    def StrucHideAxes ( self ) :

        mols = [self._struct_to_fit]
        centerMol ( mols )

        fmol = mols[0]

        try :
            self.session.models.close ( [fmol.axes] )
            fmol.axes = None
        except :
            pass


    def GenStrucMap ( self, show = True ) :

        self.SetResolution()

        res, grid = self._sim_res_and_grid

        self.status ( "Simulating map res %.3f, grid %.3f" % (res, grid) )

        if self._struct_to_fit is None:
            self.status ( "Please select a Structure to fit in the field above" )
            return

        
        mols = [self._struct_to_fit]
        centerMol ( mols )

        mol = mols[0]

        base = os.path.splitext(mol.name)[0]
        mname = base + "_" + mol.id_string + "_r%.1f_sp%.1f" % (res, grid)
        if self._use_laplace.enabled :
            mname = mname + "_L"
        mname = mname + ".mrc"

        mv = getMod ( self.session, mname )
        if mv != None :
            debug("Found", mname)
            return mv

        debug("Generating", mname)

        #cmd = "molmap #%s/C-D@CA %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
        cmd = "molmap #%s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( mol.id_string, res, grid )
        debug(" -", cmd)
        mv = self._run_command ( cmd )

        if mv is None :
            self.status ("Map not generated - molmap command did not produce expected result.")
            return

        if self._use_laplace.enabled :
            self.status ("Generating Laplacian...")
            from chimerax.map_filter import laplacian
            mvl = laplacian ( mv )
            self.session.models.close ( [mv] )
            mv = mvl
            mv.name = mname

        mv.display = show
        mv.mols = mols
        mv.struc_name = mol.name

        # for consistency when fitting maps, which need this pre-transform
        # since they don't get transformed like the molecules
        from chimerax.geometry import Place
        mv.preM = Place()

        return mv

    def _run_command(self, command):

        from chimerax.core.commands import run
        result = run ( self.session, command )
        return result

    def GenChMaps ( self, m ) :

        res, grid = self._sim_res_and_grid

        if self._struct_to_fit is None:
            self.status ( "Please select a Structure to fit in the field above" )
            return

        mols = [self._struct_to_fit]
        centerMol ( mols )

        mol = mols[0]

        base = os.path.splitext(mol.name)[0]
        mname = base + "_" + mol.id_string + "_r%.1f_sp%.1f" % (res, grid)
        if self._use_laplace.enabled :
            mname = mname + "_L"
        mname = mname + ".mrc"

        mv = getMod ( self.session, mname )
        if mv != None :
            debug("Found", mname)
            return mv

        debug("Generating", mname)

        #cmd = "molmap #%s/C-D@CA %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
        cmd = "molmap #%s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( mol.id_string, res, grid )
        debug(" -", cmd)
        self._run_command ( cmd )

        mv = None
        for mod in self._all_models :
            ts = mod.name.split()
            if len(ts) > 1 and mod.name.find("map") >=0 and mod.name.find("res") >=0 :
                debug(" - found", mod.name)
                mv = mod
                mv.name = mname
                break

        if mv == None :
            self.status ("Map not generated - molmap command did not produce expected result.")
            return

        if self._use_laplace.enabled :
            self.status ("Generating Laplacian...")
            from chimerax.map_filter import laplacian
            mvl = laplacian ( mv )
            self.session.models.close ( [mv] )
            mv = mvl
            mv.name = mname

        mv.display = show
        clr = mol.single_color
        mv.single_color = clr
        mv.mols = mols
        mv.struc_name = label

        # for consistency when fitting maps, which need this pre-transform
        # since they don't get transformed like the molecules
        from chimerax.geometry import Place
        mv.preM = Place()

        return mv





    def SaveStrucFit ( self ) :

        lfits = self.selected_listbox_fits()
        if len(lfits) == 0:
            self.status('No fits chosen from list')
            return

        def save ( path, lfits = lfits ):
            if len(lfits) > 1 and path.find('%d') == -1:
                base, suf = os.path.splitext(path)
                path = base + '_fit%d' + suf
            for i, fit in enumerate(lfits):
                p = path if len(lfits) == 1 else path % (i+1)
                self.place_molecule(fit.fit_map, fit.position, fit.target_map)
                cmd = ('save %s models #%s relModel #%s'
                       % (p, ','.join(s.id_string for s in fit.fit_map.mols), fit.target_map.id_string))
                from chimerax.core.commands import run
                run(self.session, cmd)

        mol = lfits[0].fit_map.mols[0]
        if hasattr(mol, 'filename'):
            import os.path
            idir, ifile = os.path.split(mol.filename)
            base, suf = os.path.splitext(ifile)
            if len(lfits) > 1:
                ifile = base + '_fit%d' + suf
            else:
                ifile = base + '_fit' + suf
        else:
            idir = None
            ifile = None

        from .opensave import SaveFileDialog
        SaveFileDialog ( title = 'Save Fit Molecules',
                       filters = [('PDB', '*.pdb', '.pdb')],
                       initialdir = idir, initialfile = ifile, command = save )

    def SaveFit ( self, fmap, clr=None ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        mols = self.PlaceCopy(fmap.mols, fmap.M, dmap, clr)
        path = os.path.dirname ( dmap.data.path ) + os.path.sep
        debug("Saving:")
        for mol in mols :
            debug(" - %s %s" % ( path + mol.name, mol.id_string ))
        chimera.PDBio().writePDBfile ( mols, path + mols[0].name )
        self.status ( "Saved fit (%d structures)" % len(mols) )

        return mols


    def PlaceCopy(self, molecules, mat, dmap, clr=None):

        try : fit_m_at = len ( self.fitted_mols ) + 1
        except : fit_m_at = 1; self.fitted_mols = []

        new_mols = []

        for molecule in molecules :

            mol = molecule.copy()
            mol.name = os.path.splitext ( mol.name )[0] + "_f%d.pdb" % fit_m_at

            from .regions import float_to_8bit_color
            if clr :
                mclr = float_to_8bit_color(clr)
            else :
                mclr = molecule.residues[0].ribbon_color

            if mat is not None :
                mol.scene_position = dmap.scene_position * mat
                print ('placed mol copy at', mol.scene_position.matrix)
                #molApplyT ( mol, mat )
            new_mols.append ( mol )

            res = mol.residues
            res.ribbon_displays = True
            res.ribbon_colors = mclr
            mol.atoms.displays = False
            mol.display = True

        if dmap :
            self.fitted_mols = self.fitted_mols + new_mols

        self.session.models.add ( new_mols )

        return new_mols



    def FitToEachRegion ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        fmap = None
        if self.map_to_fit :
            fmap = self.map_to_fit
        else :
            fmap = self.MoleculeMap()
            if not hasattr(fmap.mols[0], 'centered'):
                self.StrucCenter()

        regs = smod.selected_regions()
        if len(regs) == 0 :
            self.status ( "Please select one or more regions to align the structure to" )
            return

        path = os.path.dirname ( dmap.data.path ) + os.path.sep

        for reg in regs :

            self.fits = []
            reportFitRegions(fmap.name, regs)
            scores = []
            corrs = []

            sp = reg.surface_piece
            sp.display = True
            reg.show_transparent( REG_OPACITY )

            fmap.display = False
            for mol in fmap.mols : mol.display = True

            fmap.fit_regions = [reg]

            to_map = dmap
            reg_map = None
            if 1 :
                reg_map = mask_volume( [reg], dmap )

            bCloseMap = False

            if self._use_laplace.enabled :
                self.status ("Generating Laplace version of " + dmap.name)
                from chimerax.map_filter import laplacian
                to_map = laplacian ( dmap )
                bCloseMap = True

            elif self._mask_map_when_fitting.enabled :
                to_map = reg_map
                bCloseMap = True
                if to_map is None:
                    self.status ('Could not create masked map')
                    return

            tpoints = reg.map_points()
            if self._rota_search.enabled :
                self.saFitMapToPoints_byRot ( fmap, tpoints, to_map )
            else :
                self.saFitMapToPoints ( fmap, tpoints, to_map )

            scores.append ( 0 )
            corrs.append ( fmap.fit_score )

            self.status ( "Cross-correlation of fit: %f" % fmap.fit_score )

            self.cfits = self.ClusterFits ( self.fits )
            self.cfits.sort ( reverse=True, key=lambda x: x[0] )
            #self.cfits.sort()
            #self.cfits.reverse()

            #frame_at = 0

            try : nToAdd = self._num_fits_to_add.value
            except : nToAdd = len (self.cfits)
            for corr, M, regions, stats in self.cfits [ 0 : nToAdd ] :
                debug(" -- clustered Fit -- #fits:%d maxAngle:%.1f maxShift:%.2f maxHeight:%.2f" % ( stats['numFits'], stats['maxAngle'], stats['maxShift'], stats['maxHeight'] ))
                fmap.fit_score, fmap.M, fmap.fit_regions = corr, M, regions
                fmap.atomInclusion, fmap.bbAtomInclusion, fmap.bbClashes, fmap.hdoScore = self.FitScores ( fmap, reg_map )
                #frame_at = frame_at + 1
                self.add_fit (fmap, dmap)

            # FitScores fn moves the model, so move it back to top fit
            move_fit_models(fmap, self.cfits[0][1], dmap.scene_position)

            #self.status ( "Cross-correlation: %.4f\n" % (fmap.fit_score) )
            self.ReportZScore ( self.cfits )

            # close masked map if it was created
            #if bCloseMap : close_models ( [to_map] )
            close_models ( [reg_map] )


    def saFitMapToPoints ( self, fmap, points, dmap ) :

        debug("fitting %s in map %s, to %d points" % (fmap.name, dmap.name, len(points)))

        fpoints, fpoint_weights = fit_points(fmap)

        # the 4 alignments to try...
        flips = [ (1,1,1), (-1,-1,1), (-1,1,-1), (1,-1,-1) ]
        #flips = [ (1,-1,-1)  ]
        mlist = principle_axes_alignments ( points, flips, fmap.preM )

        best = (-2, None, None)
        names =  ['%.1f*X %.1f*Y %.1f*Z' % f for f in flips]

        optimize = self._optimize_fits.enabled

        fits = optimize_fits(fpoints, fpoint_weights, mlist, dmap,
                             names, None, optimize)
        corr, Mfit, i = self.make_best_fit(fits, fmap, dmap)

        f = flips[i]
        debug(" - best fit: %f for %.1f*X %.1f*Y %.1f*Z" % (
            corr, f[0], f[1], f[2] ))


    def ReportZScore ( self, fits ) :

        fit_scores = [c for c,M,regs,stats in fits]
        if ( len(fit_scores) > 3 ) :
            fit_scores.sort ()
            fit_scores.reverse ()
            best_score = fit_scores[0]
            other_scores = fit_scores[1:14]
            debug("Best score: ", best_score)
            debug("Next scores: ", other_scores)
            avg = numpy.average ( other_scores )
            stdev = numpy.std ( other_scores )
            self.zscore = (best_score - avg) / stdev
            self.status ( "Top score: %.5f, z-score: %.5f (avg: %.4f, stdev: %.4f)" % (
                best_score, self.zscore, avg, stdev) )



    def ClusterFits ( self, fits ) :

        class ClusterEntry :
            def __init__ (self, T, corr, regs, stats) :
                self.M = T
                self.COM = T.origin()
                from .quaternion import Quaternion
                self.Q = Quaternion()
                self.Q.fromXform ( T )
                self.corr = corr
                self.regs = regs
                self.stats = stats

        class Cluster :
            def __init__ ( self, e ) :
                self.entries = [ e ]
                self.COM = e.COM
                self.Q = e.Q
                self.corr = e.corr
                self.M = e.M
                self.regs = e.regs
                self.stats = {}
                self.stats['maxAngle'] = self.sumAngles = e.stats['totAngle']
                self.stats['maxShift'] = self.sumShifts = e.stats['totShift']
                self.stats['maxHeight'] = self.sumHeights = e.stats['difCC']
                self.stats['numFits'] = 1

            def AddEntry ( self, new_e ) :
                self.entries.append  ( new_e )
                if new_e.corr > self.corr :
                    self.corr = new_e.corr
                    self.M = new_e.M
                    self.regs = new_e.regs

                totAngle, totShift, difCC = new_e.stats['totAngle'], new_e.stats['totShift'], new_e.stats['difCC']
                if totAngle > self.stats['maxAngle'] : self.stats['maxAngle'] = totAngle
                if totShift > self.stats['maxShift'] : self.stats['maxShift'] = totShift
                if difCC > self.stats['maxHeight'] : self.stats['maxHeight'] = difCC

                self.stats['numFits'] = self.stats['numFits'] + 1

                # compute the new averages
                self.COM = (0,0,0)
                from .quaternion import Quaternion
                self.Q = Quaternion(0, (0,0,0))

                for e in self.entries :
                    self.COM = self.COM + e.COM
                    self.Q = self.Q + e.Q
                    self.sumAngles = self.sumAngles + totAngle
                    self.sumShifts = self.sumShifts + totShift
                    self.sumHeights = self.sumHeights + difCC

                self.COM = self.COM / float ( len(self.entries) )
                self.Q.normalize()

                self.avgAngle = self.sumAngles / float ( len(self.entries) )
                self.avgShift = self.sumShifts / float ( len(self.entries) )
                self.avgHeight = self.sumHeights / float ( len(self.entries) )


            def SimilarTo ( self, e, posTol=5.0, angleTol=5.0 ) :
                from chimerax.geometry import norm
                if ( norm(self.COM - e.COM) < posTol and
                     self.Q.angleTo ( e.Q ) * 180.0 / numpy.pi < angleTol ) :
                    return True
                return False

        posTol = self._position_tol.value
        angleTol = self._angle_tol.value
        if self._do_cluster_fits.enabled :
            debug("Clustering %d fits..." % len(fits))
            debug(" - distance < ", posTol)
            debug(" - angle < ", angleTol)

        clusters = []
        for corr, M, regs, stats in fits :

            e = ClusterEntry ( M, corr, regs, stats )

            bAdded = False

            if self._do_cluster_fits.enabled :
                for c in clusters :
                    if c.SimilarTo ( e, posTol, angleTol ) :
                        c.AddEntry ( e )
                        bAdded = True
                        break

            if bAdded == False :
                clusters.append ( Cluster (e) )

        debug("%d clusters" % len(clusters))

        cfits = []
        for c in clusters :
            cfits.append ( [c.corr, c.M, c.regs, c.stats] )

        return cfits




    def saFitMapToPoints_byRot ( self, fmap, points, dmap, N=10, M=10 ) :

        debug("fitting %s in map %s, to %d points, by rotation" % (fmap.name, dmap.name, len(points)))

        num = self._rota_search_num.value
        N = int ( numpy.floor ( numpy.sqrt ( num ) ) )
        M = int ( numpy.floor ( num / N ) )

        fpoints, fpoint_weights = fit_points ( fmap, (not self._use_laplace.enabled) )

        debug("%d fits - rotations %d axes, %d angles" % (num, N, M))
        alist = uniform_rotation_angles(N, M)

        COM, U, S, V = prAxes ( points )
        from chimerax.geometry import translation
        comT = translation(COM)

        mlist = [comT*rotation_from_angles(*angles)*fmap.preM for angles in alist]

        from math import pi
        names = ['theta %.0f, phi %.0f, rot %.0f'
                 % tuple([a*180/pi for a in a3]) for a3 in alist]
        status_text = 'Rotational fit'

        optimize = self._optimize_fits.enabled

        fits = optimize_fits(fpoints, fpoint_weights, mlist, dmap,
                             names, status_text, optimize)
        corr, Mfit, i = self.make_best_fit(fits, fmap, dmap)

        debug(" - best fit: %f\n" % ( corr, ))


    def make_best_fit(self, fits, fmap, dmap):

        i = numpy.argmax([c for Mf,c,stats in fits])
        Mfit, corr, stats = fits[i]       # highest correlation fit
        fmap.fit_score = corr
        fmap.M = Mfit

        list_fits = [(c, Mf, fmap.fit_regions, stats) for Mf,c,stats in fits]
        self.fits.extend(list_fits)

        move_fit_models(fmap, Mfit, dmap.scene_position)

        return corr, Mfit, i


    def MoleculeMap ( self, create = True, warn = True ) :

        fmol = self._struct_to_fit

        if hasattr(fmol, 'fitting_map'):
            if fmol.fitting_map.deleted:
                delattr(fmol, 'fitting_map')
            else:
                return fmol.fitting_map
        if create:
            fmol.fitting_map = self.GenStrucMap(show = False)
            return fmol.fitting_map
        return None




    def GroupAroundReg ( self, smod, regs, target_volume, bRad=-1.0 ) :

        dv_rgroups = []
        maxDepthReached = 0

        stack = [([reg], reg.enclosed_volume(), 0) for reg in regs]

        self.status ( "Making groups around %d regions" % len(regs) )

        while len(stack) > 0 :

            regs, vol_at, depth_at = stack.pop()

            if depth_at > maxDepthReached : maxDepthReached = depth_at

            if depth_at >= SAF_LS_DEPTH : continue
            if vol_at >= target_volume * (1.0 + SAF_DVOL)  : continue

            dv = abs ( vol_at - target_volume ) / target_volume
            dv_rgroups.append ( [dv, regs] )

            if len(dv_rgroups) % 100 == 0 :
                self.status ( "Making groups around %d - %d groups" % (reg.rid, len(dv_rgroups)) ),

            reg_at = regs[0]
            for cr in reg_at.contacting_regions():
                if regs.count ( cr ) != 0 : continue
                if cr.placed : continue
                vol = vol_at + cr.enclosed_volume()
                stack.insert ( 0, [ [cr]+regs, vol, depth_at+1 ] )

        dv_rgroups_f = self.FilterGroups ( dv_rgroups, bRad )

        debug(" - %d groups --> %d filtered groups" % (len(dv_rgroups), len(dv_rgroups_f)))
        return [dv_rgroups_f, maxDepthReached]





    def FilterGroups ( self, dv_rgroups, bRad = -1.0 ) :

        dv_rgroups_f = []
        len_groups = {}
        inc_regs_map = {}

        gi, ngroups = 0, len(dv_rgroups)

        for dv, regs in dv_rgroups :

            gi = gi + 1
            if gi % 100 == 0 :
                self.status ( "Filtering group %d/%d" % (gi,ngroups) )

            if dv > SAF_DVOL : continue

            included = False

            regs.sort(key = lambda r: r.rid)
            inc_regs_at = inc_regs_map
            for reg in regs :
                try : included, inc_regs_at = inc_regs_at[reg]
                except : included = False; break

            if included : continue

            if bRad > 0.0 :
                regs_bRad = regions_radius(regs)

                brad_d = abs ( regs_bRad - bRad ) / bRad

                if brad_d > SAF_DBRAD : continue

            dv_rgroups_f.append ( [dv, regs] )

            inc_regs_at = inc_regs_map
            last_arr = None
            for reg in regs :
                try :
                    last_arr = inc_regs_at[reg]
                    inc_regs_at = last_arr[1]
                except :
                    last_arr = [ False, {} ]
                    inc_regs_at[reg] = last_arr
                    inc_regs_at = last_arr[1]

            last_arr[0] = True


        return dv_rgroups_f




    def GroupAllRegions ( self, smod, target_volume, bRad=-1.0) :

        dv_rgroups = []
        maxDepthReached = 0

        self.status("Grouping %d regions in %s, target volume %.2f, bounding radius %.2f" % (
            len(smod.region_surfaces), smod.name, target_volume, bRad ))

        ri, nregs = 0, len(smod.regions)

        for reg in smod.regions :

            ri = ri + 1

            dv_rgroupsR, maxDepthReachedR = self.GroupAroundReg ( smod, [reg], target_volume, bRad )

            dv_rgroups = dv_rgroups + dv_rgroupsR

            if maxDepthReachedR > maxDepthReached : maxDepthReached = maxDepthReachedR


        debug("\n - max depth reached: %d" % maxDepthReached)

        debug(" - filtering %d groups..." % len( dv_rgroups ))
        return self.FilterGroups ( dv_rgroups, bRad )



    def FitMapToSelRGroup ( self, dmap = None ) :

        if dmap is None:
            dmap = self.segmentation_map
            if dmap == None : debug("No segmentation map"); return

        fmap = self.map_to_fit
        if fmap is None:
            fmap = self.MoleculeMap()

        thr = fmap.minimum_surface_level
        mm = fmap.data.matrix()
        mmab = numpy.where ( mm > thr, numpy.ones_like(mm), numpy.zeros_like(mm) )
        nz = numpy.shape ( numpy.nonzero ( mmab ) )[1]
        tvol = float(nz) * fmap.data.step[0] * fmap.data.step[1] * fmap.data.step[2]
        debug("%s - %d above %f, volume %.3f" % (fmap.name, nz, thr, tvol))

        smod = self.CurrentSegmentation()
        if smod == None : return

        regs = smod.selected_regions()
        if len(regs)==0 : self.status ( "Please select a region to fit to" ); return

        reportFitRegions(fmap.name, regs)

        for reg in regs:
            clr = reg.color
            reg.show_transparent( REG_OPACITY )
        debug("")

        points = numpy.concatenate ( [r.map_points()
                                      for r in regs], axis=0 )
        regions_vol = sum([r.enclosed_volume() for r in regs])

        dv = abs(regions_vol - tvol) / tvol
        debug(" - regions volume: %.2f - dv %.5f" % (regions_vol, dv))

        self.fits = []
        fmap.fit_regions = regs

        to_map = dmap
        reg_map = None
        if 1 :
            reg_map = mask_volume( regs, dmap )


        bCloseMap = False

        if self._use_laplace.enabled :
            self.status ("Generating Laplace version of " + dmap.name)
            from chimerax.map_filter import laplacian
            to_map = laplacian ( dmap )
            bCloseMap = True

        elif self._mask_map_when_fitting.enabled :
            to_map = reg_map
            bCloseMap = True
            if to_map is None:
                self.status ('Could not create masked map')
                return

        if self._rota_search.enabled:
            self.saFitMapToPoints_byRot ( fmap, points, to_map )
        else :
            self.saFitMapToPoints ( fmap, points, to_map )

        self.cfits = self.ClusterFits ( self.fits )
        self.cfits.sort ( reverse=True, key=lambda x: x[0] )
        #cfits.sort()
        #cfits.reverse()

        try : nToAdd = self._num_fits_to_add.value
        except : nToAdd = len (self.cfits)
        for corr, M, regions, stats in self.cfits [ 0 : nToAdd ] :
            debug(" -- clustered Fit -- #fits:%d maxAngle:%.1f maxShift:%.2f maxHeight:%.2f" % ( stats['numFits'], stats['maxAngle'], stats['maxShift'], stats['maxHeight'] ))
            fmap.fit_score, fmap.M, fmap.fit_regions = corr, M, regions
            fmap.atomInclusion, fmap.bbAtomInclusion, fmap.bbClashes, fmap.hdoScore  = self.FitScores ( fmap, reg_map )
            self.add_fit (fmap, dmap)

        move_fit_models(fmap, self.cfits[0][1], dmap.scene_position)

        #self.status ( "Cross-correlation: %.4f\n" % (fmap.fit_score) )
        self.ReportZScore ( self.cfits )

        # close masked map if it was created
        #if bCloseMap : close_models ( [to_map] )
        close_models ( [reg_map] )

        for m in fmap.mols :
            m.display = True





    def MapIndexesInMap ( self, ref_map, mask_map ) :

        thr = mask_map.minimum_surface_level
        mm = mask_map.data.matrix()
        mm = numpy.where ( mm > thr, mm, numpy.zeros_like(mm) )

        nze = numpy.nonzero ( mm )

        # copy is needed! transform_vertices requires contiguous array
        points =  numpy.empty ( (len(nze[0]), 3), numpy.float32)
        points[:,0] = nze[2]
        points[:,1] = nze[1]
        points[:,2] = nze[0]

        debug("Making map indices for %s in %s" % ( mask_map.name, ref_map.name ))
        debug(" - %d points above %.3f" % ( len(points), thr ))

        # transform to index reference frame of ref_map
        f1 = mask_map.data.ijk_to_xyz_transform
        f2 = mask_map.scene_position
        f3 = ref_map.scene_position.inverse()
        f4 = ref_map.data.xyz_to_ijk_transform

        tf = f4 * f3 * f2 * f1
        tf.transform_points ( points, in_place = True )

        imap = set()
        for fi, fj, fk in points :
            for i in [ int(numpy.floor(fi)), int(numpy.ceil(fi)) ] :
                for j in [ int(numpy.floor(fj)), int(numpy.ceil(fj)) ] :
                    for k in [ int(numpy.floor(fk)), int(numpy.ceil(fk)) ] :
                        imap.add((i,j,k))

        return imap


    def ZeroMatWitMap ( self, ref_mat, ref_map, mask_map ) :

        thr = mask_map.minimum_surface_level
        mm = mask_map.data.matrix()
        mm = numpy.where ( mm > thr, mm, numpy.zeros_like(mm) )

        nze = numpy.nonzero ( mm )

        # copy is needed! transform_vertices requires contiguous array
        points =  numpy.empty ( (len(nze[0]), 3), numpy.float32)
        points[:,0] = nze[2]
        points[:,1] = nze[1]
        points[:,2] = nze[0]

        debug("Making map indices for %s in %s" % ( mask_map.name, ref_map.name ))
        debug(" - %d points above %.3f" % ( len(points), thr ))

        # transform to index reference frame of ref_map
        f1 = mask_map.data.ijk_to_xyz_transform
        f2 = mask_map.scene_position
        f3 = ref_map.scene_position.inverse()
        f4 = ref_map.data.xyz_to_ijk_transform

        tf = f4 * f3 * f2 * f1
        tf.transform_points ( points, in_place = True )

        imap = set()
        for fi, fj, fk in points :
            for i in [ int(numpy.floor(fi)), int(numpy.ceil(fi)) ] :
                for j in [ int(numpy.floor(fj)), int(numpy.ceil(fj)) ] :
                    for k in [ int(numpy.floor(fk)), int(numpy.ceil(fk)) ] :
                        #imap.add((i,j,k))
                        try :
                            ref_mat[k,j,i] = 0
                        except :
                            pass







    def OverlappingRegions ( self, dmap, fmap, smod, hide_others = True ) :

        imap = self.MapIndexesInMap ( dmap, fmap )
        debug('imap', len(imap))

        try : fmap.COM
        except : fmap.COM = fmap.mols[0].COM; fmap.bRad = fmap.mols[0].BoundRad

        p = numpy.array ( [ fmap.COM ], numpy.float32 )
        fmap.scene_position.transform_points ( p, in_place = True )
        dmap.scene_position.inverse().transform_points ( p, in_place = True )
        f_COM = p[0]
        f_bRad = fmap.bRad
        debug(" center", f_COM, "brad", f_bRad)

        jregs = []

        for r in smod.regions :

            if r.placed:
                continue

            ipoints = r.points()
            noverlap = 0
            for i,j,k in ipoints :
                if (i,j,k) in imap:
                    noverlap += 1

            ov = float(noverlap) / len(ipoints)

            if ov > .8 :
                jregs.append ( r )

            try :
                if ov > r.max_ov :
                    r.max_ov = ov
                    r.max_ov_cid = fmap.chain_id
                    r.max_ov_bioM = smod.bio_mt_at
            except :
                pass


        oregs = jregs

        self.status ( "Found %d regions overlapping" % len(oregs) )
        sel_sps = []

        for sp in smod.region_surfaces :
            if oregs.count ( sp.region ) > 0 :
                sp.region.show_transparent( REG_OPACITY )
                sp.display = True
                sel_sps.append ( sp )
            else :
                sp.region.show_transparent( 1 )
                sp.display = not hide_others

        return jregs





    def ShowOverlappingRegions ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        fmap = self.MoleculeMap()
        if fmap == None : return


        oregs = self.OverlappingRegions ( dmap, fmap, smod )

        return oregs




    def FitMapToGroupsAround ( self, fmap, smod, regs, dmap, bFirst = True ) :

        bestFitScore = -1e99
        bestFitM = None
        bestFitGroup = None
        bestFitRegions = None
        fmap.fit_score = None

        tvol = self.MapVolume ( fmap )
        bRad = -1.0 # fmap.mol.BoundRad / float(dmap.data.step[0]); # self.MapBoundingRad ( fmap )
        bRad = fmap.mols[0].BoundRad

        self.status("\nMaking groups around %d regions - target vol %.3f, b-Rad %.3f" % ( len(regs), tvol, bRad ))
        smod.rgroups, maxDepthReached = self.GroupAroundReg ( smod, regs, tvol, bRad )
        smod.rgroups.sort()
        debug(" - depth reached: %d" % maxDepthReached)

        if len(smod.rgroups) == 0 : self.status ( "No groups found" ); return -1e99

        nsearchgrps = min ( len(smod.rgroups), SAF_LS_NGROUPS )
        debug("________________________________________________________________________")
        self.status ( "Fitting %s to %d/%d groups..." % ( fmap.name, nsearchgrps, len(smod.rgroups) ) )
        debug("________________________________________________________________________")


        self.fits = []

        for i, dv_regs in enumerate ( smod.rgroups[0:nsearchgrps] ) :

            dv, regs = dv_regs

            self.status ( "Fitting to group %d/%d, dVolume %.4f, %d regions" % (i+1, nsearchgrps, dv, len(regs) ) )
            debug(" - regions:", end=' ')
            for r in regs : debug(r.rid, end=' ')
            debug("")

            fmap.fit_regions = regs

            points = numpy.concatenate ( [r.map_points() for r in regs], axis=0 )

            if self._rota_search.enabled :
                self.saFitMapToPoints_byRot ( fmap, points, dmap )
            else :
                self.saFitMapToPoints ( fmap, points, dmap )

            debug("")

            if fmap.fit_score > bestFitScore :
                bestFitScore = fmap.fit_score
                bestFitM = fmap.M
                bestFitRegions = regs

        self.status ( "Best cross-correlation: %.4f\n\n" % ( bestFitScore ) )

        fmap.fit_score = bestFitScore
        fmap.M = bestFitM
        fmap.fit_regions = bestFitRegions

        xfA = dmap.scene_position * fmap.M
        fmap.scene_position = xfA
        for mol in fmap.mols : mol.scene_position = xfA

        self.cfits = self.ClusterFits ( self.fits )
        #cfits.sort ( reverse=True, key=lambda x: x[0] )
        self.cfits.sort()
        self.cfits.reverse()

        try : nToAdd = self._num_fits_to_add.value
        except : nToAdd = len (self.cfits)

        for corr, M, regions, stats in self.cfits [ 0 : nToAdd ] :
            fmap.fit_score, fmap.M, fmap.fit_regions = corr, M, regions
            fmap.atomInclusion, fmap.bbAtomInclusion, fmap.bbClashes, fmap.hdoScore  = self.FitScores ( fmap )
            self.add_fit (fmap, dmap)
            # TODO - add atom inclusion comp

        #self.status ( "Cross-correlation: %.4f\n" % (fmap.fit_score) )
        self.ReportZScore ( self.cfits )


    def FitMapToRegionsAroundSel ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        smod = self.CurrentSegmentation()
        if smod is None : return

        regs = smod.selected_regions()

        fmap = self.MoleculeMap()
        if fmap == None : return

        if timing: t0 = clock()
        self.FitMapToGroupsAround ( fmap, smod, regs, dmap )
        if timing:
            t1 = clock()
            debug("Time: %.1f sec" % (t1-t0,))

        if fmap.fit_score is None:
            self.status('No groups of regions meet size requirement')
            return

        oregs = self.OverlappingRegions ( dmap, fmap, smod, hide_others = False )

        if len(oregs) == 1 :
            oregs[0].placed = True


    def FitOpenMapsToGroupsAround ( self, smod, reg, dmap, bFirst=True ) :

        bestFitScore = -1e99
        bestFitMap = None
        bestFitM = None

        fmaps = []

        # TODO: Don't use "centered" to decide what maps to fit.
        for fmap in OML() :
            try : fmap.mols[0].centered
            except : continue
            fmap.display = False
            for mol in fmap.mols : mol.display = False
            fmaps.append ( fmap )


        for fmap in fmaps :

            debug("\n****************************************************")
            debug("Fitting: ", fmap.name)
            debug("****************************************************\n")

            for mol in fmap.mols : mol.display = True

            self.FitMapToGroupsAround ( fmap, smod, reg, dmap, bFirst )

            if fmap.fit_score == None :
                debug(" - no fits for map", fmap.name)

            elif fmap.fit_score > bestFitScore :
                bestFitScore = fmap.fit_score
                bestFitMap = fmap
                bestFitM = fmap.M

            for mol in fmap.mols : mol.display = False


        if bestFitM == None :
            debug("No best fit recorded, perhaps there were not groups to start with")
            return None

        fmap = bestFitMap
        for mol in fmap.mols : mol.display = True

        debug("\n**********************************************************")
        debug("Best fit score was %.4f for %s" % (bestFitScore, fmap.name))
        debug("**********************************************************\n")
        fmap.M = bestFitM

        xfA = dmap.scene_position * fmap.M
        fmap.scene_position = xfA
        for mol in fmap.mols : mol.scene_position = xfA

        oregs = self.OverlappingRegions ( dmap, fmap, smod, hide_others = False  )

        if oregs.count ( reg ) == 0 :
            debug("Overlapping regions not inclusive")
            return False


        if len(oregs) > 1 :
            jreg = smod.join_regions ( oregs )
            jreg.placed = True
            self.ReportRegionCount(smod)

            jsp = jreg.surface_piece
            jreg.show_transparent( REG_OPACITY )
            jsp.display = False

        elif len(oregs) == 1 :
            oregs[0].placed = True
            oregs[0].surface_piece.display = False

        else :
            for mol in fmap.mols : mol.display = False
            return False

        for mol in fmap.mols : mol.display = False

        self.add_fit(fmap, dmap)

        return True



    def FitMapsToRGroups ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        smod = self.CurrentSegmentation()
        if smod == None : return

        for sp in smod.region_surfaces :
            sp.region.show_transparent( REG_OPACITY )
            sp.display = False


        if timing: t0 = clock()

        while 1 :

            sp = None
            for spi in smod.region_surfaces :

                try :
                    spi.region.placed.display = False
                    spi.region.show_transparent( REG_OPACITY )
                    spi.display = True
                    spi.region.placed.display = True
                    spi.display = False

                except :
                    pass

                if spi.region.placed == False :
                    sp = spi
                    break

            if sp == None :
                debug("\nAll regions have maps placed")
                break

            clr = sp.region.color
            sp.region.show_transparent( REG_OPACITY )
            sp.display = True

            if self.FitOpenMapsToGroupsAround ( smod, sp.region, dmap, False ) == False :
                debug("___ No map fit for region! ___", sp.region.rid, sp.region.enclosed_volume())
                sp.failed_fit = True

            sp.region.placed = True


        if timing:
            t1 = clock()
            debug("Time: %.1f sec" % (t1-t0))

        for sp in smod.region_surfaces :
            try : sp.failed_fit
            except : continue
            debug("Region %d failed fit and still in model" % sp.region.rid)



    def MapVolume ( self, fmap ) :

        thr = fmap.minimum_surface_level
        mm = fmap.data.matrix()
        mmab = numpy.where ( mm > thr, numpy.ones_like(mm), numpy.zeros_like(mm) )
        nz = numpy.shape ( numpy.nonzero ( mmab ) )[1]
        vvol = fmap.data.step[0] * fmap.data.step[1] * fmap.data.step[2]
        tvol = vvol * float(nz)
        debug("%s - %d above %f, VOLUME %.3f" % (fmap.name, nz, thr, tvol))
        return tvol


    def Scores ( self ) :

        fmap = self.MoleculeMap()
        if fmap == None : return

        self.FitScores ( fmap )


    def SMS ( self ) :

        dmap = self.segmentation_map
        if dmap == None :
            debug("No segmentation map");
            return

        fmap = self.MoleculeMap()
        if fmap == None : return

        sms = ShapeMatchScore ( self._backbone_atoms(fmap.mols[0]), dmap )


    def _backbone_atoms(self, mol):
        atoms = mol.atoms
        anames = atoms.names
        from chimerax.atomic import concatenate, Atoms
        bbatoms = concatenate([atoms.filter(anames == 'C'),
                               atoms.filter(anames == 'N'),
                               atoms.filter(anames == 'CA')], Atoms)
        return bbatoms

    def VisiScores ( self ) :

        msg = ["Visi scores..."]
        dmap = self.segmentation_map
        if dmap == None :
            return

        msg.append(" - in map: " + dmap.name)

        molmap = None
        mols = []

        from chimerax.map import Volume
        from chimerax.atomic import Structure
        for m in self._all_models :
            if m.display == False :
                continue
            if isinstance(m, Structure) :
                msg.append(" - mol: " + m.name)
                mols.append ( m )
            if isinstance(m, Volume) :
                msg.append(" - map: " + m.name)
                molmap = m

        if molmap != None :
            fpoints, fpoint_weights = fit_points(molmap, True)
            map_values = dmap.interpolated_values ( fpoints, molmap.scene_position )
            olap, corr = overlap_and_correlation ( fpoint_weights, map_values )
            msg.append(" - Overlap: %f, Cross-correlation: %f" % (olap, corr))



        otherPoints = numpy.concatenate ( [m.atoms.scene_coords for m in mols], axis=0 )
        from chimerax import atomic
        otherAtoms = atomic.concatenate([m.atoms for m in mols], atomic.Atoms)

        # debug "Doing tree with %d %d" % ( len(otherPoints), len(otherAtoms) )

        msg.append(" - making tree, %d atoms" % len(otherAtoms))

        from chimerax.geometry import AdaptiveTree
        searchTreeAll = AdaptiveTree (otherPoints.tolist(), otherAtoms, 4.0)

        msg.append(" - checking clashes, %d atoms" % len(otherAtoms))

        numClash = 0.0
        for at in otherAtoms :
            nearby = searchTreeAll.search_tree ( at.scene_coord, 3.0 )
            for nb in nearby :
                if nb.structure != at.structure :
                    numClash = numClash + 1.0
                    break

        bbClashes = numClash / float ( len(otherAtoms) )

        msg.append(" - clashes: %.0f/%.0f = %0.3f clash-free" % (numClash, len(otherAtoms), 1.0-bbClashes))

        self.session.logger.info('\n'.join(msg))




    def FitScores ( self, fmap, regionMap = None ) :

        dmap = self.segmentation_map
        if dmap == None :
            debug("No segmentation map");
            return [0.0, 0.0, 0.0, 0.0]

        debug("Fit scores for", fmap.name, "in", dmap.name)

        import numpy

        # move fmap (and structures) to fmap.M if it's there
        # (it's not there if we do scores for a selected structure
        # that hasn't been fit yet)
        try : fmap.M; move = True
        except : move = False

        if move :
            xf = dmap.scene_position * fmap.M
            fmap.scene_position = xf
            for mol in fmap.mols :
                mol.scene_position = xf


        # ---------------------------------------------------------------
        # Cross-correlation
        # ---------------------------------------------------------------
        fpoints, fpoint_weights = fit_points(fmap)
        map_values = dmap.interpolated_values ( fpoints, fmap.scene_position )
        olap, corr = overlap_and_correlation ( fpoint_weights, map_values )
        debug(" - Overlap: %f, Cross-correlation: %f" % (olap, corr))


        # ---------------------------------------------------------------
        # By-residue cross-correlation
        # ---------------------------------------------------------------
        if 0 :
            cc_by_residue ( fmap, dmap, 16 )


        # ---------------------------------------------------------------
        # Atom inclusion -- all atoms
        # ---------------------------------------------------------------
        backbone_atoms = []
        allIncl = 0.0
        bbIncl = 0.0
        bbClashes = 0.0

        from chimerax.atomic import concatenate, Atoms
        all_atoms = concatenate([mol.atoms for mol in fmap.mols], Atoms)
        numAllAtoms = float ( len(all_atoms) )

        if len(all_atoms) == 0 :
            return [0.0, 0.0, 0.0, 0.0]

        #dmapXfInv = dmap.scene_position.inverse()
        #transform_vertices( points, dmapXfInv )
        points = all_atoms.scene_coords
        from chimerax.geometry import Place
        dvals = dmap.interpolated_values ( points, Place() )
        min_d = dmap.minimum_surface_level
        dvals = numpy.where ( dvals > min_d, dvals, numpy.zeros_like(dvals) )
        nze = numpy.nonzero ( dvals )
        allIn = float(len(nze[0]))
        allIncl = allIn / numAllAtoms

        debug(" - Atom inclusion: %.0f/%.0f = %.3f" % ( allIn, numAllAtoms, allIncl ))

        # ---------------------------------------------------------------
        # Atom inclusion -- backbone atoms
        # ---------------------------------------------------------------
        bbIncl = 0.0

        backbone_atoms = self._backbone_atoms(fmap.mols[0])

        if len(backbone_atoms) > 0 :

            points = backbone_atoms.scene_coords
            #dmapXfInv = dmap.scene_position.inverse()
            #transform_vertices( points, dmapXfInv )
            dvals = dmap.interpolated_values ( points, Place() )
            min_d = dmap.minimum_surface_level
            dvals = numpy.where ( dvals > min_d, dvals, numpy.zeros_like(dvals) )
            nze = numpy.nonzero ( dvals )
            bbIn = float(len(nze[0]))
            numBBAtoms = float(len(backbone_atoms))
            bbIncl = bbIn / numBBAtoms
            debug(" - BB Atom inclusion: %.0f/%.0f = %.3f" % (bbIn, numBBAtoms, bbIncl ));


        if 0 :
            sms = ShapeMatchScore ( backbone_atoms, dmap )


        # ---------------------------------------------------------------
        # Coverage of high-density areas - Density Occupancy
        # ---------------------------------------------------------------

        hdo = 0.0
        if regionMap :
            #fpoints, fpoint_weights = fit_points ( regionMap )
            #nz_fpoints = len(fpoints)

            nz_fpoints = len ( numpy.nonzero ( regionMap.data.full_matrix() )[0] )

            regionMap.scene_position.inverse().transform_points( points, in_place = True )
            s = regionMap.data.step[0]
            from chimerax.map_data import zone_masked_grid_data
            mdata = zone_masked_grid_data ( regionMap.data, points, numpy.sqrt(3*s*s) )
            #gv = volume_from_grid_data ( mdata )
            #gv.scene_position = dmap.scene_position
            #gv.name = "Masked"

            mat = mdata.full_matrix()
            nz_mdata = len ( numpy.nonzero ( mat )[0] )
            if nz_fpoints > 0 :
                hdo = float (nz_mdata) / float(nz_fpoints)
                debug(" - Density Occupancy: %d / %d grid points above %.3f occupied (%.4f)" % (
                    nz_mdata, nz_fpoints, dmap.minimum_surface_level, hdo ))
        else :
            debug(" - not computing density occupancy")


        # ---------------------------------------------------------------
        # Clashes with symmetric copies
        # ---------------------------------------------------------------
        if self._calc_symmetry_clashes.enabled :

            symMols = self.PlaceSym ()
            if symMols:

                otherPoints = numpy.concatenate([m.atoms.scene_coords for m in symMols], axis=0)
                from chimerax.atomic import concatenate, Atoms
                otherAtoms = concatenate([m.atoms for m in symMols], Atoms)

                # debug "Doing tree with %d %d" % ( len(otherPoints), len(otherAtoms) )

                from chimerax.geometry import AdaptiveTree
                searchTreeAll = AdaptiveTree (otherPoints.tolist(), otherAtoms, 4.0)

                #if len ( backbone_atoms ) == 0 :
                #    sel_str = "#%d@C,N,CA" % fmap.mols[0].id
                #    sel = chimera.selection.OSLSelection (sel_str)
                #    backbone_atoms = sel.atoms()

                numClash = 0.0
                for at in all_atoms :
                    nearby = searchTreeAll.search_tree ( at.scene_coord, 3.0 )
                    if len(nearby) > 0 :
                        numClash = numClash + 1.0

                bbClashes = numClash / numAllAtoms

                self.session.models.close ( symMols )

                debug(" - Clashes with symmetric copies: %.0f/%.0f = %0.3f" % (numClash, numAllAtoms, bbClashes));

        debug(fmap.name, corr, allIncl, bbClashes, hdo)

        #for i in range ( 1 ) :
        #    debug (frame_at+i),
        #    chimera.debuger.saveImage ( "./frames/%06d.png" % (frame_at + i) )
        #debug ""

        return [allIncl, bbIncl, bbClashes, hdo]


    def FitMapToRGroups ( self ) :

        debug("_______________________________________________________________")

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = self.MoleculeMap()
        if fmap == None : return
        tvol = self.MapVolume ( fmap )

        smod = self.CurrentSegmentation()
        if smod is None : return

        debug("---")

        if timing: t0 = clock()

        bRad = fmap.mols[0].BoundRad

        smod.rgroups = self.GroupAllRegions ( smod, tvol, bRad )
        smod.rgroups.sort(key = lambda vr: vr[0])

        bestFitScore = -1e99
        bestFitM = None

        debug("Got %d groups..." % (len(smod.rgroups) ))

        dmap_name = os.path.splitext ( dmap.name )[0]
        path = os.path.dirname ( dmap.data.path ) + os.path.sep

        nsearchgrps = min ( MAX_NUM_GROUPS, len(smod.rgroups) )
        if nsearchgrps == 0:
            self.status('No groups of regions meet size requirement')
            return

        self.fits = []

        for i, dv_regs in enumerate ( smod.rgroups [0:nsearchgrps] ) :

            dv, regs = dv_regs

            self.status ( "Fitting to group %d/%d, dVolume %.4f, %d regions" % (i+1, nsearchgrps, dv, len(regs) ) )
            debug(" - regions:", end=' ')
            for r in regs : debug(r.rid, end=' ')
            debug("")

            for sp in smod.region_surfaces :
                if regs.count ( sp.region ) > 0 :
                    sp.display = True
                    sp.region.show_transparent( REG_OPACITY )

                else : sp.display = False

            fmap.fit_regions = regs

            # TODO: points need to be in dmap coordinates.
            points = numpy.concatenate ( [r.map_points()
                                          for r in regs], axis=0 )
            if self._rota_search.enabled :
                self.saFitMapToPoints_byRot ( fmap, points, dmap )
            else :
                self.saFitMapToPoints ( fmap, points, dmap )

            if fmap.fit_score > bestFitScore :
                bestFitScore = fmap.fit_score
                bestFitM = fmap.M
                bestFitRegs = regs

        self.status ( "Best cross-correlation: %.4f\n\n" % ( bestFitScore ) )

        fmap.fit_score = bestFitScore
        fmap.M = bestFitM

        xfA = dmap.scene_position * fmap.M
        fmap.scene_position = xfA
        for mol in fmap.mols : mol.scene_position = xfA

        if timing:
            t1 = clock()
            debug("Time: %.1f sec" % (t1-t0))

        oregs = self.OverlappingRegions ( dmap, fmap, smod, hide_others = False  )

        self.cfits = self.ClusterFits ( self.fits )
        self.cfits.sort ( reverse=True, key=lambda x: x[0] )
        #cfits.sort()
        #cfits.reverse()

        try : nToAdd = self._num_fits_to_add.value
        except : nToAdd = len (self.cfits)

        for corr, M, regions, stats in self.cfits [ 0 : nToAdd ] :
            fmap.fit_score, fmap.M, fmap.fit_regions = corr, M, regions
            fmap.atomInclusion, fmap.bbAtomInclusion, fmap.bbClashes, fmap.hdoScore  = self.FitScores ( fmap )
            self.add_fit (fmap, dmap)
            # TODO - add atom inclusion comp

        #self.status ( "Cross-correlation: %.4f\n" % (fmap.fit_score) )
        self.ReportZScore ( self.cfits )




    def GetMapFromMolRes ( self, mol, cid, rStart, rEnd ) :

        sel_str = "#%s/%s:%d-%d" % (mol.id_string, cid, rStart, rEnd)
        debug("[%s]" % (sel_str), end=' ')

        res, grid = self._sim_res_and_grid

        cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
        self._run_command ( cmd )

        mv = None
        for mod in self._all_models :
            ts = mod.name.split()
            if len(ts) > 1 and mod.name.find("map") >=0 and mod.name.find("res") >=0 :
                #debug " - found", mod.name
                mv = mod
                mv.name = "_" + sel_str
                break

        if mv == None :
            self.status (" - error - could not find chain map")

        return mv


    @property
    def _all_models(self):

        return self.session.models.list()

    def GetMapFromMolRanges ( self, mol, cid, ranges ) :

        sel_str = "#%s:%s" % (mol.id_string, ranges)
        debug("[%s]" % (sel_str), end=' ')

        res, grid = self._sim_res_and_grid

        cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
        mv = self._run_command ( cmd )
        mv.name = "_" + sel_str

        return mv



    def GroupRegionsBySS ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        #fmap = self.MoleculeMap()
        #if fmap == None : return

        smod = self.CurrentSegmentation()
        if smod is None : return

        debug("---")

        #mol = fmap.mols[0]
        #debug mol.name

        #chain_colors = RandColorChains ( mol )

        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        from chimerax.atomic import Structure
        for mol in self._all_models :

            if not isinstance(mol, Structure) or mol.display == False : continue

            basename = os.path.splitext ( mol.name )[0]
            #chain_colors = RandColorChains ( mol )


            chainsRes = {}
            for res in mol.residues :
                try :
                    chainsRes[res.id.chainId].append ( res )
                except :
                    chainsRes[res.id.chainId] = [res]

            chainsList = list(chainsRes.keys())
            chainsList.sort()


            for chainId in chainsList :

                residues = chainsRes[chainId]

                debug(" - chain " + chainId + ", %d " % len(residues) + " residues")

                ss, rStart = "", 0
                rI = 0

                oRanges = ""

                while 1 :
                    res = residues[rI]

                    if rStart == 0 :
                        debug("  - at first res %d " % rI + ", pos: %d " % res.id.position, end=' ')

                        rStart = res.id.position
                        if res.isHelix :
                            debug(" - H")
                            ss = "H"
                        else :
                            debug("")
                            ss = ""

                    else :
                        #debug "  - at res %d " % rI + ", pos: %d " % res.id.position,

                        if res.isHelix :
                            #debug " - H "
                            if ss != "H" :
                                debug("  - _->H - at res %d " % rI + ", pos: %d " % res.id.position)
                                #mv = self.GetMapFromMolRes ( mol, chainId, rStart, res.id.position-1 )
                                #chain_maps.append ( [mv, self.MapIndexesInMap ( dmap, mv )] )
                                #mv.chain_id = basename + "_" + chainId + "_H%d" % rStart
                                if len(oRanges) > 0 : oRanges = oRanges + ","
                                oRanges = oRanges + "%d-%d.%s" % (rStart, res.id.position-1,chainId)
                                rStart = res.id.position
                                ss = "H"
                        else :
                            #debug ""
                            if ss == "H" :
                                debug("  - H->_ - at res %d " % rI + ", pos: %d " % res.id.position)
                                mv = self.GetMapFromMolRes ( mol, chainId, rStart, res.id.position-1 )
                                chain_maps.append ( [mv, self.MapIndexesInMap ( dmap, mv )] )
                                mv.chain_id = basename + "_" + chainId + "_%d" % rStart
                                rStart = res.id.position
                                ss = ""

                    rI += 1
                    if rI >= len(residues) :
                        debug("  - done chain " + chainId + " - at res %d " % rI + ", pos: %d " % res.id.position, end=' ')

                        if res.isHelix :
                            debug(" - H ")
                            mv = self.GetMapFromMolRes ( mol, chainId, rStart, res.id.position )
                            chain_maps.append ( [mv, self.MapIndexesInMap ( dmap, mv )] )
                            mv.chain_id = basename + "_" + chainId + "_" + ss + "%d" % rStart
                        else :
                            debug("")
                            if len(oRanges) > 0 : oRanges = oRanges + ","
                            oRanges = oRanges + "%d-%d.%s" % (rStart, res.id.position, chainId)


                        mv = self.GetMapFromMolRanges ( mol, chainId, oRanges )
                        chain_maps.append ( [mv, self.MapIndexesInMap ( dmap, mv )] )
                        mv.chain_id = basename + "_" + chainId

                        break;


            #break

        # debug chain_maps

        rgroups = {}

        debug(" - %d regions" % len(smod.regions))

        for ri, reg in enumerate ( smod.regions ) :

            if ri % 100 == 0 :
                debug(" %d/%d " % (ri+1, len(smod.regions) ))

            max_ov = 0.0
            max_ov_chm = None
            for chmImap in chain_maps :
                chm, imap = chmImap
                ipoints = reg.points()
                noverlap = 0
                for i,j,k in ipoints :
                    if (i,j,k) in imap:
                        noverlap += 1

                #debug " - ", chm.name, noverlap

                ov = float(noverlap) / reg.point_count()
                if ov > max_ov :
                    max_ov = ov
                    max_ov_chm = chm

            if max_ov_chm :
                try : rgroups[max_ov_chm.chain_id]
                except : rgroups[max_ov_chm.chain_id] = []
                rgroups[max_ov_chm.chain_id].append ( reg )


        from . import regions

        for chid, regs in rgroups.items () :
            debug("Chain %s - %d regions" % (chid, len(regs)))

            jregs = regions.TopParentRegions(regs)
            jreg = smod.join_regions ( jregs )
            jreg.make_surface(None, None, smod.regions_scale)


        close_models([m for m,i in chain_maps])


    def GroupRegionsByChains ( self ) :

        dmap = self.segmentation_map
        if dmap == None :
            self.status ( "Please choose map in Segment Dialog" )
            return

        #fmap = self.MoleculeMap()
        #if fmap == None : return

        smod = self.CurrentSegmentation()
        if smod is None :
            self.status ( "Please select a segmentation in Segment Dialog" )
            return

        debug("---")

        #mol = fmap.mols[0]
        #debug mol.name

        #chain_colors = RandColorChains ( mol )


        self.status ( "Grouping with chains... making chain maps..." )


        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        mols = []

        from chimerax.atomic import Structure
        for mol in self._all_models :

            if not isinstance(mol, Structure) or mol.display == False :
                continue

            mols.append ( mol )

        nchains = 0

        for i, mol in enumerate (mols) :

            ci = 1

            chain_ids = mol.residues.unique_chain_ids
            for cid in chain_ids :

                self.status ( "Grouping with chains... making map for chain %d/%d of mol %d/%d" % (ci,len(chain_ids),i+1,len(mols)) )
                ci += 1
                nchains += 1

                basename = os.path.splitext ( mol.name )[0]
                #cname = basename + "_" + cid
                cname = basename + "_" + cid
                #cname = basename.split ("__")[-1]

                sel_str = "#%s/%s" % (mol.id_string, cid)
                debug("%s [%s]" % (cname, sel_str), end=' ')

                cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
                mv = self._run_command ( cmd )
                mv.name = cname

                imap = self.MapIndexesInMap ( dmap, mv )

                chain_maps.append ( [mv, imap] )
                mv.chain_id = cname

            #break

        # debug chain_maps

        rgroups = {}

        debug(" - %d regions" % len(smod.regions))

        for ri, reg in enumerate ( smod.regions ) :

            if ri % 100 == 0 :
                self.status ( "Grouping regions... %d/%d " % (ri+1, len(smod.regions) ) )

            max_ov = 0.0
            max_ov_chm = None
            for chmImap in chain_maps :
                chm, imap = chmImap
                ipoints = reg.points()
                noverlap = 0
                for i,j,k in ipoints :
                    if (i,j,k) in imap:
                        noverlap += 1

                #debug " - ", chm.name, noverlap

                ov = float(noverlap) / reg.point_count()
                if ov > max_ov :
                    max_ov = ov
                    max_ov_chm = chm

            if max_ov_chm :
                try : rgroups[max_ov_chm.chain_id]
                except : rgroups[max_ov_chm.chain_id] = []
                rgroups[max_ov_chm.chain_id].append ( reg )


        #from .extract_region_dialog import dialog as exdialog
        base = ""
        if 0 and exdialog() != None :
            base = exdialog().saveMapsBaseName.get()

        from .regions import TopParentRegions
        for chid, regs in rgroups.items () :

            cid = chid.split("_")[-1]

            debug("Chain %s - %d regions -> %s" % (chid, len(regs), cid))

            jregs = TopParentRegions(regs)
            jreg = smod.join_regions ( jregs )
            jreg.make_surface(None, None, smod.regions_scale)
            jreg.chain_id = chid.split("_")[-1]
            #jreg.chain_id = chid

            if 0 and exdialog() != None :
                exdialog().saveMapsBaseName.set( base % cid )
                exdialog().Extract2 ( dmap, dmap, smod, [jreg] )


        close_models([m for m,i in chain_maps])

        self.status ( "Done - total %d chains in %d visible Molecules" % (nchains,len(mols)) )


    def MaskWithSel ( self ) :

        selats = chimera.selection.currentAtoms()
        debug("%d selected atoms" % len(selats))

        dmap = None
        for m in self._volumes :
            if m.display == True :
                dmap = m
                break

        if dmap == None :
            return

        debug("map: %s" % dmap.name)


        points = selats.scene_coords

        dmap.scene_position.inverse().transform_points ( points, in_place = True )

        s = dmap.data.step[0]
        s2 = numpy.sqrt ( s*s + s*s + s*s )
        from chimerax.map_data import zone_masked_grid_data
        mdata = zone_masked_grid_data ( dmap.data, points, numpy.sqrt(s2) )

        from chimerax.map_filter import gaussian
        gvm = gaussian.gaussian_convolution ( mdata.full_matrix(), (.1,.1,.1) )
        #gvm = gvol.full_matrix()

        from chimerax.map_data import ArrayGridData
        gdata = ArrayGridData ( gvm, dmap.data.origin, dmap.data.step, dmap.data.cell_angles, name = dmap.name + "_m" )
        from chimerax.map import volume_from_grid_data
        nvg = volume_from_grid_data ( gdata, self.session )
        nvg.name = dmap.name + "___"





    def GroupRegionsByMols ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        #fmap = self.MoleculeMap()
        #if fmap == None : return

        smod = self.CurrentSegmentation()
        if smod is None : return

        debug("---")

        #mol = fmap.mols[0]
        #debug mol.name

        #chain_colors = RandColorChains ( mol )

        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f ______________" % (res, grid))

        from chimerax.atomic import Structure
        for mol in self._all_models :

            if not isinstance(mol, Structure) or mol.display == False : continue

            basename = os.path.splitext ( mol.name )[0]
            cname = basename
            sel_str = "#%s" % (mol.id_string)
            debug("%s [%s]" % (mol.name, sel_str), end=' ')

            cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
            mv = self._run_command ( cmd )
            mv.name = cname

            imap = self.MapIndexesInMap ( dmap, mv )

            chain_maps.append ( [mv, imap] )
            mv.chain_id = cname

            #break

        # debug chain_maps

        rgroups = {}

        debug(" - %d regions" % len(smod.regions))

        for ri, reg in enumerate ( smod.regions ) :

            if ri % 100 == 0 :
                self.status ( " %d/%d " % (ri+1, len(smod.regions) ) )

            max_ov = 0.0
            max_ov_chm = None
            for chmImap in chain_maps :
                chm, imap = chmImap
                ipoints = reg.points()
                noverlap = 0
                for i,j,k in ipoints :
                    if (i,j,k) in imap:
                        noverlap += 1

                #debug " - ", chm.name, noverlap

                ov = float(noverlap) / reg.point_count()
                if ov > 0.8 and ov > max_ov :
                    max_ov = ov
                    max_ov_chm = chm

            if max_ov_chm :
                try : rgroups[max_ov_chm.chain_id]
                except : rgroups[max_ov_chm.chain_id] = []
                rgroups[max_ov_chm.chain_id].append ( reg )


        from . import regions

        for chid, regs in rgroups.items () :
            debug("Chain %s - %d regions" % (chid, len(regs)))

            jregs = regions.TopParentRegions(regs)
            jreg = smod.join_regions ( jregs )
            jreg.make_surface(None, None, smod.regions_scale)


        close_models([m for m,i in chain_maps])


    def GroupRegionsByFittedMols ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        #fmap = self.MoleculeMap()
        #if fmap == None : return

        smod = self.CurrentSegmentation()
        if smod is None : return

        debug("---")

        #mol = fmap.mols[0]
        #debug mol.name

        #chain_colors = RandColorChains ( mol )

        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        #lfits = self.selected_listbox_fits()

        lfits = self.list_fits

        if len(lfits) == 0:
            self.status ( "No selected fitted molecules" )
            return

        self.status('Looking at %d fitted molecules' % len(lfits))

        fit_i = 1
        for fit in lfits:
            for mol in fmap.mols :
                if mol.deleted:
                    self.status('Fit molecule was closed - ')
                    return

            self.place_molecule(fit.fit_map, fit.position, fit.target_map)

            mol = fit.fit_map.mols[0]

            basename = os.path.splitext ( mol.name )[0]
            cname = basename
            sel_str = "#%s" % (mol.id_string)
            debug("%s [%s]" % (mol.name, sel_str), end=' ')

            cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
            mv = self._run_command(cmd)
            mv.name = cname

            imap = self.MapIndexesInMap ( fit.target_map, mv )

            chain_maps.append ( [fit_i, imap] )
            #mv.chain_id = cname
            fit_i += 1
            close_models ( [mv] )

            #break

        # debug chain_maps

        rgroups = {}

        debug(" - %d regions" % len(smod.regions))

        for ri, reg in enumerate ( smod.regions ) :

            if ri % 1000 == 0 :
                #debug " %d/%d " % (ri, len(smod.regions) )
                self.status ( " %d/%d " % (ri, len(smod.regions) ) )

            max_ov = 0.1
            max_ov_chm = 0
            for chmImap in chain_maps :
                fit_i, imap = chmImap
                ipoints = reg.points()
                noverlap = 0
                for i,j,k in ipoints :
                    if (i,j,k) in imap:
                        noverlap += 1


                ov = float(noverlap) / reg.point_count()

                #debug " - fit %d to reg %d, num ov %d, ov %.2f " % (fit_i, ri, noverlap, ov)

                if ov > max_ov :
                    max_ov = ov
                    max_ov_chm = fit_i

            if max_ov_chm > 0 :
                try : rgroups[max_ov_chm]
                except : rgroups[max_ov_chm] = []
                rgroups[max_ov_chm].append ( reg )


        from . import regions

        debug(len( list(rgroups.keys()) ), "groups")

        sregs = []

        for chid, regs in rgroups.items () :
            debug("Fit %d - %d regions" % (chid, len(regs)))

            jregs = regions.TopParentRegions(regs)
            jreg = smod.join_regions ( jregs )
            sregs.append ( jreg )
            jreg.make_surface(None, None, smod.regions_scale)


        return

        #sel_regs = set ( smod.selected_regions() )
        surfs = [r.surface_piece for r in sregs
                 if not r in sel_regs and r.surface_piece]

        chimera.selection.clearCurrent ()
        chimera.selection.addCurrent ( surfs )

        smod.remove_regions ( regs, remove_children = True )




    def GroupRegionsByVisiMaps ( self ) :

        self.status ( "Grouping by visible maps..." )

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        #fmap = self.MoleculeMap()
        #if fmap == None : return

        smod = self.CurrentSegmentation()
        if smod is None : return

        debug("---")

        #mol = fmap.mols[0]
        #debug mol.name

        #chain_colors = RandColorChains ( mol )

        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        for mmap in self._volumes:

            if mmap.display == False : continue

            debug(" -- map: ", mmap.name)

            imap = self.MapIndexesInMap ( dmap, mmap )
            chain_maps.append ( [mmap, imap] )
            mmap.chain_id = mmap.name

            #break

        # debug chain_maps

        rgroups = {}

        debug(" - %d regions" % len(smod.regions))

        for ri, reg in enumerate ( smod.regions ) :

            if ri % 100 == 0 :
                self.status ( " %d/%d " % (ri+1, len(smod.regions) ) )
                debug(",", end=' ')

            max_ov = 0.0
            max_ov_chm = None
            for chmImap in chain_maps :
                chm, imap = chmImap
                ipoints = reg.points()
                noverlap = 0
                for i,j,k in ipoints :
                    if (i,j,k) in imap:
                        noverlap += 1

                #debug " - ", chm.name, noverlap

                ov = float(noverlap) / reg.point_count()
                if ov > max_ov :
                    max_ov = ov
                    max_ov_chm = chm

            if max_ov_chm :
                try : rgroups[max_ov_chm.chain_id]
                except : rgroups[max_ov_chm.chain_id] = []
                rgroups[max_ov_chm.chain_id].append ( reg )


        from . import regions
        debug(".")

        for chid, regs in rgroups.items () :
            debug("Chain %s - %d regions" % (chid, len(regs)))

            jregs = regions.TopParentRegions(regs)
            jreg = smod.join_regions ( jregs )
            jreg.make_surface(None, None, smod.regions_scale)

        self.status ( "Done grouping by visible maps" )


        #close_models( chain_maps )



        # -----------------------------------------------------------------------------------------------------


    def ZeroMapBySel ( self ) :

        debug("0")


    def ZeroMapByMols ( self ) :

        debug("0")



    def ZeroMapFittedMols ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        vmat = dmap.full_matrix().copy()

        debug("---")

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        #lfits = self.selected_listbox_fits()

        lfits = self.list_fits

        if len(lfits) == 0:
            self.status ( "No selected fitted molecules" )
            return

        self.status('Looking at %d fitted molecules' % len(lfits))


        for fit in lfits:

            for mol in fit.fit_map.mols :
                if mol.deleted:
                    self.status('Fit molecule was closed - ')
                    return

            self.place_molecule(fit.fit_map, fit.position, fit.target_map)

            mol = fit.fit_map.mols[0]

            basename = os.path.splitext ( mol.name )[0]
            cname = basename
            sel_str = "#%s" % (mol.id_string)
            debug("%s [%s]" % (mol.name, sel_str), end=' ')

            cmd = "molmap %s %f sigmaFactor 0.187 gridSpacing %f replace false" % ( sel_str, res, grid )
            mv = self._run_command ( cmd )
            mv.name = cname

            self.ZeroMatWitMap ( vmat, dmap, mv )
            close_models ( [mv] )

            #break

        # debug chain_maps

        nname = os.path.splitext(dmap.name)[0] + "_zeroed"

        from chimerax.map_data import ArrayGridData
        mgrid = ArrayGridData ( vmat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles, name=nname)
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( mgrid, self.session, show_data = False, show_dialog = False )
        nv.name = nname
        #nv.copy_settings_from(volume)
        nv.show()




    def ValuesInMap ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        dmat = dmap.full_matrix().copy()

        chain_maps = []

        res, grid = self._sim_res_and_grid

        debug("_____________ res %2f _______ grid %.2f _________________________________" % (res, grid))


        for mmap in self._volumes:

            if mmap.display == False : continue

            debug(" -- map: ", mmap.name)

            imap = self.MapIndexesInMap ( dmap, mmap )
            chain_maps.append ( [mmap, imap] )
            mmap.chain_id = mmap.name

            #break

        sumd = 0
        n = 0
        imap = set()
        values = []

        for cm, points in chain_maps :
            debug(" --- at map --- : " + cm.name)
            #n += len(points)
            for fi, fj, fk in points :
                val = dmat[fk,fj,fi]
                if val < 17 :
                    sumd += dmat[fk,fj,fi]
                    values.append ( dmat[fk,fj,fi] )
                    #debug dmat[fk,fj,fi]
                    n += 1.0

        avg = sumd / len(points)

        debug(" Average value: %.3f"%avg + " at %d"%len(points) + " points")

        return;

        import numpy
        min = numpy.min(values)
        amax = numpy.max(values)
        max = numpy.min ( [amax, 16] )
        d = 1
        debug("Min: %.2f, max: %.2f (%.2f), step %.2f, avg %.2f" % (min, amax, max, d, numpy.average(values)))
        buckets = numpy.zeros ( (max - min) / d )
        for v in values :
            if v > max :
                continue
            r = (v - min) / (max - min)
            bi = int ( numpy.floor ( r * (len(buckets)-1) ) )
            buckets[bi] += 1

        for bi, bnum in enumerate ( buckets ) :
            bv = float (bi) / float(len(buckets)) * (max - min) + min
            debug("%.1f,%d" % (bv,bnum))





    def MaskMapWithSel ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - got molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - got map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return

        df_mat = self.Map2Map ( fmap, dmap )

        debug(" - using surf level %.5f for mask" % fmap.minimum_surface_level)

        if 1 :

            res, grid = self._sim_res_and_grid

            s = dmap.data.step # A/pixel
            diag_l = numpy.sqrt ( s[0]*s[0] + s[1]*s[1] + s[2]*s[2] ) # A/pixel
            num_it = res / diag_l # how many iterations will reach the desired width
            numit = int ( numpy.ceil ( num_it ) )

            debug(" - using res %.4f for dropoff, diag is %.3f, #it: %d" % (res, diag_l, numit))

            in_mask = numpy.where ( df_mat > fmap.minimum_surface_level, numpy.ones_like(df_mat), numpy.zeros_like(df_mat) )
            out_mask = numpy.where ( in_mask > 0, numpy.zeros_like(in_mask), numpy.ones_like(in_mask) )
            gvm = in_mask.copy();
            for i in range (numit) :
                nv_1 = numpy.roll(gvm, 1, axis=0)
                nv_2 = numpy.roll(gvm, -1, axis=0)
                nv_3 = numpy.roll(gvm, 1, axis=1)
                nv_4 = numpy.roll(gvm, -1, axis=1)
                nv_5 = numpy.roll(gvm, 1, axis=2)
                nv_6 = numpy.roll(gvm, -1, axis=2)
                gvm = 1.0/6.0 * ( nv_1 + nv_2 + nv_3 + nv_4 + nv_5 + nv_6 )
                gvm = out_mask * gvm + in_mask
                self.status ("Adding drop-off - iteration %d" % i)

            df_mat = gvm


        mmat = dmap.data.full_matrix() * df_mat

        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles, name=(dmap.name + "__MaskedWith__" + fmap.name) )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )


        if 0 :
            mapMean, mapStDev = MapStats ( df_v )
            df_v = AddNoiseToMap ( df_v, mapMean, mapStDev / 3.0 )


        df_v.name = dmap.name + "__MaskedWith__" + fmap.name
        df_v.scene_position = dmap.scene_position





        # -----------------------------------------------------------------------------------------------------




    def MolOrMapSelected ( self ) :

        fmol = self._struct_to_fit
        if fmol is None:
            self.status ( "No structure selected" )
            return [None, None]

        from chimerax.map import Volume
        if isinstance(fmol, Volume):
            fmap = fmol
            fmol = None

        return [fmol, fmap]



    def Map2Map ( self, densitiesFromMap, toGridOfMap, mask = False ) :

        #debug "Taking densities from %s with grid of %s" % ( densitiesFromMap.name, toGridOfMap.name )

        #mmc = fmap.writable_copy ( require_copy = True )
        #mmc.name = rname
        #debug " - cloned", fmap.name

        fmap = toGridOfMap
        dmap = densitiesFromMap

        n1, n2, n3 = fmap.data.size[0], fmap.data.size[1], fmap.data.size[2]
        from chimerax.map_data import grid_indices
        f_points = grid_indices( (n1,n2,n3), numpy.single )  # i,j,k indices
        fmap.data.ijk_to_xyz_transform.transform_points( f_points, in_place = True )

        d_vals = dmap.interpolated_values ( f_points, fmap.scene_position )
        df_mat = d_vals.reshape( (n3,n2,n1) )

        if mask :
            f_mat = fmap.data.full_matrix()
            f_mask = numpy.where ( f_mat > fmap.minimum_surface_level, numpy.ones_like(f_mat), numpy.zeros_like(f_mat) )
            df_mat = df_mat * f_mask

        return df_mat


    def Map2MapResize (self, fmap, dmap) :

        from . import axes
        fpoints, weights = axes.map_points ( fmap )
        debug("Fit map - got %d points in contour" % len (fpoints))

        #debug "Fit map - xf: ", fmap.scene_position
        fmap.scene_position.transform_points( fpoints, in_place = True )
        #debug "Seg map - xf: ", dmap.scene_position
        dmap.scene_position.inverse().transform_points( fpoints, in_place = True )
        dmap.data.xyz_to_ijk_transform.transform_points ( fpoints, in_place = True )
        #debug "points in %s ref:" % dmap.name, fpoints

        bound = 5
        li,lj,lk = numpy.min ( fpoints, axis=0 ) - (bound, bound, bound)
        hi,hj,hk = numpy.max ( fpoints, axis=0 ) + (bound, bound, bound)

        n1 = hi - li + 1
        n2 = hj - lj + 1
        n3 = hk - lk + 1

        #debug " - bounds - %d %d %d --> %d %d %d --> %d %d %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3 )

        #nmat = numpy.zeros ( (n1,n2,n3), numpy.float32 )
        #dmat = dmap.full_matrix()

        nstep = (fmap.data.step[0], fmap.data.step[1], fmap.data.step[2] )
        #nstep = (fmap.data.step[0]/2.0, fmap.data.step[1]/2.0, fmap.data.step[2]/2.0 )

        nn1 = int ( round (dmap.data.step[0] * float(n1) / nstep[0]) )
        nn2 = int ( round (dmap.data.step[1] * float(n2) / nstep[1]) )
        nn3 = int ( round (dmap.data.step[2] * float(n3) / nstep[2]) )

        O = dmap.data.origin
        #debug " - %s origin:" % dmap.name, O
        nO = ( O[0] + float(li) * dmap.data.step[0],
               O[1] + float(lj) * dmap.data.step[1],
               O[2] + float(lk) * dmap.data.step[2] )

        #debug " - new map origin:", nO

        nmat = numpy.zeros ( (nn1,nn2,nn3), numpy.float32 )
        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, nstep, dmap.data.cell_angles )

        #debug " - fmap grid dim: ", numpy.shape ( fmap.full_matrix() )
        #debug " - new map grid dim: ", numpy.shape ( nmat )

        from chimerax.map_data import grid_indices
        npoints = grid_indices ( (nn1, nn2, nn3), numpy.single)  # i,j,k indices
        ndata.ijk_to_xyz_transform.transform_points ( npoints, in_place = True )

        dvals = fmap.interpolated_values ( npoints, dmap.scene_position )
        #dvals = numpy.where ( dvals > threshold, dvals, numpy.zeros_like(dvals) )
        #nze = numpy.nonzero ( dvals )

        nmat = dvals.reshape( (nn3,nn2,nn1) )
        #f_mat = fmap.data.full_matrix()
        #f_mask = numpy.where ( f_mat > fmap.minimum_surface_level, numpy.ones_like(f_mat), numpy.zeros_like(f_mat) )
        #df_mat = df_mat * f_mask

        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, nstep, dmap.data.cell_angles )
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, self.session )


        fmap_base = os.path.splitext(fmap.name)[0]
        dmap_base = os.path.splitext(dmap.name)[0]
        fmap_path = os.path.splitext (fmap.data.path)[0]
        dmap_path = os.path.splitext (dmap.data.path)[0]

        nv.name = fmap_base + "__in__" + dmap_base
        nv.scene_position = dmap.scene_position

        #npath = dmap_path + fnamesuf
        #nv.write_file ( npath, "mrc" )
        #debug "Wrote ", npath

        return nv



    def TakeDMap_with_FMap ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - got molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - got map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return


        df_mat = self.Map2Map ( dmap, fmap )
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, fmap.data.origin, fmap.data.step, fmap.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )
        df_v.name = dmap.name + "_in_" + fmap.name
        df_v.scene_position = fmap.scene_position



    def TakeFMap_with_DMap0 ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - got molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - got map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return

        df_mat = self.Map2Map ( fmap, dmap )
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )


        if 0 :
            mapMean, mapStDev = MapStats ( df_v )
            df_v = AddNoiseToMap ( df_v, mapMean, mapStDev / 3.0 )


        df_v.name = fmap.name + "_in_" + dmap.name
        df_v.scene_position = dmap.scene_position



    def TakeFMap_with_DMapN ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - got molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - got map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return

        df_mat = self.Map2Map ( fmap, dmap )
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )


        if 1 :
            mapMean, mapStDev = MapStats ( df_v )
            df_v = AddNoiseToMap ( df_v, mapMean, mapStDev / 3.0 )


        df_v.name = fmap.name + "_in_" + dmap.name
        df_v.scene_position = dmap.scene_position




    def TakeFMap_with_DMap ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - got molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - got map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return

        nv = self.Map2MapResize ( fmap, dmap )




    def FitAllVisMaps ( self ) :

        from chimerax.map import Volume
        from chimerax.atomic import Structure
        mlist = self.session.models.list(type = (Volume,Structure))
        for m in mlist :
            label = m.name + " (%d)" % m.id
            debug("---------------------", label, "---------------------")

            if m.display == False :
                continue

            self._struct_to_fit = m
            self.Fit()


    @property
    def _volumes(self):
        from chimerax.map import Volume
        return self.session.models.list(type = [Volume])

    def AvgFMaps ( self ) :

        mlist = self._volumes

        fmap = None
        avgMat = None
        N = 0.0

        for m in mlist :
            if m.display == True :
                debug(m.name)

                if avgMat == None :
                    avgMat = m.data.full_matrix()
                    fmap = m
                    N = 1.0
                else :
                    avgMat = avgMat + m.data.full_matrix()
                    N = N + 1.0

        avgMat = avgMat / N

        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( avgMat, fmap.data.origin, fmap.data.step, fmap.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )
        df_v.name = "Avg"
        df_v.scene_position = fmap.scene_position

        return


    def DifFMaps2 ( self ) :

        mlist = self._volumes

        smaps = []
        for m in mlist :
            if m.display == True :
                debug(" - ", m.name)
                smaps.append ( m )


        if len(smaps) != 2 :
            self.status ( "Need only 2 maps visible" )
            return


        m1 = smaps[0]
        m2 = smaps[1]


        m2_mat = self.Map2Map ( m2, m1 )

        difMat = NormalizeMat ( m1.data.full_matrix() ) - NormalizeMat ( m2_mat )

        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( difMat, m1.data.origin, m1.data.step, m1.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )
        df_v.name = m1.name + "__-__" + m2.name
        df_v.scene_position = m1.scene_position

        return



    def AvgFMaps2 (self) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        from . import extract_region_dialog
        importlib.reload ( extract_region_dialog )

        superSampleBy = 1

        if superSampleBy > 1 :
            ndata = extract_region_dialog.MapSS ( dmap, superSampleBy )
            from chimerax.map import volume_from_grid_data
            nmap = volume_from_grid_data ( ndata, self.session )
            nmap.name = dmap.name + "_M%d" % n
            nmap.scene_position = dmap.scene_position
            dmap = nmap


        mlist = self._volumes

        if 0 :
            debug(" -- making base map -- ")

            bmap = None
            m0 = None
            for m in mlist :
                if m.display == True :
                    debug(m.name)
                    if bmap == None :
                        bmap = m
                        m0 = m
                    else :
                        bmap0 = bmap
                        bmap = self.Map2MapResize (m, bmap)
                        if bmap0 != m0 :
                            close_models ( [bmap0] )


            bmap.name = "base"
            dmap = bmap

        debug(" -- finding base map --- ")
        largestMap = None
        maxD = 0
        for m in mlist :
            if m.display == True :
                d = numpy.sum ( m.data.size )
                if d > maxD :
                    maxD = d
                    largestMap = m

        debug(" - largest map: ", largestMap.name)
        dmap = largestMap
        #dmap.display = False


        fmap = None
        avgMat = None
        N = 0.0

        debug(" ----------- Averaging... ---------------------")

        for m in mlist :
            #if m.display == True and m != dmap :
            if m.display == True :
                debug(m.name)

                df_mat = self.Map2Map ( m, dmap )
                m.display = False

                weights = df_mat.ravel()
                smin = numpy.min (weights)
                sdev = numpy.std (weights)
                savg = numpy.average(weights)
                smax = numpy.max (weights)

                thr = 0 # m.minimum_surface_level

                debug("%s - (%.4f,%.4f) |%.4f| +/- %.4f -- %.4f" % (m.name, smin, smax, savg, sdev, thr))

                N = N + 1.0
                #df_mat = df_mat - ( numpy.ones_like(df_mat)*thr )

                #df_mat = numpy.where ( df_mat > thr, df_mat, numpy.zeros_like(df_mat) )

                df_mat = df_mat * (1.0 / smax)
                #df_mat = df_mat + ( numpy.ones_like(df_mat) * 10.0 )

                if 0 :
                    imhist,bins = numpy.histogram ( df_mat.flatten(), 20, normed=True )
                    debug(" ------- Histogram:")
                    debug(imhist)
                    debug(" ------- Bins:")
                    debug(bins)

                    cdf = imhist.cumsum() #cumulative distribution function
                    cdf = 10.0 * cdf / cdf[-1] #normalize

                    debug(cdf)

                    #use linear interpolation of cdf to find new pixel values
                    #df_mat = numpy.interp ( df_mat.flatten(), bins[:-1], cdf )
                    #df_mat = df_mat.reshape(dmap.data.full_matrix().shape)




                if avgMat == None :
                    avgMat = df_mat
                    fmap = m
                else :
                    avgMat = avgMat + df_mat

        debug(" ----------- n=%f ---------------------" % N)

        avgMat = avgMat / N
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( avgMat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles, name="avg" )
        from chimerax.map import volume_from_grid_data
        df_v = volume_from_grid_data ( df_data, self.session )
        df_v.name = "Avg"
        df_v.scene_position = dmap.scene_position

        nv = self.ShrinkMap ( df_v, 1e-3 )
        close_models ( [df_v] )

        if 0 :
            stdMat = None
            N = 0.0

            for m in mlist :
                if m.display == True :
                    debug(m.name)

                    if m.name == "Avg" :
                        debug("skipping avg vol")
                        continue

                    df_mat = self.Map2Map ( m, dmap )
                    N = N + 1.0

                    debug(" - sub from avg...")
                    d = numpy.power ( df_mat - avgMat, 2 )
                    if stdMat == None :
                        stdMat = d
                    else :
                        stdMat = stdMat + d

            stdMat = numpy.power ( stdMat / N, 0.5 )
            from chimerax.map_data import ArrayGridData
            df_data = ArrayGridData ( stdMat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )
            from chimerax.map import volume_from_grid_data
            df_v = volume_from_grid_data ( df_data, self.session )
            df_v.name = "Stdev"
            df_v.scene_position = dmap.scene_position



        # close_models ( [dmap] )

    def ShrinkMap ( self, dmap, thr ) :

        from . import axes
        dmap.surfaces[0].set_level(thr)
        fpoints, weights = axes.map_points ( dmap )
        #debug "%s / %f - %d points in contour" % (dmap.name, thr, len (fpoints))

        #debug "Fit map - xf: ", fmap.scene_position
        #transform_vertices( fpoints,  fmap.scene_position )

        #debug "Seg map - xf: ", dmap.scene_position
        #transform_vertices( fpoints,  dmap.scene_position.inverse() )
        dmap.data.xyz_to_ijk_transform.transform_points ( fpoints, in_place = True )
        #debug "points in %s ref:" % dmap.name, fpoints

        bound = 4
        li,lj,lk = numpy.min ( fpoints, axis=0 ) - (bound, bound, bound)
        hi,hj,hk = numpy.max ( fpoints, axis=0 ) + (bound, bound, bound)

        n1 = int(hi - li + 1)
        n2 = int(hj - lj + 1)
        n3 = int(hk - lk + 1)

        #debug " - bounds - %d %d %d --> %d %d %d --> %d %d %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3 )

        #nmat = numpy.zeros ( (n1,n2,n3), numpy.float32 )
        #dmat = dmap.full_matrix()

        O = dmap.data.origin
        #debug " - %s origin:" % dmap.name, O
        #debug " - %s step:" % dmap.name, dmap.data.step
        nO = ( O[0] + float(li) * dmap.data.step[0],
               O[1] + float(lj) * dmap.data.step[1],
               O[2] + float(lk) * dmap.data.step[2] )

        #debug " - new map origin:", nO

        nmat = numpy.zeros ( (n1,n2,n3), numpy.float32 )
        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, dmap.data.step, dmap.data.cell_angles )

        #debug " - new map grid dim: ", numpy.shape ( nmat )

        from chimerax.map_data import grid_indices
        npoints = grid_indices ( (n1, n2, n3), numpy.single)  # i,j,k indices
        ndata.ijk_to_xyz_transform.transform_points ( npoints, in_place = True )

        dvals = dmap.interpolated_values ( npoints, dmap.scene_position )
        #dvals = numpy.where ( dvals > threshold, dvals, numpy.zeros_like(dvals) )
        #nze = numpy.nonzero ( dvals )

        nmat = dvals.reshape( (n3,n2,n1) )
        #f_mat = fmap.data.full_matrix()
        #f_mask = numpy.where ( f_mat > fmap.minimum_surface_level, numpy.ones_like(f_mat), numpy.zeros_like(f_mat) )
        #df_mat = df_mat * f_mask

        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmat, nO, dmap.data.step, dmap.data.cell_angles, name = dmap.name )
        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, self.session )

        return nv




    def TakeFMapsVis ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        mlist = self._volumes
        for m in mlist :
            if m.display == True :

                df_mat = self.Map2Map ( m, dmap )
                from chimerax.map_data import ArrayGridData
                df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )
                from chimerax.map import volume_from_grid_data
                df_v = volume_from_grid_data ( df_data, self.session )
                df_v.scene_position = dmap.scene_position

                mdir, mfile = os.path.split(m.data.path)
                df_v.name = "f_" + mfile

                debug(m.name, "->", df_v.name)

                dpath = mdir + "/" + df_v.name
                df_v.write_file ( dpath, "mrc" )



    def DifferenceMap ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - using molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - using map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return


        debug("\n\nDiff map ", dmap.name, " <=> ", fmap.name)

        closeDMap = False

        smod = self.CurrentSegmentation()
        regs = smod.selected_regions()
        if len(regs) > 0 :
            dmap = mask_volume( regs, dmap )
            closeDMap = True



        df_mat = self.Map2Map ( fmap, dmap )
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )

        #MapStats ( dmap )
        #MapDataStats ( df_data )

        debug("")
        debug("Normalizing", dmap.name)
        dmap_data_n = NormalizeData ( dmap.data )

        if 0 :
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( dmap_data_n, self.session )
            nv.name = os.path.splitext(dmap.name)[0] + "_norm.mrc"
            nv.scene_position = dmap.scene_position
        #fmapn = NormalizeMap ( fmap )

        debug("")
        debug("Normalizing transferred fit map")
        df_data_n = NormalizeData (  df_data )

        if 0 :
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( df_data_n, self.session )
            nv.name = os.path.splitext(dmap.name)[0] + "_fmap_norm.mrc"
            nv.scene_position = dmap.scene_position


        diff_mat = numpy.fabs ( dmap_data_n.full_matrix () - df_data_n.full_matrix () )
        weights = diff_mat.ravel()
        smin = numpy.min (weights)
        sdev = numpy.std (weights)
        savg = numpy.average(weights)
        smax = numpy.max(weights)

        debug("")
        debug("Difference map:")
        #debug " -", len(nz), " nonzero"
        debug(" - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

        from chimerax.map_data import ArrayGridData
        diff_data = ArrayGridData ( diff_mat, df_data.origin, df_data.step, df_data.cell_angles )

        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( diff_data, self.session )

        nv.name = os.path.splitext(dmap.name)[0] + "_--_" + fmap.name
        nv.scene_position = dmap.scene_position

        close_models ( [closeDMap] )



    def IntersectionMap ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - using molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - using map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return


        debug("\n\nDiff map ", dmap.name, " <=> ", fmap.name)

        closeDMap = False

        smod = self.CurrentSegmentation()
        regs = smod.selected_regions()
        if len(regs) > 0 :
            dmap = mask_volume( regs, dmap )
            closeDMap = True


        df_mat = self.Map2Map ( fmap, dmap )
        from chimerax.map_data import ArrayGridData
        df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )

        #MapStats ( dmap )
        #MapDataStats ( df_data )

        debug("")
        debug("Normalizing", dmap.name)
        dmap_data_n = NormalizeData ( dmap.data )

        if 0 :
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( dmap_data_n, self.session )
            nv.name = os.path.splitext(dmap.name)[0] + "_norm.mrc"
            nv.scene_position = dmap.scene_position
        #fmapn = NormalizeMap ( fmap )

        debug("")
        debug("Normalizing transferred fit map")
        df_data_n = NormalizeData (  df_data )

        if 0 :
            from chimerax.map import volume_from_grid_data            
            nv = volume_from_grid_data ( df_data_n, self.session )
            nv.name = os.path.splitext(dmap.name)[0] + "_fmap_norm.mrc"
            nv.scene_position = dmap.scene_position


        diff_mat = numpy.fabs ( dmap_data_n.full_matrix () - df_data_n.full_matrix () )
        weights = diff_mat.ravel()
        smin = numpy.min (weights)
        sdev = numpy.std (weights)
        savg = numpy.average(weights)
        smax = numpy.max(weights)

        debug("")
        debug("Difference map:")
        #debug " -", len(nz), " nonzero"
        debug(" - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

        from chimerax.map_data import ArrayGridData
        diff_data = ArrayGridData ( diff_mat, df_data.origin, df_data.step, df_data.cell_angles )

        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( diff_data, self.session )

        nv.name = os.path.splitext(dmap.name)[0] + "_--_" + fmap.name
        nv.scene_position = dmap.scene_position

        close_models ( [closeDMap] )


    def ShapeMatch ( self ) :

        dmap = self.segmentation_map
        if dmap == None : debug("No segmentation map"); return

        fmap = None
        [fmol, fmap2] = self.MolOrMapSelected ();
        if fmol != None :
            debug(" - using molecule map")
            fmap = self.MoleculeMap()
        elif fmap2 != None :
            debug(" - using map map")
            fmap = fmap2
        else :
            self.status ('Please select an open molecule or map in the field above')
            return


        debug("\n\nDiff map ", dmap.name, " <=> ", fmap.name)

        closeDMap = False
        realDMap = dmap

        smod = self.CurrentSegmentation()
        if smod != None :
            regs = smod.selected_regions()
            if len(regs) > 0 :
                dmap = mask_volume( regs, dmap )
                closeDMap = True


        df_mat = self.Map2Map ( fmap, dmap )
        #from chimerax.map_data import ArrayGridData
        #df_data = ArrayGridData ( df_mat, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )


        thr = dmap.minimum_surface_level

        self.status ("Generating 1/-1 map for " + dmap.name + " thr: %.3f" % thr)

        m0 = dmap.data.full_matrix()
        m1 = numpy.where ( m0 > realDMap.minimum_surface_level, numpy.ones_like(m0)*1, numpy.zeros_like(m0) )

        m2 = numpy.where ( df_mat > fmap.minimum_surface_level, numpy.ones_like(df_mat)*1, numpy.zeros_like(df_mat) )

        mi = m1 * m2
        mu = m1 + m2

        if 0 :
            from chimerax.map_data import ArrayGridData
            mid = ArrayGridData ( mi, realDMap.data.origin, realDMap.data.step, realDMap.data.cell_angles, name="inter" )
            mud = ArrayGridData ( mu, realDMap.data.origin, realDMap.data.step, realDMap.data.cell_angles, name="union" )
            from chimerax.map import volume_from_grid_data
            nv = volume_from_grid_data ( mid, self.session )
            nv = volume_from_grid_data ( mud, self.session )


        nz_int =  numpy.shape ( (mi).nonzero () )[1]
        nz_uni =  numpy.shape ( (mu).nonzero () )[1]

        sm_score = float(nz_int) / float (nz_uni)

        debug(" - intersection %d, union %d - sm: %.3f" % (nz_int, nz_uni, sm_score))


        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( mi, dmap.data.origin, dmap.data.step, dmap.data.cell_angles )

        from chimerax.map import volume_from_grid_data
        nv = volume_from_grid_data ( ndata, dmap.session )

        nv.name = os.path.splitext(dmap.name)[0] + "_--_" + fmap.name
        nv.scene_position = dmap.scene_position


        close_models ( [dmap] )

    # State save/restore in ChimeraX
    _save_attrs = ['_lump_subids', 
                   '_sim_res', '_sim_grid_sp',
                   '_combined_selected_regions', '_each_selected_region', '_around_selected', '_all_groups',
                   '_prin_axes_search', '_rota_search', '_rota_search_num',
                   '_mask_map_when_fitting',
                   '_use_laplace',
                   '_optimize_fits',
                   '_do_cluster_fits', '_position_tol', '_angle_tol',
                   '_num_fits_to_add',
                   '_calc_symmetry_clashes', '_symmetry']
  
    def take_snapshot(self, session, flags):
        data = {
            'fits': [fit for fit in self.list_fits if not fit.maps_deleted()],
            'version': 1
        }
        for attr in FitSegmentsDialog._save_attrs:
            data[attr] = getattr(self, attr).value
        return data

    @staticmethod
    def restore_snapshot(session, data):
        d = FitSegmentsDialog.get_singleton(session)
        for attr in FitSegmentsDialog._save_attrs:
            getattr(d, attr).value = data[attr]
        d.list_fits = fits = data['fits']
        for fit in fits:
            d._add_fit_to_listbox(fit)
        return d


# State base class handles session save and restore using
# take_snapshot() and restore_snapshot() methods.
from chimerax.core.state import State

class Fit ( State ):
    def __init__(self, fit_map, target_map, position, correlation,
                 atom_inclusion, backbone_inclusion, backbone_clash, high_density_occupancy,
                 regions):
        self.fit_map = fit_map
        self.target_map = target_map
        self.position = position
        self.correlation = correlation
        self.atom_inclusion = atom_inclusion
        self.backbone_inclusion = backbone_inclusion
        self.backbone_clash = backbone_clash
        self.high_density_occupancy = high_density_occupancy
        self.regions = regions

    # State save/restore in ChimeraX
    _save_attrs = ['fit_map', 'target_map', 'position', 'correlation', 'atom_inclusion',
                   'backbone_inclusion', 'backbone_clash', 'high_density_occupancy', 'regions']
  
    def take_snapshot(self, session, flags):
        data = { 'version': 1 }
        for attr in Fit._save_attrs:
            data[attr] = getattr(self, attr)
        data['fit_name'] = self.fit_map.struc_name
        data['fit_mols'] = [m for m in self.fit_map.mols if not m.deleted]
        return data

    @staticmethod
    def restore_snapshot(session, data):
        kw = {attr: data[attr] for attr in Fit._save_attrs }
        f = Fit(**kw)
        f.fit_map.struc_name = data['fit_name']
        f.fit_map.mols = data['fit_mols']
        return f

    def maps_deleted(self):
        return self.fit_map.deleted or self.target_map.deleted

def close_models(models):

    if models:
        ses = models[0].session
        ses.models.close(models)


def fit_segments_dialog ( session, create = True ) :

    return FitSegmentsDialog.get_singleton(session, create = create)

def show_fit_segments_dialog ( session ):

    d = fit_segments_dialog ( session, create = True )
    d.display(True)
    return d


# -----------------------------------------------------------------------------
#
def optimize_fits(fpoints, fpoint_weights, mlist, dmap,
                  names = None, status_text = None,
                  optimize = True, use_threads = False):

    from time import time
    c0 = time()

    darray = dmap.data.matrix()
    xyz_to_ijk_tf = dmap.data.xyz_to_ijk_transform

    if use_threads:
        # TODO: report status messages.
        fits = parallel_fitting(fpoints, fpoint_weights,
                                mlist, darray, xyz_to_ijk_tf, optimize)
    else:
        fits = []
        for i, Mi in enumerate(mlist):
            #if names:
            #    debug "%d/%d : %s" % ( i+1, len(mlist), names[i] )
            if status_text:
                debug ( "%s %d/%d" % (status_text, i+1, len(mlist)) )
            Mfit, corr, stats = FitMap_T(fpoints, fpoint_weights, Mi, darray, xyz_to_ijk_tf, optimize = optimize)
            #debug "Fit ", i, ":", "Shift: ", stats['totShift'], "Angle:", stats['totAngle'], "height", stats['difCC'], "Final", corr
            fits.append((Mfit, corr, stats))

    c1 = time()
    debug('%d fits took %.2f seconds' % (len(fits), c1-c0))

    return fits


# -----------------------------------------------------------------------------
#
def parallel_fitting(fpoints, fpoint_weights, mlist, darray, xyz_to_ijk_tf,
                     optimize = True):

    #
    # Choose number of threads to match number of cores.  Using more threads
    # creates large inefficiency (2x slower) in Python 2.7 due to context
    # switching overhead (Dave Beazley lecture).
    #
    # System usually reports twice actual number of cores due to hyperthreading.
    # Hyperthreading doesn't help if fitting tests so half that number.
    #
    import multiprocessing
    threads = multiprocessing.cpu_count() / 2
    debug('parallel fitting using %d threads' % threads)

    # Avoid periodic Python context switching.
    import sys
    original_check_interval = sys.getcheckinterval()
    sys.setcheckinterval(1000000000)

    # Define thread class for fitting.
    from threading import Thread
    class Fit_Thread(Thread):
        def __init__(self, mlist):
            Thread.__init__(self)
            self.mlist = mlist
        def run(self):
            self.fits = [FitMap_T(fpoints, fpoint_weights, m, darray,
                                  xyz_to_ijk_tf, optimize = optimize)
                         for m in self.mlist]

    # Starts threads with each calculating an equal number of fits.
    n  = len(mlist)
    g = [mlist[(n*c)/threads:(n*(c+1))/threads] for c in range(threads)]
    threads = [Fit_Thread(ml) for ml in g]
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Restore periodic context switching.
    sys.setcheckinterval(original_check_interval)

    # Collect fit results from all threads.
    fits = []
    for t in threads:
        for Mfit, corr, stats in t.fits:
            fits.append((Mfit, corr))

    return fits


# -----------------------------------------------------------------------------
#
def FitMap_T ( fpoints, fpoint_weights, M, darray, xyz_to_ijk_transform,
               bTrans=True, bRot=True, optimize=True ) :

    xyz_to_ijk_tf = xyz_to_ijk_transform * M

    if optimize:
        from chimerax.map_fit import locate_maximum
        totShift = 0.0
        totAngle = 0.0
        from chimerax.map_data import interpolate_volume_data
        map_values, outside = interpolate_volume_data(fpoints, xyz_to_ijk_tf, darray)
        initOlap, initCC = overlap_and_correlation ( fpoint_weights, map_values )

        for i in range (5) :
            move_tf, stats = locate_maximum(fpoints, fpoint_weights,
                                            darray, xyz_to_ijk_tf,
                                            max_steps = 1000,
                                            ijk_step_size_min = 0.01,
                                            ijk_step_size_max = 0.5,
                                            optimize_translation = bTrans,
                                            optimize_rotation = bRot,
                                            metric = 'sum product',
                                            request_stop_cb = None)

            M = M * move_tf
            corr = stats['correlation']

            #debug ' \t%d steps: d %.3g, r %.3g, cor %f' % (stats['steps'], stats['shift'], stats['angle'], corr )

            totShift = totShift + stats['shift']
            totAngle = totAngle + stats['angle']

            if ( stats['shift'] < 0.1 and stats['angle'] < 0.1 ) :
                break

            xyz_to_ijk_tf = xyz_to_ijk_transform * M

        stats['totAngle'] = totAngle
        stats['totShift'] = totShift
        stats['difCC'] = corr - initCC

    else:
        from chimerax.map_data import interpolate_volume_data
        map_values, outside = interpolate_volume_data(fpoints, xyz_to_ijk_tf,
                                                      darray )
        olap, corr = overlap_and_correlation ( fpoint_weights, map_values )
        stats = {}

        stats['totAngle'] = 0.0
        stats['totShift'] = 0.0
        stats['difCC'] = 0.0

    return M, corr, stats


def molApplyT ( mol, T ) :

    atoms = mol.atoms
    atoms.coords = xyz = T * atoms.coords
    mol.COM = xyz.mean()

#
# Change atom coordinates so the center of mass is at the origin and
# the principal axes are x, y and z.  Make a compensating transformation
# of the molecule coordinate system so the molecule does not move in the
# graphics window.
#
def centerMol ( mols ):

    if len(mols) == 0 :
        debug("Failed to center molecule")
        return []

    if hasattr(mols[0], 'centered') :
        return mols

    from chimerax.atomic import concatenate, Atoms
    atoms = concatenate([m.atoms for m in mols], Atoms)
    
    debug ( "Centering %d structures, %d atoms" % (len(mols), len(atoms) ) )

    points = atoms.coords
    COM, U, S, V = prAxes ( points )

    # move COM to origin and align pr. axes with XYZ
    from chimerax.geometry import Place, identity
    tAO = Place ( [
        [ 1, 0, 0, -COM[0] ],
        [ 0, 1, 0, -COM[1] ],
        [ 0, 0, 1, -COM[2] ] ] )

    tAR = Place ( [
        [ V[0,0], V[0,1], V[0,2], 0 ],
        [ V[1,0], V[1,1], V[1,2], 0 ],
        [ V[2,0], V[2,1], V[2,2], 0 ] ] )

    # Adjust coordinate system so molecule does not appear to move.
    tf = (tAR*tAO).inverse()

    for fmol in mols :

        fmol.COM, fmol.U, fmol.S, fmol.V = COM, U, S, V

        debug("Mol %s" % (fmol.id_string))
        molApplyT ( fmol, tAO )
        debug(" - COM after translation:", fmol.COM)
        molApplyT ( fmol, tAR )
        debug(" - COM after rotation:", fmol.COM)

        fmol.position = fmol.position * tf

        fmol.mT = identity()
        fmol.mR = identity()

        fmol.M = fmol.mT * fmol.mR

    points = atoms.coords

    for fmol in mols :
        fmol.COM, fmol.U, fmol.S, fmol.V = prAxes ( points )

        ppoints = points * fmol.U

        fmol.BoundRad = numpy.sqrt ( numpy.max ( numpy.sum ( numpy.square (ppoints), 1 ) ) )
        fmol.Extents = numpy.asarray ( numpy.max ( numpy.abs ( ppoints ), 0 ) )[0]

        fmol.Extents[0] = fmol.Extents[0] + 5.0
        fmol.Extents[1] = fmol.Extents[1] + 5.0
        fmol.Extents[2] = fmol.Extents[2] + 5.0

        fmol.centered = True

        debug ( "Centered %s (%s) (radius %.2fA, extents %.2fA %.2fA %.2fA)" % (
            fmol.name, fmol.id_string, fmol.BoundRad, fmol.Extents[0], fmol.Extents[1], fmol.Extents[2] ) )

    return mols


def fit_points(fmap, useThreshold = True):

    mat = fmap.data.full_matrix()
    threshold = fmap.minimum_surface_level

    if useThreshold == False :
        threshold = -1e9
        debug(" - not using threshold")

    from chimerax.map import high_indices
    points = high_indices(mat, threshold)
    fpoints = points.astype(numpy.single)
    fpoint_weights = mat[points[:,2],points[:,1],points[:,0]]

    nz = numpy.nonzero( fpoint_weights )[0]
    if len(nz) < len (fpoint_weights) :
        fpoints = numpy.take( fpoints, nz, axis=0 )
        fpoint_weights = numpy.take(fpoint_weights, nz, axis=0)

    fmap.data.ijk_to_xyz_transform.transform_points( fpoints, in_place = True )

    if 0 : debug("FitPoints from %s with threshold %.4f, %d nonzero" % (
        fmap.name, threshold, len(nz) ))

    return fpoints, fpoint_weights



def move_fit_models(fmap, M, dmap_xform):

    xfA = dmap_xform * M
    fmap.scene_position = xfA

    debug("moving %d mols to fitted position" % len(fmap.mols))
    for mol in fmap.mols :
        mol.scene_position = xfA


def principle_axes_alignments ( points, flips, preM ):

    COM, U, S, V = prAxes ( points )

    from chimerax.geometry import Place
    comT = Place ( [
        [ 1, 0, 0, COM[0] ],
        [ 0, 1, 0, COM[1] ],
        [ 0, 0, 1, COM[2] ] ] )

    mlist = []
    for j in range( len(flips) ) :

        af = flips[j]

        mR = Place ( [
            [ af[0]*U[0,0], af[1]*U[0,1], af[2]*U[0,2], 0 ],
            [ af[0]*U[1,0], af[1]*U[1,1], af[2]*U[1,2], 0 ],
            [ af[0]*U[2,0], af[1]*U[2,1], af[2]*U[2,2], 0 ] ] )

        M = comT * mR * preM
        mlist.append(M)

    return mlist

#
# Return list of rotation xforms uniformly distributed rotating about
# N axis vectors and M angles about each axis.
#
# http://www.math.niu.edu/~rusin/known-math/97/spherefaq
#
def uniform_rotation_angles(N, M) :

    thetas, phis = [], []
    from math import acos, sin, cos, sqrt, pi
    for k in range ( 1, N+1 ) :
        h = -1.0 + ( 2.0*float(k-1)/float(N-1) )
        phis.append ( acos(h) )
        thetas.append ( 0 if k == 1 or k == N else
                        (thetas[k-2] + 3.6/sqrt(N*(1.0-h**2.0))) % (2*pi) )

    ralist = []
    for theta, phi in zip(thetas, phis):
        for m in range ( M ) :
            rot = 2*pi*float(m)/float(M)
            ralist.append((theta,phi,rot))

    return ralist


def rotation_from_angles(theta, phi, rot) :

    from math import sin, cos, pi
    v = (sin(phi)*cos(theta), sin(phi)*sin(theta), cos(phi))
    from chimerax.geometry import rotation
    xfR = rotation ( v, rot*180/pi )
    return xfR


def place_map_resample ( fmap, dmap, fnamesuf ) :

    # get bounds of points above threshold
    from chimerax.map_data import grid_indices
    fpoints = grid_indices (fmap.data.size, numpy.single)  # i,j,k indices
    fmap.data.ijk_to_xyz_transform.transform_points ( fpoints, in_place = True )
    mat = fmap.data.full_matrix ()
    fpoint_weights = numpy.ravel(mat).astype(numpy.single)
    threshold = fmap.minimum_surface_level
    ge = numpy.greater_equal(fpoint_weights, threshold)
    fpoints = numpy.compress(ge, fpoints, 0)
    fpoint_weights = numpy.compress(ge, fpoint_weights)
    nz = numpy.nonzero( fpoint_weights )[0]
    debug(" - %d above %f in %s" % (len(nz), threshold, fmap.name))
    #debug "points: ", fpoints
    #debug "weights: ", fpoint_weights

    tf = dmap.data.xyz_to_ijk_transform * dmap.scene_position.inverse() * fmap.scene_position
    tf.transform_points ( fpoints, in_place = True )
    #debug "points in %s ref:" % dmap.name, fpoints

    bound = 2
    li,lj,lk = numpy.min ( fpoints, axis=0 ) - (bound, bound, bound)
    hi,hj,hk = numpy.max ( fpoints, axis=0 ) + (bound, bound, bound)

    n1 = hi - li + 1
    n2 = hj - lj + 1
    n3 = hk - lk + 1

    debug(" - bounds - %d %d %d --> %d %d %d --> %d %d %d" % ( li, lj, lk, hi, hj, hk, n1,n2,n3 ))

    #nmat = numpy.zeros ( (n1,n2,n3), numpy.float32 )
    #dmat = dmap.full_matrix()

    nn1 = int ( round (dmap.data.step[0] * float(n1) / fmap.data.step[0]) )
    nn2 = int ( round (dmap.data.step[1] * float(n2) / fmap.data.step[1]) )
    nn3 = int ( round (dmap.data.step[2] * float(n3) / fmap.data.step[2]) )

    O = dmap.data.origin
    debug(" - %s origin:" % dmap.name, O)
    nO = ( O[0] + float(li) * dmap.data.step[0],
           O[1] + float(lj) * dmap.data.step[1],
           O[2] + float(lk) * dmap.data.step[2] )

    debug(" - new map origin:", nO)

    nmat = numpy.zeros ( (nn1,nn2,nn3), numpy.float32 )
    from chimerax.map_data import ArrayGridData
    ndata = ArrayGridData ( nmat, nO, fmap.data.step, dmap.data.cell_angles )

    debug(" - fmap grid dim: ", numpy.shape ( fmap.full_matrix() ))
    debug(" - new map grid dim: ", numpy.shape ( nmat ))

    from chimerax.map_data import grid_indices
    npoints = grid_indices ( (nn1, nn2, nn3), numpy.single)  # i,j,k indices
    ndata.ijk_to_xyz_transform.transform_points ( npoints, in_place = True )

    dvals = fmap.interpolated_values ( npoints, dmap.scene_position )
    #dvals = numpy.where ( dvals > threshold, dvals, numpy.zeros_like(dvals) )
    #nze = numpy.nonzero ( dvals )

    nmat = dvals.reshape( (nn3,nn2,nn1) )
    #f_mat = fmap.data.full_matrix()
    #f_mask = numpy.where ( f_mat > fmap.minimum_surface_level, numpy.ones_like(f_mat), numpy.zeros_like(f_mat) )
    #df_mat = df_mat * f_mask



    fmap_base = os.path.splitext(fmap.name)[0]
    from chimerax.map_data import ArrayGridData
    ndata = ArrayGridData ( nmat, nO, fmap.data.step, dmap.data.cell_angles, name=(fmap_base + ' resampled') )
    from chimerax.map import volume_from_grid_data
    nv = volume_from_grid_data ( ndata, dmap.session )
    nv.scene_position = dmap.scene_position
    

    '''
    # TODO: Not sure why this routine is saving the map to a file.
    dmap_path = os.path.splitext (dmap.data.path)[0]
    npath = dmap_path + fnamesuf
#    nv.write_file ( npath, "mrc" )
    from chimerax.core.commands import run, quote_if_necessary
    cmd = 'save %s model #%s format mrc' % (quote_if_necessary(npath), nv.id_string)
    run(dmap.session, cmd)
    debug("Wrote ", npath)
    '''

    return nv




def map_overlap_and_correlation (map1, map2, above_threshold):

    from chimerax.map_fit import map_overlap_and_correlation
    olap, cor = map_overlap_and_correlation ( v1, v2, above_threshold )[:2]
    return olap, cor



def overlap_and_correlation ( v1, v2 ):

    from chimerax.map_fit import overlap_and_correlation
    olap, cor = overlap_and_correlation ( v1, v2 )[:2]
    return olap, cor



def reportFitRegions(map_name, regs):

    r = ', '.join(str(reg.rid) for reg in regs[:5])
    if len(regs) > 5:
        r += '...'
    debug ( "Fitting %s to %d regions (%s)" % ( map_name, len(regs), r ) )


def getMod ( session, name ) :

    mlist = session.models.list ()
    for mol in mlist :
        if mol.name == name :
            return mol
    return None




def ShapeMatchScore ( atoms, dmap, bDebug=False ) :

    #fmol = fmap.mol
    #debug "atoms from", fmol.name
    #points = fmol.atoms.scene_coords

    debug("shape match of %d atoms with map %s" % (len(atoms), dmap.name))
    points = atoms.scene_coords
    dmap.scene_position.inverse().transform_points ( points, in_place = True )
    points0 = points.copy()
    dmap.data.xyz_to_ijk_transform.transform_points ( points, in_place = True )
    #debug "points in %s ref:" % dmap.name, fpoints

    bound = int ( numpy.ceil (3.0 * max(dmap.data.step)) ) + 2
    debug(" - bound:", bound)
    lo = numpy.floor ( numpy.min ( points, axis=0 ) ) - (bound, bound, bound)
    hi = numpy.ceil  ( numpy.max ( points, axis=0 ) ) + (bound, bound, bound)
    debug(" - min:", lo)
    debug(" - max:", hi)


    O = list ( dmap.data.origin )
    n = list ( dmap.data.size )
    s = dmap.data.step
    debug(" - dmap size:", n)
    debug(" - dmap O:", O)

    for i in (0,1,2) :
        if lo[i] < 0 :
            n[i] -= lo[i]
            O[i] += lo[i]*s[i]

    for i in (0,1,2) :
        if hi[i] > n[i] :
            n[i] = hi[i]

    debug(" - dmap size:", n)
    debug(" - dmap O:", O)

    nmat = numpy.ones ( (n[2], n[1], n[0]) )
    eps = 0.5 * numpy.sqrt ( (s[0] * s[0]) + (s[1] * s[1]) + (s[2] * s[2]) )
    from chimerax.map_data import ArrayGridData, zone_masked_grid_data
    ndata = ArrayGridData ( nmat, O, s, dmap.data.cell_angles )
    amap_data = zone_masked_grid_data ( ndata, points0, max(3.0, eps) )
    amat = amap_data.full_matrix()
    if 0 :
        from chimerax.map import volume_from_grid_data
        amap = volume_from_grid_data ( amap_data, dmap.session )
        amap.name = dmap.name + "_()_" + atoms[0].molecule.name
        amap.scene_position = dmap.scene_position

    from chimerax.map_data import grid_indices
    npoints = grid_indices ( (int(n[0]), int(n[1]), int(n[2])), numpy.single)  # i,j,k indices
    ndata.ijk_to_xyz_transform.transform_points ( npoints, in_place = True )
    dvals = dmap.interpolated_values ( npoints, dmap.scene_position )
    #dvals = numpy.where ( dvals > threshold, dvals, numpy.zeros_like(dvals) )
    #nze = numpy.nonzero ( dvals )

    nmat = dvals.reshape( (n[2], n[1], n[0]) )
    nmatm = numpy.where ( nmat > dmap.minimum_surface_level, numpy.ones_like(nmat), numpy.zeros_like(nmat) )
    #df_mat = df_mat * f_mask

    if 0 :
        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( nmatm, O, s, dmap.data.cell_angles )
        from chimerax.map import volume_from_grid_data
        nmap = volume_from_grid_data ( ndata, dmap.session )
        nmap.name = dmap.name + "_(2)"
        nmap.scene_position = dmap.scene_position

    nmatm = nmatm.astype ( numpy.int )
    amat = amat.astype ( numpy.int )
    imat = nmatm & amat
    umat = nmatm | amat

    if 0 :
        from chimerax.map_data import ArrayGridData
        ndata = ArrayGridData ( umat, O, s, dmap.data.cell_angles )
        from chimerax.map import volume_from_grid_data
        nmap = volume_from_grid_data ( ndata, dmap.session )
        nmap.name = dmap.name + "_(U)_" + atoms[0].molecule.name
        nmap.scene_position = dmap.scene_position

        ndata = ArrayGridData ( imat, O, s, dmap.data.cell_angles )
        nmap = volume_from_grid_data ( ndata, dmap.session )
        nmap.name = dmap.name + "_(I)_" + atoms[0].molecule.name
        nmap.scene_position = dmap.scene_position


    nz_int =  numpy.shape ( (imat).nonzero () )[1]
    nz_uni =  numpy.shape ( (umat).nonzero () )[1]

    sm_score = float(nz_int) / float (nz_uni)

    debug(" - intersection %d, union %d - sm: %.3f" % (nz_int, nz_uni, sm_score))

    return sm_score



def makeMap ( session, sel_str, res, gridSpacing, clr, map_name ) :

    cmd = "molmap %s %.3f sigmaFactor 0.187 gridSpacing %.3f replace false" % (
        sel_str, res, gridSpacing )
    #debug ">>>", cmd
    from chimerax.core.commands import run
    mv = run ( session, cmd )
    mv.name = map_name
    if 0 :
        #debug " - saving to:", map_name
        mv.write_file ( map_name, "mrc" )
        xf = mv.scene_position
        #debug " - closing:", map_name
        session.models.close ( [mv] )
        from chimerax.map.volume import open_volume_file
        mv = open_volume_file ( map_name, session )[0]
        #debug " - opened:", mv.name
        mv.scene_position = xf

    mv.surfaces[0].set_level(0.001)

    from chimerax.map import RenderingOptions
    ro = RenderingOptions()
    mv.update_surface ( False, ro )
    from .regions import float_to_8bit_color
    for sp in mv.surfaces :
        v, t = sp.geometry
        if len(v) == 8 and len(t) == 12 : sp.display = False
        sp.single_color = float_to_8bit_color( clr )

    return mv


def cc_by_residue ( fmap, dmap, w ) :

    rccs = []
    rmap = None
    rmap_pos = None
    rpoints, rpoint_weights = None, None
    if hasattr ( fmap, "mols" ) :
        for mol in fmap.mols :
            for ri, res in enumerate ( mol.residues ) :

                try :
                    cat = res.atomsMap["CA"][0]
                except :
                    continue

                xf = None
                if rmap == None :
                    rmap = makeMap ( mol.session, "#%d:%d@CA" % (mol.id, res.id.position)
                                     , 16.0, 1.0, (.5, .5, .5, 1.0), "resmap" )
                    rmap_pos = cat.coord()
                    rpoints, rpoint_weights = fit_points(rmap)
                    xf = rmap.scene_position

                else :
                    #new_rmap_pos = cat.coord()
                    d = cat.coord() - rmap_pos
                    xf = rmap.scene_position * translation ( d )

                rmap_values = dmap.interpolated_values ( rpoints, xf )
                olap, corr = overlap_and_correlation ( rpoint_weights, rmap_values )
                #debug " - overlap: %f, cross-correlation: %f" % (olap, corr)
                #close_models ( [rmap] )
                rccs.append ( corr )
                #debug corr,

        fp = open ( "ff_prcc_w%d.txt" % w, "a" )
        fp.write ( "%s" % fmap.mols[0].name )
        for i, cc in enumerate ( rccs ) :
            if w == 1 :
                fp.write ( "\t%f" % cc )
            else :
                wscores = rccs [ max(i-w, 0) : min(i+w,len(rccs)) ]
                wscore = float ( sum ( wscores ) ) / float( len(wscores) )
                fp.write ( "\t%f" % wscore )
        fp.write ( "\n" )
        fp.close ()
        close_models ( [rmap] )




def RandColorChains ( m ) :

    chain_clrs = {}
    
    # color ribbons and atoms
    from .regions import float_to_8bit_color
    for s, cid, res in m.residues.by_chain :
        clr = float_to_8bit_color ( ( rand()*.7, rand()*.7, rand()*.7, 1.0 ) )
        chains_clrs[cid] = clr
        r.ribbon_color = clr
        r.ribbon_display = True
        ratoms = r.atoms
        ratoms.displays = False
        ratoms.color = clr

    return chains_clrs



def MapStats ( dmap, aboveZero = True ) :

    debug("map: %s" % (dmap.name))

    MapDataStats ( dmap.data )


def MapDataStats ( data, aboveZero = True ) :

    mat = data.full_matrix ()

    if aboveZero :
        mat = numpy.where ( mat >= 0.0, mat, numpy.zeros_like(mat) )

    weights = mat.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    #nz = numpy.nonzero( weights )[0]

    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    #debug " -", len(nz), " nonzero"
    debug(" - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))



def NormalizeMap ( dmap ) :

    debug("Normalizing map: %s" % (dmap.name))

    ndata = NormalizeData ( dmap.data )

    from chimerax.map import volume_from_grid_data
    nv = volume_from_grid_data ( ndata, dmap.session )

    nv.name = os.path.splitext(dmap.name)[0] + "_norm.mrc"
    nv.scene_position = dmap.scene_position

    return nv



def NormalizeData ( data ) :

    O = data.origin
    mat = data.full_matrix ()

    mat = numpy.where ( mat >= 0.0, mat, numpy.zeros_like(mat) )

    weights = mat.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    #nz = numpy.nonzero( weights )[0]

    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    debug(" - initial - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

    #mat0 = mat0 - savg
    mat0 = mat / sdev
    #mat0 = mat / smax

    weights = mat0.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    debug(" - normalized - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

    from chimerax.map_data import ArrayGridData
    return ArrayGridData ( mat0, O, data.step, data.cell_angles )


def NormalizeMat ( mat ) :

    #mat = numpy.where ( mat >= 0.0, mat, numpy.zeros_like(mat) )

    weights = mat.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    #nz = numpy.nonzero( weights )[0]

    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    debug(" - initial - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

    #mat0 = mat0 - savg
    mat0 = mat / sdev
    #mat0 = mat / smax

    weights = mat0.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    debug(" - normalized - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

    return mat0



def OneMinusOneMap ( dmap ) :

    thr = dmap.minimum_surface_level

    debug ("Generating 1/-1 map for " + dmap.name + " thr: %.3f" % thr)

    m2 = None


    if 0 :
        m1 = dmap.data.full_matrix()
        m2 = numpy.where ( m1 > thr, numpy.ones_like(m1)*1, numpy.ones_like(m1)*-1.0 )
    else :

        m0 = dmap.data.full_matrix()
        inside_start = numpy.where ( m0 > thr, numpy.ones_like(m0)*1, numpy.zeros_like(m0) )
        outside_mask = numpy.where ( m0 < thr, numpy.ones_like(m0)*1, numpy.zeros_like(m0) )

        gvm = inside_start.copy();
        for i in range (numit) :
            nv_1 = numpy.roll(gvm, 1, axis=0)
            nv_2 = numpy.roll(gvm, -1, axis=0)
            nv_3 = numpy.roll(gvm, 1, axis=1)
            nv_4 = numpy.roll(gvm, -1, axis=1)
            nv_5 = numpy.roll(gvm, 1, axis=2)
            nv_6 = numpy.roll(gvm, -1, axis=2)
            gvm = 1.0/6.0 * ( nv_1 + nv_2 + nv_3 + nv_4 + nv_5 + nv_6 )
            gvm = outside_mask * gvm + inside_start


    from chimerax.map_data import ArrayGridData
    mgrid = ArrayGridData ( m2, dmap.data.origin, dmap.data.step, dmap.data.cell_angles, name="map_one_minus_one")

    from chimerax.map import volume_from_grid_data
    #nv = volume_from_grid_data ( mgrid, show_data = False, show_dialog = False )
    return volume_from_grid_data ( mgrid, dmap.session )



def MapStats ( dmap, aboveZero = False ) :

    debug("Map Stats: %s" % (dmap.name))

    mat = dmap.data.full_matrix ()

    if aboveZero :
        mat = numpy.where ( mat >= 0.0, mat, numpy.zeros_like(mat) )

    weights = mat.ravel()
    #ge = numpy.greater_equal(weights, 0.0)
    #weights = numpy.compress(ge, weights)
    #nz = numpy.nonzero( weights )[0]

    smin = numpy.min (weights)
    sdev = numpy.std (weights)
    savg = numpy.average(weights)
    smax = numpy.max(weights)

    #debug " -", len(nz), " nonzero"
    debug(" - range: %.3f -> %.3f, avg=%.3f, sdev=%.3f" % (smin, smax, savg, sdev))

    return savg, sdev



def AddNoiseToMap ( mv, mean, stdev ) :

    debug("\n---adding noise mean:",mean, " stdev:", stdev, "---\n")

    nvm = mv.full_matrix()
    #f_mask = numpy.where ( nvm > 0, numpy.zeros_like(nvm), numpy.ones_like(nvm) )

    from numpy.random import standard_normal as srand
    s=mv.data.size

    noisem = srand ( (s[2],s[1],s[0]) ) * stdev - (numpy.ones_like(nvm) * mean)
    ngvm = noisem + nvm

    from chimerax.map_data import ArrayGridData
    ndata = ArrayGridData ( ngvm, mv.data.origin, mv.data.step, mv.data.cell_angles )
    from chimerax.map import volume_from_grid_data
    nvg = volume_from_grid_data ( ndata, mv.session )
    nvg.name = mv.name

    session.models.close ( [mv] )
    return nvg
