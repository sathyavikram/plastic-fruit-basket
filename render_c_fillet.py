import FreeCAD
import Part
App.ActiveDocument = App.newDocument()
part = Part.read("/Users/intelligentmachine/Documents/workspace/3d-models/plastic-fruit-basket/c_fillet.step")
obj = App.ActiveDocument.addObject("Part::Feature", "c_fillet")
obj.Shape = part
Part.show(part)
