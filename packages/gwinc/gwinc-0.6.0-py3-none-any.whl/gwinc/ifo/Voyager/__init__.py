from gwinc.ifo import PLOT_STYLE
from gwinc import noise
from gwinc import nb
from gwinc.ifo.noises import Strain


class Quantum(nb.Budget):
    """Quantum Vacuum

    """
    style = dict(
        label='Quantum Vacuum',
        color='#ad03de',
    )

    noises = [
        noise.quantum.AS,
        noise.quantum.Arm,
        noise.quantum.SEC,
        noise.quantum.FilterCavity,
        noise.quantum.Injection,
        noise.quantum.Readout,
    ]


class Voyager(nb.Budget):

    name = 'Voyager'

    noises = [
        Quantum,
        noise.seismic.Seismic,
        noise.newtonian.Newtonian,
        noise.suspensionthermal.SuspensionThermal,
        noise.coatingthermal.CoatingBrownian,
        noise.coatingthermal.CoatingThermoOptic,
        noise.substratethermal.ITMThermoRefractive,
        noise.substratethermal.SubstrateBrownian,
        noise.substratethermal.SubstrateThermoElastic,
        noise.residualgas.ResidualGas,
    ]

    calibrations = [
        Strain,
    ]

    plot_style = PLOT_STYLE


class Displacement(Voyager):
    calibrations = []
