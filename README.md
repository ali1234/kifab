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
