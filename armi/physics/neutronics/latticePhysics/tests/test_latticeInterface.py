# Copyright 2021 TerraPower, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test the Lattice Interface"""
# pylint: disable=abstract-method,missing-function-docstring,missing-class-docstring,protected-access,invalid-name,no-method-argument,import-outside-toplevel
import unittest
from collections import OrderedDict

from armi.physics.neutronics.latticePhysics.latticePhysicsInterface import (
    LatticePhysicsInterface,
)
from armi.tests import mockRunLogs
from armi import settings
from armi.settings.fwSettings.globalSettings import CONF_RUN_TYPE
from armi.physics.neutronics.settings import CONF_GEN_XS
from armi.operators.operator import Operator
from armi.reactor.reactors import Reactor, Core
from armi.physics.neutronics.crossSectionGroupManager import CrossSectionGroupManager
from armi.reactor.tests.test_blocks import buildSimpleFuelBlock
from armi.reactor.assemblies import (
    HexAssembly,
    grids,
)
from armi.nuclearDataIO.cccc import isotxs
from armi.tests import ISOAA_PATH

# As an interface, LatticePhysicsInterface must be subclassed to be used
class LatticeInterfaceTester(LatticePhysicsInterface):
    def __init__(self, r, cs):
        self.name = "LatticeInterfaceTester"
        super().__init__(r, cs)

    def _getExecutablePath(self):
        return "/tmp/fake_path"

    def readExistingXSLibraries(self, cycle):
        pass


class LatticeInterfaceTesterLibFalse(LatticeInterfaceTester):
    """subclass setting _newLibraryShouldBeCreated = False"""

    def _newLibraryShouldBeCreated(self, cycle, representativeBlockList, xsIDs):
        return False


class TestLatticePhysicsInterfaceBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create empty reactor core
        cls.o = Operator(settings.Settings())
        cls.o.r = Reactor("testReactor", None)
        cls.o.r.core = Core("testCore")
        # add an assembly with a single block
        cls.assembly = HexAssembly("testAssembly")
        cls.assembly.spatialGrid = grids.axialUnitGrid(1)
        cls.assembly.spatialGrid.armiObject = cls.assembly
        cls.assembly.add(buildSimpleFuelBlock())
        # cls.o.r.core.add(assembly)
        # init and add interfaces
        cls.xsGroupInterface = CrossSectionGroupManager(cls.o.r, cls.o.cs)
        cls.o.addInterface(cls.xsGroupInterface)


class TestLatticePhysicsInterface(TestLatticePhysicsInterfaceBase):
    """Test Lattice Physics Interface."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.latticeInterface = LatticeInterfaceTesterLibFalse(cls.o.r, cls.o.cs)
        cls.o.addInterface(cls.latticeInterface)

    def setUp(self):
        self.o.r.core.lib = "Nonsense"

    def test_LatticePhysicsInterface(self):
        """Super basic test of the LatticePhysicsInterface"""
        self.assertEqual(self.latticeInterface._updateBlockNeutronVelocities, True)
        self.assertEqual(self.latticeInterface.executablePath, "/tmp/fake_path")
        self.assertEqual(self.latticeInterface.executableRoot, "/tmp")
        self.latticeInterface.updateXSLibrary(0)
        self.assertEqual(len(self.latticeInterface._oldXsIdsAndBurnup), 0)

    def test_interactCoupled_Snapshots(self):
        """should change self.o.r.core.lib from Nonesense to None"""
        self.o.cs[CONF_RUN_TYPE] = "Snapshots"
        self.latticeInterface.interactCoupled(iteration=0)
        self.assertIsNone(self.o.r.core.lib)
        # reset runtype
        self.o.cs[CONF_RUN_TYPE] = "Standard"

    def test_interactCoupled_TimeNode0(self):
        """make sure updateXSLibrary is run"""
        self.latticeInterface.interactCoupled(iteration=0)
        self.assertIsNone(self.o.r.core.lib)

    def test_interactCoupled_TimeNode1(self):
        """make sure updateXSLibrary is NOT run"""
        self.o.r.p.timeNode = 1
        self.latticeInterface.interactCoupled(iteration=0)
        self.assertEqual(self.o.r.core.lib, "Nonsense")


class TestLatticePhysicsLibraryCreation(TestLatticePhysicsInterfaceBase):
    """test variations of _newLibraryShouldBeCreated"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.latticeInterface = LatticeInterfaceTester(cls.o.r, cls.o.cs)
        cls.o.addInterface(cls.latticeInterface)
        cls.xsGroupInterface.representativeBlocks = OrderedDict({"AA": cls.assembly[0]})
        cls.b, cls.xsIDs = cls.latticeInterface._getBlocksAndXsIds()

    def setUp(self):
        """reset representativeBlocks and CONF_GEN_XS"""
        self.xsGroupInterface.representativeBlocks = OrderedDict(
            {"AA": self.assembly[0]}
        )
        self.assembly[0].p.xsType = "A"
        self.o.cs[CONF_GEN_XS] = ""
        self.o.r.core.lib = isotxs.readBinary(ISOAA_PATH)

    def test_libCreation_NoGenXS(self):
        """no ISOTXS and xs gen not requested"""
        self.o.r.core.lib = None
        with mockRunLogs.BufferLog() as mock:
            xsGen = self.latticeInterface._newLibraryShouldBeCreated(
                1, self.b, self.xsIDs
            )
            self.assertIn(
                "Cross sections will not be generated on cycle 1.", mock.getStdout()
            )
            self.assertFalse(xsGen)

    def test_libCreation_GenXS(self):
        """no ISOTXS and xs gen requested"""
        self.o.cs[CONF_GEN_XS] = "Neutron"
        self.o.r.core.lib = None
        with mockRunLogs.BufferLog() as mock:
            xsGen = self.latticeInterface._newLibraryShouldBeCreated(
                1, self.b, self.xsIDs
            )
            self.assertIn(
                "Cross sections will be generated on cycle 1 for the following XS IDs: ['AA']",
                mock.getStdout(),
            )
            self.assertTrue(xsGen)

    def test_libCreation_NoGenXS_2(self):
        """ISOTXS present and has all of the necessary information"""
        with mockRunLogs.BufferLog() as mock:
            xsGen = self.latticeInterface._newLibraryShouldBeCreated(
                1, self.b, self.xsIDs
            )
            self.assertIn(
                "The generation of XS will be skipped.",
                mock.getStdout(),
            )
            self.assertFalse(xsGen)

    def test_libCreation_GenXS_2(self):
        """ISOTXS present and does not have all of the necessary information"""
        self.xsGroupInterface.representativeBlocks = OrderedDict(
            {"BB": self.assembly[0]}
        )
        b, xsIDs = self._modifyXSType()
        with mockRunLogs.BufferLog() as mock:
            xsGen = self.latticeInterface._newLibraryShouldBeCreated(1, b, xsIDs)
            self.assertIn(
                "is not enabled, but will be run to generate these missing cross sections.",
                mock.getStdout(),
            )
            self.assertTrue(xsGen)

    def test_libCreation_GenXS_3(self):
        """ISOTXS present and does not have all of the necessary information"""
        self.o.cs[CONF_GEN_XS] = "Neutron"
        b, xsIDs = self._modifyXSType()
        with mockRunLogs.BufferLog() as mock:
            xsGen = self.latticeInterface._newLibraryShouldBeCreated(1, b, xsIDs)
            self.assertIn("These will be generated on cycle ", mock.getStdout())
            self.assertTrue(xsGen)

    def _modifyXSType(self):
        self.xsGroupInterface.representativeBlocks = OrderedDict(
            {"BB": self.assembly[0]}
        )
        self.assembly[0].p.xsType = "B"
        return self.latticeInterface._getBlocksAndXsIds()


if __name__ == "__main__":
    unittest.main()
