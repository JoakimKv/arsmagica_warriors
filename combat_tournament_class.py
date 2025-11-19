
# combat_tournament_class.py


from warrior_fighter_class import WarriorFighter
from warrior_class import Warrior
from combat_duel_class import CombatDuel
from print_out_text_handler_class import PrintOutTextHandler



class CombatTournament:

   nr_of_tournament_constant = 20

   def __init__(self, warriorList, nrOfTournament = nr_of_tournament_constant):

      self.warriorList = []
      self.warriorFighterList = []

      # The number of rounds you make a "round robin" ("all meets all").      
      self.nrOfTournament = nrOfTournament

      self.strStoredText = ""

      # The value n is the number of warriors in the list.
      n = 0

      if (warriorList):  
                                           
         if (len(warriorList) >= 2):
           
            n = len(warriorList)
            self.warriorList = []

            for index in range(n):

               self.warriorList.append(warriorList[index].makeCopyOfWarriorObject()) 
               self.warriorFighterList.append(WarriorFighter(self.warriorList[index]))

      self.combatDuel = None

      self.indexA = 0
      self.indexB = 0

      self.printOutTextHandler = PrintOutTextHandler()

      self.bIsVerbose = self.printOutTextHandler.getIsVerbose()

   def getNrOfTournamentRounds(self):

      return self.nrOfTournament
   
   def setNrOfTournamentRounds(self, nrOfTournament):

      self.nrOfTournament = nrOfTournament
      
   def isWarriorListsOK(self):
   
      bOK = False

      # List must not be empty.
      if (self.warriorList):

         # Must contain at least two warriors.
         if (len(self.warriorList) >= 2):

            bOK = True
   
      return bOK

   def setIsVerbose(self, bIsVerbose):

      self.printOutTextHandler.setIsVerbose(bIsVerbose)
      self.bIsVerbose = self.printOutTextHandler.getIsVerbose()

   def getIsVerbose(self):

      return self.printOutTextHandler.getIsVerbose()
   
   def isIndicesOK(self):
      
      bOK = False
      n = len(self.warriorList)

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

   def createWarriorListFromFighters(self):
      
      n = len(self.warriorFighterList)

      for index in range(n):
               
         self.warriorList[index] = self.warriorFighterList[index].getWarrior()

   def getWarriorList(self):
      
      self.createWarriorListFromFighters()

      return self.warriorList.copy()

   def makeOneRoundOfTournament(self):

      n = len(self.warriorFighterList)

      for outer_count in range(n):

         for inner_count in range(outer_count + 1, n, 1):

            self.combatDuel = CombatDuel(self.warriorFighterList[inner_count],
                                         self.warriorFighterList[outer_count])
            
            self.combatDuel.setIsVerbose(False)

            self.combatDuel.makeEntireCombat()
            self.strStoredText += self.combatDuel.strStoredText

            self.warriorFighterList[inner_count] = self.combatDuel.getWarriorFighterA()
            self.warriorFighterList[outer_count] = self.combatDuel.getWarriorFighterB()

   def makeAllRoundsOfTournament(self):

      n = self.nrOfTournament

      for outer_count in range(n):

         self.makeOneRoundOfTournament()
