#===============================================================================
# Travelling Wave Model (TLine) Wizard
#===============================================================================

"""
============
TLine Wizard
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


#===============================================================================
# Exports
#===============================================================================

__all__ = ['TLineWizard',
           'Bergeron', 'FreqDep',
           'YZ',
           'ConductorData', 'SubConductorData', 'GroundWireData',
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
# XML Constants
#===============================================================================

_TWM_DEFN_STR = '''\
    <Definition id="0" classid="RowDefn" name="{name}" group="" url="" version="RowDefn" build="RowDefn" crc="0" key="" view="false" date="-1">
      <paramlist>
        <param name="Description" value="" />
        <param name="type" value="{type}" />
      </paramlist>
      <schematic classid="RowCanvas">
        <paramlist>
          <param name="show_border" value="0" />
          <param name="show_grid" value="0" />
          <param name="size" value="0" />
          <param name="orient" value="1" />
        </paramlist>
        <grouping />
      </schematic>
    </Definition>
'''


#===============================================================================
# Models
#===============================================================================

@dataclass
class _Model:
    Interp1: bool = True
    Inflen: bool = False


#-------------------------------------------------------------------------------

@dataclass
class Bergeron(_Model):
    """
    Parameters for the `Line_Berg_Options` Bergeron Model

    The Bergeron Model is a very simple, constant frequency model based on
    travelling waves.  

    It is useful for studies wherever it is important to get the correct
    steady state impedance/admittance of the line or cable, but should not
    be used where the transient or harmonic behaviour is important.
    """
    
    BDamp: bool = False
    F1: Value = Value('2000 [Hz]')
    TZ: Value = Value('0.005 [ms]')
    TP: Value = Value('0.005 [ms]')


#-------------------------------------------------------------------------------

@dataclass
class FreqDep(_Model):
    """
    Parameters for the `Line_FrePhase_Options` Frequency Dependent Model

    The Fre-Dep (Phase) Model (Universal Line Model) is a frequency dependent
    transmission line model based on travelling waves.  It is the most advanced
    time domain model available as it represents the full frequency dependence
    of all line parameters.  This model accurately considers the  effect of a
    frequency dependent transform.

    It is useful for studies wherever the transient or harmonic behaviour of
    the line or cable is important.
    """

    # Configuration (see also _Model class)
    Output: bool = False

    # Curve Fitting
    FS: Value = Value('0.01 [Hz]')
    FE: Value = Value('1.0e6 [Hz]')
    Numf: int = 100

    # Characteristic Admittance (Yc)
    YMaxP: int = 20
    YMaxE: Value = Value('0.2 [%]')

    # Least Squares Weighting Factors
    W1: float = 1.0
    W2: float = 1.0
    W3: float = 1.0

    # Propagation Function (H)
    AMaxP: int = 20
    AMaxE: Value = Value('0.2 [%]')
    MaxRPtol: float = 2000000.0

    # Passivity Enforcement
    CPASS: str = 'DISABLE'

    # Frequency Range for passivity
    NFP: int = 1000
    FSP: Value = Value('0.001 [Hz]')
    FEP: Value = Value('1000.0 [Hz]')
    FDIS: str = 'LOG_LINEAR'

    # Spectral Residue Pertubation
    ET_PE: float = 1e-12
    MER_PE: float = 2.0
    MIT_PE: int = 5

    # DC Correction
    DCenab: str = 'DISABLED'
    DCCOR: str = 'FUNCTIONAL_FORM'
    shntcab: Value = Value('1.0E-9 [mho/m]')
    enablf: bool = True


#===============================================================================
# Bergeron YZ Data
#===============================================================================

@dataclass
class YZ:
    """
    Parameters for Manual Entry of Y, Z

    The Manual Entry Data component can only be used with the Bergeron Model.

    If you require Frequency Dependent Mode or Phase Domain line models,
    you must enter the conductor geometry with the ground and  tower components.
    """
    
    NCond: int = 3

    # Manual YZ Data Configuration
    PU: str = 'R_XL_XC_PU_M'
    Estim: str = 'ENTER_0_DATA'
    REst: float = 10.15
    ZEst: float = 1.915
    TEst: float = 1.36
    LONGLN: str = 'NO'

    # R,Xl,Xc Data Entry [pu/m]
    VR: Value = Value('230 [kV]')
    MVA: Value = Value('100 [MVA]')
    RPUP: Value = Value('6.76e-8 [pu/m]')
    XLPUP: Value = Value('9.6e-7 [pu/m]')
    XCPUP: Value = Value('5.78e5 [pu*m]')
    RPUZ: Value = Value('6.86e-7 [pu/m]')
    XLPUZ: Value = Value('2.5e-6 [pu/m]')
    XCPUZ: Value = Value('8.14e5 [pu*m]')
    RPUZM: Value = Value('5.35e-7 [pu/m]')
    XLPUZM: Value = Value('6.37e-7 [pu/m]')
    XCPUZM: Value = Value('5.4e7 [pu*m]')

    # R,Xl,Xc Data Entry [ohm/m]
    RP: Value = Value('3.576e-5 [ohm/m]')
    XLP: Value = Value('5.078e-4 [ohm/m]')
    XCP: Value = Value('305.8 [Mohm*m]')
    RZ: Value = Value('3.63e-4 [ohm/m]')
    XLZ: Value = Value('1.323e-3 [ohm/m]')
    XCZ: Value = Value('430.6 [Mohm*m]')
    RZM: Value = Value('2.83e-4 [ohm/m]')
    XLZM: Value = Value('3.37e-4 [ohm/m]')
    XCZM: Value = Value('28560.0 [Mohm*m]')

    # Zsurge and Travel Time
    RTP: Value = Value('3.576e-5 [ohm/m]')
    TTP: Value = Value('3.4185e-9 [s/m]')
    ZTP: Value = Value('394.06 [ohm]')
    RTZ: Value = Value('3.63e-4 [ohm/m]')
    TTZ: Value = Value('4.65e-9 [s/m]')
    ZTZ: Value = Value('754.77 [ohm]')
    RTZM: Value = Value('2.83e-4 [ohm/m]')
    TTZM: Value = Value('0.288e-9 [s/m]')
    ZTZM: Value = Value('3102.4 [ohm]')

    # R, X, B Data Entry [pu/m]
    VR2: Value = Value('230 [kV]')
    MVA2: Value = Value('100 [MVA]')
    RPUP2: Value = Value('6.76e-8 [pu/m]')
    XLPUP2: Value = Value('9.6e-7 [pu/m]')
    BPUP2: Value = Value('1.73e-6 [pu/m]')
    RPUZ2: Value = Value('6.86e-7 [pu/m]')
    XLPUZ2: Value = Value('2.5e-6 [pu/m]')
    BPUZ2: Value = Value('1.23e-6 [pu/m]')
    RPUZM2: Value = Value('5.35e-7 [pu/m]')
    XLPUZM2: Value = Value('6.37e-7 [pu/m]')
    BPUZM2: Value = Value('1.85e-8 [pu/m]')

    # Y,Z Direct Entry
    fname: str = 'inputYZ.txt'
    path: str = 'RELATIVE'
    dformat: str = 'PER_METRE'

    # Y, Z Direct Entry (Multiple Freq)
    fname2: str = 'inputYZ.txt'
    path2: str = 'RELATIVE'


#===============================================================================
# Tower Data (Bergeron & FreqDep)
#===============================================================================

@dataclass
class ConductorData:
    """
    TLine Conductor Data
    """
    
    # Data Entry Config
    CDataType: str = 'DIRECT'
    CName: str = 'chukar'
    Hollow: str = 'SOLID_CORE'
    ShuntG: Value = Value('1e-11 [mho/m]')

    # Conductor Properties
    CLName: str = '..\\conductor.clb'
    RadiusC: Value = Value('0.0203454 [m]')
    RadiusCin: Value = Value('0.0 [m]')
    num_tot_strnd: int = 19
    num_out_strnd: int = 12
    RadiusS: Value = Value('0.003 [m]')
    DCResC: Value = Value('0.03206 [ohm/km]')
    PERMC: float = 1.0
    SAGC: Value = Value('10.0 [m]')


#-------------------------------------------------------------------------------

@dataclass
class SubConductorData:
    """
    TLine Sub-Conductor Data
    """
    
    # Sub-Conductor Bundling
    NCondB: int = 1
    BundSym: str = 'SYMMETRICAL'
    BSP: Value = Value('0.4572 [m]')
    SHBund: str = 'VISIBLE'

    # Asymmetrical Bundling Positions
    XB1: Value = Value('-0.1 [m]')
    YB1: Value = Value('0.1 [m]')
    XB2: Value = Value('-0.1 [m]')
    YB2: Value = Value('0.1 [m]')
    XB3: Value = Value('-0.1 [m]')
    YB3: Value = Value('0.1 [m]')
    XB4: Value = Value('-0.1 [m]')
    YB4: Value = Value('0.1 [m]')
    XB5: Value = Value('-0.1 [m]')
    YB5: Value = Value('0.1 [m]')
    XB6: Value = Value('-0.1 [m]')
    YB6: Value = Value('0.1 [m]')
    XB7: Value = Value('-0.1 [m]')
    YB7: Value = Value('0.1 [m]')
    XB8: Value = Value('-0.1 [m]')
    YB8: Value = Value('0.1 [m]')
    XB9: Value = Value('-0.1 [m]')
    YB9: Value = Value('0.1 [m]')
    XB10: Value = Value('-0.1 [m]')
    YB10: Value = Value('0.1 [m]')
    XB11: Value = Value('-0.1 [m]')
    YB11: Value = Value('0.1 [m]')
    XB12: Value = Value('-0.1 [m]')
    YB12: Value = Value('0.1 [m]')
    XB13: Value = Value('-0.1 [m]')
    YB13: Value = Value('0.1 [m]')
    XB14: Value = Value('-0.1 [m]')
    YB14: Value = Value('0.1 [m]')
    XB15: Value = Value('-0.1 [m]')
    YB15: Value = Value('0.1 [m]')


#-------------------------------------------------------------------------------

@dataclass
class GroundWireData:
    """
    TLine Ground Wire Data
    """
    
    # General
    NG: int = 2
    GWSame: str = 'IDENTICAL'
    ElimGW: str = 'ENABLED'
    SAGG: Value = Value('10.0 [m]')
    XG: Value = Value('10.0 [m]')

    # Data Entry Configuration
    GDataType: str = 'DIRECT'
    GLName: str = '..\\conductor.clb'

    # Ground Wire 1 Properties
    GName: str = '1/2_HighStrengthSteel'
    RadiusG: Value = Value('0.0055245 [m]')
    DCResG: Value = Value('2.8645 [ohm/km]')
    PERMG: float = 1.0

    # Ground Wire 2 Properties
    G2Name: str = '1/2_HighStrengthSteel'
    RadiusG2: Value = Value('0.0055245 [m]')
    DCResG2: Value = Value('2.8645 [ohm/km]')
    PERMG2: float = 1.0


#===============================================================================
# TLine/Cable Ground Data (Bergeron & FreqDep)
#===============================================================================

@dataclass
class Ground:
    """
    TLine Ground (Earth Return) Data
    """
    
    # Earth Return Representation
    EarthForm2: str = 'DERISEMLYEN'
    EarthForm: str = 'DIRECT_NUMERICAL_INTEGRATION'
    EarthForm3: str = 'LUCCA'

    # Electrical Properties
    GrRho: str = 'CONSTANT_RESISTIVITY'
    GRRES: Value = Value('100.0 [ohm*m]')
    GPERM: float = 1.0
    K0: Value = Value('0.001 [S/m]')
    K1: Value = Value('0.01 [S/m]')
    alpha: float = 0.7
    GRP: float = 10.0


#===============================================================================
# Additional Options
#===============================================================================

@dataclass
class AdditionalOptions:
    """
    Additons Options for the optional `Line_Out_Disp` component
    """
    
    # General
    DataF: Value = Value('60.0 [Hz]')
    Zero_Tol: float = 1e-19
    Vbase: Value = Value('230.0 [kV]')
    MVAbase: Value = Value('100.0 [MVA]')

    # Equivalent PI-Section Creation
    picomp: str = 'DISABLED'
    Rip: Value = Value('1.0E5 [ohm]')


#===============================================================================
# TLine Wizard
#===============================================================================

class TLineWizard:
    """
    TLine construction wizard

    Example::
        prj = pscad.project('simpleac')
        main = prj.canvas('Main')
        
        tlw = TLineWizard(freq_dep=False)
        tlw.tower_3_flat(0.0, 30.0, 10.0, SHSag="VISIBLE", NCondB=2)
        tlw.make_defn(prj, 'FLAT230b')
        tline = tlw.create(main, 27, 20, Name="FLAT230b"
                           Mode="LOCAL_CONNECTION", Length="100.0 [km]")
    """


    #-----------------------------------------------------------------------

    __slots__ = ('_model', '_ground', '_yz', '_options', '_defn', '_canvas',
                 '_conductor_data', '_subconductor_data', '_ground_wire_data',
                 '_towers', '_nodes', )


    _model: Union[Bergeron, FreqDep]
    _ground: Ground
    _yz: Optional[YZ]
    _options: Optional[AdditionalOptions]
    _defn: Optional[Definition]
    _canvas: Optional[Canvas]
    _conductior_data: ConductorData
    _subconductior_data: SubConductorData
    _ground_wire_data: GroundWireData
    _nodes: int
    _towers: List[Dict]


    #-----------------------------------------------------------------------

    def __init__(self, freq_dep: bool = False):
        self._model = FreqDep() if freq_dep else Bergeron()
        self._yz = None
        self._options = None

        self._conductor_data = ConductorData()
        self._subconductor_data = SubConductorData()
        self._ground_wire_data = GroundWireData()
        self._ground = Ground()

        self.clear()


    #-----------------------------------------------------------------------

    def _reset(self):
        self._defn = None
        self._canvas = None


    #-----------------------------------------------------------------------

    def clear(self):
        """
        Remove all Towers from the TLine wizard, in preparation for creating
        a TLine with a new tower configuration.
        """

        self._towers = []
        self._nodes = 0
        self._reset()


    #-----------------------------------------------------------------------

    @property
    def model(self) -> _Model:
        """
        Travelling Wave Model

        The Bergeron Model is a very simple, constant frequency model based
        on travelling waves.  It is useful for studies wherever it is important
        to get the correct steady state impedance/admittance of the line or
        cable, but should not be used where the transient or harmonic
        behaviour is important.

        The Frequence Dependent Model is based on travelling waves.  It is
        useful for studies wherever the transient or harmonic behaviour of the
        line or cable is important.

        When the wizard is created, the model is set to either a `Bergeron()`
        or `FreqDep()` instance.  That instance's parameters may be changed,
        or the `model` property may be overwritten with a new instance.

        The value stored in the `model` property is only used when `make_defn`
        is finally called.
        """

        return self._model

    @model.setter
    def model(self, model: Union[Bergeron, FreqDep]):
        if not isinstance(model, (Bergeron, FreqDep)):
            raise TypeError("Model must be Bergeron or FreqDep")

        if isinstance(model, FreqDep):
            self._yz = None
            if self._ground is None:
                self._ground = Ground()

        self._model = model
        self._reset()


    #-----------------------------------------------------------------------

    @property
    def options(self) -> Optional[AdditionalOptions]:
        """
        Additional Options

        Per-Unit output of the RXB values in the output file is based on
        100 MVA, 230kV base.  This base value can be changed by assigning an
        `AdditionalOptions` instance to the `options` property.

        The value stored in the `options` property is only used when `make_defn`
        is finally called.  `None` may be assigned to `options` if these
        additional options are not required.
        """

        return self._options

    @options.setter
    def options(self, options: Optional[AdditionalOptions]):
        if options is not None and not isinstance(options, AdditionalOptions):
            raise TypeError()

        self._options = options
        self._reset()


    #-----------------------------------------------------------------------

    @property
    def ground(self) -> Ground:
        """
        Ground Resistivity

        When conductor geometry is used (ie, direct Y,Z entry is not used),
        the Ground (Earth Return) parameters must be stored in a `Ground`
        instance.

        That ground parameters may be changed, or the `ground` property may be
        overwritten with a new `Ground()` instance.  The value stored in the
        `ground` property is only used when `make_defn` is finally called,
        if the Bergeron model is selected and Direct Y,Z entry is not used.
        """
        
        return self._ground

    @ground.setter
    def ground(self, ground: Ground):
        if not isinstance(ground, Ground):
            raise TypeError()

        self._ground = ground
        self._reset()

    #-----------------------------------------------------------------------


    @property
    def yz(self) -> Optional[YZ]:
        """
        Direct Y, Z Entry (Bergeron Model Only)

        If the Bergeron Model is selected, the `yz` property may be assigned
        a `YZ()` instance with the appropriate values.

        The instance stored in the `yz` property is only used when `make_defn`
        is finally called if the Bergeron model is selected.
        """
        
        return self._yz

    @ground.setter
    def yz(self, yz: Optional[YZ]):
        if yz is not None and not isinstance(yz, YZ):
            raise TypeError()

        self._yz = yz
        self._reset()


    #-----------------------------------------------------------------------

    @property
    def conductor_data(self) -> ConductorData:
        """
        Conductor Data

        If TLine towers are created in the wizard, the conductor data for
        the tower is first read from this `conductor_data` property.

        The `.conductor_data` parameters may be changed, or the
        `.conductor_data` property may be overwritten with a new
        `ConductorData()` instance with different values.  The values stored
        in the `conductor_data` property are copied when each `.tower_xxxxx()`
        method is called.

        Example::
            tlw = TLineWizard(freq_dep=True)

            # Two 3-conductor towers with identical conductor data
            tlw.conductor_data = ConductorData(...)
            tlw.tower_3_flat(...)
            tlw.tower_3_flat(...)

            # The third tower has different conductor data
            tlw.conductor_data = ConductorData(...)
            tlw.tower_3_vert(...)

            tlw.make_defn(prj, tline_name)
            tline = tlw.create(canvas, x, y, ...)
        """

        return self._conductor_data

    @conductor_data.setter
    def conductor_data(self, data: ConductorData):
        if not isinstance(data, ConductorData):
            raise TypeError()

        self._conductor_data = data


    #-----------------------------------------------------------------------

    @property
    def subconductor_data(self) -> SubConductorData:
        """
        Sub-Conductor Data

        If TLine towers are created in the wizard, the subconductor data for
        the tower is first read from this `.subconductor_data` property.

        Like `.conductor_data`, the `.subconductor_data` parameters may be
        changed, or the `.subconductor_data` property may be overwritten with
        a new `SubConductorData()` instance with different values.  The values
        stored in the `.subconductor_data` property are copied when each
        `.tower_xxxxx()` method is called.
        """

        return self._subconductor_data

    @subconductor_data.setter
    def subconductor_data(self, data: SubConductorData):
        if not isinstance(data, SubConductorData):
            raise TypeError()

        self.subconductor_data = data


    #-----------------------------------------------------------------------

    @property
    def ground_wire_data(self) -> GroundWireData:
        """
        Ground Wire Data

        If TLine towers are created in the wizard, the ground wire data for
        the tower is first read from this `.ground_wire_data` property.

        Like `.conductor_data`, the `.ground_wire_data` parameters may be
        changed, or the `.ground_wire_data` property may be overwritten with
        a new `GroundWireData()` instance with different values.  The values
        stored in the `.ground_wire_data` property are copied when each
        `.tower_xxxxx()` method is called.
        """

        return self._ground_wire_data

    @ground_wire_data.setter
    def ground_wire_data(self, data: GroundWireData):
        if not isinstance(data, GroundWireData):
            raise TypeError()

        self._ground_wire_data = data


    #-----------------------------------------------------------------------

    _TOWER_Y = {'1': 29,
                '2_Flat': 29,
                '3-Flat': 25, '3_Delta': 29, '3_Concent': 27, '3_Offset': 29,
                '3_Vert': 25,
                '6_Vert1': 22, '6_Concent': 27, '6_Offset': 29, '6_Vert': 25,
                '6_Flat': 29, '6_Delta': 29,
                '12_Vert': 22,
                }

    def _create(self, defn: str, x: int, y: int, data=None):
        assert self._canvas is not None
        cmp = self._canvas.create_component(f'master:{defn}', x, y)
        if data is not None:
            if not isinstance(data, dict):
                data = asdict(data)            
            cmp.parameters(parameters=data)
        return cmp

    def _create_tower(self, x, tower_data):
        parameters = dict(tower_data)
        defn = parameters.pop('-defn-')

        y = self._TOWER_Y.get(defn, 22)
        tower = self._create(f'Line_Tower_{defn}', x, y, parameters)

    def _create_towers(self):
        towers = sorted(self._towers, key=lambda tower: tower['X'])
        x = 9
        for tower in towers:
            if tower['-defn-'] == 'Universal':
                x += 10
            self._create_tower(x, tower)
            x += 17
            if tower['-defn-'] == 'Universal':
                x += 8


    #-----------------------------------------------------------------------

    def _make_defn(self, class_id, project: Project, name: str):

        defn_str = _TWM_DEFN_STR.format(name=name, type=class_id)

        defn = project.create_definition(defn_str)
        self._defn = defn
        self._canvas = defn.canvas()

        if isinstance(self._model, Bergeron):
            self._create('Line_Berg_Options', 32, 10, self._model)
            if self._yz:
                self._create('Line_ManualYZ', 32, 19, self._yz)
            else:
                self._create('Line_Ground', 23, 35, self._ground)
        else:
            self._create('Line_FrePhase_Options', 33, 10, self._model)
            self._create('Line_Ground', 23, 39, self._ground)

        if self._options:
            self._create('Line_Out_Disp', 56, 5, self._options)

        if self._towers:
            self._create_towers()


    def make_defn(self, project: Project, name: str) -> Definition:
        """
        Make the Definition

        Create the TLine definition in the indicated project, with the
        given name (if available).

        The values set in the `.model`, `.yz`, `.ground`, and `.options`
        properties are used during this call in the creation of the TLine
        definition.
        """

        self._make_defn("TLine", project, name)

        return self._defn


    #-----------------------------------------------------------------------

    def create(self, canvas: Canvas, x: int, y: int, *, orient: int = 0,
               **props) -> Component:
        """
        Create a component using the current definition.
        """

        if not self._defn:
            raise ValueError("Definition has not been created.")

        if 'Name' not in props:
            props['Name'] = self._defn.name

        props['Dim'] = self._nodes

        return canvas.create_component(self._defn, x, y, orient, **props)


    #-----------------------------------------------------------------------

    def _tower(self, num_conductors, tower_defn, extra, **kwargs):

        tower = {**asdict(self._conductor_data),
                 **asdict(self._subconductor_data),
                 **asdict(self._ground_wire_data), **extra, **kwargs}

        if tower_defn == 'Universal':
            # Universal tower defines ground wire positions: XG1 & XG2,
            # not the distance between ground wires: XG
            del tower['XG']

        for key in ('X', 'Y', 'X2', 'Y2', 'XC', 'Y3'):
            if key in tower:
                tower[key] = m(tower[key])

        gw_nodes = int(tower['NG'])
        gw_elim = tower['ElimGW']
        if str(gw_elim).lower() in {'1', 'true', 'enabled'}:
            gw_nodes = 0

        for c in range(1, num_conductors + 1):
            tower[f'NC{c}'] = c + self._nodes
        self._nodes += num_conductors

        for gw in range(1, 3):
            tower[f'NG{gw}'] = gw + self._nodes
        self._nodes += gw_nodes

        tower['-defn-'] = tower_defn
        self._towers.append(tower)

        self._reset()

        return tower


    #-----------------------------------------------------------------------
    # Add TLine Towers
    #-----------------------------------------------------------------------

    def tower_1(self, x: Distance, y: Distance, **kwargs):
        """
        Add a single conductor tower

        The conductor is located at the given (x, y) coordinate.
        """

        tower = self._tower(1, '1', kwargs, X=x, Y=y)

        tower.pop('Transp', None)  # Single phases can't be transposed


    def tower_2_flat(self, x: Distance, y: Distance, xc: Distance, **kwargs):
        """
        Add a 2-conductor tower

        The conductors are located at (x - xc / 2, y) and (x + xc / 2, y).
        """

        self._tower(2, '2_Flat', kwargs,X=x, Y=y, XC=xc)


    def tower_3_flat(self, x: Distance, y: Distance, xc: Distance, **kwargs):
        """
        Add a 3-conductor tower

        The conductors are located at (x - xc, y), (x, y), and (x + xc, y).
        """

        self._tower(3, '3-Flat', kwargs, X=x, Y=y, XC=xc)


    def tower_3_delta(self, x: Distance, y: Distance, xc: Distance,
                      y2: Distance, **kwargs):
        """
        Add a 3-conductor tower

        The conductors are at (x - xc, y), (x, y + y2), and (x + xc, y).
        """

        self._tower(3, '3_Delta', kwargs, X=x, Y=y, XC=xc, Y2=y2)


    def tower_3_concent(self, x: Distance, y: Distance, x2: Distance,
                        y2: Distance, **kwargs):
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x + x2, y + y2), and (x, y + 2 y2).
        If x2 is negative, the second conductor is to left of the other two.
        """

        x2 = m(x2)

        tower = self._tower(3, '3_Concent', kwargs,
                            X=x, Y=y, X2=abs(x2), Y2=y2, side=(x2>0))


    def tower_3_offset(self, x: Distance, y: Distance, x2: Distance,
                       y2: Distance, **kwargs):
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x + x2, y), and (x, y + y2).
        If x2 is negative, the second conductor is to left of the other two.
        """

        x2 = m(x2)

        self._tower(3, '3_Offset', kwargs, X=x, Y=y, X2=abs(x2), Y2=y2,
                    side=(x2>0))


    def tower_3_vert(self, x: Distance, y: Distance, y2: Distance, **kwargs):
        """
        Add a 3-conductor tower

        The conductors are at (x, y), (x, y + y2), and (x, y + 2 y2).
        If x2 is negative, the second conductor is to left of the other two.
        """

        self._tower(3, '3_Vert', kwargs, X=x, Y=y, Y2=y2)


    def tower_6_vert1(self, x: Distance, y: Distance, y2: Distance,
                      y3: Distance, **kwargs):
        """
        Add a 6-conductor tower

        The first 3 conductors are at (x, y), (x, y + y2), and (x, y + 2 y2).
        The next 3 conductors are an additional y3 higher.
        """

        y2 = m(y2)
        y3 = m(y3)
        if y3 < 3 * y2:
            raise ValueError("y3 should be at least triple y2")

        self._tower(6, '6_Vert1', kwargs, X=x, Y=y, Y2=y2, Y3=y3)

    def tower_6_concent(self, x: Distance, y: Distance, xc: Distance,
                        x2: Distance, y2: Distance, **kwargs):
        """
        Add a 6-conductor tower

        The conductors are at
        (x - xc/2, y), (x - xc/2 - x2, y + y2), (x - xc/2, y + 2 y2),
        (x + xc/2, y), (x + xc/2 + x2, y + y2), and (x + xc/2, y + 2 y2).
        """

        self._tower(6, '6_Concent', kwargs, X=x, Y=y, XC=xc, X2=x2, Y2=y2)


    def tower_6_offset(self, x: Distance, y: Distance, xc: Distance,
                       x2: Distance, y2: Distance, **kwargs):
        """
        Add a 6-conductor tower

        The conductors are arranged in a two mirrored L-shape.
        """

        self._tower(6, '6_Offset', kwargs, X=x, Y=y, XC=xc, X2=x2, Y2=y2)


    def tower_6_vert(self, x: Distance, y: Distance, xc: Distance, y2: Distance,
                     **kwargs):
        """
        Add a 6-conductor tower

        The conductors are at
        (x - xc/2, y), (x - xc/2, y + y2), (x - xc/2, y + 2 y2).
        (x + xc/2, y), (x + xc/2, y + y2), and (x + xc/2, y + 2 y2).
        """

        self._tower(6, '6_Vert', kwargs, X=x, Y=y, XC=xc, Y2=y2)


    def tower_6_flat(self, x: Distance, y: Distance, xc: Distance, y2: Distance,
                     **kwargs):
        """
        Add a 6-conductor tower

        The first 3 conductors are at (x, y), (x + xc, y), and (x + 2 xc, y).
        The next 3 conductors are an additional y2 higher.
        """

        self._tower(6, '6_Flat', kwargs, X=x, Y=y, XC=xc, Y2=y2)


    def tower_6_delta(self, x: Distance, y: Distance, xc: Distance,
                      x2: Distance, y2: Distance, **kwargs):
        """
        Add a 6-conductor tower

        The conductors are arranged in a two delta shape.
        """

        self._tower(6, '6_Delta', kwargs, X=x, Y=y, XC=xc, X2=x2, Y2=y2)


    def tower_12_vert(self, x: Distance, y: Distance, xc: Distance,
                      y2: Distance, y3: Distance, **kwargs):
        """
        Add a 12-conductor tower
        """

        y2 = m(y2)
        y3 = m(y3)
        if y3 < 3 * y2:
            raise ValueError("y3 should be at least triple y2")

        self._tower(12, '12_Vert', kwargs, X=x, Y=y, XC=xc, Y2=y2, Y3=y3)


    def tower_universal(self, conductors: list, ground_wires: list, **kwargs):
        """
        Add a tower with between 1 and 12 conductors, and between 0 and 2
        grounds wires.

        Both the conductors and the ground wires must be given as lists
        of (x,y) pairs:

        Examples::
            tlw = TLineWizard()
            tlw.tower_universal([(-10, 30), (0, 35), (+10, 30),
        """

        nc = len(conductors)
        ng = len(ground_wires)

        if nc < 1 or nc > 12:
            raise ValueError("Requires 1-12 conductors")

        if len(ground_wires) > 2:
            raise ValueError("Maximum 2 ground wires")

        coords = {}
        for i, (x, y) in enumerate(conductors, 1):
            coords[f'XC{i}'] = m(x)
            coords[f'YC{i}'] = m(y)
        for i, (x, y) in enumerate(ground_wires, 1):
            coords[f'XG{i}'] = m(x)
            coords[f'YG{i}'] = m(y)

        self._tower(nc, 'Universal', kwargs, Nc=nc, NG=ng, **coords)
