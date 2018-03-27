## Export fabrication files from KiCad using a YAML config.

Kifab creates plot and drill files according to a config file similar
to how Eagle uses a CAM file. The config file is written in YAML and
describes which layers should be plotted, the plotting options, and can
also override the output filename extensions.

Kifab has no warranty. Check anything it produces carefully before
submitting for fabrication.

    usage: kifab [-h] [-o OUTDIR] [-s SUFFIX] PCBFILE FABFILE

    positional arguments:
      PCBFILE               Kicad PCB file.
      FABFILE               Kifab FAB file.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTDIR, --outdir OUTDIR
                            Generate files in this directory.
      -s SUFFIX, --suffix SUFFIX
                            Common suffix for generated files.

### Example configs:

This will create a single gerber containing the top copper layer, using
default options, and the output file with use the Protel extension .gtl:

    plots:
      - comment: Top Copper
        layers:
          id: F_Cu

This will export Edge.Cuts gerber but the output file will have the
extension .gml instead of .gm1:

    plots:
      - comment: Mechanical
        extension: .gml
        layers:
          id: Edge_Cuts

This will produce two separate gerbers, one for the top copper and one
for the bottom:

    plots:
      - comment: Top Copper
        layers:
          - id: F_Cu

      - comment: Bottom Copper
        layers:
          - id: B_Cu

This will produce an SVG file with the listed layers. The colours will
not be used because KiCad does not yet support setting colours from
python script. Instead, the default layer colours will be used:

    plots:
      - comment: Top Render
        format: PLOT_FORMAT_SVG
        suffix: top
        aux_origin: False
        layers:
          - id: Edge_Cuts
          - id: F_Cu
            colour: [0.7, 0.7, 0.7, 1.0]
          - id: F_Mask
            colour: [1.0, 0.0, 0.0, 0.5]
          - id: F_SilkS
            colour: [1.0, 1.0, 1.0, 1.0]
          - id: Dwgs_User

The config file contains a list of plots, and each plot contains a list
of layers to be plotted. Both plots and layers have properties which are
passed to Board.plot and Board.plot_layer respectively. In other words,
you can see the available options by looking at the keyword arguments to
those functions.

Each plot can have a suffix, which is added to the output filename
before the global suffix (from the command line).

The config file can also contain drill settings:

    drill:
        merge_npth: False

This will export Excellion drill files. Separate files for plated and
non-plated holes will be produced.

The options for the drill item are passed to Board.drill.

See also example.fab.


### Example usage - building a zip file:

    #!/bin/sh

    PROJECT=zerostem
    VERSION=$(git describe)

    if [ -z "$VERSION" ]; then \
        echo "Please tag this commit before generating a zip."
        exit 1
    fi

    FULLNAME=$PROJECT-$VERSION

    TEMPDIR=$(mktemp -d)
    mkdir $TEMPDIR/$FULLNAME

    kifab -o $TEMPDIR/$FULLNAME -s $VERSION $PROJECT.kicad_pcb $PROJECT.fab
    cp -r docs/* $TEMPDIR/$FULLNAME
    cd $TEMPDIR
    zip -r $FULLNAME.zip $FULLNAME/
    cd -
    cp $TEMPDIR/$FULLNAME.zip .
    rm -rf --one-file-system $TEMPDIR
