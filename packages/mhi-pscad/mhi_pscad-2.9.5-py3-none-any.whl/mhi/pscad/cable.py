#===============================================================================
# Travelling Wave Model (Cable) Wizard
#===============================================================================

"""
============
Cable Wizard
============

.. versionadded:: 2.10
"""

#===============================================================================
# Imports
#===============================================================================

from enum import Enum, IntEnum
from typing import Dict, List, Optional, Union
from dataclasses import asdict, dataclass, is_dataclass

from mhi.pscad import Canvas, Component, Definition, Project
from mhi.pscad.unit import Value
from mhi.pscad.tline import *


#===============================================================================
# Exports
#===============================================================================

__all__ = ['CableWizard',
           'Bergeron', 'FreqDep',
           'YZ',
           'CableData', 'PipeData',
           'Ground',
           'AdditionalOptions',
           ]


#===============================================================================
# Types
#===============================================================================

# 1.0, "1.0 [m]", and Value("1 [ft]", "m") are all "Distance" types
Distance = Union[float, Value, str]


#===============================================================================
# Units
#===============================================================================

def m(x: Distance) -> Value:
    """
    Convert a distance measurement into a `Value` (in metres)

    `5`, `5.0`, and `"500 [cm]"` will all become `Value(5.0, "m")`
    """

    if isinstance(x, int):
        x = float(x)

    return Value(x, "m")


#===============================================================================
# Cable Data
#===============================================================================

@dataclass
class CableData:
    """
    Coaxial Cable Data
    """

    # Config
    RorT: str = 'RADIAL_FROM_CENTRE'
    LL: str = 'C1_I1_C2_I2_C3_I3'

    # Config - Ideal Cross-Bonding / Transposition
    CROSSBOND: str = 'DISABLED'
    GROUPNO: int = 1
    CBC1: int = 0
    CBC2: int = 1
    CBC3: int = 0
    CBC4: int = 0

    # Config - Mathematical Conductor Elimination
    LC: str = 'NONE'
    elim1: str = 'RETAIN'
    elim2: str = 'RETAIN'
    elim3: str = 'RETAIN'

    # Layer 1: Core Conductor
    R1: Value = Value('0.0 [m]')
    R2: Value = Value('0.022 [m]')
    RHOC: Value = Value('1.68e-8 [ohm*m]')
    PERMC: float = 1.0

    # Layer 2: First Insulator & Semi-Conductor
    R3: Value = Value('0.0395 [m]')
    T3: Value = Value('0.0175 [m]')
    EPS1: float = 4.1
    PERM1: float = 1.0
    SemiCL: str = 'ABSENT'
    SL1: Value = Value('0.001 [m]')
    SL2: Value = Value('0.001 [m]')

    # Layer 3: Sheath Conductor
    R4: Value = Value('0.044 [m]')
    T4: Value = Value('0.0045 [m]')
    RHOS: Value = Value('2.2e-7 [ohm*m]')
    PERMS: float = 1.0

    # Layer 4: Second Insulator
    R5: Value = Value('0.0475 [m]')
    T5: Value = Value('0.0035 [m]')
    EPS2: float = 2.3
    PERM2: float = 1.0

    # Layer 5: Armour Conductor
    R6: Value = Value('0.0583 [m]')
    T6: Value = Value('0.0108 [m]')
    RHOA: Value = Value('1.8e-7 [ohm*m]')
    PERMA: float = 400.0

    # Layer 6: Third Insulator
    R7: Value = Value('0.0635 [m]')
    T7: Value = Value('0.0052 [m]')
    EPS3: float = 1.0
    PERM3: float = 1.0

    # Layer 7: Outer Conductor
    R8: Value = Value('0.07 [m]')
    T8: Value = Value('0.0065 [m]')
    RHOO: float = Value('1.8e-7 [ohm*m]')
    PERMO: float = 400.0

    # Layer 8: Outer Insulator
    R9: Value = Value('0.08 [m]')
    T9: Value = Value('0.01 [m]')
    EPS4: float = 1.0
    PERM4: float = 1.0


#===============================================================================
# Pipe Data
#===============================================================================

@dataclass
class PipeData:
    """
    Pipe Data
    """

    # General
    OHC: Value = 'UNDERGROUND'
    icabsame: bool = False
    SHRad: str = 'SHOW'
    elimp: bool = False
    poins: bool = True
    FLT: Value = Value('60.0 [Hz]')

    # Inner Insulator
    RP1: Value = Value('0.041 [m]')
    EPSPipeI: float = 3.0
    LFPipeI: float = 0.0001
    PERMPipeI: Value = 1.0

    # Outer Insulator
    RP2: Value = Value('0.042 [m]')
    RHOPipe: Value = Value('1.71e-7 [ohm*m]')
    PERMPipe: float = 200.0
    RP3: Value = Value('0.043 [m]')

    # Pipe Conductor
    EPSPipeO: float = 2.3
    LFPipeO: float = 0.0001
    PERMPipeO: float = 1.0
    


#===============================================================================
# Cable Wizard
#===============================================================================

class CableWizard(TLineWizard):
    """
    Cable construction wizard

    Example::
        cw = CableWizard(freq_dep=False)
        cw.cable_coax(0.0, 10.0)
        cw.cable_coax(3.0, 10.0)
        cw.cable_coax(6.0, 10.0)
        cw.make_defn(prj, 'Cable3')
        cable = cw.create(main, 2, 2, Length="100.0 [km]")
    """


    #-----------------------------------------------------------------------

    __slots__ = ('_cables', '_num_cables', '_num_pipes',
                 '_cable_data', '_pipe_data')

    _cables: List[Dict]
    _num_cables: int
    _num_pipes: int


    #-----------------------------------------------------------------------

    def __init__(self, freq_dep: bool = False):
        super().__init__(freq_dep)
        self._cable_data = CableData()
        self._pipe_data = PipeData()



    #-----------------------------------------------------------------------

    def clear(self):
        super().clear()
        self._cables = []
        self._num_cables = 0
        self._num_pipes = 0


    #-----------------------------------------------------------------------

    @property
    def cable_data(self) -> CableData:
        return self._cable_data

    @cable_data.setter
    def cable_data(self, data: CableData):
        if not isinstance(data, CableData):
            raise TypeError()
        
        self._cable_data = data


    #-----------------------------------------------------------------------

    @property
    def pipe_data(self) -> PipeData:
        return self._pipe_data

    @pipe_data.setter
    def pipe_data(self, data: PipeData):
        if not isinstance(data, PipeData):
            raise TypeError()

        self._pipe_data = data


    #-----------------------------------------------------------------------

    def _create_cable(self, x, cable_data):
        parameters = dict(cable_data)
        defn = parameters.pop('-defn-')

        y = 52
        cable = self._create(f'Cable_{defn}', x, y, parameters)

    def _create_cables(self):
        cables = sorted(self._cables, key=lambda cable: cable['X'])
        x = 11
        for cable in cables:
            self._create_cable(x, cable)
            x += 17

    #-----------------------------------------------------------------------

    def make_defn(self, project: Project, name: str) -> Definition:
        """
        Make the Definition

        Create the Cable definition in the indicated project, with the
        given name (if available).

        The values set in the `.model`, `.yz`, `.ground`, and `.options`
        properties are used during this call in the creation of the Cable
        definition.
        """

        self._make_defn("Cable", project, name)

        if self._cables:
            self._create_cables()

        return self._defn


    #-----------------------------------------------------------------------

    def _cable(self, num_cables, defn, extra, **kwargs):


        if isinstance(extra, dict):
            extra = dict(extra)
        else:
            extra = asdict(extra)


        cable = {**extra, **kwargs}

        if self._num_cables + num_cables > 12:
            raise ValueError("Too many cables")

        cable['-defn-'] = defn
        self._cables.append(cable)
        self._num_cables += num_cables

        self._nodes += num_cables

        self._reset()

        return cable


    #-----------------------------------------------------------------------

    @staticmethod
    def _ohc(kwargs, y, name):

        y = m(y)

        aerial = str(kwargs.get('OHC', '')).upper()
        if aerial == '':
            aerial = 'AERIAL' if y < 0 else 'UNDERGROUND'

        if aerial in {'1', 'TRUE', 'AERIAL'}:
            kwargs['OHC'] = 'AERIAL'
            kwargs[name] = m(abs(y))
        elif aerial in {'0', 'FALSE', 'UNDERGROUND'}:
            kwargs['OHC'] = 'UNDERGROUND'
            kwargs['Y'] = m(abs(y))


    #-----------------------------------------------------------------------

    def cable_coax(self, x: Distance, y: Distance,
                   **kwargs):

        aerial = kwargs.get('OHC', 'UNDERGROUND').upper()

        kwargs['X'] = m(x)
        self._ohc(kwargs, m(y), 'Y2')

        self._cable(1, 'Coax', self._cable_data, **kwargs)


    #-----------------------------------------------------------------------

    def cable_pipe(self, x: Distance, y: Distance, *cables,
                   **kwargs):

        num_cables = len(cables)
        if num_cables > 8:
            raise ValueError("Too many cables")

        aerial = kwargs.get('OHC', 'UNDERGROUND').upper()

        kwargs['X'] = m(x)
        self._ohc(kwargs, m(y), 'Y10')

        for cn, cable in enumerate(cables, 1):
            if len(cable) not in {2, 3}:
                raise ValueError("Cable tuple must be (radius, angle [, data])")

            if len(cable) == 2:
                dcc, ang = cable
                data = self._cable_data
            else:
                dcc, ang, data = cable

            kwargs[f'NC{cn}'] = cn + self._num_cables
            kwargs[f'dcc{cn}'] = m(dcc)
            kwargs[f'ang{cn}'] = Value(ang, 'deg')

            if isinstance(data, dict):
                params: dict = data
            else:
                assert is_dataclass(data)
                params = asdict(data)

            for key, val in params.items():
                kwargs[f'{key}{cn}'] = val


        pipe = self._cable(num_cables, 'PipeType', self.pipe_data, **kwargs)

        self._num_pipes += 1
        pipe['pnum'] = self._num_pipes


    #-----------------------------------------------------------------------

    def cable_simplified(self, x, y, **kwargs):
        raise NotImplementedError("Not yet implemented")
