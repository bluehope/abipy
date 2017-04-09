"""Tests for symmetries module"""
from __future__ import print_function, division, absolute_import, unicode_literals

#import unittest
import numpy as np
import abipy.data as abidata

from abipy.core import Structure
from abipy.core.symmetries import *
from abipy.core.testing import AbipyTest
from abipy.abilab import abiopen


class TestSymmetries(AbipyTest):
    """"Test symmetries."""

    def test_silicon(self):
        """Test silicon space group."""
        structure = Structure.from_file(abidata.ref_file("si_scf_WFK.nc"))

        assert structure.has_abi_spacegroup
        assert structure.abi_spacegroup.is_symmorphic

        #print(structure)
        print("composition:", structure.composition)
        self.serialize_with_pickle(structure, test_eq=True)

        spgrp = structure.abi_spacegroup
        print("spgrp:\n", spgrp)

        #print("mult_tables:\n", spgrp.mult_table)
        # Classes cover the entire group.
        assert sum(len(cls) for cls in spgrp.groupby_class()) == len(spgrp)

        # Operation in the same class have the same trace and determinant.
        for cls in spgrp.groupby_class():
            #print(cls)
            op0 = cls[0]
            ref_trace, ref_det = op0.trace, op0.det
            for op in cls[1:]:
                assert op.trace == ref_trace
                assert op.det == ref_det

        assert spgrp == spgrp
        # FIXME: Temporary disabled spgid is set to 0 in the WFK file.
        #assert spgrp.spgid == 227
        assert spgrp.has_timerev
        assert len(spgrp) == 48 * 2
        assert spgrp.num_spatial_symmetries == 48

        assert spgrp.is_group()
        # TODO
        #si_symrel =
        si_tnons = np.reshape(24 * [0, 0, 0, 0.25, 0.25, 0.25], (48, 3))
        si_symafm = np.ones(48, dtype=np.int)

        self.assert_almost_equal(si_tnons, spgrp.tnons)
        self.assert_almost_equal(si_symafm, spgrp.symafm)

        for idx, symmop in enumerate(spgrp):
            assert symmop in spgrp
            assert spgrp.count(symmop) == 1
            assert spgrp.find(symmop) == idx
            assert abs(symmop.det) == 1

        # Test pickle
        self.serialize_with_pickle(spgrp[0], protocols=None, test_eq=True)

        for idx in range(len(spgrp)-1):
            assert spgrp[idx] == spgrp[idx]
            assert spgrp[idx] != spgrp[idx+1]

        for fmop in spgrp.fm_symmops:
            assert fmop.is_fm

        ucell_coords = np.reshape([site.frac_coords for site in structure], (len(structure), 3))

        err_msg = ""
        for site in structure:
            for symop in spgrp:
                rot_coords = symop.rotate_r(site.frac_coords, in_ucell=True)

                for atom_coords in ucell_coords:
                    #print (atom_coords - rot_coords)
                    if np.allclose(atom_coords,  rot_coords):
                        break
                else:
                    err_msg += "Cannot find symmetrical image of %s\n" % str(rot_coords)

                assert not err_msg

        # Test little group.
        # TODO
        #ltg_symmops, g0vecs, isyms = spgrp.find_little_group(kpoint=[0,0,0])
        #assert len(ltg_symmops) == len(spgrp)
        #for o1, o2 in zip(ltg_symmops, spgrp):
        #    assert o1 == o2


class LatticeRotationTest(AbipyTest):

    def test_base(self):
        """Testing LatticeRotation."""
        E = LatticeRotation([1, 0, 0, 0, 1, 0, 0, 0, 1])
        I = LatticeRotation([-1,  0,  0, 0, -1,  0, 0,  0, -1])

        assert E.isE and E.is_proper and E.inverse() == E
        assert I.isI and not I.is_proper and I.inverse() == I

        # Test Basic operations
        assert E != I
        assert +E == E
        assert -I == E
        assert E * I == I
        assert I ** 0 == E
        assert I ** 3 == I

        # Test pickle.
        self.serialize_with_pickle([E, I])


class BilbaoPointGroupTest(AbipyTest):

    def test_database(self):
        from abipy.core.symmetries import bilbao_ptgroup, sch_symbols
        for sch_symbol in sch_symbols:
            #print(sch_symbol)
            ptg = bilbao_ptgroup(sch_symbol)
            str(ptg)
            ptg.show_character_table()
            #for irrep_name in ptg.irrep_names: ptg.show_irrep(irrep_name)
            assert ptg.auto_test() == 0


class LittleGroupTest(AbipyTest):

    #@unittest.skipIf(True, "Temporarily disabled")
    def test_silicon_little_group(self):
        """Testing little group in Silicon."""
        with abiopen(abidata.ref_file("si_scf_WFK.nc")) as wfk_file:

            spgrp = wfk_file.structure.abi_spacegroup
            assert spgrp is not None
            str(spgrp)

            kpoints = [[0,0,0],
                       [0.5, 0, 0],
                       [1/3, 1/3, 1/3],
                       [1/4,1/4,0],
                      ]

            for kpoint in kpoints:
                ltk = spgrp.find_little_group(kpoint)
                str(ltk)
                #wfk_file.classify_ebands(0, kpoint, bands_range=range(0,5))


# reduced_symmetry_matrices =
#  1, 0, 0,
#  0, 1, 0,
#  0, 0, 1,
#  -1, 0, 0,
#  0, -1, 0,
#  0, 0, -1,
#  0, -1, 1,
#  0, -1, 0,
#  1, -1, 0,
#  0, 1, -1,
#  0, 1, 0,
#  -1, 1, 0,
#  -1, 0, 0,
#  -1, 0, 1,
#  -1, 1, 0,
#  1, 0, 0,
#  1, 0, -1,
#  1, -1, 0,
#  0, 1, -1,
#  1, 0, -1,
#  0, 0, -1,
#  0, -1, 1,
#  -1, 0, 1,
#  0, 0, 1,
#  -1, 0, 0,
#  -1, 1, 0,
#  -1, 0, 1,
#  1, 0, 0,
#  1, -1, 0,
#  1, 0, -1,
#  0, -1, 1,
#  1, -1, 0,
#  0, -1, 0,
#  0, 1, -1,
#  -1, 1, 0,
#  0, 1, 0,
#  1, 0, 0,
#  0, 0, 1,
#  0, 1, 0,
#  -1, 0, 0,
#  0, 0, -1,
#  0, -1, 0,
#  0, 1, -1,
#  0, 0, -1,
#  1, 0, -1,
#  0, -1, 1,
#  0, 0, 1,
#  -1, 0, 1,
#  -1, 0, 1,
#  -1, 1, 0,
#  -1, 0, 0,
#  1, 0, -1,
#  1, -1, 0,
#  1, 0, 0,
#  0, -1, 0,
#  1, -1, 0,
#  0, -1, 1,
#  0, 1, 0,
#  -1, 1, 0,
#  0, 1, -1,
#  1, 0, -1,
#  0, 0, -1,
#  0, 1, -1,
#  -1, 0, 1,
#  0, 0, 1,
#  0, -1, 1,
#  0, 1, 0,
#  0, 0, 1,
#  1, 0, 0,
#  0, -1, 0,
#  0, 0, -1,
#  -1, 0, 0,
#  1, 0, -1,
#  0, 1, -1,
#  0, 0, -1,
#  -1, 0, 1,
#  0, -1, 1,
#  0, 0, 1,
#  0, -1, 0,
#  0, -1, 1,
#  1, -1, 0,
#  0, 1, 0,
#  0, 1, -1,
#  -1, 1, 0,
#  -1, 0, 1,
#  -1, 0, 0,
#  -1, 1, 0,
#  1, 0, -1,
#  1, 0, 0,
#  1, -1, 0,
#  0, 1, 0,
#  1, 0, 0,
#  0, 0, 1,
#  0, -1, 0,
#  -1, 0, 0,
#  0, 0, -1,
#  0, 0, -1,
#  0, 1, -1,
#  1, 0, -1,
#  0, 0, 1,
#  0, -1, 1,
#  -1, 0, 1,
#  1, -1, 0,
#  0, -1, 1,
#  0, -1, 0,
#  -1, 1, 0,
#  0, 1, -1,
#  0, 1, 0,
#  0, 0, 1,
#  1, 0, 0,
#  0, 1, 0,
#  0, 0, -1,
#  -1, 0, 0,
#  0, -1, 0,
#  -1, 1, 0,
#  -1, 0, 0,
#  -1, 0, 1,
#  1, -1, 0,
#  1, 0, 0,
#  1, 0, -1,
#  0, 0, 1,
#  0, 1, 0,
#  1, 0, 0,
#  0, 0, -1,
#  0, -1, 0,
#  -1, 0, 0,
#  1, -1, 0,
#  0, -1, 0,
#  0, -1, 1,
#  -1, 1, 0,
#  0, 1, 0,
#  0, 1, -1,
#  0, 0, -1,
#  1, 0, -1,
#  0, 1, -1,
#  0, 0, 1,
#  -1, 0, 1,
#  0, -1, 1,
#  -1, 1, 0,
#  -1, 0, 1,
#  -1, 0, 0,
#  1, -1, 0,
#  1, 0, -1,
#  1, 0, 0 ;
