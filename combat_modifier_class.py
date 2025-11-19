
# combat_modifier_class.py


from warrior_fighter_class import WarriorFighter



class CombatModifier:

   list_of_stances_constant = ["Christian style", "Dual wield", "Dual wield (Axe)",
                               "Spear", "Shield and weapon", "No stance"]

   def __init__(self):

      self.listOfStances = CombatModifier.list_of_stances_constant.copy()

      self.attackDefenseModifiers = { 
                                      "warriorA_AttMod": 0, 
                                      "warriorA_DefMod": 0,
                                      "warriorB_AttMod": 0, 
                                      "warriorB_DefMod": 0 
                                    }
      
      # Define which stance beats which.

      # "Shield and weapon" beats "spear".
      # "Spear" beats "dual wield" and "Dual wield (Axe)".
      # "Dual wield (Axe)" beats "Shield and weapon".
      # "Christian style" beats "No stance".
      
      self.winningRules = {

         "Shield and weapon": ["Spear"],               
         "Spear": ["Dual wield", "Dual wield (Axe)"],  
         "Dual wield (Axe)": ["Shield and weapon"],
         "Christian style": ["No stance"]

      }

   def setValuesToAttackDefenseModifiers(self, warriorA_AttMod, warriorA_DefMod, 
                                         warriorB_AttMod, warriorB_DefMod):
       
      self.attackDefenseModifiers = {

         "warriorA_AttMod": warriorA_AttMod,
         "warriorA_DefMod": warriorA_DefMod,
         "warriorB_AttMod": warriorB_AttMod,
         "warriorB_DefMod": warriorB_DefMod

      }      

   def getAttackDefenseModifiers(self, warriorFighterA, warriorFighterB):
   
      stanceA = warriorFighterA.getWarrior().stance
      stanceB = warriorFighterB.getWarrior().stance

      # Check winning rule table.

      # A wins.
      if stanceB in self.winningRules.get(stanceA, []):

         self.setValuesToAttackDefenseModifiers(1, 1, 0, 0)

      # B wins.
      elif stanceA in self.winningRules.get(stanceB, []):

         self.setValuesToAttackDefenseModifiers(0, 0, 1, 1)

      # No advantage.
      else:
         
         self.setValuesToAttackDefenseModifiers(0, 0, 0, 0)  

      return self.attackDefenseModifiers.copy()   
    