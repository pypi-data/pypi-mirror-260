# -*- coding: utf-8 -*-
# PyBEST: Pythonic Black-box Electronic Structure Tool
# Copyright (C) 2016-- The PyBEST Development Team
#
# This file is part of PyBEST.
#
# PyBEST is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# PyBEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --


from pybest.geminals import ROOpCCD


def test_load_orbitals_same_geometry(water):
    """Load orbitals from some IOData container (same molecular geometry).

    Args:
        water (Molecule instance): Contains all data (ints, orbitals, IOData)
    """
    # We need RHF data
    water.do_hf()
    # We choose ROOpCCD as an example class.
    pccd = ROOpCCD(water.lf, water.occ_model)

    # First, pass None
    orb, olp = pccd.load_orbitals(water.one, water.eri, None, None, water.data)

    assert orb == water.data.orb_a, "Got wrong orbitals"
    assert olp == water.data.olp, "Got wrong overlap integrals"

    # Second, pass the same olp
    orb, olp = pccd.load_orbitals(
        water.one, water.eri, water.olp, water.orb_a, water.data
    )

    assert orb == water.data.orb_a, "Got wrong orbitals"
    assert olp == water.data.olp, "Got wrong overlap integrals"


def test_load_orbitals_different_geometry(water, water_2):
    """Load orbitals from some IOData container (different molecular geometry).

    Args:
        water (Molecule instance): Contains all data (ints, orbitals, IOData)
        water_2 (Molecule instance): Contains new orbitals used to overwrite
                                     water.orb_a (through projection)
    """
    # We need RHF data
    water.do_hf()
    water_2.do_hf()
    # We choose ROOpCCD as an example class as we cannot access the ABC
    pccd = ROOpCCD(water.lf, water.occ_model)

    # Generate copy to access later (as it will be overwritten)
    orb_ = water.orb_a.copy()
    # First, pass None (should pass)
    orb, olp = pccd.load_orbitals(
        water.one, water.eri, None, None, water_2.data
    )

    assert orb == water_2.data.orb_a, "Got wrong orbitals"
    assert olp == water_2.data.olp, "Got wrong overlap integrals"

    # Second, pass the different olp
    assert not (water.orb_a == water_2.orb_a), "Orbitals do not differ!"
    orb, olp = pccd.load_orbitals(
        water.one, water.eri, water.olp, water.orb_a, water_2.data
    )

    assert orb == water.data.orb_a, "Overwriting orbitals did not work"
    assert olp == water.olp, "Overlap should be the same"
    assert olp == water.data.olp, "Overlap should be the same"
    assert not (orb == water_2.data.orb_a), "Projecting orbitals did not work"
    assert not (orb_ == orb), "Projecting orbitals did not work"


def test_fix_core_energy(water):
    """Recalculate frozen core energy.
    We only test the case (RHF external energy -> external + frozen core) as
    all other cases are similar.

    Args:
        water (Molecule instance): Contains all data (ints, orbitals, IOData)
    """
    # We need RHF data
    water.do_hf()
    # We choose ROOpCCD as an example class as we cannot access the ABC
    pccd = ROOpCCD(water.lf, water.occ_model)
    # Get RHF external energy (will change!)
    e_core_rhf = water.external
    # First e_core should be 0 (as set in __init__)
    assert pccd.e_core == 0, f"Wrong e_core, expected 0, got {pccd.e_core}!"
    # Now, overwrite e_core with external (this is usually done in __call__)
    pccd.e_core = water.external
    assert pccd.e_core == e_core_rhf, f"Wrong e_core, expected {e_core_rhf}!"

    # Now, update e_core (we use auto_ncore)
    pccd.fix_core_energy(water.one, water.eri, water.orb_a, "tensordot")

    assert pccd.e_core != 0, f"Wrong e_core: got {pccd.e_core}!"
    assert pccd.e_core != e_core_rhf, f"Wrong e_core: got {e_core_rhf}!"
    # If you parameterize this test, update the core energy below
    error_msg = (
        f"Wrong core energy! Got {pccd.e_core} but expected 52.152765293542"
    )
    assert abs(pccd.e_core + 52.152765293542) < 1e-8, error_msg
