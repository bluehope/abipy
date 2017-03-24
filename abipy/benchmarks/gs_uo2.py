#!/usr/bin/env python
"""
UO2 with 96 atoms. PAW and nsppol=2
GS calculations with paralkgb==1. Compare wfoptalg in [default, 1].
"""

from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import operator
import numpy as np
import abipy.abilab as abilab
import abipy.flowtk as flowtk
import abipy.data as abidata

from functools import reduce
from itertools import product
from pymatgen.core.units import bohr_to_ang
from abipy.benchmarks import bench_main, BenchmarkFlow


def make_input():
    """
    UO2 with 96 atoms.
    GS calculations with paralkgb==1
    """
    pseudos = abidata.pseudos("u.paw", "o.paw")

    # Atomic Positions.
    xred = np.fromstring("""
   0.00000000000000   0.00000000000000   0.00000000000000
   0.25000000000000   0.25000000000000   0.00000000000000
   0.25000000000000   0.00000000000000   0.25000000000000
   0.00000000000000   0.25000000000000   0.25000000000000
   0.00000000000000   0.00000000000000   0.50000000000000
   0.25000000000000   0.25000000000000   0.50000000000000
   0.25000000000000   0.00000000000000   0.75000000000000
   0.00000000000000   0.25000000000000   0.75000000000000
   0.00000000000000   0.50000000000000   0.00000000000000
   0.25000000000000   0.75000000000000   0.00000000000000
   0.25000000000000   0.50000000000000   0.25000000000000
   0.00000000000000   0.75000000000000   0.25000000000000
   0.00000000000000   0.50000000000000   0.50000000000000
   0.25000000000000   0.75000000000000   0.50000000000000
   0.25000000000000   0.50000000000000   0.75000000000000
   0.00000000000000   0.75000000000000   0.75000000000000
   0.50000000000000   0.00000000000000   0.00000000000000
   0.75000000000000   0.25000000000000   0.00000000000000
   0.75000000000000   0.00000000000000   0.25000000000000
   0.50000000000000   0.25000000000000   0.25000000000000
   0.50000000000000   0.00000000000000   0.50000000000000
   0.75000000000000   0.25000000000000   0.50000000000000
   0.75000000000000   0.00000000000000   0.75000000000000
   0.50000000000000   0.25000000000000   0.75000000000000
   0.50000000000000   0.50000000000000   0.00000000000000
   0.75000000000000   0.75000000000000   0.00000000000000
   0.75000000000000   0.50000000000000   0.25000000000000
   0.50000000000000   0.75000000000000   0.25000000000000
   0.50000000000000   0.50000000000000   0.50000000000000
   0.75000000000000   0.75000000000000   0.50000000000000
   0.75000000000000   0.50000000000000   0.75000000000000
   0.50000000000000   0.75000000000000   0.75000000000000
   0.12500000000000   0.12500000000000   0.12500000000000
   0.12500000000000   0.37500000000000   0.12500000000000
   0.37500000000000   0.12500000000000   0.12500000000000
   0.37500000000000   0.37500000000000   0.12500000000000
   0.12500000000000   0.12500000000000   0.37500000000000
   0.12500000000000   0.37500000000000   0.37500000000000
   0.37500000000000   0.12500000000000   0.37500000000000
   0.37500000000000   0.37500000000000   0.37500000000000
   0.12500000000000   0.12500000000000   0.62500000000000
   0.12500000000000   0.37500000000000   0.62500000000000
   0.37500000000000   0.12500000000000   0.62500000000000
   0.37500000000000   0.37500000000000   0.62500000000000
   0.12500000000000   0.12500000000000   0.87500000000000
   0.12500000000000   0.37500000000000   0.87500000000000
   0.37500000000000   0.12500000000000   0.87500000000000
   0.37500000000000   0.37500000000000   0.87500000000000
   0.12500000000000   0.62500000000000   0.12500000000000
   0.12500000000000   0.87500000000000   0.12500000000000
   0.37500000000000   0.62500000000000   0.12500000000000
   0.37500000000000   0.87500000000000   0.12500000000000
   0.12500000000000   0.62500000000000   0.37500000000000
   0.12500000000000   0.87500000000000   0.37500000000000
   0.37500000000000   0.62500000000000   0.37500000000000
   0.37500000000000   0.87500000000000   0.37500000000000
   0.12500000000000   0.62500000000000   0.62500000000000
   0.12500000000000   0.87500000000000   0.62500000000000
   0.37500000000000   0.62500000000000   0.62500000000000
   0.37500000000000   0.87500000000000   0.62500000000000
   0.12500000000000   0.62500000000000   0.87500000000000
   0.12500000000000   0.87500000000000   0.87500000000000
   0.37500000000000   0.62500000000000   0.87500000000000
   0.37500000000000   0.87500000000000   0.87500000000000
   0.62500000000000   0.12500000000000   0.12500000000000
   0.62500000000000   0.37500000000000   0.12500000000000
   0.87500000000000   0.12500000000000   0.12500000000000
   0.87500000000000   0.37500000000000   0.12500000000000
   0.62500000000000   0.12500000000000   0.37500000000000
   0.62500000000000   0.37500000000000   0.37500000000000
   0.87500000000000   0.12500000000000   0.37500000000000
   0.87500000000000   0.37500000000000   0.37500000000000
   0.62500000000000   0.12500000000000   0.62500000000000
   0.62500000000000   0.37500000000000   0.62500000000000
   0.87500000000000   0.12500000000000   0.62500000000000
   0.87500000000000   0.37500000000000   0.62500000000000
   0.62500000000000   0.12500000000000   0.87500000000000
   0.62500000000000   0.37500000000000   0.87500000000000
   0.87500000000000   0.12500000000000   0.87500000000000
   0.87500000000000   0.37500000000000   0.87500000000000
   0.62500000000000   0.62500000000000   0.12500000000000
   0.62500000000000   0.87500000000000   0.12500000000000
   0.87500000000000   0.62500000000000   0.12500000000000
   0.87500000000000   0.87500000000000   0.12500000000000
   0.62500000000000   0.62500000000000   0.37500000000000
   0.62500000000000   0.87500000000000   0.37500000000000
   0.87500000000000   0.62500000000000   0.37500000000000
   0.87500000000000   0.87500000000000   0.37500000000000
   0.62500000000000   0.62500000000000   0.62500000000000
   0.62500000000000   0.87500000000000   0.62500000000000
   0.87500000000000   0.62500000000000   0.62500000000000
   0.87500000000000   0.87500000000000   0.62500000000000
   0.62500000000000   0.62500000000000   0.87500000000000
   0.62500000000000   0.87500000000000   0.87500000000000
   0.87500000000000   0.62500000000000   0.87500000000000
   0.87500000000000   0.87500000000000   0.87500000000000
""", sep=" ").reshape((-1,3))

    # Crystal structure with acell 3*11. angstrom natom 96 ntypat 2
    structure = abilab.Structure.from_abivars(
        acell=3 * [11. / bohr_to_ang],
        rprim=np.eye(3), 
        typat=32*[1] + 64*[2],
        znucl=[92, 8],
        xred=xred,
    )

    inp = abilab.AbinitInput(structure, pseudos)
    inp.set_vars(
        # SCF algorithm
        paral_kgb=1,
        wfoptalg=1,
        nline=6,
        fftalg=402,
        #fftalg=302,  ! To use FFTW instead of ABINIT FFT

        # Basis set
        ecut=6,
        pawecutdg=10,

        # SCF parameters 
        toldfe=1.e-5,
        nstep=28,
        #diemac 500.

        # K-Points and symmetries.
        nkpt=1,
        kpt=[0.5, 0.5, 0.5],
        kptopt=0,
        istwfk="*1",
        nsym=0,
        maxnsym=2048,
        chksymbreak=0,
        chkprim=0,

        # Bands and occupation scheme 
        nsppol=2,
        nband=448,
        nbdbuf=20,
        occopt=3,
        tsmear=0.0005,

        # IO
        optforces=2,
        optstress=1,
        prtwf=0,
        prtden=0,
        prteig=0,
        timopt=-1,

        # Initial magnetization.
        spinat="""
            2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1
            2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1
            2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1
            2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1 2*0 1
            192*0""",
    )

    return inp


def build_flow(options):
    flow = BenchmarkFlow(workdir=options.get_workdir(__file__), remove=options.remove)

    template = make_input()

    # Processor distribution.
    pconfs = [
        dict(npkpt=2, npband=8 , npfft=8 ),  # 128 processeurs
        dict(npkpt=2, npband=16, npfft=8 ),  # 256 processeurs
        dict(npkpt=2, npband=16, npfft=16),  # 512 processeurs
        dict(npkpt=2, npband=16, npfft=32),  # 1024 processeurs
    ]

    for wfoptalg in [None, 1]:
        work = flowtk.Work()
        for d, omp_threads in product(pconfs, options.omp_list):
            mpi_procs = reduce(operator.mul, d.values(), 1)
            if not options.accept_mpi_omp(mpi_procs, omp_threads): continue
            manager = options.manager.new_with_fixed_mpi_omp(mpi_procs, omp_threads)
            if options.verbose: print("wfoptalg:", wfoptalg, "done with MPI_PROCS:", mpi_procs, "and:", d)
            inp = template.new_with_vars(d, np_slk=64)
            work.register_scf_task(inp, manager=manager)

        flow.register_work(work)

    return flow.allocate()


@bench_main
def main(options):
    if options.info:
        # print doc string and exit.
        print(__doc__)
        return 

    flow = build_flow(options)
    flow.build_and_pickle_dump()
    return flow


if __name__ == "__main__":
    sys.exit(main())
