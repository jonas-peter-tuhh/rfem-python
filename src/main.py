import os
import sys

from RFEM.ImportExport.exports import ExportResultTablesToCSV

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
from RFEM.initModel import *
from RFEM.BasicObjects.node import Node
from RFEM.BasicObjects.material import Material
from RFEM.BasicObjects.section import Section
from RFEM.BasicObjects.member import Member
from RFEM.TypesForNodes.nodalSupport import *
from RFEM.Loads.lineLoad import *
from RFEM.Loads.memberLoad import *
from RFEM.Loads.nodalLoad import *
from RFEM.LoadCasesAndCombinations.staticAnalysisSettings import *
from RFEM.LoadCasesAndCombinations.loadCase import *

# Schritt 2 Modell initialisieren
Model(new_model=True, model_name='Einfeldträger Bernoulli')
Model.clientModel.service.begin_modification('new')

#Forschleife
for i in range(5):

# Schritt 3 Knoten
    Node(no=2*i+1, coordinate_X=0, coordinate_Y=i, coordinate_Z=0)
    length = 5.
    Node(no=2*i+2, coordinate_X=5, coordinate_Y=i, coordinate_Z=0)

# Schritt 4 Querschnitt
    Section(i+1, 'IPE 200')

# Schritt 5 Material
    Material(i+1, 'S235')

# Schritt 6 Balken
    Member(no=i+1, start_node_no=2*i+1, end_node_no=2*i+2, rotation_angle=0.0, start_section_no=i+1, end_section_no=i+1)

# Schritt 7 Knotenlager
    a=int(2*i+1)
# NodalSupport(1, '1', NodalSupportType.HINGED)
# Die Lagerung des Modells war instabil. Der Balken konnte sich frei um die X-Achse drehen.
# Mit dem folgenden Lager wird die Verdrehung um X gehalten:
    NodalSupport(2*i+1, str(a), [inf, inf, inf, inf, 0, 0])
# Die ersten drei Werte in der Liste sind die Verschiebungen, die letzten drei die Verdrehungen. 'inf' bedeutet
# unendlich, also gehalten.
    b=int(2*i+2)
    NodalSupport(2*i+2, str(b), NodalSupportType.ROLLER_IN_X)

# Schritt 10 Analyseeinstellungen
    StaticAnalysisSettings(1, '1. Ordnung', StaticAnalysisType.GEOMETRICALLY_LINEAR)

# Schritt 8 Lastfall
# LoadCase.StaticAnalysis(1, 'LF1', [False])
    LoadCase(1, 'LF1', [False])

# Schritt 9 Linienlast
    f = 5
# NodalLoad(no=1,
#          load_case_no=1,
#          nodes_no='2',
#          load_direction=LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W,
#          magnitude=f * 1000)
    MemberLoad(no=i+1,
               load_case_no=1,
               members_no=str(i+1),
    #           load_direction=LoadDirectionType.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W,
               magnitude=f * 1000)
    # MemberLoad(1, magnitude=200)

# Schritt 10 Berechnung
Calculate_all()

# Schritt 12 Veränderungen beenden und speichern
Model.clientModel.service.finish_modification()
ExportResultTablesToCSV('C:\\Users\\Jonas\\PycharmProjects\\rfem-python\\results\\result.csv')
