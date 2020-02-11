# PyFoil
A Python script that pulls and parses aerodynamic data for various airfoils into a spreadsheet. Made in early 2018 (this is not the highest quality code as a result...)

## Details
This script was made in early 2018 for the UQ Racing team. A database for aerofoil information would be highly beneficial for the team’s aerodynamic development, as it would provide a centralised location for the newly formed aero development team to quantitatively compare different aerofoil shapes with information such as thickness, camber, leading edge, trailing edge as well as lift and drag coeffficients at various AoA (angles of attack). The script pulls data for a number of airfoils from [Airfoil Tools](http://airfoiltools.com/) and parses it through the [XFOIL](https://web.mit.edu/drela/Public/web/xfoil/) program. 

The process is split into 4 functions:
- `get_foil_list()` goes to the [UIUC database](https://m-selig.ae.illinois.edu/ads/coord_database.html) and returns a list of all aerofoils.
- `get_foils()` downloads the corresponding Selig format source files from Airfoil Tools.
- `xfoil(re)` processes all of the foils listed in `get_foil_list()` and exports .pol files for the given Reynolds number `re`.
- `process_dat()` opens the .pol files and exports to .csv also including file data such as thickness, camber, leading edges, trailing edges and more.
The functions must be run in this sequence. The program also contains some lines at the beginning to initialise some variables.

## Usage
To run, this script requires a Windows system as this is what XFOIL is based on.
1. Create the empty directories `csv`, `dat`, `datexcl` and `pol` in this folder.
2. Copy the files from `XFOIL.zip` (see XFOIL website) into the same directory as the `pyfoil3.py` file.
3. Edit `pyfoil3.py` to run the required functions to make a database.
4. Run `pyfoil3.py` in a Windows command line.

