import os
import pcbnew

class Board(object):

    def __init__(self, filename):
        self._board = pcbnew.LoadBoard(filename)
        self._name = os.path.basename(filename).rsplit('.', 1)[0]
        self._pctl = pcbnew.PLOT_CONTROLLER(self._board)
        self._popt = self._pctl.GetPlotOptions()


    def plot_layer(self, id=None, colour=None):
        if id is None:
            raise Exception('Layer has no id.')

        self._pctl.SetLayer(getattr(pcbnew, id))
        if colour is None:
            self._pctl.SetColorMode(False)
        else:
            self._pctl.SetColorMode(True)
            # Setting a colour currently does not work
            # see https://lists.launchpad.net/kicad-developers/msg28776.html
            self._popt.SetColor(pcbnew.COLOR4D(*colour))
        self._popt.SetSkipPlotNPTH_Pads(id <= pcbnew.B_Cu)
        self._pctl.PlotLayer()


    def plot(self, dest, global_suffix='',
                suffix='',
                format='PLOT_FORMAT_GERBER',
                extension=None,
                layers=None,
                comment='',
                mirror=False,
                negative=False,
                aux_origin=True,
                no_tent_vias=False,
                exclude_edge=False,
                precision=6,
             ):

        if layers is None:
            raise Exception('No layers for plot.')

        suffix = '-'.join([suffix, global_suffix]).strip('- ')

        self._popt.SetPlotFrameRef(False)              # "Plot sheet reference on all layers" NOTE: Must be false
        self._popt.SetPlotValue(True)                  # "Plot footprint values"
        self._popt.SetPlotReference(True)              # "Plot footprint references"
        self._popt.SetPlotInvisibleText(False)         # "Force plotting of invisible values/references"
        self._popt.SetPlotViaOnMaskLayer(no_tent_vias) # "Do not tent vias"
        self._popt.SetExcludeEdgeLayer(exclude_edge)   # "Exclude PCB edge layer from other layers"
        self._popt.SetPlotPadsOnSilkLayer(False)       # "Exclude pads from silkscreen" NOTE: meaning is reversed from GUI
        self._popt.SetMirror(mirror)                   # "Mirrored plot" NOTE: affects entire file
        self._popt.SetNegative(negative)               # "Negative plot" NOTE: affects entire file
        self._popt.SetUseAuxOrigin(aux_origin)         # "Use auxiliary axis as origin"

        self._popt.SetDrillMarksType( pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE )
        self._popt.SetAutoScale(False)
        self._popt.SetScale(1)
        self._popt.SetPlotMode(pcbnew.FILLED)
        self._popt.SetLineWidth(pcbnew.FromMM(0.1))

        self._popt.SetUseGerberProtelExtensions(extension is None)
        self._popt.SetUseGerberAttributes(False)
        #popt.SetUseGerberAdvancedAttributes(False) # NOTE: missing from API
        self._popt.SetCreateGerberJobFile(False)
        self._popt.SetSubtractMaskFromSilk(False)

        self._popt.SetGerberPrecision(precision) # 5 or 6

        self._popt.SetOutputDirectory(os.path.abspath(dest))

        # for gerbers, we must set the layer before opening the file
        # for the attributes to be set correctly.
        self._pctl.SetLayer(getattr(pcbnew, layers[0]['id']))

        self._pctl.OpenPlotfile(suffix, getattr(pcbnew, format), comment)

        for layer in layers:
            self.plot_layer(**layer)

        filename = self._pctl.GetPlotFileName()
        self._pctl.ClosePlot()
        if extension is not None:
            os.rename(filename, filename.replace('.gbr', extension))


    def drill(self, dest, global_suffix='',
              merge_npth=False,
              extension=None,
              mirror=False,
              aux_origin=True,
              minimal_header=False,
              metric=True,
              ):

        dctl = pcbnew.EXCELLON_WRITER(self._board)
        if aux_origin:
            offset = self._board.GetAuxOrigin()
        else:
            offset = pcbnew.wxPoint(0,0)
        dctl.SetOptions(mirror, minimal_header, offset, merge_npth )
        dctl.SetFormat(metric)
        dctl.CreateDrillandMapFilesSet(dest, aGenDrill=True, aGenMap=False)

        oldname = os.path.join(dest, self._name)
        if len(global_suffix):
            newname = os.path.join(dest, self._name + '-' + global_suffix)
        else:
            newname = oldname

        oldext = '.drl'
        if extension is not None:
            newext = extension
        else:
            newext = oldext

        if newname != oldname or newext != oldext:
            if merge_npth:
                os.rename(oldname + oldext, newname + newext)
            else:
                for s in ['-PTH', '-NPTH']:
                    os.rename(oldname + s + oldext, newname + s + newext)
