#!/usr/bin/env python
"""
Gold with 107 atoms. Gamma-point.
GS calculations with paralkgb==1 and wfoptalg in [default, 1]
"""
from __future__ import division, print_function, unicode_literals, absolute_import

import sys
import operator
import numpy as np
import abipy.abilab as abilab
import abipy.data as abidata

from itertools import product
from abipy.benchmarks import bench_main, BenchmarkFlow


def make_input():
    """
    GS calculations with paralkgb==1
    Gold with 107 atoms.
    """
    pseudos = abidata.pseudos("au.paw")

    # Atomic Positions.
    xred = np.fromstring("""
0.0000000000E+00  1.6326095981E-01  1.6326095981E-01
1.6326095981E-01  0.0000000000E+00  1.6326095981E-01
1.6326095981E-01  1.6326095981E-01  0.0000000000E+00
0.0000000000E+00  1.6641506689E-01  5.0000000000E-01
1.6641506689E-01  0.0000000000E+00  5.0000000000E-01
1.6596912386E-01  1.6596912386E-01  3.3213568011E-01
0.0000000000E+00  0.0000000000E+00  3.3251308046E-01
0.0000000000E+00  1.6326095981E-01  8.3673904019E-01
1.6326095981E-01  0.0000000000E+00  8.3673904019E-01
1.6596912386E-01  1.6596912386E-01  6.6786431989E-01
0.0000000000E+00  0.0000000000E+00  6.6748691954E-01
0.0000000000E+00  5.0000000000E-01  1.6641506689E-01
1.6596912386E-01  3.3213568011E-01  1.6596912386E-01
1.6641506689E-01  5.0000000000E-01  0.0000000000E+00
0.0000000000E+00  3.3251308046E-01  0.0000000000E+00
0.0000000000E+00  5.0000000000E-01  5.0000000000E-01
1.6649623194E-01  3.3291657817E-01  5.0000000000E-01
1.6649623194E-01  5.0000000000E-01  3.3291657817E-01
0.0000000000E+00  3.3314040855E-01  3.3314040855E-01
0.0000000000E+00  5.0000000000E-01  8.3358493311E-01
1.6596912386E-01  3.3213568011E-01  8.3403087614E-01
1.6649623194E-01  5.0000000000E-01  6.6708342183E-01
0.0000000000E+00  3.3314040855E-01  6.6685959145E-01
0.0000000000E+00  8.3673904019E-01  1.6326095981E-01
1.6596912386E-01  6.6786431989E-01  1.6596912386E-01
1.6326095981E-01  8.3673904019E-01  0.0000000000E+00
0.0000000000E+00  6.6748691954E-01  0.0000000000E+00
0.0000000000E+00  8.3358493311E-01  5.0000000000E-01
1.6649623194E-01  6.6708342183E-01  5.0000000000E-01
1.6596912386E-01  8.3403087614E-01  3.3213568011E-01
0.0000000000E+00  6.6685959145E-01  3.3314040855E-01
0.0000000000E+00  8.3673904019E-01  8.3673904019E-01
1.6596912386E-01  6.6786431989E-01  8.3403087614E-01
1.6596912386E-01  8.3403087614E-01  6.6786431989E-01
0.0000000000E+00  6.6685959145E-01  6.6685959145E-01
3.3213568011E-01  1.6596912386E-01  1.6596912386E-01
5.0000000000E-01  0.0000000000E+00  1.6641506689E-01
5.0000000000E-01  1.6641506689E-01  0.0000000000E+00
3.3251308046E-01  0.0000000000E+00  0.0000000000E+00
3.3291657817E-01  1.6649623194E-01  5.0000000000E-01
5.0000000000E-01  0.0000000000E+00  5.0000000000E-01
5.0000000000E-01  1.6649623194E-01  3.3291657817E-01
3.3314040855E-01  0.0000000000E+00  3.3314040855E-01
3.3213568011E-01  1.6596912386E-01  8.3403087614E-01
5.0000000000E-01  0.0000000000E+00  8.3358493311E-01
5.0000000000E-01  1.6649623194E-01  6.6708342183E-01
3.3314040855E-01  0.0000000000E+00  6.6685959145E-01
3.3291657817E-01  5.0000000000E-01  1.6649623194E-01
5.0000000000E-01  3.3291657817E-01  1.6649623194E-01
5.0000000000E-01  5.0000000000E-01  0.0000000000E+00
3.3314040855E-01  3.3314040855E-01  0.0000000000E+00
3.3316116420E-01  5.0000000000E-01  5.0000000000E-01
5.0000000000E-01  3.3316116420E-01  5.0000000000E-01
5.0000000000E-01  5.0000000000E-01  3.3316116420E-01
3.3302887829E-01  3.3302887829E-01  3.3302887829E-01
3.3291657817E-01  5.0000000000E-01  8.3350376806E-01
5.0000000000E-01  3.3291657817E-01  8.3350376806E-01
5.0000000000E-01  5.0000000000E-01  6.6683883580E-01
3.3302887829E-01  3.3302887829E-01  6.6697112171E-01
3.3213568011E-01  8.3403087614E-01  1.6596912386E-01
5.0000000000E-01  6.6708342183E-01  1.6649623194E-01
5.0000000000E-01  8.3358493311E-01  0.0000000000E+00
3.3314040855E-01  6.6685959145E-01  0.0000000000E+00
3.3291657817E-01  8.3350376806E-01  5.0000000000E-01
5.0000000000E-01  6.6683883580E-01  5.0000000000E-01
5.0000000000E-01  8.3350376806E-01  3.3291657817E-01
3.3302887829E-01  6.6697112171E-01  3.3302887829E-01
3.3213568011E-01  8.3403087614E-01  8.3403087614E-01
5.0000000000E-01  6.6708342183E-01  8.3350376806E-01
5.0000000000E-01  8.3350376806E-01  6.6708342183E-01
3.3302887829E-01  6.6697112171E-01  6.6697112171E-01
6.6786431989E-01  1.6596912386E-01  1.6596912386E-01
8.3673904019E-01  0.0000000000E+00  1.6326095981E-01
8.3673904019E-01  1.6326095981E-01  0.0000000000E+00
6.6748691954E-01  0.0000000000E+00  0.0000000000E+00
6.6708342183E-01  1.6649623194E-01  5.0000000000E-01
8.3358493311E-01  0.0000000000E+00  5.0000000000E-01
8.3403087614E-01  1.6596912386E-01  3.3213568011E-01
6.6685959145E-01  0.0000000000E+00  3.3314040855E-01
6.6786431989E-01  1.6596912386E-01  8.3403087614E-01
8.3673904019E-01  0.0000000000E+00  8.3673904019E-01
8.3403087614E-01  1.6596912386E-01  6.6786431989E-01
6.6685959145E-01  0.0000000000E+00  6.6685959145E-01
6.6708342183E-01  5.0000000000E-01  1.6649623194E-01
8.3403087614E-01  3.3213568011E-01  1.6596912386E-01
8.3358493311E-01  5.0000000000E-01  0.0000000000E+00
6.6685959145E-01  3.3314040855E-01  0.0000000000E+00
6.6683883580E-01  5.0000000000E-01  5.0000000000E-01
8.3350376806E-01  3.3291657817E-01  5.0000000000E-01
8.3350376806E-01  5.0000000000E-01  3.3291657817E-01
6.6697112171E-01  3.3302887829E-01  3.3302887829E-01
6.6708342183E-01  5.0000000000E-01  8.3350376806E-01
8.3403087614E-01  3.3213568011E-01  8.3403087614E-01
8.3350376806E-01  5.0000000000E-01  6.6708342183E-01
6.6697112171E-01  3.3302887829E-01  6.6697112171E-01
6.6786431989E-01  8.3403087614E-01  1.6596912386E-01
8.3403087614E-01  6.6786431989E-01  1.6596912386E-01
8.3673904019E-01  8.3673904019E-01  0.0000000000E+00
6.6685959145E-01  6.6685959145E-01  0.0000000000E+00
6.6708342183E-01  8.3350376806E-01  5.0000000000E-01
8.3350376806E-01  6.6708342183E-01  5.0000000000E-01
8.3403087614E-01  8.3403087614E-01  3.3213568011E-01
6.6697112171E-01  6.6697112171E-01  3.3302887829E-01
6.6786431989E-01  8.3403087614E-01  8.3403087614E-01
8.3403087614E-01  6.6786431989E-01  8.3403087614E-01
8.3403087614E-01  8.3403087614E-01  6.6786431989E-01
6.6697112171E-01  6.6697112171E-01  6.6697112171E-01
""", sep=" ").reshape((-1,3))

    # Crystal structure.
    structure = abilab.Structure.from_abivars(
        acell=3*[23.01],
        rprim=np.eye(3), 
        typat=107*[1],
        znucl=79.,
        xred=xred,
    )

    inp = abilab.AbinitInput(structure, pseudos)
    inp.set_vars(
        # Basis set.
        ecut=10.,
        pawecutdg=20.,

        # SCF algorithm
        paral_kgb=1,
        wfoptalg=1,
        fftalg=402,
        #fftalg=302,  # To use FFTW instead of ABINIT FFT

        # SCF cycle 
        toldfe=1.e-5,
        nstep=20,

        # K-points and symmetries.
        nkpt=1,
        kpt=3*[0.],
        kptopt=0,
        istwfk="*1",
        nsym=0,
        chksymbreak=0,
        chkprim=0,

        # Bands and occupation scheme 
        nband=650,
        occopt=3,
        tsmear=0.002,
        nbdbuf=20,

        # IO
        optforces=2,
        optstress=1,
        prtwf=0,
        prtden=0,
        prteig=0,
        timopt=-1,
    )

    return inp


def build_flow(options):
    flow = BenchmarkFlow(workdir=options.get_workdir(__file__), remove=options.remove)

    template = make_input()

    # Processor distribution.
    pconfs = [
      dict(npkpt=1, npband=13, npfft=10), # 130   
      dict(npkpt=1, npband=26, npfft=10), # 260   
      dict(npkpt=1, npband=65, npfft=8 ), # 520   
      dict(npkpt=1, npband=65, npfft=16), # 1040  
    ]

    for wfoptalg in [None, 1]:
        work = abilab.Work()
        for d, omp_threads in product(pconfs, options.omp_list):
            mpi_procs = reduce(operator.mul, d.values(), 1)
            if not options.accept_mpi_omp(mpi_procs, omp_threads): continue
            manager = options.manager.new_with_fixed_mpi_omp(mpi_procs, omp_threads)
            print("wfoptalg:", wfoptalg, "done with MPI_PROCS:", mpi_procs, "and:", d)
            inp = template.new_with_vars(d, wfoptalg=wfoptalg)
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