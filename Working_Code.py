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

#Creating Worksets from the name list
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

#Batch Naming View Names
Levels=IN[1]
TemNames=IN[0]
ViewNames=[]
for l in Levels:
    for t in TemNames:
        if l!=None:
            ViewNames.append(t+"_"+l)
OUT=ViewNames

# Set View Properties
import clr
# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
import System
from System import Array
from System.Collections.Generic import *
for i in IN[0]: #list of view template
	    	update = False
            #get all the parameters from current view template
	    	vt = UnwrapElement(i)
	    	allParams = [id.IntegerValue for id in vt.GetTemplateParameterIds()]
            #exclude the view templates in the code block
	    	exclude = set(IN[1])
	    	toSet = []
	    	for j in allParams:
	    		if j in exclude:# focus only on the specified templates
	    			toSet.append(ElementId(j))
	    			update = True
	    	if update:
	    		sysList = List[ElementId](toSet)
	    		vt.SetNonControlledTemplateParameterIds(sysList)
            TransactionManager.Instance.TransactionTaskDone()
# Assign your output to the OUT variable
if None == errorReport:
    OUT = 0
else:
    OUT = errorReport