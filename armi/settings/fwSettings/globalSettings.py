# Copyright 2019 TerraPower, LLC
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

"""
Framework-wide settings definitions and constants.

This should contain Settings definitions for general-purpose "framework" settings. These
should only include settings that are not related to any particular physics or plugins.

TODO: There are lots of settings in here that violate the above rule, which still need
to be migrated to their respective plugins: they are clearly separated for review.
"""
import os
from typing import List

import voluptuous as vol

from armi import context
from armi.settings import setting
from armi.utils.mathematics import isMonotonic
from armi.settings.fwSettings import tightCouplingSettings


# Framework settings
CONF_NUM_PROCESSORS = "numProcessors"
CONF_INITIALIZE_BURN_CHAIN = "initializeBurnChain"
CONF_BURN_CHAIN_FILE_NAME = "burnChainFileName"
CONF_AXIAL_MESH_REFINEMENT_FACTOR = "axialMeshRefinementFactor"
CONF_UNIFORM_MESH_MINIMUM_SIZE = "uniformMeshMinimumSize"
CONF_AUTOMATIC_VARIABLE_MESH = "automaticVariableMesh"
CONF_TRACE = "trace"
CONF_PROFILE = "profile"
CONF_COVERAGE = "coverage"
CONF_COVERAGE_CONFIG_FILE = "coverageConfigFile"
CONF_MIN_MESH_SIZE_RATIO = "minMeshSizeRatio"
CONF_CYCLE_LENGTH = "cycleLength"
CONF_CYCLE_LENGTHS = "cycleLengths"
CONF_AVAILABILITY_FACTOR = "availabilityFactor"
CONF_AVAILABILITY_FACTORS = "availabilityFactors"
CONF_POWER_FRACTIONS = "powerFractions"
CONF_BURN_STEPS = "burnSteps"
CONF_BETA = "beta"
CONF_DECAY_CONSTANTS = "decayConstants"
CONF_BRANCH_VERBOSITY = "branchVerbosity"
CONF_BU_GROUPS = "buGroups"
CONF_BURNUP_PEAKING_FACTOR = "burnupPeakingFactor"
CONF_CIRCULAR_RING_PITCH = "circularRingPitch"
CONF_COMMENT = "comment"
CONF_COPY_FILES_FROM = "copyFilesFrom"
CONF_COPY_FILES_TO = "copyFilesTo"
CONF_DEBUG = "debug"
CONF_DEBUG_MEM = "debugMem"
CONF_DEBUG_MEM_SIZE = "debugMemSize"
CONF_DEFAULT_SNAPSHOTS = "defaultSnapshots"
CONF_DETAIL_ALL_ASSEMS = "detailAllAssems"
CONF_DETAIL_ASSEM_LOCATIONS_BOL = "detailAssemLocationsBOL"
CONF_DETAIL_ASSEM_NUMS = "detailAssemNums"
CONF_DUMP_SNAPSHOT = "dumpSnapshot"
CONF_PHYSICS_FILES = "savePhysicsFiles"
CONF_DO_ORIFICED_TH = "doOrificedTH"  # zones
CONF_EQ_DIRECT = "eqDirect"  # fuelCycle/equilibrium coupling
CONF_FRESH_FEED_TYPE = "freshFeedType"
CONF_GEOM_FILE = "geomFile"
CONF_START_CYCLE = "startCycle"
CONF_LOADING_FILE = "loadingFile"
CONF_START_NODE = "startNode"
CONF_LOAD_STYLE = "loadStyle"
CONF_LOW_POWER_REGION_FRACTION = "lowPowerRegionFraction"  # reports
CONF_MODULE_VERBOSITY = "moduleVerbosity"
CONF_MPI_TASKS_PER_NODE = "mpiTasksPerNode"
CONF_N_CYCLES = "nCycles"
CONF_TIGHT_COUPLING = "tightCoupling"
CONF_TIGHT_COUPLING_MAX_ITERS = "tightCouplingMaxNumIters"
CONF_TIGHT_COUPLING_SETTINGS = "tightCouplingSettings"
CONF_CYCLES_SKIP_TIGHT_COUPLING_INTERACTION = "cyclesSkipTightCouplingInteraction"
CONF_OPERATOR_LOCATION = "operatorLocation"
CONF_OUTPUT_FILE_EXTENSION = "outputFileExtension"
CONF_PLOTS = "plots"
CONF_POWER = "power"
CONF_RUN_TYPE = "runType"
CONF_EXPLICIT_REPEAT_SHUFFLES = "explicitRepeatShuffles"
CONF_SKIP_CYCLES = "skipCycles"
CONF_SMALL_RUN = "smallRun"
CONF_REALLY_SMALL_RUN = "reallySmallRun"
CONF_STATIONARY_BLOCK_FLAGS = "stationaryBlockFlags"
CONF_TARGET_K = "targetK"  # lots of things use this
CONF_TRACK_ASSEMS = "trackAssems"
CONF_VERBOSITY = "verbosity"
CONF_ZONE_DEFINITIONS = "zoneDefinitions"
CONF_ACCEPTABLE_BLOCK_AREA_ERROR = "acceptableBlockAreaError"
CONF_FLUX_RECON = "fluxRecon"  # strange coupling in fuel handlers
CONF_INDEPENDENT_VARIABLES = "independentVariables"
CONF_T_IN = "Tin"
CONF_T_OUT = "Tout"
CONF_DEFERRED_INTERFACES_CYCLE = "deferredInterfacesCycle"
CONF_DEFERRED_INTERFACE_NAMES = "deferredInterfaceNames"
CONF_OUTPUT_CACHE_LOCATION = "outputCacheLocation"
CONF_MATERIAL_NAMESPACE_ORDER = "materialNamespaceOrder"
CONF_DETAILED_AXIAL_EXPANSION = "detailedAxialExpansion"
CONF_NON_UNIFORM_ASSEM_FLAGS = "nonUniformAssemFlags"
CONF_BLOCK_AUTO_GRID = "autoGenerateBlockGrids"
CONF_INPUT_HEIGHTS_HOT = "inputHeightsConsideredHot"
CONF_CYCLES = "cycles"
CONF_USER_PLUGINS = "userPlugins"
CONF_ASSEM_FLAGS_SKIP_AXIAL_EXP = "assemFlagsToSkipAxialExpansion"

# TODO: Unused by ARMI, slated for removal
CONF_CONDITIONAL_MODULE_NAME = "conditionalModuleName"  # mcfr
CONF_GROW_TO_FULL_CORE_AFTER_LOAD = "growToFullCoreAfterLoad"  # mcnp & gui
CONF_MEM_PER_NODE = "memPerNode"  # unused
CONF_NUM_CONTROL_BLOCKS = "numControlBlocks"  # unused
CONF_REMOVE_PER_CYCLE = "removePerCycle"  # crucible, equilibrium, gui
CONF_USE_INPUT_TEMPERATURES_ON_DBLOAD = "useInputTemperaturesOnDBLoad"  # unused


def defineSettings() -> List[setting.Setting]:
    """Return a list of global framework settings."""
    settings = [
        setting.Setting(
            CONF_NUM_PROCESSORS,
            default=1,
            label="CPUs",
            description="Number of CPUs to request on the cluster",
            schema=vol.All(vol.Coerce(int), vol.Range(min=1)),
        ),
        setting.Setting(
            CONF_INITIALIZE_BURN_CHAIN,
            default=True,
            label="Initialize Burn Chain",
            description=(
                f"This setting is paired with the `{CONF_BURN_CHAIN_FILE_NAME}` setting. "
                f"When enabled, this will initialize the burn-chain on initializing the case and "
                f"is required for running depletion calculations where the transmutations and decays "
                f"are controlled by the framework. If an external software, such as ORIGEN, contains "
                f"data for the burn-chain already embedded then this may be disabled."
            ),
        ),
        setting.Setting(
            CONF_BURN_CHAIN_FILE_NAME,
            default=os.path.join(context.RES, "burn-chain.yaml"),
            label="Burn Chain File",
            description="Path to YAML file that has the depletion chain defined in it",
        ),
        setting.Setting(
            CONF_AXIAL_MESH_REFINEMENT_FACTOR,
            default=1,
            label="Axial Mesh Refinement Factor",
            description="Multiplicative factor on the Global Flux number of mesh per "
            "block. Used for axial mesh refinement.",
            schema=vol.All(vol.Coerce(int), vol.Range(min=0, min_included=False)),
        ),
        setting.Setting(
            CONF_UNIFORM_MESH_MINIMUM_SIZE,
            default=None,
            label="Minimum axial mesh size in cm for uniform mesh",
            description="Minimum mesh size used when generating an axial mesh for the "
            "uniform mesh converter. Providing a value for this setting allows fuel "
            "and control material boundaries to be enforced better in uniform mesh.",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0.0, min_included=False)),
        ),
        setting.Setting(
            CONF_DETAILED_AXIAL_EXPANSION,
            default=False,
            label="Detailed Axial Expansion",
            description=(
                "Allow each assembly to expand independently of the others. Results in non-uniform "
                "axial mesh. Neutronics kernel must be able to handle."
            ),
        ),
        setting.Setting(
            CONF_NON_UNIFORM_ASSEM_FLAGS,
            default=[],
            label="Non Uniform Assem Flags",
            description=(
                "Assemblies that match a flag group on this list will not have their "
                "mesh changed with the reference mesh of the core for uniform mesh cases (non-"
                "detailed axial expansion). Another plugin may need to make the mesh uniform if "
                "necessary."
            ),
        ),
        setting.Setting(
            CONF_INPUT_HEIGHTS_HOT,
            default=True,
            label="Input Height Considered Hot",
            description=(
                "This is a flag to determine if block heights, as provided in blueprints, are at hot dimensions. "
                "If false, block heights are at cold/as-built dimensions and will be thermally expanded as appropriate."
            ),
        ),
        setting.Setting(
            CONF_CONDITIONAL_MODULE_NAME,
            default="",
            label="Burn End Conditional",
            description="File name (directory not included) of the Python "
            "module that contains a conditional function to determine the end of burn "
            "cycles",
        ),
        setting.Setting(
            CONF_AUTOMATIC_VARIABLE_MESH,
            default=False,
            label="Automatic Neutronics Variable Mesh",
            description="Flag to let ARMI add additional mesh points if the "
            "neutronics mesh is too irregular",
        ),
        setting.Setting(
            CONF_TRACE,
            default=False,
            label="Use the Python Tracer",
            description="Activate Python trace module to print out each line as it's "
            "executed",
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_PROFILE,
            default=False,
            label="Turn On the Profiler",
            description="Turn on the profiler for the submitted case. The profiler "
            "results will not include all import times.",
            isEnvironment=True,
            oldNames=[
                ("turnOnProfiler", None),
            ],
        ),
        setting.Setting(
            CONF_COVERAGE,
            default=False,
            label="Turn On Coverage Report Generation",
            description="Turn on coverage report generation which tracks all the lines "
            "of code that execute during a run",
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_COVERAGE_CONFIG_FILE,
            default="",
            label="File to Define Coverage Configuration",
            description="User-defined coverage configuration file",
        ),
        setting.Setting(
            CONF_MIN_MESH_SIZE_RATIO,
            default=0.15,
            label="Minimum Mesh Size Ratio",
            description="This is the minimum ratio of mesh sizes (dP1/(dP1 + dP2)) "
            "allowable -- only active if automaticVariableMesh flag is set to True",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0, min_included=False)),
        ),
        setting.Setting(
            CONF_CYCLE_LENGTH,
            default=365.242199,
            label="Cycle Length",
            description="Duration of one single cycle in days. If `availabilityFactor` is below "
            "1, the reactor will be at power less than this. If variable, use "
            "`cycleLengths` setting.",
            oldNames=[
                ("burnTime", None),
            ],
            schema=(
                vol.Any(
                    vol.All(vol.Coerce(float), vol.Range(min=0, min_included=False)),
                    None,
                )
            ),
        ),
        setting.Setting(
            CONF_CYCLE_LENGTHS,
            default=[],
            label="Cycle Durations",
            description="List of durations of each cycle in days. The at-power "
            "duration will be affected by `availabilityFactor`. R is repeat. For "
            "example [100, 150, '9R'] is 1 100 day cycle followed by 10 150 day "
            "cycles. Empty list is constant duration set by `cycleLength`.",
            schema=vol.Any([vol.Coerce(str)], None),
        ),
        setting.Setting(
            CONF_AVAILABILITY_FACTOR,
            default=1.0,
            label="Plant Availability Factor",
            description="Availability factor of the plant. This is the fraction of the "
            "time that the plant is operating. If variable, use `availabilityFactors` "
            "setting.",
            oldNames=[
                ("capacityFactor", None),
            ],
            schema=(vol.Any(vol.All(vol.Coerce(float), vol.Range(min=0)), None)),
        ),
        setting.Setting(
            CONF_AVAILABILITY_FACTORS,
            default=[],
            label="Availability Factors",
            description="List of availability factor of each cycle as a fraction "
            "(fraction of time plant is not in an outage). R is repeat. For example "
            "[0.5, 1.0, '9R'] is 1 50% followed by 10 100%. Empty list is "
            "constant duration set by `availabilityFactor`.",
            schema=vol.Any([vol.Coerce(str)], None),
        ),
        setting.Setting(
            CONF_POWER_FRACTIONS,
            default=[],
            label="Power Fractions",
            description="List of power fractions at each cycle (fraction of rated "
            "thermal power the plant achieves). R is repeat. For example [0.5, 1.0, "
            "'9R'] is 1 50% followed by 10 100%. Specify zeros to indicate "
            "decay-only cycles (i.e. for decay heat analysis). None implies "
            "always full rated power.",
            schema=vol.Any([vol.Coerce(str)], None),
        ),
        setting.Setting(
            CONF_BURN_STEPS,
            default=4,
            label="Burnup Steps per Cycle",
            description="Number of depletion substeps, n, in one cycle. Note: There "
            "will be n+1 time nodes and the burnup step time will be computed as cycle "
            "length/n when the simple cycles input format is used.",
            schema=(vol.Any(vol.All(vol.Coerce(int), vol.Range(min=0)), None)),
        ),
        setting.Setting(
            CONF_BETA,
            default=None,
            label="Delayed Neutron Fraction",
            description="Individual precursor group delayed neutron fractions",
            schema=vol.Any(
                [
                    vol.All(
                        vol.Coerce(float),
                        vol.Range(min=0, min_included=True, max=1, max_included=True),
                    )
                ],
                None,
                vol.All(
                    vol.Coerce(float),
                    vol.Range(min=0, min_included=True, max=1, max_included=True),
                ),
                msg="Expected NoneType, float, or list of floats.",
            ),
            oldNames=[
                ("betaComponents", None),
            ],
        ),
        setting.Setting(
            CONF_DECAY_CONSTANTS,
            default=None,
            label="Decay Constants",
            description="Individual precursor group delayed neutron decay constants",
            schema=vol.Any(
                [vol.All(vol.Coerce(float), vol.Range(min=0, min_included=True))],
                None,
                vol.All(vol.Coerce(float), vol.Range(min=0, min_included=True)),
                msg="Expected NoneType, float, or list of floats.",
            ),
        ),
        setting.Setting(
            CONF_BRANCH_VERBOSITY,
            default="error",
            label="Worker Log Verbosity",
            description="Verbosity of the non-primary MPI nodes",
            options=[
                "debug",
                "extra",
                "info",
                "important",
                "prompt",
                "warning",
                "error",
            ],
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_MODULE_VERBOSITY,
            default={},
            label="Module-Level Verbosity",
            description="Verbosity of any module-specific loggers that are set",
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_BU_GROUPS,
            default=[10, 20, 30, 100],
            label="Burnup Groups",
            description="The range of burnups where cross-sections will be the same "
            "for a given assembly type (units of %FIMA)",
            schema=vol.Schema(
                [
                    vol.All(
                        vol.Coerce(int), vol.Range(min=0, min_included=False, max=100)
                    )
                ]
            ),
        ),
        setting.Setting(
            CONF_BURNUP_PEAKING_FACTOR,
            default=0.0,
            label="Burn-up Peaking Factor",
            description="None",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_CIRCULAR_RING_PITCH,
            default=1.0,
            label="Circular Ring Relative Pitch",
            description="The relative pitch to be used to define a single circular "
            "ring in circular shuffling",
        ),
        setting.Setting(
            CONF_COMMENT,
            default="",
            label="Case Comments",
            description="A comment describing this case",
        ),
        setting.Setting(
            CONF_COPY_FILES_FROM, default=[], label="None", description="None"
        ),
        setting.Setting(
            CONF_COPY_FILES_TO, default=[], label="None", description="None"
        ),
        setting.Setting(
            CONF_DEBUG, default=False, label="Python Debug Mode", description="None"
        ),
        setting.Setting(
            CONF_DEBUG_MEM,
            default=False,
            label="Debug Memory",
            description="Turn on memory debugging options to help find problems with "
            "the code",
        ),
        setting.Setting(
            CONF_DEBUG_MEM_SIZE,
            default=False,
            label="Debug Memory Size",
            description="Show size of objects during memory debugging",
        ),
        setting.Setting(
            CONF_DEFAULT_SNAPSHOTS,
            default=False,
            label="Basic Reactor Snapshots",
            description="Generate snapshots at BOL, MOL, and EOL.",
        ),
        setting.Setting(
            CONF_DETAIL_ALL_ASSEMS,
            default=False,
            label="Detailed Assems - All",
            description="All assemblies will have 'detailed' treatment. Note: This "
            "option is interpreted differently by different modules.",
        ),
        setting.Setting(
            CONF_DETAIL_ASSEM_LOCATIONS_BOL,
            default=[],
            label="Detailed Assems - BOL Location",
            description="Assembly locations for assemblies that will have 'detailed' "
            "treatment. This option will track assemblies in the core at BOL. Note: "
            "This option is interpreted differently by different modules.",
        ),
        setting.Setting(
            CONF_DETAIL_ASSEM_NUMS,
            default=[],
            label="Detailed Assems - ID",
            description="Assembly numbers(IDs) for assemblies that will have "
            "'detailed' treatment. This option will track assemblies that not in the "
            "core at BOL. Note: This option is interpreted differently by different "
            "modules.",
            schema=vol.Schema([int]),
        ),
        setting.Setting(
            CONF_DUMP_SNAPSHOT,
            default=[],
            label="Detailed Reactor Snapshots",
            description="List of snapshots to perform detailed reactor analysis, "
            "such as reactivity coefficient generation.",
        ),
        setting.Setting(
            CONF_PHYSICS_FILES,
            default=[],
            label="Dump Snapshot Files",
            description="List of snapshots to dump reactor physics kernel input and "
            "output files. Can be used to perform follow-on analysis.",
        ),
        setting.Setting(
            CONF_DO_ORIFICED_TH,
            default=False,
            label="Perform Core Orificing",
            description="Perform orificed thermal hydraulics (requires bounds file "
            "from a previous case)",
        ),
        setting.Setting(
            CONF_EQ_DIRECT,
            default=False,
            label="Direct Eq Shuffling",
            description="Does the equilibrium search with repetitive shuffing but with "
            "direct shuffling rather than the fast way",
        ),
        setting.Setting(
            CONF_FLUX_RECON,
            default=False,
            label="Flux/Power Reconstruction",
            description="Perform detailed flux and power reconstruction",
        ),
        setting.Setting(
            CONF_FRESH_FEED_TYPE,
            default="feed fuel",
            label="Fresh Feed Type",
            description="None",
            options=["feed fuel", "igniter fuel", "inner driver fuel"],
        ),
        setting.Setting(
            CONF_GEOM_FILE,
            default="",
            label="Core Map Input File",
            description="Input file containing BOL core map",
        ),
        setting.Setting(
            CONF_GROW_TO_FULL_CORE_AFTER_LOAD,
            default=False,
            label="Expand to Full Core on Snapshot Load",
            description="Grows from 1/3 to full core after loading a 1/3 "
            "symmetric snapshot. Note: This is needed when a full core model is needed "
            "and the database was produced using a third core model.",
        ),
        setting.Setting(
            CONF_START_CYCLE,
            default=0,
            label="Start Cycle",
            description="Cycle number to continue calculation from. Database will "
            "load from the time step just before. For snapshots use `dumpSnapshot`.",
            oldNames=[
                ("loadCycle", None),
            ],
            schema=vol.All(vol.Coerce(int), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_LOADING_FILE,
            default="",
            label="Blueprints File",
            description="The blueprints/loading input file path containing "
            "component dimensions, materials, etc.",
        ),
        setting.Setting(
            CONF_START_NODE,
            default=0,
            label="Start Node",
            description="Timenode number (0 for BOC, etc.) to continue calulation from. "
            "Database will load from the time step just before.",
            oldNames=[
                ("loadNode", None),
            ],
            schema=vol.All(vol.Coerce(int), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_LOAD_STYLE,
            default="fromInput",
            label="Load Style",
            description="Description of how the ARMI case will be initialized",
            options=["fromInput", "fromDB"],
        ),
        setting.Setting(
            CONF_LOW_POWER_REGION_FRACTION,
            default=0.05,
            label="Low-power Region Fraction",
            description="Description needed",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0, max=1)),
        ),
        setting.Setting(
            CONF_MEM_PER_NODE,
            default=2000,
            label="Memory per Node",
            description="Memory requested per cluster node",
        ),
        setting.Setting(
            CONF_MPI_TASKS_PER_NODE,
            default=0,
            label="MPI Tasks per Node",
            description="Number of independent processes that are allocated to each "
            "cluster node. 0 means 1 process per CPU.",
            schema=vol.All(vol.Coerce(int), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_N_CYCLES,
            default=1,
            label="Number of Cycles",
            description="Number of cycles that will be simulated. Fuel management "
            "happens at the beginning of each cycle. Can include active (full-power) "
            "cycles as well as post-shutdown decay-heat steps. For restart cases, "
            "this value should include both cycles from the restart plus any additional "
            "cycles to be run after `startCycle`.",
            schema=vol.All(vol.Coerce(int), vol.Range(min=1)),
        ),
        setting.Setting(
            CONF_NUM_CONTROL_BLOCKS,
            default=6,
            label="Number of Control Blocks",
            description="Number of blocks with control for a REBUS poison search",
        ),
        setting.Setting(
            CONF_TIGHT_COUPLING,
            default=False,
            label="Tight Coupling",
            description="Boolean to turn on/off tight coupling",
        ),
        setting.Setting(
            CONF_TIGHT_COUPLING_MAX_ITERS,
            default=4,
            label="Maximum number of iterations for tight coupling.",
            description="Maximum number of iterations for tight coupling.",
        ),
        setting.Setting(
            CONF_CYCLES_SKIP_TIGHT_COUPLING_INTERACTION,
            default=[],
            label="Cycles to skip the tight coupling interaction.",
            description="List of cycle numbers skip tight coupling interaction for. "
            "Will still update component temps, etc during these cycles, will just "
            "not iterate a second (or more) time.",
        ),
        tightCouplingSettings.TightCouplingSettingDef(
            CONF_TIGHT_COUPLING_SETTINGS,
        ),
        setting.Setting(
            CONF_OPERATOR_LOCATION,
            default="",
            label="Operator Location",
            description="The path to the operator code to execute for this run (for "
            "custom behavior)",
        ),
        setting.Setting(
            CONF_OUTPUT_FILE_EXTENSION,
            default="jpg",
            label="Plot File Extension",
            description="The default extension for plots",
            options=["jpg", "png", "svg", "pdf"],
        ),
        setting.Setting(
            CONF_PLOTS,
            default=False,
            label="Plot Results",
            description="Generate additional plots throughout the ARMI analysis",
        ),
        setting.Setting(
            CONF_POWER,
            default=0.0,
            label="Reactor Thermal Power (W)",
            description="Nameplate thermal power of the reactor. Can be varied by "
            "setting the powerFractions setting.",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_REMOVE_PER_CYCLE, default=3, label="Move per Cycle", description="None"
        ),
        setting.Setting(
            CONF_RUN_TYPE,
            default="Standard",
            label="Run Type",
            description="Type of run that this is, e.g. a normal run through all "
            "cycles, a snapshot-loaded reactivity coefficient run, etc.",
            options=["Standard", "Equilibrium", "Snapshots"],
        ),
        setting.Setting(
            CONF_EXPLICIT_REPEAT_SHUFFLES,
            default="",
            label="Explicit Shuffles File",
            description="Path to file that contains a detailed shuffling history that "
            "is to be repeated exactly.",
            oldNames=[("movesFile", None), ("shuffleFileName", None)],
        ),
        setting.Setting(
            CONF_SKIP_CYCLES,
            default=0,
            label="Number of Cycles to Skip",
            description="Number of cycles to be skipped during the calculation. Note: "
            "This is typically used when repeating only a portion of a calculation or "
            "repeating a run.",
            schema=vol.All(vol.Coerce(int), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_SMALL_RUN,
            default=False,
            label="Clean Up Files at EOL",
            description="Clean up intermediate files after the run completes (EOL)",
        ),
        setting.Setting(
            CONF_REALLY_SMALL_RUN,
            default=False,
            label="Clean Up Files at BOC",
            description="Clean up files at the beginning of each cycle (BOC)",
        ),
        setting.Setting(
            CONF_STATIONARY_BLOCK_FLAGS,
            default=["GRID_PLATE"],
            label="stationary Block Flags",
            description="Blocks with these flags will not move in moves. "
            "Used for fuel management.",
        ),
        setting.Setting(
            CONF_TARGET_K,
            default=1.005,
            label="Criticality Search Target (k-effective)",
            description="Target criticality (k-effective) for cycle length, branch, "
            "and equilibrium search",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0)),
        ),
        setting.Setting(
            CONF_TRACK_ASSEMS,
            default=False,
            label="Save Discharged Assemblies",
            description="Track assemblies for detailed fuel histories. For instance, "
            "assemblies are tracked after they come out of a reactor by putting them "
            "in a Spent Fuel Pool. This might be necessary for your work, but it "
            "certainly increases the memory usage of the program.",
        ),
        setting.Setting(
            CONF_VERBOSITY,
            default="info",
            label="Primary Log Verbosity",
            description="How verbose the output will be",
            options=[
                "debug",
                "extra",
                "info",
                "important",
                "prompt",
                "warning",
                "error",
            ],
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_ZONE_DEFINITIONS,
            default=[],
            label="Zone Definitions",
            description="Manual definitions of zones as lists of assembly locations "
            "(e.g. 'zoneName: loc1, loc2, loc3') . Zones are groups of assemblies used "
            "by various summary and calculation routines.",
        ),
        setting.Setting(
            CONF_ACCEPTABLE_BLOCK_AREA_ERROR,
            default=1e-05,
            label="Acceptable Block Area Error",
            description="The limit of error between a block's cross-"
            "sectional area and the reference block used during the assembly area "
            "consistency check",
            schema=vol.All(vol.Coerce(float), vol.Range(min=0, min_included=False)),
        ),
        setting.Setting(
            CONF_INDEPENDENT_VARIABLES,
            default=[],
            label="Independent Variables",
            description="List of (independentVarName, value) tuples to inform "
            "optimization post-processing",
        ),
        setting.Setting(
            CONF_T_IN,
            default=360.0,
            label="Inlet Temperature",
            description="The inlet temperature of the reactor in C",
            schema=vol.All(vol.Coerce(float), vol.Range(min=-273.15)),
        ),
        setting.Setting(
            CONF_T_OUT,
            default=510.0,
            label="Outlet Temperature",
            description="The outlet temperature of the reactor in C",
            schema=vol.All(vol.Coerce(float), vol.Range(min=-273.15)),
        ),
        setting.Setting(
            CONF_USE_INPUT_TEMPERATURES_ON_DBLOAD,
            default=False,
            label="Temperatures From Input on DB Load",
            description="When loading from a database, first set all component "
            "temperatures to the input temperatures. Required when a coupled TH "
            "case is being derived from a case without any coupled TH.",
        ),
        setting.Setting(
            CONF_DEFERRED_INTERFACES_CYCLE,
            default=0,
            label="Deferred Interface Start Cycle",
            description="The supplied list of interface names in deferredInterfaceNames"
            " will begin normal operations on this cycle number",
        ),
        setting.Setting(
            CONF_DEFERRED_INTERFACE_NAMES,
            default=[],
            label="Deferred Interface Names",
            description="Interfaces to delay the normal operations of for special "
            "circumstance problem avoidance",
        ),
        setting.Setting(
            CONF_OUTPUT_CACHE_LOCATION,
            default="",
            label="Location of Output Cache",
            description="Location where cached calculations are stored and "
            "retrieved if exactly the same as the calculation requested. Empty "
            "string will not cache.",
            isEnvironment=True,
        ),
        setting.Setting(
            CONF_MATERIAL_NAMESPACE_ORDER,
            default=[],
            label="Material Namespace Order",
            description=(
                "Ordered list of Python namespaces for finding materials by class name. "
                "This allows users to choose between different implementations of reactor "
                "materials. For example, the framework comes with a basic UZr material, "
                "but power users will want to override it with their own UZr subclass. "
                "This allows users to specify to get materials out of a plugin rather "
                "than from the framework."
            ),
        ),
        # It may make sense to remove this setting when MILs become more stable.
        setting.Setting(
            CONF_BLOCK_AUTO_GRID,
            default=True,
            label="Auto-generate Block grids",
            description="Should block blueprints attempt to auto-generate a spatial "
            "grid upon construction? This feature makes heavy use of multi-index "
            "locations, which are not yet universally supported.",
        ),
        setting.Setting(
            CONF_CYCLES,
            default=[],
            label="Cycle information",
            description="YAML list defining the cycle history of the case. Options"
            " at each cycle include: `name`, `cumulative days`, `step days`, `availability"
            " factor`, `cycle length`, `burn steps`, and `power fractions`."
            " If specified, do not use any of the case settings `cycleLength(s)`,"
            " `availabilityFactor(s)`, `powerFractions`, or `burnSteps`. Must also"
            " specify `nCycles` and `power`.",
            schema=vol.Schema(
                [
                    vol.All(
                        {
                            "name": str,
                            "cumulative days": vol.All(
                                [vol.Any(float, int)], _isMonotonicIncreasing
                            ),
                            "step days": [vol.Coerce(str)],
                            "power fractions": [vol.Coerce(str)],
                            "availability factor": vol.All(
                                vol.Coerce(float), vol.Range(min=0, max=1)
                            ),
                            "cycle length": vol.All(
                                vol.Coerce(float), vol.Range(min=0)
                            ),
                            "burn steps": vol.All(vol.Coerce(int), vol.Range(min=0)),
                        },
                        _mutuallyExclusiveCyclesInputs,
                    )
                ]
            ),
        ),
        setting.Setting(
            CONF_USER_PLUGINS,
            default=[],
            label=CONF_USER_PLUGINS,
            description="YAML list defining the locations of UserPlugin subclasses. "
            "You can enter the full armi import path: armi.test.test_what.MyPlugin, "
            "or you can enter the full file path: /path/to/my/pluginz.py:MyPlugin ",
            schema=vol.Any([vol.Coerce(str)], None),
        ),
        setting.Setting(
            CONF_ASSEM_FLAGS_SKIP_AXIAL_EXP,
            default=[],
            label="Assembly Flags to Skip Axial Expansion",
            description=(
                "Assemblies that match a flag on this list will not be axially expanded."
            ),
        ),
    ]
    return settings


def _isMonotonicIncreasing(inputList):
    if isMonotonic(inputList, "<"):
        return inputList
    else:
        raise vol.error.Invalid(f"List must be monotonicically increasing: {inputList}")


def _mutuallyExclusiveCyclesInputs(cycle):
    cycleKeys = cycle.keys()
    if (
        sum(
            [
                "cumulative days" in cycleKeys,
                "step days" in cycleKeys,
                "cycle length" in cycleKeys or "burn steps" in cycleKeys,
            ]
        )
        != 1
    ):
        baseErrMsg = (
            "Must have exactly one of either 'cumulative days', 'step days', or"
            " 'cycle length' + 'burn steps' in each cycle definition."
        )

        raise vol.Invalid(
            (baseErrMsg + " Check cycle {}.".format(cycle["name"]))
            if "name" in cycleKeys
            else baseErrMsg
        )
    return cycle
