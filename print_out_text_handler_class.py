
# print_out_text_handler_class.py


class PrintOutTextHandler:

   def __init__(self):

      self.bIsVerbose = True
      self.strText = ""

   def clear(self):

      self.strText = ""

   def setIsVerbose(self, bIsVerbose):

      self.bIsVerbose = bIsVerbose

   def getIsVerbose(self):

      return self.bIsVerbose

   def getText(self):

      return self.strText
   
   def addMoreText(self, strNewText):

      self.strText += strNewText

   def printOutText(self):

      if self.bIsVerbose:

         print(self.strText) 
