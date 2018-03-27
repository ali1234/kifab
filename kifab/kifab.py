import argparse
import os
import pcbnew

class Board(object):
    def __init__(self, filename):
        self._board = pcbnew.LoadBoard(filename)
        self._name = os.path.basename(filename).rsplit('.', 1)[0]

    def mk_suffixed_name(self, suffix=''):
        if len(suffix):
            return '-'.join([self._name, suffix])
        else:
            return self._name

    def plot_gerbers(self, dest, suffix):

        pctl = pcbnew.PLOT_CONTROLLER(self._board)

        popt = pctl.GetPlotOptions()

        popt.SetOutputDirectory(os.path.abspath(dest))

        popt.SetPlotFrameRef(False)         # "Plot sheet reference on all layers"
        popt.SetPlotValue(True)             # "Plot footprint values"
        popt.SetPlotReference(True)         # "Plot footprint references"
        popt.SetPlotInvisibleText(False)    # "Force plotting of invisible values/references"
        popt.SetPlotViaOnMaskLayer(False)   # "Do not tent vias"
        popt.SetExcludeEdgeLayer(False)     # "Exclude PCB edge layer from other layers"
        popt.SetPlotPadsOnSilkLayer(False)  # "Exclude pads from silkscreen" NOTE: meaning is reversed from GUI
        popt.SetMirror(False)               # "Mirrored plot"
        popt.SetNegative(False)             # "Negative plot"
        popt.SetUseAuxOrigin(True)          # "Use auxiliary axis as origin"

        popt.SetDrillMarksType( pcbnew.PCB_PLOT_PARAMS.NO_DRILL_SHAPE )
        popt.SetAutoScale(False)
        popt.SetScale(1)
        popt.SetPlotMode(pcbnew.FILLED)
        popt.SetLineWidth(pcbnew.FromMM(0.1))

        popt.SetUseGerberProtelExtensions(False)
        popt.SetUseGerberAttributes(False)
        #popt.SetUseGerberAdvancedAttributes(False) # NOTE: missing from API
        popt.SetCreateGerberJobFile(False)
        popt.SetSubtractMaskFromSilk(False)

        popt.SetGerberPrecision(6) # 5 or 6

        plot_plan = [
            ( ".GTL", pcbnew.F_Cu, "Copper Top" ),
            ( ".GBL", pcbnew.B_Cu, "Copper Bottom" ),
            ( ".GTS", pcbnew.F_SilkS, "Silk Top" ),
            ( ".GBS", pcbnew.B_SilkS, "Silk Bottom" ),
            ( ".GTM", pcbnew.F_Mask, "Solder Mask Stop Top" ),
            ( ".GBM", pcbnew.B_Mask, "Solder Mask Stop Bottom" ),
            ( ".GML", pcbnew.Edge_Cuts, "Mechanical" ),
        ]

        for layer_info in plot_plan:
            if layer_info[1] < pcbnew.B_Cu:
                popt.SetSkipPlotNPTH_Pads( True )
            else:
                popt.SetSkipPlotNPTH_Pads( False )

            pctl.SetLayer(layer_info[1])
            pctl.OpenPlotfile(suffix, pcbnew.PLOT_FORMAT_GERBER, layer_info[2])
            pctl.PlotLayer()
            filename = pctl.GetPlotFileName()
            pctl.ClosePlot()
            os.rename(filename, filename.replace('.gbr', layer_info[0]))

    def plot_drills(self, dest, suffix):
        dctl = pcbnew.EXCELLON_WRITER(self._board)

        mirror = False
        minimalHeader = False
        offset = self._board.GetAuxOrigin()
        mergeNPTH = False # two files
        dctl.SetOptions( mirror, minimalHeader, offset, mergeNPTH )

        metricFmt = True
        dctl.SetFormat( metricFmt )

        dctl.CreateDrillandMapFilesSet(dest, aGenDrill=True, aGenMap=False)

        oldname = os.path.join(dest, self._name)
        newname = os.path.join(dest, self.mk_suffixed_name(suffix))
        os.rename(oldname + '-PTH.drl', newname + '-PTH.TXT')
        os.rename(oldname + '-NPTH.drl', newname + '-NPTH.TXT')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Kicad PCB file to export.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output directory.')
    parser.add_argument('-s', '--suffix', type=str, default='',
                        help='Suffix for generated files.')

    args = parser.parse_args()

    board = Board(args.input)

    board.plot_gerbers(args.output, args.suffix)
    board.plot_drills(args.output, args.suffix)

if __name__ == '__main__':
    main()