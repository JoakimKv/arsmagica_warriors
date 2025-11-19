
# combat_duel_class.py


from warrior_fighter_class import WarriorFighter
from combat_modifier_class import CombatModifier
from print_out_text_handler_class import PrintOutTextHandler
from rating_calculator_class import RatingCalculator
from dice_result_class import DiceResult
from combat_data_class import CombatData


class CombatDuel:

   # The number of rounds to skip when you botch.
   max_nr_of_rounds_to_skip_constant = 2

   # Finnish the combat after this number of turns.
   max_nr_of_turns = 100

   def __init__(self, warriorFighterA, warriorFighterB, 
                maxNrOfRoundsToSkip = max_nr_of_rounds_to_skip_constant,
                maxNrOfTurns = max_nr_of_turns):

      self.strStoredText = ""

      self.warriorFighterA = warriorFighterA.makeCopyOfWarriorFighterObject()
      self.warriorFighterB = warriorFighterB.makeCopyOfWarriorFighterObject()

      self.maxNrOfRoundsToSkip = maxNrOfRoundsToSkip
      self.maxNrOfTurns = maxNrOfTurns

      self.combatDataAttackerA = None
      self.combatDataAttackerB = None     

      self.combatModifier = CombatModifier()
      self.attDefMod = self.combatModifier.getAttackDefenseModifiers(self.warriorFighterA, 
                                                                     self.warriorFighterB)
      
      self.warriorFighterA.setCombatModifierValues(attackMod = self.attDefMod["warriorA_AttMod"], 
                                                   defenseMod = self.attDefMod["warriorA_DefMod"])
      
      self.warriorFighterB.setCombatModifierValues(attackMod = self.attDefMod["warriorB_AttMod"], 
                                                   defenseMod = self.attDefMod["warriorB_DefMod"])      

      self.indexA = 0
      self.indexB = 0

      self.diceResultA = DiceResult()
      self.diceResultB = DiceResult()

      warriorRatingA = self.warriorFighterA.getWarrior().getRating()
      warriorRatingB = self.warriorFighterB.getWarrior().getRating()

      self.refreshWarriorsBeforeFight()

      self.ratingCalculator = RatingCalculator(ratingA = warriorRatingA, ratingB = warriorRatingB)

      self.printOutTextHandler = PrintOutTextHandler()

   def refreshWarriorsBeforeFight(self):

      self.warriorFighterA.resetWoundData()
      self.warriorFighterB.resetWoundData()

      self.warriorFighterA.setMissedTurns(0)
      self.warriorFighterB.setMissedTurns(0)

      self.warriorFighterA.bIsInBerserkerMode = False
      self.warriorFighterB.bIsInBerserkerMode = False

   def getMaxNrOfRoundsToSkip(self):

      return self.maxNrOfRoundsToSkip
   
   def setMaxNrOfRoundsToSkip(self, maxNrOfRoundsToSkip):

      self.maxNrOfRoundsToSkip = maxNrOfRoundsToSkip

   def getMaxNrOfTurns(self):

      return self.maxNrOfTurns
   
   def setMaxNrOfTurns(self, maxNrOfTurns):

      self.maxNrOfTurns = maxNrOfTurns

   def setIsVerbose(self, bIsVerbose):

      self.printOutTextHandler.setIsVerbose(bIsVerbose)

   def getIsVerbose(self):

      return self.printOutTextHandler.getIsVerbose()
   
   def getWarriorFighterA(self):

      return self.warriorFighterA.makeCopyOfWarriorFighterObject()

   def getWarriorFighterB(self):

      return self.warriorFighterB.makeCopyOfWarriorFighterObject()
   
   def getWarriorA(self):

      return self.warriorFighterA.getWarrior()

   def getWarriorB(self):

      return self.warriorFighterB.getWarrior()
      
   def isIndicesOK(self, n):
      
      bOK = False

      # Note that n is the length of the warrior list.

      # Too short list of warriors, must be at least two warriors.
      if (n < 2):             
         return bOK
      
      # Can not be the same warrior that meets himself in combat.
      if (self.indexA == self.indexB):         
         return bOK
      
      # Check that both of the indices lies in the list.
      if ((0 <= self.indexA <= (n - 1)) and (0 <= self.indexB <= (n - 1))):      
         bOK = True
      
      return bOK
   
   def setWarriorFightersIndices(self, indexA, indexB):
      
      self.indexA = indexA
      self.indexB = indexB

   def getWarriorFightersIndices(self):
      
      return self.indexA, self.indexB
   
   def getWarriorFighterIndexA(self):

      return self.indexA

   def getWarriorFighterIndexB(self):

      return self.indexB

   def getTextOfWarriorsAreBerserker(self):

      strText = ""

      nameA = self.warriorFighterA.warrior.name
      nameB = self.warriorFighterB.warrior.name

      if self.warriorFighterA.bIsBerserker:

         strText += (
            f"Warrior A ({nameA}) is a berserker "
            f"with a score {self.warriorFighterA.berserkerValue}.\n\n"
         )

      if self.warriorFighterB.bIsBerserker:
         strText += (
            f"Warrior B ({nameB}) is a berserker "
            f"with a score {self.warriorFighterB.berserkerValue}.\n\n"
         )

      return strText

   def makeOneCombatTurn(self, roundNr):

      bIsKnockedDownA = False
      bIsKnockedDownB = False

      nameA = self.warriorFighterA.warrior.name
      nameB = self.warriorFighterB.warrior.name

      self.printOutTextHandler.clear()
      strText = f"Start of round number: {roundNr}.\n\n"

      if roundNr == 1:

         strText += self.getTextOfWarriorsAreBerserker()

      # Create combat data.
      self.combatDataA = CombatData(attacker = self.warriorFighterA,
                                    defender = self.warriorFighterB,
                                    bIsWarriorA = True,
                                    maxRoundsToSkip = self.maxNrOfRoundsToSkip)

      self.combatDataB = CombatData(attacker = self.warriorFighterB,
                                    defender = self.warriorFighterA,
                                    bIsWarriorA = False,
                                    maxRoundsToSkip = self.maxNrOfRoundsToSkip)
      
      # Perform attacks.
      strText += self.combatDataA.performAttack() + "\n"
      strText += self.combatDataB.performAttack() + "\n"

      # Apply wounds to real warriors.
      if self.combatDataA.totalDamageDone > 0:
        
         self.warriorFighterB.addWoundToWarrior(self.combatDataA.totalDamageDone)
         bIsKnockedDownB = self.warriorFighterB.isWarriorKnockedDown()

         if not bIsKnockedDownB:

            if self.warriorFighterB.bIsBerserker:

               bBeserkerModeB, bAlreadyBerserkB, rollB = self.warriorFighterB.isWarriorGoingBerserkAndRollValue()

               if bBeserkerModeB and not bAlreadyBerserkB:
                  self.warriorFighterB.bIsInBerserkerMode = bBeserkerModeB
                  strText += ( 
                     f"Warrior B ({nameB}) rolled [{rollB}] and had a berserker score of "
                     f"{self.warriorFighterB.berserkerValue} and is now in berserker mode.\n\n"
                  )

      if self.combatDataB.totalDamageDone > 0:
       
         self.warriorFighterA.addWoundToWarrior(self.combatDataB.totalDamageDone)
         bIsKnockedDownA = self.warriorFighterA.isWarriorKnockedDown()

         if not bIsKnockedDownA:

            if self.warriorFighterA.bIsBerserker:

               bBeserkerModeA, bAlreadyBerserkA, rollA = self.warriorFighterA.isWarriorGoingBerserkAndRollValue()

               if bBeserkerModeA and not bAlreadyBerserkA:
                  self.warriorFighterA.bIsInBerserkerMode = bBeserkerModeA
                  strText += ( 
                     f"Warrior B ({nameA}) rolled [{rollA}] and had a berserker score of "
                     f"{self.warriorFighterA.berserkerValue} and is now in berserker mode.\n\n"
                  )

      if bIsKnockedDownA:

         strText += f"Warrior A ({nameA}) is knocked down and is out of the fight.\n\n"

      if bIsKnockedDownB:
        
        strText += f"Warrior B ({nameB}) is knocked down and is out of the fight.\n\n"

      # Determine if combat should continue
      bMoreTurns = not (bIsKnockedDownA or bIsKnockedDownB)

      self.printOutTextHandler.addMoreText(strText)
      self.strStoredText += self.printOutTextHandler.getText()
      self.printOutTextHandler.printOutText()
      self.printOutTextHandler.clear()

      return bMoreTurns, bIsKnockedDownA, bIsKnockedDownB
 
   def makeEntireCombat(self):

      """
      Run the full combat between warrior A and warrior B.
      Updates their ratings at the end.
      """

      self.refreshWarriorsBeforeFight()
      self.strStoredText = ""

      roundNr = 1
      maxRounds = self.getMaxNrOfTurns()
      moreTurns = True

      while moreTurns and roundNr <= maxRounds:

         moreTurns, knockedOutA, knockedOutB = self.makeOneCombatTurn(roundNr)
         roundNr += 1

      # Determine result for rating.

      # A wins.
      if knockedOutB and not knockedOutA: 
         s_A = 1

      # B wins, so A loses.
      elif knockedOutA and not knockedOutB:
         s_A = 0

      # Draw.
      else:
         s_A = 0.5    

      # Update ratings.
      oldRatingA = self.warriorFighterA.getRating()
      oldRatingB = self.warriorFighterB.getRating()

      newRatingA, newRatingB = self.ratingCalculator.calculateNewRatings(oldRatingA, oldRatingB, s_A)

      self.warriorFighterA.setRating(newRatingA)
      self.warriorFighterB.setRating(newRatingB)
