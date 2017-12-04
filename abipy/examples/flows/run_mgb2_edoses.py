#!/usr/bin/env python
r"""
Flow for Bands + DOS
====================

Band structure and the electron DOS of MgB2 with different k-point samplings.
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import os
import sys
import abipy.data as abidata
import abipy.abilab as abilab
from abipy import flowtk


def make_scf_nscf_inputs(structure, pseudos, paral_kgb=1):
    """return GS, NSCF (band structure), and DOSes input."""

    multi = abilab.MultiDataset(structure, pseudos=pseudos, ndtset=5)

    # Global variables
    global_vars = dict(ecut=10,
                       nband=11,
                       timopt=-1,
                       occopt=4,    # Marzari smearing
                       tsmear=0.03,
                       paral_kgb=paral_kgb,
                    )

    multi.set_vars(global_vars)

    # Dataset 1 (GS run)
    multi[0].set_kmesh(ngkpt=[8,8,8],  shiftk=structure.calc_shiftk())
    multi[0].set_vars(tolvrs=1e-6)

    # Dataset 2 (NSCF Band Structure)
    multi[1].set_kpath(ndivsm=6)
    multi[1].set_vars(tolwfr=1e-12)

    # Dos calculations with increasing k-point sampling.
    for i, nksmall in enumerate([4, 8, 16]):
        multi[i+2].set_vars(
            iscf=-3,   # NSCF calculation
            ngkpt=structure.calc_ngkpt(nksmall),
            shiftk=[0.0, 0.0, 0.0],
            tolwfr=1.0e-10,
        )

    # return GS, NSCF (band structure), DOSes input.
    return  multi.split_datasets()


def build_flow(options):
    # Working directory (default is the name of the script with '.py' removed and "run_" replaced by "flow_")
    if not options.workdir:
        options.workdir = os.path.basename(__file__).replace(".py", "").replace("run_", "flow_")

    #pseudos = abidata.pseudos("12mg.pspnc", "5b.pspnc")
    structure = abidata.structure_from_ucell("MgB2")

    # Get pseudos from a table.
    table = abilab.PseudoTable(abidata.pseudos("12mg.pspnc", "5b.pspnc"))
    pseudos = table.get_pseudos_for_structure(structure)

    nval = structure.num_valence_electrons(pseudos)
    #print(nval)

    inputs = make_scf_nscf_inputs(structure, pseudos)
    scf_input, nscf_input, dos_inputs = inputs[0], inputs[1], inputs[2:]
    #print(scf_input.pseudos)

    return flowtk.bandstructure_flow(options.workdir, scf_input, nscf_input,
                                     dos_inputs=dos_inputs, manager=options.manager)


# This block generates the thumbnails in the Abipy gallery.
# You can safely REMOVE this part if you are using this script for production runs.
if os.getenv("GENERATE_SPHINX_GALLERY", False):
    __name__ = None
    import tempfile
    options = flowtk.build_flow_main_parser().parse_args(["-w", tempfile.mkdtemp()])
    build_flow(options).plot_networkx()


@flowtk.flow_main
def main(options):
    """
    This is our main function that will be invoked by the script.
    flow_main is a decorator implementing the command line interface.
    Command line args are stored in `options`.
    """
    return build_flow(options)


if __name__ == "__main__":
    sys.exit(main())
