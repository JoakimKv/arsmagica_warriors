
# combat_data_class.py


class CombatData:
    
    """
    Represents one attack in a combat turn: attacker vs defender.
    Handles all calculations, status, and text output without
    immediately affecting the real WarriorFighter objects.
    """
    
    def __init__(self, attacker, defender, bIsWarriorA = True , maxRoundsToSkip = 2):
        
        # Make WarriorFighter copies inside the class.
        self.attacker = attacker     
        self.defender = defender

        # This data can be obtained from CombatDuel class.      
        self.maxRoundsToSkip = maxRoundsToSkip

        if bIsWarriorA:          
           self.letterList = ["A", "B"]
        else:         
           self.letterList = ["B", "A"]

        self.totalDamageDone = 0
        self.woundType = ""

        self.strText = ""

        self.bIsBerserkModeDef = (self.defender.bIsInBerserkerMode and self.defender.bIsBerserker)
        self.bIsBerserkModeAtt = (self.attacker.bIsInBerserkerMode and self.attacker.bIsBerserker)

    def performAttack(self):
      
       """
       Perform one attack sequence for attacker vs defender.
       Returns descriptive string.
       """

       self.strText = ""
       attName = self.attacker.warrior.name
       defName = self.defender.warrior.name
       attLetter, defLetter = self.letterList

       # Check if attacker is skipping due to an earlier botch.
       if self.attacker.isMoreMissedTurns():
          
          self.strText += f"Warrior {attLetter} ({attName}) needs to skip his turn due to an earlier botch.\n"
          self.attacker.setMissedTurns(self.attacker.getMissedTurns() - 1)
          return self.strText

       # Roll dice
       diceResult = self.attacker.rollAndGetDiceResult()
       roll = diceResult.rollValue
       diceRollList = diceResult.diceRollsAsList
       status = diceResult.status

       self.strText += f"Warrior {attLetter} ({attName}) rolled: {diceRollList}.\n"

       if status == "botched":
          
          self.strText += f"Warrior {attLetter} ({attName}) needs to skip his turn due to an imminent botch.\n"
          self.attacker.setMissedTurns(self.maxRoundsToSkip - 1)
          return self.strText

       # Calculate attack and defense.

       woundPenaltyAtt = self.attacker.calculateTotalWoundPenaltyAllCases()
       woundPenaltyDef = self.defender.calculateTotalWoundPenaltyAllCases()

       if self.bIsBerserkModeAtt:
          totAttack = max((self.attacker.calculateTotalAttackWithNoDice() + roll), 0)
          dmgFromAttacker = self.attacker.calculateTotalDamage() + abs(woundPenaltyAtt)
       else:       
          totAttack = max((self.attacker.calculateTotalAttackWithNoDice() + roll + woundPenaltyAtt), 0)
          dmgFromAttacker = self.attacker.calculateTotalDamage()

       if self.bIsBerserkModeDef:          
          totDefense = max((self.defender.calculateTotalDefense()), 0)
       else:
          totDefense = max((self.defender.calculateTotalDefense() - (abs(woundPenaltyDef) // 2)), 0)

       armour = max((self.defender.calculateTotalArmour()), 0)

       diff = totAttack - totDefense

       if diff <= 0:

          self.strText += f"Warrior {attLetter} ({attName}) missed warrior {defLetter} ({defName}).\n"
          self.totalDamageDone = 0

       else:
          
          dmg = max((diff + dmgFromAttacker), 0) - armour
          if dmg <= 0:
             
             self.strText += f"Warrior {attLetter} ({attName}) hit the opponent but did not make a dent in the armour.\n"
             self.totalDamageDone = 0

          else:
             
             self.totalDamageDone = dmg
             self.woundType = self.defender.calculateWoundType(dmg)
             if self.bIsBerserkModeDef and self.woundType != "death":
                self.strText += (
                   f"Warrior {defLetter} ({defName}) took a(n) {self.woundType} wound "
                   f"(but as a berserker it means that the warrior took a minor wound).\n"
                )
             else:
                self.strText += f"Warrior {defLetter} ({defName}) took a(n) {self.woundType} wound.\n"

       return self.strText
