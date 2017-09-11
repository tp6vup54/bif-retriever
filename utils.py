from lxml import etree

class XMLParser:
    def __init__(self, strXMLFilePath):
        self.file_path = strXMLFilePath
        self.tree = etree.parse(strXMLFilePath)
        self.root = self.tree.getroot()

    def getElement(self, strElementPath):
        return self.root.find(strElementPath)
    
    def setAttribute(self, strElementPath, strName, strValue):
        element = self.getElement(strElementPath)
        element.set(strName, strValue)
        print "Set '%s' = '%s'" % (strName, strValue)
        
    def getAttribute(self, strElementPath, strName):
        element = self.getElement(strElementPath)
        strValue = element.get(strName)
        print "Get '%s' = '%s'" % (strName, strValue)
        return strValue
        
    def getText(self, strElementPath):
        element = self.getElement(strElementPath)
        strValue = element.text
        print "Get text = '%s'" % strValue
        return strValue        

    def setText(self, strElementPath, strText):
        element = self.getElement(strElementPath)
        element.text = strText
        print "Set text = '%s'" % strText
    
    def write(self):
        with open(self.file_path, 'w') as f:
            f.write(etree.tostring(self.root, pretty_print=True))

def getText(strXMLFilePath, strElementPath):
    objXml = XMLParser(strXMLFilePath)
    return objXml.getText(strElementPath)

def setText(strXMLFilePath, strElementPath, strText):
    objXml = XMLParser(strXMLFilePath)
    objXml.setText(strElementPath, strText)
    objXml.write()

def getAttribute(strXMLFilePath, strElementPath, strName):
    objXml = XMLParser(strXMLFilePath)
    return objXml.getAttribute(strElementPath, strName)
    
def setAttribute(strXMLFilePath, strElementPath, strName, strValue):
    objXml = XMLParser(strXMLFilePath)
    objXml.setAttribute(strElementPath, strName, strValue)
    objXml.write()
    
def appendAttribute(strXMLFilePath, strElementPath, strName, strValue, strdelimiter=','):
    objXml = XMLParser(strXMLFilePath)
    strCurrentValue = objXml.getAttribute(strElementPath, strName)
    strNewValue = strCurrentValue + strdelimiter + strValue
    objXml.setAttribute(strElementPath, strName, strNewValue)
    objXml.write()

def removeFromAttribute(strXMLFilePath, strElementPath, strName, strValue, strdelimiter=','):
    objXml = XMLParser(strXMLFilePath)
    strCurrentValue = objXml.getAttribute(strElementPath, strName)
    listValue = strCurrentValue.split(strdelimiter)
    if strValue in listValue:
        listValue.remove(strValue)
        strNewValue = strdelimiter.join(listValue)
        objXml.setAttribute(strElementPath, strName, strNewValue)
        objXml.write()