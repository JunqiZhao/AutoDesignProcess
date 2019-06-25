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
# Package Preparation
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc=DocumentManager.Instance.CurrentDBDocument #access the currently openned project

# Define Functions
## Select worksets to be visible in the current view template
def select_ws(worksets,trade,phase): #The input "worksets" is the name list of all available worksets, "trade" and "phase" are extracted from view template name
    rst=[]
    for i in worksets:
    	if trade in i:
    		if phase in i or 'EXISTING' in i: #For given trade, we need to turn on current phase (get from view template names) and "Existing" phase
    			rst.append(i)
    return rst
## Setup visibility
def TurnON(vt,targeted_ws): #Turn on the targeted worksets of a view template
    doc = DocumentManager.Instance.CurrentDBDocument
    view = vt
    Worksets = targeted_ws #workset name TBD
    coll = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    TransactionManager.Instance.EnsureInTransaction(doc)
    #Turn on the identified worksets and turn off others
    for Workset in targeted_ws:
        for ws in coll:
            if vt.IsWorksetVisible(ws.Id):
                continue # this line of code will be explained later
            if ws.Name.Contains(Workset) or ws.Name.Contains('LINKED') or ws.Name.Contains('Shared') or ws.Name.Contains('Workset1'):
                view.SetWorksetVisibility(ws.Id , WorksetVisibility.Visible)
            #else:
                #view.SetWorksetVisibility(ws.Id , WorksetVisibility.Hidden)
    TransactionManager.Instance.TransactionTaskDone()
    
def TurnoffAll(vt): #Turn off all the workset visibility under current view template
    doc = DocumentManager.Instance.CurrentDBDocument
    TransactionManager.Instance.EnsureInTransaction(doc)
    coll = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    TransactionManager.Instance.EnsureInTransaction(doc)
    for ws in coll:
        vt.SetWorksetVisibility(ws.Id , WorksetVisibility.Hidden)
# Execution
## Get all the view templates in current project    
vt=[t for t in FilteredElementCollector(doc).OfClass(View).ToElements() if t.IsTemplate and 'DEMO' in t.ViewName or 'NEW' in t.ViewName] # select the view templates with phase
## Modify the visibility for each view template
for temp in vt:
    vt_temp=[]
    TurnoffAll(temp) # First, we turn off all the worksets' visibility for in a view template
    vt_temp.append(temp.ViewName)
    trade,phase=vt_temp[0].split()[0],vt_temp[0].split()[1] # Secondly, extract the trade name and phase from the name of current view template
    targeted_ws=select_ws(IN[0],trade,phase) # Thirdly, find all the worksets to be turned on
    TurnON(temp,targeted_ws) #Finally, turn on all the targeted worksets in this project
'''The reason of turn off then turn on is that we may have multiple targted worksets for a view template. When processing the second targted workset, we might change the first targeted workset (which has been turned on) to off condition by mistake. So, we cheek whether the current processed workset is on or off, if it's on, we continue without doing anything'''
OUT='Program Finish'