primer = """Your goal is to convert molecular biology protocols into python pseudocode. Here is an example of how to convert a protocol into pseudocode:

EXAMPLE: 
example protocol entitled '{example_title}':
{example_protocol}

example pseudocode:
{example_pseudocode}


YOUR TASK:
Here is a molecular biology protocol entitled '{title}' The protocol steps are as follows:

protocol:
{protocol}

Please convert this protocol into python pseudocode. Please define the python functions you will use at the start of the pseudocode, and ensure that these functions have parameters where appropriate.

pseudocode:"""

example_title = "Recombinant protein expression and purification of codon-optimized Bst-LF polymerase"

protocol_example = """
1. Transform 100 ng of pET15b plasmid containing codon-optimized Bst-LF polymerase into E. coli C41 competent cells using either heat shock or electroporation.
2. Spread transformed cells in LB Agar plates supplemented with 0.1 mg/mL Amp. Grow plate overnight at 37 °C.
3. Select a single colony from the LB agar plate to prepare a preinoculum in 10mL LB media supplemented with 0.1 mg/mL Amp. Grow overnight at 250 rpm, 37 °C.
4. Use the full volume of the preinoculum to inoculate 1L of LB media supplemented with 0.1 mg/mL Amp. Grow at 200 rpm 18 °C until reaching an optical density at 600 nm (OD600) = 0.8.
5. Upon reaching OD600 = 0.8, add IPTG to a final concentration of 0.5 millimolar (mM) and incubate overnight at 200 rpm 18 °C.
6. Centrifuge the cell culture at 4000 x g, 4°C, for 30 minutes. Then, resuspend the cell pellet in 40 mL of Buffer A freshly supplemented with 1.0 millimolar (mM) PMSF and 0.2 mg/mL lysozyme.
7. Incubate the resuspended cells at 80 rpm, Room temperature (RT), for 30 minutes.
8. Sonicate on ice for 8 minutes using cycles of one second on ON and four seconds OFF at 40% amplitude
9. On an ultracentrifugation tube, incubate the unclarified lysate at 65 °C for 25 minutes to precipitate most of E. coli proteins, and then place on ice for 5 minutes. Centrifuge (20000 x g, 4°C, 30 minutes) and collect the supernatant. 
10. On a 5 mL HisTrap column pre-equilibrated with 10 column volumes (c.v.) (here, 50 mL) of Buffer A, load the supernant. Wash with 10-20 c.v. of Buffer B. Then, elute with 5 c.v. of Buffer C, collecting the eluted fractions every 1 mL in 1.5 ml tubes.
11. To pool the fractions containing the protein of interest, prepare a 96-well plate or 1.5 mL tubes with 40 µL of 5X Bradford reagent and 160 µL of distilled water. Add 10 µL of each protein fraction and compare against a blank reference sample corresponding to 10 µL of Buffer B. You can determine your protein-containing fractions either by absorbance at 595 nm on a plate reader or visually by comparing the blue coloration of each fraction against the blank reference. Pool your fractions.
12. To decrease the imidazole concentration, perform a buffer exchange step with an Amicon Ultra-15 concentrator. Centrifuge (3000 x g, 10°C, 10 minutes), discard the flowthrough, and add Buffer D to decrease the imidazole concentration. Repeat this step until the imidazole concentration reaches < 30 mM.
13. Recover the concentrated protein and determine its concentration using the Bradford assay. Then, supplement with 0.2 mM EDTA, 0.2 % volume Triton X-100, 2 mM DTT and add glycerol up to 50 % volume to reach Storage Conditions."""


pseudocode_example = """
def transform_cells(plasmid, method):
    pass

def grow_cells_on_agar(amp_conc, temperature, time):
    pass

def prepare_preinoculum(colony, media_vol, amp_conc, rpm, temperature):
    pass

def inoculate(preinoculum, media_vol, amp_conc, rpm, temperature, time):
    pass

def induce_protein_expression(iptg_conc, rpm, temperature, time):
    pass

def harvest_cells(culture, centrifuge_settings):
    pass

def resuspend_cells(buffer_vol, buffer_composition):
    pass

def incubate_cells(incubation_params):
    pass

def lyse_cells(sonication_params):
    pass

def purify_protein(purification_params):
    pass

def identify_protein_fractions(bradford_params):
    pass

def buffer_exchange(protein_solution, buffer_composition, centrifuge_settings, repetitions):
    pass

def finalize_protein_concentration(storage_composition):
    pass

# Protocol steps
transform_cells(cells="E. coli C41", plasmid="pET15b-Bst-LF", method="heat shock")
grow_cells_on_agar(amp_conc="0.1 mg/mL", temperature=37, time="overnight")
prepare_preinoculum(colony="single colony", media_vol="10 mL LB", amp_conc="0.1 mg/mL", rpm=250, temperature=37)
inoculate(preinoculum="full volume", media_vol="1 L LB", amp_conc="0.1 mg/mL", rpm=200, temperature=18, time="until OD600 = 0.8")
induce_protein_expression(iptg_conc="0.5 mM", rpm=200, temperature=18, time="overnight")
harvest_cells(culture="1 L culture", centrifuge_settings="4000 x g, 4°C, 30 minutes")
resuspend_cells(buffer_vol="40 mL", buffer_composition="Buffer A + 1.0 mM PMSF + 0.2 mg/mL lysozyme")
incubate_cells(incubation_params="80 rpm, RT, 30 minutes")
lyse_cells(sonication_params="8 minutes, 40% amplitude")
incubate_cells(incubation_params="65 °C, 25 minutes")
purify_protein(purification_params="HisTrap column, 10 c.v. Buffer A, 10-20 c.v. Buffer B, 5 c.v. Buffer C")
identify_protein_fractions(bradford_params="40 µL 5X Bradford reagent + 160 µL distilled water + 10 µL protein fraction")
buffer_exchange(protein_solution="protein-containing fractions", buffer_composition="Buffer D", centrifuge_settings="3000 x g, 10°C, 10 minutes", repetitions="until imidazole concentration < 30 mM")
finalize_protein_concentration(storage_composition="0.2 mM EDTA + 0.2 % volume Triton X-100 + 2 mM DTT + 50 % volume glycerol")
"""


complete_prompt = """
Your goal is to convert molecular biology protocols into python pseudocode. 

EXAMPLE
Here is an example of how to convert a protocol for recombinant protein expression and purification of codon-optimized Bst-LF polymerase into python pseudocode

example protocol:
1. Transform 100 ng of pET15b plasmid containing codon-optimized Bst-LF polymerase into E. coli C41 competent cells using either heat shock or electroporation.
2. Spread transformed cells in LB Agar plates supplemented with 0.1 mg/mL Amp. Grow plate overnight at 37 °C.
3. Select a single colony from the LB agar plate to prepare a preinoculum in 10mL LB media supplemented with 0.1 mg/mL Amp. Grow overnight at 250 rpm, 37 °C.
4. Use the full volume of the preinoculum to inoculate 1L of LB media supplemented with 0.1 mg/mL Amp. Grow at 200 rpm 18 °C until reaching an optical density at 600 nm (OD600) = 0.8.
5. Upon reaching OD600 = 0.8, add IPTG to a final concentration of 0.5 millimolar (mM) and incubate overnight at 200 rpm 18 °C.
6. Centrifuge the cell culture at 4000 x g, 4°C, for 30 minutes. Then, resuspend the cell pellet in 40 mL of Buffer A freshly supplemented with 1.0 millimolar (mM) PMSF and 0.2 mg/mL lysozyme.
7. Incubate the resuspended cells at 80 rpm, Room temperature (RT), for 30 minutes.
8. Sonicate on ice for 8 minutes using cycles of one second on ON and four seconds OFF at 40% amplitude
9. On an ultracentrifugation tube, incubate the unclarified lysate at 65 °C for 25 minutes to precipitate most of E. coli proteins, and then place on ice for 5 minutes. Centrifuge (20000 x g, 4°C, 30 minutes) and collect the supernatant. 
10. On a 5 mL HisTrap column pre-equilibrated with 10 column volumes (c.v.) (here, 50 mL) of Buffer A, load the supernant. Wash with 10-20 c.v. of Buffer B. Then, elute with 5 c.v. of Buffer C, collecting the eluted fractions every 1 mL in 1.5 ml tubes.
11. To pool the fractions containing the protein of interest, prepare a 96-well plate or 1.5 mL tubes with 40 µL of 5X Bradford reagent and 160 µL of distilled water. Add 10 µL of each protein fraction and compare against a blank reference sample corresponding to 10 µL of Buffer B. You can determine your protein-containing fractions either by absorbance at 595 nm on a plate reader or visually by comparing the blue coloration of each fraction against the blank reference. Pool your fractions.
12. To decrease the imidazole concentration, perform a buffer exchange step with an Amicon Ultra-15 concentrator. Centrifuge (3000 x g, 10°C, 10 minutes), discard the flowthrough, and add Buffer D to decrease the imidazole concentration. Repeat this step until the imidazole concentration reaches < 30 mM.
13. Recover the concentrated protein and determine its concentration using the Bradford assay. Then, supplement with 0.2 mM EDTA, 0.2 % volume Triton X-100, 2 mM DTT and add glycerol up to 50 % volume to reach Storage Conditions.


example python pseudocode:
def transform_cells(plasmid, method):
    pass

def grow_cells_on_agar(amp_conc, temperature, time):
    pass

def prepare_preinoculum(colony, media_vol, amp_conc, rpm, temperature):
    pass

def inoculate(preinoculum, media_vol, amp_conc, rpm, temperature, time):
    pass

def induce_protein_expression(iptg_conc, rpm, temperature, time):
    pass

def harvest_cells(culture, centrifuge_settings):
    pass

def resuspend_cells(buffer_vol, buffer_composition):
    pass

def incubate_cells(incubation_params):
    pass

def lyse_cells(sonication_params):
    pass

def purify_protein(purification_params):
    pass

def identify_protein_fractions(bradford_params):
    pass

def buffer_exchange(protein_solution, buffer_composition, centrifuge_settings, repetitions):
    pass

def finalize_protein_concentration(storage_composition):
    pass

# Protocol steps
transform_cells(cells="E. coli C41", plasmid="pET15b-Bst-LF", method="heat shock")
grow_cells_on_agar(amp_conc="0.1 mg/mL", temperature=37, time="overnight")
prepare_preinoculum(colony="single colony", media_vol="10 mL LB", amp_conc="0.1 mg/mL", rpm=250, temperature=37)
inoculate(preinoculum="full volume", media_vol="1 L LB", amp_conc="0.1 mg/mL", rpm=200, temperature=18, time="until OD600 = 0.8")
induce_protein_expression(iptg_conc="0.5 mM", rpm=200, temperature=18, time="overnight")
harvest_cells(culture="1 L culture", centrifuge_settings="4000 x g, 4°C, 30 minutes")
resuspend_cells(buffer_vol="40 mL", buffer_composition="Buffer A + 1.0 mM PMSF + 0.2 mg/mL lysozyme")
incubate_cells(incubation_params="80 rpm, RT, 30 minutes")
lyse_cells(sonication_params="8 minutes, 40% amplitude")
incubate_cells(incubation_params="65 °C, 25 minutes")
purify_protein(purification_params="HisTrap column, 10 c.v. Buffer A, 10-20 c.v. Buffer B, 5 c.v. Buffer C")
identify_protein_fractions(bradford_params="40 µL 5X Bradford reagent + 160 µL distilled water + 10 µL protein fraction")
buffer_exchange(protein_solution="protein-containing fractions", buffer_composition="Buffer D", centrifuge_settings="3000 x g, 10°C, 10 minutes", repetitions="until imidazole concentration < 30 mM")
finalize_protein_concentration(storage_composition="0.2 mM EDTA + 0.2 % volume Triton X-100 + 2 mM DTT + 50 % volume glycerol")
# end of protocol


YOUR TASK:
Here is a molecular biology protocol entitled '{title}' The protocol steps are as follows:

{protocol}

Please convert this protocol into python pseudocode. Please define the python functions you will use at the start of the pseudocode, and ensure that these functions have parameters where appropriate.

python pseudocode:
"""
