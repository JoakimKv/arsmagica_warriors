
# warrior_fighter_class.py


import re

from dice_result_class import DiceResult
from dice_roller_arsm_class import DiceRollerArsM


class WarriorFighter:
   
   max_wound_penalty_constant = 7
   automatic_defense_constant = 6
    
   def __init__(self, newWarrior, maxWoundPenalty = max_wound_penalty_constant, 
                automaticDefense = automatic_defense_constant):
        
      self.warrior = newWarrior.makeCopyOfWarriorObject()

      self.maxWoundPenalty = maxWoundPenalty

      self.woundData = {"minor": 0, "medium": 0, "heavy": 0, 
                        "incapacitated": 0, "death": 0}
      
      self.woundPenalties = {"minor": -1, "medium": -3, "heavy": -5, 
                             "incapacitated": -self.maxWoundPenalty, 
                             "death": -self.maxWoundPenalty}
      
      self.woundPenaltiesBerserker = {"minor": -1, "medium": -1, "heavy": -1, 
                                      "incapacitated": -1, 
                                      "death": -self.maxWoundPenalty}
            
      self.bIsBerserker, self.berserkerValue = self.retrieveBerserkerDataFromComments()
      self.bIsInBerserkerMode = False

      self.woundScalingFactor = self.calculateWoundScalingFactor()

      self.automaticDefense = automaticDefense

      self.woundList = ["minor", "medium", "heavy", "incapacitated", "death"]

      self.diceRollerArsM = DiceRollerArsM()

      self.diceResult = DiceResult()
      self.diceResultBerserkTest = DiceResult()

      # The default values on attackMod and defenseMod are zero.
      self.setCombatModifierValues()

      # The default value on missedTurns is zero (so "self.missedTurns = 0").
      self.setMissedTurns(0)

   def setCombatModifierValues(self, attackMod = 0, defenseMod = 0):

      self.attackMod = attackMod
      self.defenseMod = defenseMod

   def setMissedTurns(self, missedTurns):

      self.missedTurns = missedTurns

   def getMissedTurns(self):

      return self.missedTurns
   
   def isMoreMissedTurns(self):

      bMore = (self.missedTurns > 0)

      return bMore

   def retrieveBerserkerDataFromComments(self):

      comments = self.warrior.comments.lower()

      if "berserker" in comments:

         bIsBerserker = True

         # Match [6], {6}, (6), : 6, = 6, or space 6 after "berserker".
         match = re.search(r'berserker\s*(?:\(|\[|\{|:|=)?\s*(\d+)?', comments)

         if match and match.group(1):

            berserkerValue = int(match.group(1))

         else:

            berserkerValue = 1

      else:

         bIsBerserker = False
         berserkerValue = 0
      
      return bIsBerserker, berserkerValue 

   def getRating(self):

      return self.warrior.rating
   
   def setRating(self, newRating):

      self.warrior.rating = newRating

   def getWarrior(self):

      return self.warrior.makeCopyOfWarriorObject()
   
   def rollAndGetDiceResult(self):

      self.diceResult = self.diceRollerArsM.rollDice()

      return self.diceResult.makeCopyOfDiceResultObject()
   
   def getDiceResult(self):

      return self.diceResult.makeCopyOfDiceResultObject()

   def calculateWoundType(self, dmg):

      woundTypeIndex = (dmg - 1) // (self.woundScalingFactor)

      if (woundTypeIndex > 4):
         
         woundTypeIndex = 4

      return self.woundList[woundTypeIndex]
      
   def addWoundToWarrior(self, dmg):

      woundType = self.calculateWoundType(dmg)
      self.woundData[woundType] += 1

   def isWarriorGoingBerserkAndRollValue(self):

      roll = 0
      bIsInBerserkerMode = False
      bIsAlreadyBerserk = False

      if self.bIsInBerserkerMode:

         bIsInBerserkerMode = True
         bIsAlreadyBerserk = True
         return bIsInBerserkerMode, bIsAlreadyBerserk, roll

      if self.bIsBerserker:

         # The berserker should roll equal or below his or her berserker score 
         # (no botch is possible).
         self.diceResultBerserkTest = self.rollAndGetDiceResult()
         roll = self.diceResultBerserkTest.rollValue

         if (self.berserkerValue - roll) >= 0:
            bIsInBerserkerMode = True

      return bIsInBerserkerMode, bIsAlreadyBerserk, roll
   
   def removeWoundFromWarrior(self, dmg):

      woundType = self.calculateWoundType(dmg)
      self.woundData[woundType] = max((self.woundData[woundType] - 1), 0)

   def resetWoundData(self):
        
      for key in self.woundData:
         
         self.woundData[key] = 0

   def calculateWoundScalingFactor(self):
      
      scalingFactor = self.warrior.body_size + 5

      if self.warrior.body_size < -4:

         scalingFactor = 1

      return scalingFactor

   def calculateTotalWoundPenalty(self):
      
      totalPenalty = 0
        
      for key in self.woundData:
         
         totalPenalty += self.woundData[key] * self.woundPenalties[key]

      return totalPenalty
   
   def calculateTotalWoundPenaltyBerserker(self):
      
      totalPenalty = 0
        
      for key in self.woundData:
         
         totalPenalty += self.woundData[key] * self.woundPenaltiesBerserker[key]

      return totalPenalty
   
   def calculateTotalWoundPenaltyAllCases(self):

      if self.bIsInBerserkerMode:

         return self.calculateTotalWoundPenaltyBerserker()

      else:

         return self.calculateTotalWoundPenalty()
         
   def isWarriorKnockedDown(self):
      
     bIsKnockedDown = False

     totalWoundPenalty = 0

     # The warrior is berserker and is in berserker mode.     
     if (self.bIsBerserker and self.bIsInBerserkerMode):
        
        totalWoundPenalty = abs(self.calculateTotalWoundPenaltyBerserker())

     else:
        
        totalWoundPenalty = abs(self.calculateTotalWoundPenalty())

     if (totalWoundPenalty >= abs(self.maxWoundPenalty)):
        
        bIsKnockedDown = True

     return bIsKnockedDown
   
   def calculateTotalAttackWithNoDice(self):

      # A die roll needs to be added to this value.
      totalAttack = self.warrior.attack + self.attackMod

      return totalAttack   
   
   def calculateTotalDefense(self):

      totalDefense = self.warrior.defense + self.automaticDefense + self.defenseMod

      return totalDefense
   
   def calculateTotalDamage(self):

      return self.warrior.damage
   
   def calculateTotalArmour(self):

      return self.warrior.armour

   def makeCopyOfWarriorFighterObject(self):
      
      warriorFighterCopy = WarriorFighter(newWarrior = self.warrior.makeCopyOfWarriorObject(), 
                                          maxWoundPenalty = self.maxWoundPenalty, 
                                          automaticDefense = self.automaticDefense)
      
      return warriorFighterCopy
