
# dice_result_class.py


class DiceResult:
    
   def __init__(self, rollValue = 2, nrOfDice = 1, status = "normal", 
                diceRollsAsList = None):
      
      self.rollValue = rollValue
      self.nrOfDice = nrOfDice
      self.status = status

      if diceRollsAsList:
         
         self.diceRollsAsList = diceRollsAsList.copy()

      # If empty list or none create a list with one element.
      else:
         
         self.diceRollsAsList = [rollValue]

   def copyDiceResultDataFromObject(self, diceResultCopy):
        
      self.rollValue = diceResultCopy.rollValue
      self.nrOfDice = diceResultCopy.nrOfDice
      self.status = diceResultCopy.status
      self.diceRollsAsList = diceResultCopy.diceRollsAsList.copy()

   def makeCopyOfDiceResultObject(self):
      
      diceRollsList = self.diceRollsAsList.copy()

      diceResultCopy = DiceResult(rollValue = self.rollValue, nrOfDice = self.nrOfDice, 
                                  status = self.status, diceRollsAsList = diceRollsList)
      
      return diceResultCopy
