#Code for creating (all possible) worksets
PhaseNames=IN[0]
TradeNames=IN[1]
DefaultSets=IN[2]
WorksetNames=list()
for TN in TradeNames:
    for PN in PhaseNames:
        WorksetNames.append(TN+"_"+PN)
for DS in DefaultSets:
    WorksetNames.append(DS)
for TN in TradeNames:
    WorksetNames.append(TN)
OUT=WorksetNames

#Creating Worksets
import clr
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
WorksetName=IN[0]
doc=DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)
for name in WorksetName:
    Workset.Create(doc,name)

#Test of creating views in batch