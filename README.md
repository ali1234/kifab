Export fabrication files from Kicad using a YAML config.


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


Example usage:

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
