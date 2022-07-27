import sys
import os

baseName = os.path.basename(__file__)
dirName = os.path.dirname(__file__)
print('basename:    ', baseName)
print('dirname:     ', dirName)

PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir)
)
sys.path.append(PROJECT_ROOT)

# Schritt 1 Bibliotheken importieren
from RFEM.enums import *
from RFEM.initModel import *
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import *
from RFEM.Loads.nodalLoad import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.LoadCasesAndCombinations.loadCase import *

# Schritt 2 Modell initialisieren
Model(new_model=True, model_name='Einfeldträger Bernoulli')
Model.clientModel.service.begin_modification('new')

# Schritt 3 Knoten
Node(1, 0, 0, 0)
beam_length = 5
Node(2, 1, 0, 0)

# Schritt 4 Querschnitt
Section(1, 'IPE200')

# Schritt 5 Material
Material(1, 'S235')

# Schritt 6 Balken
Member(1, 1, 2, 0.0, 1, 1)

# Schritt 7 Knotenlager
NodalSupport(1, '1', NodalSupportType.FIXED)

# Schritt 8 Last
LoadCase(1, 'LF1', [False])

# Schritt 9 Knotenlast
load = 5
NodalLoad(1, 1, '2', LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, load*1000)

# Schritt 10 Analyseeinstellungen
StaticAnalysisSett
0,\


ings(1, '1. Ordnung', StaticAnalysisType.GEOMETRICALLY_LINEAR)

# Schritt 10 Berechnung
# todo debug
Calculate_all()
