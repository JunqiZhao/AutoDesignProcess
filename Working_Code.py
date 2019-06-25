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
    
    
    
    
'''Try to Simplify the Turn on/off funcationality script'''

# Set View Properties (Code: https://forum.dynamobim.com/t/setting-view-template-includes/15969)
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
TransactionManager.Instance.EnsureInTransaction(doc)

# Batch setup the view template properties
for i in IN[0]: #list of view templates
	    	#update = False
            #get all the parameters from current view template
	    	vt = UnwrapElement(i)
	    	allParams = [id.IntegerValue for id in vt.GetTemplateParameterIds()]
            #turn off the view templates in the code block
	    	focus = set(IN[1])
	    	toSet = []
	    	for j in allParams:
	    		if j in focus:# focus only on the specified templates to turn off (with others turned on)
	    			toSet.append(ElementId(j))
	    	sysList = List[ElementId](toSet)
	    	vt.SetNonControlledTemplateParameterIds(sysList) #This API will turn off the specified parameters
TransactionManager.Instance.TransactionTaskDone()
# Assign your output to the OUT variable
OUT=0


'''Try to Change the scale parameters of view template'''

# Set View Properties (Code: https://forum.dynamobim.com/t/setting-view-template-includes/15969)
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
TransactionManager.Instance.EnsureInTransaction(doc)

# Batch setup the view template properties
for i in IN[0]: #list of view templates
            #get all the parameters from current view template
	    	vt = UnwrapElement(i)
	    	allParams = [id.IntegerValue for id in vt.GetTemplateParameterIds()]
            #turn off the view templates in the code block
	    	focus = set(IN[1])
	    	toSet = []
	    	for j in allParams:
	    		if j in focus:# focus only on the specified templates to turn off (with others turned on)
	    			toSet.append(ElementId(j))
	    	sysList = List[ElementId](toSet)
	    	vt.SetNonControlledTemplateParameterIds(sysList) #This API will turn off the specified parameters
TransactionManager.Instance.TransactionTaskDone()
# Assign your output to the OUT variable
OUT=0

'''Set the V/G of worksets'''
###Test of accessing view template by names###
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc=DocumentManager.Instance.CurrentDBDocument #access the currently openned project

## Get the related worksets
def select_ws(worksets,trade,phase): #The input worksets is the name list of all available worksets
    rst=[]
    for i in worksets:
    	if trade in i:
    		if phase in i or 'EXISTING' in i:
    			rst.append(i)
    return rst
## Setup Visibility
def TurnON(vt,targeted_ws): #Turn on the related worksets of a view template
    doc = DocumentManager.Instance.CurrentDBDocument
    view = vt
    Worksets = targeted_ws #workset name TBD
    coll = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    TransactionManager.Instance.EnsureInTransaction(doc)
    #Turn on the identified worksets and turn off others
    for Workset in targeted_ws:
        for ws in coll:
            if vt.IsWorksetVisible(ws.Id):
                continue
            if ws.Name.Contains(Workset) or ws.Name.Contains('LINKED') or ws.Name.Contains('Shared') or ws.Name.Contains('Workset1'):
                view.SetWorksetVisibility(ws.Id , WorksetVisibility.Visible)
            #else:
                #view.SetWorksetVisibility(ws.Id , WorksetVisibility.Hidden)
    TransactionManager.Instance.TransactionTaskDone()

def TurnoffAll(vt):
    doc = DocumentManager.Instance.CurrentDBDocument
    TransactionManager.Instance.EnsureInTransaction(doc)
    coll = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    TransactionManager.Instance.EnsureInTransaction(doc)
    for ws in coll:
        vt.SetWorksetVisibility(ws.Id , WorksetVisibility.Hidden)

#get all the view template for modification    
vt=[t for t in FilteredElementCollector(doc).OfClass(View).ToElements() if t.IsTemplate and 'DEMO' in t.ViewName or 'NEW' in t.ViewName]
#modify the visibility
for temp in vt:
    vt_temp=[]
    TurnoffAll(temp)
    vt_temp.append(temp.ViewName)
    trade,phase=vt_temp[0].split()[0],vt_temp[0].split()[1]
    targeted_ws=select_ws(IN[0],trade,phase)
    TurnON(temp,targeted_ws)

OUT=targeted_ws