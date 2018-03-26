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

        popt.SetOutputDirectory(dest)

        popt.SetPlotFrameRef(False)
        popt.SetLineWidth(pcbnew.FromMM(0.1))
        popt.SetAutoScale(False)
        popt.SetScale(1)
        popt.SetMirror(False)
        popt.SetUseGerberAttributes(True)
        popt.SetExcludeEdgeLayer(False)
        popt.SetScale(1)
        popt.SetUseAuxOrigin(True)

        popt.SetSubtractMaskFromSilk(False)

        plot_plan = [
            ( ".GTL", pcbnew.F_Cu, "Copper Top" ),
            ( ".GBL", pcbnew.B_Cu, "Copper Bottom" ),
            ( ".GTS", pcbnew.F_SilkS, "Silk Top" ),
            ( ".GBS", pcbnew.B_SilkS, "Silk Bottom" ),
            ( ".GTM", pcbnew.B_Mask, "Solder Mask Stop Top" ),
            ( ".GBM", pcbnew.F_Mask, "Solder Mask Stop Bottom" ),
            ( ".GML", pcbnew.Edge_Cuts, "Mechanical" ),
        ]

        for layer_info in plot_plan:
            pctl.OpenPlotfile(suffix, pcbnew.PLOT_FORMAT_GERBER, layer_info[2])
            pctl.SetLayer(layer_info[1])
            pctl.PlotLayer()
            filename = pctl.GetPlotFileName()
            pctl.ClosePlot()
            os.rename(filename, filename.replace('.gbr', layer_info[0]))

    def plot_drills(self, dest, suffix):
        dctl = pcbnew.EXCELLON_WRITER(self._board)
        dctl.SetMergeOption(False)
        dctl.SetFormat(False)
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