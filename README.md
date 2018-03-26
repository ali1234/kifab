Export gerbers from Kicad and renames them to the defacto standard filenames:

 - F_Cu -> .GTL
 - B_Cu -> .GBL
 - F_SilkS -> .GTS
 - B_SilkS -> .GBS
 - F_Mask -> .GTM
 - B_Mask -> .GBM
 - Edge_Cuts -> .GML

Options:

 - -i: Input PCB file.
 - -o: Output path for export.
 - -s: additional suffix for exported files.

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

    kifab -i $PROJECT.kicad_pcb -o $TEMPDIR/$FULLNAME -s $VERSION
    cp -r docs/* $TEMPDIR/$FULLNAME
    cd $TEMPDIR
    zip -r $FULLNAME.zip $FULLNAME/
    cd -
    cp $TEMPDIR/$FULLNAME.zip .
    rm -rf --one-file-system $TEMPDIR

