#Test case 1
python wumpus2csp.py --input wumpus_maps/wumpus_01.json --action north --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_01_north_b.csp
python solver.py wumpus_outputs/wumpus_01_north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_01.json --action east --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_01_east_b.csp
python solver.py wumpus_outputs/wumpus_01_east_a.csp

#------------------------------------------------------------------------------------------------------
#Test case 2
python wumpus2csp.py --input wumpus_maps/wumpus_02.json --action north --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_02_north_b.csp --output wumpus_outputs/wumpus_02_north_b.csp
python solver.py wumpus_outputs/wumpus_02_north_b.csp
python solver.py wumpus_outputs/wumpus_02_north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_02.json --action east --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_02_east_b.csp --output wumpus_outputs/wumpus_02_east_b.csp
python solver.py wumpus_outputs/wumpus_02_east_b.csp
python solver.py wumpus_outputs/wumpus_02_east_a.csp

#------------------------------------------------------------------------------------------------------
#Test case 3
python wumpus2csp.py --input wumpus_maps/wumpus_03.json --action east --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_03_east_b.csp
python solver.py wumpus_outputs/wumpus_03_east_a.csp

#------------------------------------------------------------------------------------------------------
#Test case 4
python wumpus2csp.py --input wumpus_maps/wumpus_04.json --action north --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_04 north_b.csp
python solver.py wumpus_outputs/wumpus_04_north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_04.json --action east --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_04 east _b.csp
python solver.py wumpus_outputs/wumpus_04 east _a.csp

#------------------------------------------------------------------------------------------------------
#Test case 5
python wumpus2csp.py --input wumpus_maps/wumpus_05.json --action north --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_05_north_b.csp --output wumpus_outputs/wumpus_05_north_b.csp
python solver.py wumpus_outputs/wumpus_05 north_b.csp
python solver.py wumpus_outputs/wumpus_05 _north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_05.json --action south --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_05_south_b.csp --output wumpus_outputs/wumpus_05_south_b.csp
python solver.py wumpus_outputs/wumpus_05 south _b.csp
python solver.py wumpus_outputs/wumpus_05 south _a.csp

#------------------------------------------------------------------------------------------------------
#Test case 6
python wumpus2csp.py --input wumpus_maps/wumpus_06.json --action east --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_06_east_b.csp --output wumpus_outputs/wumpus_06_east_b.csp
python solver.py wumpus_outputs/wumpus_06 north_b.csp
python solver.py wumpus_outputs/wumpus_06_north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_06.json --action south --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_06_south_b.csp --output wumpus_outputs/wumpus_06_south_b.csp
python solver.py wumpus_outputs/wumpus_06 south _b.csp
python solver.py wumpus_outputs/wumpus_06 south _a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_06.json --action west --output wumpus_outputs
python n_to_bin.py --input wumpus_outputs/wumpus_06_west_b.csp --output wumpus_outputs/wumpus_06_west_b.csp
python solver.py wumpus_outputs/wumpus_06 west _b.csp
python solver.py wumpus_outputs/wumpus_06 west _a.csp
#------------------------------------------------------------------------------------------------------
#Test case 7
python wumpus2csp.py --input wumpus_maps/wumpus_07.json --action north --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_07 north_b.csp
python solver.py wumpus_outputs/wumpus_07 _north_a.csp

python wumpus2csp.py --input wumpus_maps/wumpus_07.json --action east --output wumpus_outputs
python solver.py wumpus_outputs/wumpus_07 east _b.csp
python solver.py wumpus_outputs/wumpus_07 east _a.csp