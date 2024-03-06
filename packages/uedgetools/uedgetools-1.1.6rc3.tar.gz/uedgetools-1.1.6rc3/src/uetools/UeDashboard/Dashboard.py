try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
    from PyQt5.QtCore import (
        Qt, 
        QMargins,
        QTimer,
        QSize,
    )
    from PyQt5.QtWidgets import QMenu
    from PyQt5.QtGui import (
        QFont, 
        QDoubleValidator,
        QStatusTipEvent,
    )
    from .range_slider import RangeSlider
    from functools import partial
    from PyQt5.QtWidgets import (
        QAction,
        QWidget,
        QApplication, 
        QLabel, 
        QMainWindow,
        QMenu,
        QAction,
        QSlider,
        QVBoxLayout,
        QHBoxLayout,
        QGridLayout,
        QPushButton,
        QLineEdit,
        QTabWidget,
        QRadioButton,
        QButtonGroup,
        QCheckBox,
        QFrame,
        QFormLayout,
        QSizePolicy,
        QComboBox,
        QFileDialog,
        QDialog,
        QDialogButtonBox,
        QInputDialog,
    )
except:
    pass


    # update permanent bar
# TODO: Display file name somewhere else


# TODO: Store previously opened files in separate yaml under .uedgerc
# TODO: Make dialogue work with active UEDGE run
# TODO: make raise_message bolded red in bar


# TODO: How to deal with CX/psorx?
# TODO: Set zeros to 1e-10


class CaseDashboard(QWidget):
    """Main Window."""
    def __init__(self, case, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.file = case.filename

        self.centralWidget = QWidget(self)
        self.caseplot = HeatmapInteractiveFigure(case)
        # Cannibalize Case functions
        self.inplace = case.inplace
        self.casevars = case.vars
        self.get = case.get
        self.nx = case.nx
        self.ny = case.ny
        self.ionarray = case.ionarray
        self.gasarray = case.gasarray
        self.casename = case.casename
        self.ionspecies = 0
        self.gasspecies = 0
        self.species = ''


        self._createVarButtons()
        self._createSwitches()
        self._createRadios()
        self._createMiscOptions()

        self.plot_te()
        self.caseplot.setTitle("Electron temperature [eV]")

        self.settings = QVBoxLayout()
        self.settings.addWidget(self.misc['frame'])
        self.settings.addWidget(self.switches['frame'])

        self.menu = QGridLayout()
        self.menu.addLayout(self.buttons['layout'],    
                0, 0, 1, 2
        )
        self.menu.addLayout(self.radios['layout'],
                0, 2, 1, 1
        )
#        self.menu.addLayout(self.settings, 1, 0, 1, 3)
        self.fullmenu = QVBoxLayout()
        self.fullmenu.addLayout(self.menu)
        self.fullmenu.addStretch()
        self.fullmenu.addLayout(self.settings)

        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.fullmenu)
        self.layout.addWidget(self.caseplot)
    
        self.centralWidget.setLayout(self.layout)

        
    """ ===========================
               WIDGET CREATION
        ==========================="""

    def _createMiscOptions(self):
        from matplotlib.pyplot import colormaps
        self.misc = {
            'frame': QFrame(),
            'items': {
                'abs': QCheckBox(),
                'varscale': MyLineEdit("1"),
                'ulim': MyClearLineEdit(),
                'llim': MyClearLineEdit(),
                'cmap': QComboBox(),
            }
        }
        tmp = self.misc['items']

        form =  QFormLayout()
        form.addRow("Variable absolute value", tmp["abs"])
        tmp['abs'].toggled.connect(self.toggle_abs)
        tmp['abs'].setToolTip("Plots the absolute value of variables.")

        tmp['varscale'].setValidator(QDoubleValidator())
        tmp['varscale'].returnPressed.connect(self.change_varscale)
        tmp['varscale'].setFixedWidth(50)
        form.addRow("Variable scaling factor", tmp["varscale"])
        tmp['varscale'].mousePressEvent = lambda _ : tmp['varscale'].selectAll()
        tmp['varscale'].setToolTip("Hit return to apply.")

        tmp['ulim'].setValidator(QDoubleValidator())
        tmp['ulim'].returnPressed.connect(self.change_ulim)
        tmp['ulim'].setFixedWidth(50)
        tmp['ulim'].setToolTip("Hit return to apply.")
        form.addRow("Set upper plot range", tmp ['ulim'])

        tmp['llim'].setValidator(QDoubleValidator())
        tmp['llim'].returnPressed.connect(self.change_llim)
        tmp['llim'].setFixedWidth(50)
        tmp['llim'].setToolTip("Hit return to apply.")
        form.addRow("Set lower plot range", tmp ['llim'])

        form.addRow("Colormap", tmp["cmap"])
        i = 0
        for  colormap in colormaps():
            if colormap == self.caseplot.cmap:
                default = i
            tmp['cmap'].addItem(colormap, i)
            i+=1
        tmp["cmap"].setCurrentIndex(default) 
#        tmp['cmap'].setFixedWidth(150)
        tmp['cmap'].activated[str].connect(self.set_cmap)

        self.misc['frame'].setFrameStyle(QFrame.Panel | QFrame.Raised)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.title("Plot options")))
        layout.addLayout(form)
        self.misc['frame'].setLayout(layout)

    def _createVarButtons(self):
        self.buttons = {
            'layout': QGridLayout(),
            'title': QLabel(self.title("Plots")),
            'items': {
                'te': 'Electron temperature',
                'ti': 'Ion temperature',
                'tg': 'Gas temperature',
                'ne': 'Electron density',
                'ni': 'Ion density',
                'ng': 'Gas density',
                'phi': 'Potential',
                'prad': 'Total radiated power',
                'pradhyd': 'Hyd. radiated power',
                'pradimp': 'Imp. radiated power',
                'psorc': "Ion ioniz. source",
                'psorgc': "Gas ioniz. sink",
                'psorxrc': "Ion rec. + CX sink",
                'psorrgc': "Gas rec. source",
                'psorcxg': "Gas CX source",
            },
        }
        self.buttons["title"].setAlignment(Qt.AlignHCenter)
        self.buttons['layout'].setSpacing(0)

        maxbuttons = 8
        cols = [QVBoxLayout() for x in range(int(len(self.buttons['items'])/maxbuttons+1))]
        i = 0
        for key, setup in self.buttons['items'].items():
            self.buttons['items'][key] = QPushButton(setup)
            self.buttons['items'][key].clicked.connect(
                self.__getattribute__(f"plot_{key}"))
            cols[int(i/maxbuttons)].addWidget(
                self.buttons['items'][key], 
            )
            i += 1
        for vbox in cols:
            vbox.addStretch()
        # Add drop-down
        self.buttons['items']['dropdown'] = QComboBox()
        varlist = list(self.buttons['items'].keys())
        self.buttons['items']['dropdown'].addItem("", 0)
        # TODO: Check that can be plotted --> len(shape)
        for vartype in ['centered', 'staggered']:
            if self.inplace:
                for var, path in self.casevars.items():
                    if (vartype in path) and (var not in varlist):
                        if (len(self.get(var).shape) <= 3) and \
                            (len(self.get(var).shape) > 1):
                            self.buttons['items']['dropdown'].addItem(var, i)

        cols[-1].addWidget(self.buttons['items']['dropdown'])
        self.buttons['items']['dropdown'].activated[str].connect(self.plot_dropdown)

        custom = QVBoxLayout()
        custom.addWidget(QLabel("Custom formula"))
        self.buttons['items']['custom'] = MyLineEdit()
        self.buttons['items']['custom'].mousePressEvent = \
            lambda _ : self.buttons['items']['custom'].selectAll()
        self.buttons['items']['custom'].returnPressed.connect(self.plot_custom)
        self.buttons['items']['custom'].setToolTip("Plots custom formula. "+
            "Access var by get('var'). Python syntax applies. Expects output"+
            "of shape ({},{}). Hit return to apply. ".format(self.nx, self.ny))
        custom.addWidget(self.buttons['items']['custom'])
        custom.addStretch()

        self.buttons['layout'].addWidget(self.buttons['title'],0,0,1, len(cols))
        for i in range(len(cols)):
            self.buttons['layout'].addLayout(cols[i], 1, i, 1, 1)
        self.buttons['layout'].addLayout(custom, 2,0,1,len(cols))


    def _createRadios(self):
        self._createIonRadio()
        self._createGasRadio()
        self.radios = {'layout': QGridLayout()}

        self.radios['layout'].addWidget(self.ion_radio['frame'], 0, 0, 1, 1)
        self.radios['layout'].addWidget(self.gas_radio['frame'], 1, 0, 1, 1)

    def _createIonRadio(self):
        self.ion_radio = {
            'frame': QFrame(),
            'layout': QVBoxLayout(),
            'group': QButtonGroup(),
            'title': QLabel(self.title("Ion species")),
            'labels': self.ionarray,
            'items': {}
        }
        self.ion_radio['title'].setAlignment(\
                    Qt.AlignHCenter |\
                    Qt.AlignVCenter
        )
        self.ion_radio['layout'].addWidget(self.ion_radio['title'])
        ind = 0
        for label in self.ion_radio['labels']:
            self.ion_radio['items'][label] = QRadioButton(label)
            self.ion_radio['layout'].addWidget(\
                    self.ion_radio['items'][label])
            self.ion_radio['group'].addButton(\
                    self.ion_radio['items'][label], ind)
            self.ion_radio['items'][label].clicked.connect(self.ion_radio_clicked)
            ind += 1
        self.ion_radio['frame'].setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.ion_radio['frame'].setLayout(self.ion_radio['layout'])
        self.ion_radio['items'][self.ionarray[0]].setChecked(True)

    def _createGasRadio(self):
        self.gas_radio = {
            'frame': QFrame(),
            'layout': QVBoxLayout(),
            'group': QButtonGroup(),
            'title': QLabel(self.title("Gas species")),
            'labels': self.gasarray,
            'items': {}
        }
        self.gas_radio['title'].setAlignment(\
                    Qt.AlignHCenter |\
                    Qt.AlignVCenter
        )
        self.gas_radio['layout'].addWidget(self.gas_radio['title'])
        ind = 0
        for label in self.gas_radio['labels']:
            self.gas_radio['items'][label] = QRadioButton(label)
            self.gas_radio['layout'].addWidget(\
                    self.gas_radio['items'][label])
            self.gas_radio['group'].addButton(\
                    self.gas_radio['items'][label], ind)
            self.gas_radio['items'][label].clicked.connect(self.gas_radio_clicked)
            ind += 1
        self.gas_radio['layout'].addStretch()
        self.gas_radio['frame'].setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.gas_radio['frame'].setLayout(self.gas_radio['layout'])
        self.gas_radio['items'][self.gasarray[0]].setChecked(True)


    """ ===========================
                 ACTIONS
        ==========================="""

    def set_cmap(self, cmap):
        self.cmap = cmap
        self.caseplot.setCmap(cmap)

    def toggle_abs(self):
        self.caseplot.toggleAbs()

    def change_varscale(self):
        self.caseplot.setVarscale(float(self.misc['items']['varscale'].text()))
        self.misc['items']['varscale'].clearFocus()

    def change_ulim(self):
        self.caseplot.setUpperSlider(float(self.misc['items']['ulim'].text()))
        self.misc['items']['ulim'].clear()
        self.misc['items']['ulim'].clearFocus()

    def change_llim(self):
        self.caseplot.setLowerSlider(float(self.misc['items']['llim'].text()))
        self.misc['items']['llim'].clear()
        self.misc['items']['llim'].clearFocus()

    def ion_radio_clicked(self):
        self.ionspecies = self.ion_radio['group'].checkedId()
        title = self.caseplot.getTitle()
        if self.multispecies == 'ion':
            if " for " in title:
                title = title.split("for")[0] + "for {}".format(
                    self.ionarray[self.ionspecies])
            self.caseplot.setTitle(title)
        self.caseplot.setVar(self.get_speciesvar())
        
    def gas_radio_clicked(self):
        self.gasspecies = self.gas_radio['group'].checkedId()
        if self.multispecies == 'gas':
            title = self.caseplot.getTitle()
            if " for " in title:
                title = title.split("for")[0] + "for {}".format(
                    self.gasarray[self.gasspecies])
            self.caseplot.setTitle(title)
        self.caseplot.setVar(self.get_speciesvar())


    def _createSwitches(self):
        self.switches = {
            'frame': QFrame(),
            'layout': QVBoxLayout(),
            'title': QLabel(self.title("Switches")),
            'items': {}
        }
        
        grid = QHBoxLayout()
        col = QHBoxLayout()
        grid.addLayout(col)

        self.switches['layout'].addWidget(self.switches['title'])
        self.switches['layout'].addLayout(grid)
        self.switches['layout'].setSpacing(5)
        grid.setSpacing(5)
        self.switches['frame'].setLayout(self.switches['layout'])
        self.switches['frame'].setFrameStyle(QFrame.Panel | QFrame.Raised)

        i = 0
        for switch in ["Vessel", "Plates", "Separatrix", "Grid", "Scale"]:
            if switch != "Scale":
                on, off = "On", "Off"
            else:
                on, off = "Lin", "Log"
            self.switches['items'][switch.lower()] = {
                    'group': QButtonGroup(),
                    on.lower(): QRadioButton(on),
                    off.lower(): QRadioButton(off),
                    'layout': QVBoxLayout()
            }
            tmpsw = self.switches['items'][switch.lower()]
            tmpsw[on.lower()].toggled.connect(self.__getattribute__(\
                "{}_switch_clicked".format(switch.lower())))
            tmpsw['group'].addButton(tmpsw[on.lower()], 1)
            tmpsw['group'].addButton(tmpsw[off.lower()], 0)
            tmpsw['layout'].addWidget(QLabel(f"<b>{switch}</b>"))
            tmpsw['layout'].addWidget(tmpsw[on.lower()])
            tmpsw['layout'].addWidget(tmpsw[off.lower()])
            tmpsw['layout'].setContentsMargins(0,0,0,0)
            tmpsw['layout'].setSpacing(0)
            col.addLayout(tmpsw['layout'])
            i += 1
        self.switches['items']['vessel']['on'].setChecked(True)
        self.switches['items']['plates']['on'].setChecked(True)
        self.switches['items']['separatrix']['on'].setChecked(True)
        self.switches['items']['grid']['off'].setChecked(True)
        self.switches['items']['scale']['lin'].setChecked(True)
        self.plates_switch_clicked()
        self.vessel_switch_clicked()
        self.separatrix_switch_clicked()
        self.scale_switch_clicked()


    def plates_switch_clicked(self):
        self.caseplot.togglePlates()

    def grid_switch_clicked(self):
        self.caseplot.toggleGrid()

    def separatrix_switch_clicked(self):
        self.caseplot.toggleSeparatrix()

    def vessel_switch_clicked(self):
        self.caseplot.toggleVessel()

    def scale_switch_clicked(self):
        from matplotlib.colors import LogNorm, Normalize
        from numpy import log
        lims = self.caseplot.get_lims()
        if (lims[0] <= 0) and (self.caseplot.log is False):
            self.raise_message("Negative values in var: masking array!")
        self.caseplot.toggleLog()
        # TODO: detect log from figure?

    """ ===========================
                PLOT ACTIONS
        ==========================="""

    def get_speciesvar(self):
        if self.multispecies == 'gas':
            self.species = self.gasarray[self.gasspecies]
            return self.var[:, :, self.gasspecies]
        elif self.multispecies == 'ion':
            self.species = self.ionarray[self.ionspecies]
            return self.var[:, :, self.ionspecies]
        else:
            return self.var

    def is_nonzero(self):
        from numpy import sum
        if sum(self.get_speciesvar()) == 0:
            self.raise_message("Requested variable unpopulated! "+
                "Select another variable or species to plot.")
            return False
        else:
            return True


    def plot_driver(self, var, title, multispecies=False):
        from numpy.ma import masked_array
        from numpy import sum
        # Save variable as masked_array to mask for log
        self.var = masked_array(var, mask=False)
        self.multispecies = multispecies
        if not self.is_nonzero():
            return
        if (self.get_speciesvar().min() <= 0) and self.caseplot.log:
            self.raise_message("Non-positive values in logarithmic plot "+
                "have been masked!")
        self.caseplot.setTitle(title + \
                f" for {self.species}"*(multispecies is not False))
        self.caseplot.setVar(self.get_speciesvar())
        self.buttons['items']['dropdown'].setCurrentIndex(0)
        command = self.buttons['items']['custom'].clear()
 

    def plot_dropdown(self, text):
        # TODO: attempt auto-detecting shape
        self.raise_message(text)
        var = self.get(text)
        if len(var.shape) == 3:
            if var.shape[-1] == len(self.ionarray):
                self.multispecies = 'ion'
                self.var = var
                if not self.is_nonzero():
                    return
                self.caseplot.setTitle(text + " for {}".format(\
                    self.ionarray[self.ionspecies]))
                self.caseplot.setVar(self.get_speciesvar())
            elif var.shape[-1] == len(self.gasarray):
                self.multispecies = 'gas'
                self.var = var
                if not self.is_nonzero():
                    return
                self.caseplot.setTitle(text + " for {}".format(\
                    self.gasarray[self.gasspecies]))
                self.caseplot.setVar(self.get_speciesvar())
            else:
                self.raise_message("Could not determine species"+
                    f" index of {text}")
                return
        elif len(var.shape) == 2:
            self.var = var
            self.caseplot.setVar(self.var)
            if not self.is_nonzero():
                return
            self.caseplot.setTitle(text)
        else:
            self.raise_message(f"Could not determine shape of {text}")
            return
        self.buttons['items']['custom'].clear()

    def plot_custom(self):
        try:
            from uedge import com, bbb, grd, flx, aph, api
        except:
            pass
        command = self.buttons['items']['custom'].text()
        self.buttons['items']['dropdown'].setCurrentIndex(0)
        get = self.get
        try:
            exec("locals()['var'] =" + command)
            locals()['var'].shape # Fails non-ndarray results
        except:
            self.raise_message(f"{command} not recognized!")
            return
        if len(locals()['var'].shape) > 2:
            self.raise_message("Command variable has wrong shape: "+
                "{}, expected ({},{})".format(\
                    locals()['var'].shape,
                    self.nx+2,
                    self.ny+2
                )
            )
        else:
            self.var = locals()['var']
            self.multispecies = False
            if not self.is_nonzero():
                return
            self.caseplot.setVar(self.var)
            for substr in ['get', '("', '")', "('", "')",
                '"', "'", ".", "bbb", "com",
                "grd", "flx", "aph", "api", "self"]:
                command = command.replace(substr, '')
            self.caseplot.setTitle(command)
            self.buttons['items']['custom'].clearFocus()


       

    def plot_te(self):
        self.plot_driver(
            self.get('te')/1.602e-19,
            'Electron temperature [eV]',
        )

    def plot_ti(self):
        self.plot_driver(
            self.get('ti')/1.602e-19,
            'Ion temperature [eV]',
        )

    def plot_tg(self):
        self.plot_driver(
            self.get('tg')/1.602e-19,
            'Gas temperature [eV]',
            'gas'
        )

    def plot_ne(self):
        self.plot_driver(
            self.get('ne'),
            r'Electron density [m$\mathrm{{}^{-3}}$]',
        )

    def plot_ni(self):
        self.plot_driver(
            self.get('ni'),
            r'Ion density [m$\mathrm{{}^{-3}}$]',
            'ion'
        )

    def plot_ng(self):
        self.plot_driver(
            self.get('ng'),
            r'Gas density [m$\mathrm{{}^{-3}}$]',
            'gas'
        )

    def plot_phi(self):
        self.plot_driver(
            self.get('phi'),
            'Electrical potential [V]',
        )

    def plot_prad(self):
        self.plot_driver(
            self.get('prad')+self.get('pradhyd'),
            'Total radiated power [W/m$\mathrm{{}^{-3}}$]',
        )

    def plot_pradhyd(self):
        self.plot_driver(
            self.get('pradhyd'),
            'Hydrogenic radiated power [W/m$\mathrm{{}^{-3}}$]',
        )

    def plot_pradimp(self):
        self.plot_driver(
            self.get('prad'),
            'Impurity radiated power [W/m$\mathrm{{}^{-3}}$]',
        )

    def plot_psorc(self):
        self.plot_driver(
            self.get('psorc'),
            'Ion ionization source [parts/s]',
            'ion'
        )

    def plot_psorgc(self):
        self.plot_driver(
            self.get('psorgc'),
            'Gas ionization sink [parts/s]',
            'gas'
        )

    def plot_psorxrc(self):
        self.plot_driver(
            self.get('psorxrc'),
            'Ion recombination + CX sink [parts/s]',
            'ion'
        )

    def plot_psorrgc(self):
        self.plot_driver(
            self.get('psorrgc'),
            'Gas recombination source [parts/s]',
            'gas'
        )

    def plot_psorcxg(self):
        self.plot_driver(
            self.get('psorcxg'),
            'Gas CX source [parts/s]',
            'gas'
        )

    """ ===========================
                FORMATTERS 
        ==========================="""
    def title(self, text):
        return f"<b><font size=4>{text}</font></b>"

    def raise_message(self, message, time=5000):
        QApplication.sendEvent(self, QStatusTipEvent(message))
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_message)
        self.timer.start(time)

    def hide_message(self):
        QApplication.sendEvent(self, QStatusTipEvent(''))

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, MyLineEdit):
            focused_widget.clearFocus()
        if isinstance(focused_widget, MyClearLineEdit):
            focused_widget.clear()
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)



class HeatmapInteractiveFigure(QWidget):
    """Figure Widget with slider."""
    def __init__(self, case, parent=None):
        from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
        """Initializer."""
        from numpy import zeros
        super().__init__(parent)

        # TODO: Figure out what is needed to initialize a figure!
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setMinimumWidth(650)
        self.canvas.setMinimumHeight(750)
        self.case = case        
#        self.case.plotmesh(ax=self.canvas.axes, colorbar=True)
        self.case.te2D(ax=self.canvas.axes)
        self.case.set_speciesarrays()
        self.verts = self.case.Qvertices
        
        self._createSlider()
        # TODO: moce to MplCanvas??
        self.canvastoolbar = NavigationToolbar2QT(self.canvas, self)
        self.test = QVBoxLayout()
        self.test.addWidget(self.canvastoolbar)
        self.test.addWidget(self.canvas)
        self.sliderControl = QGridLayout()
        self.sliderControl.addWidget(self.slider['items']['ulim'],
            0,0,1,3)
        self.sliderControl.addWidget(self.slider['items']['slider'],
            1,1,1,1)
        self.sliderControl.addWidget(self.slider['items']['llim'],
            2,0,1,3)
        self.canvaslayout = QHBoxLayout(self)
#        self.cvl2.addWidget(self.canvastoolbar)
#        self.slider = VerticalSlider(self.verts, self)
#        self.canvaslayout.addWidget(self.canvas)
        self.canvaslayout.addLayout(self.test)
        self.canvaslayout.addLayout(self.sliderControl)
#        self.canvaslayout.addWidget(self.slider)
#        self.get_lims = self.slider.get_lims
#        self.get_slider_values = self.slider.get_slider_values 
#        self.value2position = self.slider.value2position

#        self.canvaslayout.addWidget(self.canvastoolbar)
#        self.canvaslayout.addWidget(self.canvas)

        (ax, cax) = self.canvas.fig.get_axes()
        old_cax = cax.get_position()
        old_ax = ax.get_position()
        dx = 0.055
        cax.set_position([old_cax.x0+dx, old_cax.y0, old_cax.x1+dx, 0.85])
        ax.set_anchor("C")
        ax.set_position([0.1, old_ax.y0, 0.75, 0.85])

        self.casename = self.case.casename
        self.gasspecies = 0
        self.ionspecies = 0
        self.cmap = 'magma'
        self.grid = False
        self.log = False
        self.abs = False
        self.varscale = 1
        self.suptitle = ""
        self.verts.set_cmap(self.cmap)
        self.verts.set_edgecolor('face')
        self.verts.set_linewidths(1)
        self.xy = self.case.get("nx") * self.case.get("ny")
        self.var = zeros((self.case.get("nx"), self.case.get("ny")))
        for line in self.canvas.axes.lines:
            if "child" in line.get_label():
                line.remove()


#        self.layout = QHBoxLayout()
#        self.layout.addLayout(self.canvaslayout)
#        self.layout.addLayout(self.sliderControl)

        self.centralWidget = QWidget(self)
#        self.centralWidget.setLayout(self.layout)
        self.canvas.draw()

    def title(self, text):
        return f"<b><font size=4>{text}</font></b>"


    def _createSlider(self):
        lims = self.get_lims()
        self.slider = {
            'layout': QVBoxLayout(),
            'items': {
                'ulim': QLabel(self.title("{:.3g}".format(lims[1]))),
                'slider': RangeSlider(Qt.Vertical),
                'llim': QLabel(self.title("{:.3g}".format(lims[0]))),
            }
        }

        self.slider['items']['llim'].setAlignment(\
                        Qt.AlignHCenter | \
                        Qt.AlignVCenter
        )
        self.slider['items']['ulim'].setAlignment(\
                        Qt.AlignHCenter | \
                        Qt.AlignVCenter
        )
        self.slider['items']['ulim'].setFixedWidth(80)
        self.slider['items']['llim'].setFixedWidth(80)

        self.slider['items']['slider'].setMinimum(0)
        self.slider['items']['slider'].setMaximum(1000)
        self.slider['items']['slider'].setLow(0)
        self.slider['items']['slider'].setHigh(1000)
        self.slider['items']['slider'].setMinimumHeight(30)
        self.slider['items']['slider'].setValue(1000)
        self.slider['items']['slider'].sliderMoved.connect(\
                self.update_plot_range)


    """ ===========================
               SLIDER HELPERS 
        ==========================="""
    def get_lims(self):
        var = self.verts.get_array()
        if var is None:
            return (0, 1)
        return (var.min(), var.max())

    def get_slider_position(self):
        return (self.slider_lower_position(), self.slider_higher_position())

    def get_slider_values(self):
        pos = self.get_slider_position()
        return  (max(min(self.position2value(pos[0]), 1000), 0),
                 max(min(self.position2value(pos[1]), 1000),0))

    def slider_higher_position(self):
        return self.slider['items']['slider'].high()

    def slider_lower_position(self):
        return self.slider['items']['slider'].low()

    def position2value(self, pos):
        lims = self.get_lims()
        pos /= 1000
        if self.log:
            return (lims[1]**pos)*(lims[0]**(1-pos))
        else:
            return pos*lims[1] + (1-pos)*lims[0]

    def value2position(self, val):
        from numpy import log
        from numpy.ma import is_masked
        lims = self.get_lims()
        if abs(lims[0]-lims[1])<1e-20:
            return 0
        for lim in lims:
            if is_masked(lim):
                return 0
        if self.log:
            return 1000/(1+(log(lims[1])-log(val))/max(1e-20, 
                        (log(val)-log(lims[0]))))
        else:
            return 1000/(1 + ((lims[1]-val)/max(1e-10,(val-lims[0]))))
        
    def update_plot_range(self, l, u):
        from numpy.ma import is_masked
        nl = self.position2value(l)
        nu = self.position2value(u)
        for var in [nl, nu]:
            if is_masked(var):
                return 0
        self.verts.set_clim((nl, nu))
        self.verts.set_cmap(self.verts.get_cmap())
        self.slider['items']['llim'].setText(self.title("{:.3g}".format(nl)))
        self.slider['items']['ulim'].setText(self.title("{:.3g}".format(nu)))
        self.canvas.draw()



    def setTitle(self, title):
        self.suptitle = title
        self.canvas.fig.suptitle(self.suptitle)
        self.canvas.draw()

    def getTitle(self):
        return self.suptitle

    def setVar(self, var):
        from numpy.ma import masked_array
        self.var = masked_array(var)
        self.updatePlot()

    def getVar(self):
        return self.var

    def setCmap(self, cmap):
        self.cmap = cmap
        self.verts.set_cmap(cmap)
        self.canvas.draw()

    def toggleAbs(self):
        self.abs = not self.abs
        self.updatePlot()

    def toggleSeparatrix(self):
        for line in self.canvas.axes.lines:
            if line.get_label() == "lcfs":
                line.set_visible(not line.get_visible())
        self.canvas.draw()

    def setVarscale(self, val):
        self.varscale = val
        self.updatePlot()

    def toggleVessel(self):
        for line in self.canvas.axes.lines:
            if line.get_label() == 'vessel':
                line.set_visible(not line.get_visible())
        self.canvas.draw()

    def toggleLog(self):
        from matplotlib.colors import LogNorm, Normalize
        from numpy.ma import is_masked
        from numpy import log
        lims = self.get_lims()

        if (lims[0] <= 0) and (self.log is False):
            var = self.verts.get_array()
            if var is not None:
                var.mask=(var<=0)
                self.verts.set_array(var)
                lims = list(self.get_lims())
                if is_masked(lims[0]):
                    lims[0]=1e-100
                if is_masked(lims[1]):
                    lims[1]=1e100
        else:
            var = self.verts.get_array()
            if var is not None:
                var.mask=False
                self.verts.set_array(var)
                lims = self.get_lims()
        if self.log:
            self.verts.set_norm(Normalize(*lims))#vmin=lims[0], vmax=lims[1])
        else:
            self.verts.set_norm(LogNorm(*lims))
        vals = self.get_slider_values()
        self.log = not self.log 
        newpos = [int(self.value2position(x)) for x in vals]
        if newpos[0] == newpos[1]:
            newpos = [0, 1000]
        self.slider['items']['slider'].setLow(newpos[0])
        self.slider['items']['slider'].setHigh(newpos[1])
        clim = list(self.verts.get_clim())
        if self.log:
            if clim[0] <= 0:
                clim[0]=1e-100
            if (clim[1] <= 0) or (clim[1]<clim[0]):
                clim[1]=1e100
        self.verts.set_clim(clim)
        self.canvas.draw()


    def togglePlates(self):
        for line in self.canvas.axes.lines:
            if 'plate' in line.get_label():
                line.set_visible(not line.get_visible())
        self.canvas.draw()

    def toggleGrid(self):
        if self.grid:
            self.verts.set_edgecolor('face')
            self.verts.set_linewidths(1)
        else:
            self.verts.set_edgecolor('lightgrey')
            self.verts.set_linewidths(0.08)
        self.grid = not self.grid
        self.canvas.draw()


    def updatePlot(self):
        from copy import deepcopy
        from numpy import sum


        if self.log:
            self.var.mask=(self.var<=0)
        self.suptitle = self.suptitle.split("(")[0] \
            + (self.varscale != 1)*" (x{:.3g})".format(self.varscale)
        var = self.varscale*self.var
        if sum(var) == 0:
            self.raise_message("Requested variable unpopulated! "+
                "Select another variable or species to plot.")
            return
        if self.abs:
            var = abs(var)
#        if (var.min() < 0) and self.log:
#            self.raise_message("Negative values in var: masking array!")
#            var.mask=(var<=0)
        # Record old values slider values
        [llim, ulim] = deepcopy(self.verts.get_clim())
        self.verts.set_array(var[1:-1,1:-1].reshape(self.xy))
        clim = self.verts.get_clim()
        lims = self.get_lims()
        if ulim <= lims[0]:
            ulim = lims[1]
        ulim = min(ulim, lims[1])
        if llim >= lims[1]:
            llim = lims[0]
        llim = max(llim, lims[0])
        # Enseure some separation between sliders when var is constant
        if lims[1]==lims[0]:
            llim, ulim = 1, 1e100
        # Enseure some separation between sliders when bounds are maintained
        if abs(ulim-llim)/max(1e-10, abs(lims[1]-lims[0])) < 1e-2:
            llim, ulim = lims[0], lims[1]
        # NOTE
        # I HAVE NO CLUE WHY THE LOWER LIMIT DOES NOT REGISTER
        # AT THE FIRST CET_CLIM CALL, AND DONT ASK ME HOW LONG
        # IT TOOK TO FIGURE IT OUT!!!
        self.verts.set_clim((llim, ulim))
        self.verts.set_clim((llim, ulim))
        self.slider['items']['ulim'].setText(\
                self.title("{:.3g}".format(ulim)
        ))
        self.slider['items']['llim'].setText(\
                self.title("{:.3g}".format(llim)
        ))
        self.slider['items']['slider'].setHigh(
            int( self.value2position(ulim)
        ))
        self.slider['items']['slider'].setLow(
            int( self.value2position(llim)
        ))
        self.verts.set_cmap(self.verts.get_cmap())
        self.canvas.fig.suptitle(self.suptitle)
        self.canvas.draw()

    def setUpperSlider(self, ulim):
        clim = self.verts.get_clim()
        lims = self.get_lims()
        if ulim <= clim[0]:
            self.raise_message("Requested upper range {:.3g} is".format(ulim)+
                " below the current lower limit {:.3g}".format(clim[0]))
            return
        ulim = min(ulim, lims[1])
        self.verts.set_clim((clim[0], ulim))
        self.slider['items']['ulim'].setText(\
                self.title("{:.3g}".format(ulim)
        ))
        self.slider['items']['slider'].setHigh(
           int( self.value2position(ulim)
        ))
        self.canvas.draw()

    def setLowerSlider(self, llim):
        clim = self.verts.get_clim()
        lims = self.get_lims()
        if llim >= clim[1]:
            self.raise_message("Requested lower range {:.3g} is".format(llim)+
                " above the current upper limit {:.3g}".format(clim[1]))
            return
        llim = max(llim, lims[0])
        self.verts.set_clim((llim, clim[1]))
        self.slider['items']['llim'].setText(\
                self.title("{:.3g}".format(llim)
        ))
        self.slider['items']['slider'].setLow(
           int( self.value2position(llim)
        ))
        self.canvas.draw()


    def raise_message(self, message, time=5000):
        QApplication.sendEvent(self, QStatusTipEvent(message))
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_message)
        self.timer.start(time)

    def hide_message(self):
        QApplication.sendEvent(self, QStatusTipEvent(''))

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=2, height=4, dpi=300):
        from matplotlib.figure import Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)

class MyLineEdit(QLineEdit):
        pass

class MyClearLineEdit(QLineEdit):
        pass
 
class PopUp(QMainWindow):
    def __init__(self, parent=None):
        super(PopUp, self).__init__(parent)
 

class MainMenu(QMainWindow):
    """Main Window."""

    # TODO: pop-out tab option

    def __init__(self, parent=None, case=None):
        """Initializer."""
        from os import getcwd
        super().__init__(parent)
        
        self.tablist = []
        self.file = "No file loaded!"
        self.lastpath = getcwd()

        self.setFocus()
        self.setWindowTitle("UETOOLS Main Menu")
        self.resize(1300, 900)
        self.popups = []

        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self._createStatusBar()
        

        self.centralWidget = QTabWidget(self)#QLabel("Hello, World")
        self.centralWidget.setMinimumWidth(1300)
        self.centralWidget.setMinimumHeight(900)
        self.centralWidget.setTabsClosable(True)
        self.centralWidget.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.centralWidget)
        self.tabMenu.setDisabled(True)

        if case is not None:
            self.openFile(case)


    def closeTab(self, index):
        self.centralWidget.removeTab(index)
        if self.centralWidget.count() == 0:
            self.tabMenu.setDisabled(True)


    def openFile(self):#, caseobj=None):
        from uetools import Case
        # Logic for opening an existing file goes here...
        if 1==1:
            file = QFileDialog.getOpenFileName(self, 'Open UETOOLS save', 
            self.lastpath, "All files (*.*)")[0]
            self.lastpath = "/".join(file.split("/")[:-1])
        else:
            file = "/Users/holm10/Documents/fusion/uedge/src/"+\
                    "UETOOLS/dashboard_test/testcase_hires/nc20.hdf5"
            print("USING TUTORIAL CASE")
        if len(file.strip()) == 0:
            return
        try:
            case =  CaseDashboard(Case(file, inplace=True))
        except:
            self.raise_message(f"File {file} is not a valid UETOOLS save file!")
            return
        case.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # TODO: Figure out how to resize Widget with Window?!
        self.tablist.append(self.centralWidget.addTab(case,
            f"{case.casename} heatmap")
        )
        self.centralWidget.setTabToolTip(self.tablist[-1], file)
        self.centralWidget.setCurrentIndex(self.tablist[-1])
        self.raise_message(f"File > Opened {file}.")
        self.tabMenu.setDisabled(False)


    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAction)
        self.tabMenu = menuBar.addMenu("&Tab")
        self.tabMenu.addAction(self.renameTabAction)
        self.tabMenu.addAction(self.popOutTabAction)
#        helpMenu = menuBar.addMenu("&Help")
#        helpMenu.addAction(self.helpContentAction)
#        helpMenu.addAction(self.aboutAction)



    def _createActions(self):
        # Creating actions using the second constructor
        self.openAction = QAction("Open heatmap from HDF5 save...", self)
        self.renameTabAction = QAction("Rename tab", self)
        self.popOutTabAction = QAction("Pop out figure", self)
        self.exitAction = QAction("&Exit", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        
    def _createStatusBar(self):
        self.statusbar = self.statusBar()

    def _connectActions(self):
        # Connect File actions
        self.openAction.triggered.connect(self.openFile)
        self.renameTabAction.triggered.connect(self.renameTab)
        self.popOutTabAction.triggered.connect(self.popTab)
        self.exitAction.triggered.connect(self.close)

    def populateOpenRecent(self):
        # Step 1. Remove the old options from the menu
        self.openRecentMenu.clear()
        # Step 2. Dynamically create the actions
        actions = []
        filenames = [f"File-{n}" for n in range(5)]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentFile, filename))
            actions.append(action)
        # Step 3. Add the actions to the menu
        self.openRecentMenu.addActions(actions)

    def renameTab(self):
        # Logic for opening an existing file goes here...

        newname, ok = QInputDialog().getText(self, "Edit tab name",
                "New tab name:", QLineEdit.Normal,
                self.centralWidget.tabText(self.activeTab()))
        if ok and newname:
            self.centralWidget.setTabText(
                self.centralWidget.currentIndex(), 
                newname
            )
    
    def activeTab(self):
        return self.centralWidget.currentIndex()

    def transfer_HeatmapInteractiveFigure(self, plot):
        newplot=HeatmapInteractiveFigure(plot.case)
        lines = {}
        for line in plot.canvas.axes.lines:
            lines[line.get_label()] = line.get_visible()
        for line in newplot.canvas.axes.lines:
            line.set_visible(lines[line.get_label()])
        if plot.grid:
            newplot.toggleGrid()
        if plot.log:
            newplot.toggleLog()
            var = newplot.verts.get_array()
            var.masked = (var <= 0)
            newplot.verts.set_array(var)
        clim = plot.verts.get_clim()
        newplot.setTitle(plot.suptitle)
        newplot.verts.set_clim(clim)
        newplot.canvas.axes.set_xlim(plot.canvas.axes.get_xlim())
        newplot.canvas.axes.set_ylim(plot.canvas.axes.get_ylim())
        newplot.verts.set_array(plot.verts.get_array())
        newplot.setUpperSlider(clim[1])
        newplot.setLowerSlider(clim[0])
        newplot.verts.set_cmap(plot.verts.get_cmap())
        newplot.canvas.draw()
        return newplot


    def popTab(self):
        widget = self.centralWidget.widget(self.activeTab())
        plot = widget.caseplot
        newplot = self.__getattribute__(
            "transfer_{}".format(type(plot).__name__))(plot)
        self.popups.append(PopUp(self))
        self.popups[-1].show()
        title = plot.suptitle
        for substr in ["$", "\mathrm", "{","}"]:
            title = title.replace(substr, "")
        title = self.centralWidget.tabText(self.activeTab())
        self.popups[-1].setWindowTitle(title)
        self.popups[-1].setCentralWidget(newplot)



    def populateOpenRecent(self):
        # Step 1. Remove the old options from the menu
        self.openRecentMenu.clear()
        # Step 2. Dynamically create the actions
        actions = []
        filenames = [f"File-{n}" for n in range(5)]
        for filename in filenames:
            action = QAction(filename, self)
            action.triggered.connect(partial(self.openRecentFile, filename))
            actions.append(action)
        # Step 3. Add the actions to the menu
        self.openRecentMenu.addActions(actions)

    def raise_message(self, message, time=5000):
        self.statusbar.showMessage(message, time)


if __name__ == "__main__":
    import sys
    import matplotlib
    matplotlib.use('Qt5Agg')

    app = QApplication(sys.argv)

    win = MainMenu()
    win.show()
    sys.exit(app.exec_())

def uedashboard():
    import sys
    import matplotlib
    matplotlib.use('Qt5Agg')

    app = QApplication(sys.argv)
    win = MainMenu()
    win.show()
    sys.exit(app.exec_())
    
#else:
#    app = QApplication(sys.argv)
#    win = CaseDashboard(self)    
#    win.show()
#    sys.exit(app.exec_())
