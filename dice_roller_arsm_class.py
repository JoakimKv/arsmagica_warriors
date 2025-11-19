
# dice_roller_arsm_class.py

from random import Random

from dice_result_class import DiceResult


class DiceRollerArsM:

   max_dice_constant = 10
   max_nr_of_botches_constant = 1
   
   def __init__(self, maxNrOfBotches = max_nr_of_botches_constant, 
                maxDice = max_dice_constant):
        
      self.maxNrOfBotches = maxNrOfBotches

      self.maxDice = maxDice

      self.rand = Random()

   def getMaxNrOfBotches(self):

      return self.maxNrOfBotches
   
   def setMaxNrOfBotches(self, maxNrOfBotches):

      self.maxNrOfBotches = maxNrOfBotches
       
   def simpleRollDice(self):

      roll = self.rand.randint(0, (self.maxDice - 1))

      return roll
  
   def rollDice(self):

      roll = self.simpleRollDice()
      
      # Default settings.

      status = "normal"
      nr_of_normal = 1
      nr_of_botches = 0
      nr_of_ones = 0
      roll_from_ones = 0
      last_dice = 0

      new_roll = 0

      dice_roll_list = []
      dice_roll_list.append(roll)

      # Check if botch, roll the chosen number of botch dice.
      if roll == 0:

         for count in range(self.maxNrOfBotches):

            new_roll = self.simpleRollDice()
            dice_roll_list.append(new_roll)

            if new_roll == 0:

               nr_of_botches += 1
               status = "botched"

         if nr_of_botches > 0:

            diceResult = DiceResult(roll, nr_of_botches, status, dice_roll_list) 

            return diceResult
         
         else:

            diceResult = DiceResult(roll, nr_of_normal, status, dice_roll_list)
            
            return diceResult

      # Check if "crit" (ones are obtained and doubled), roll until 
      # you do not get a one anymore.      
      elif roll == 1:

         nr_of_ones += 1
         bMoreOnes = True
         status = "ones" 

         while bMoreOnes:

            new_roll = self.simpleRollDice()
            dice_roll_list.append(new_roll)

            if new_roll == 1:

               nr_of_ones += 1

            elif new_roll == 0:

               last_dice = 10
               bMoreOnes = False 

            else:

               last_dice = new_roll
               bMoreOnes = False

         roll_from_ones = 2 ** (nr_of_ones) * last_dice

         diceResult = DiceResult(roll_from_ones, nr_of_ones, status, dice_roll_list)

         return diceResult
      
      # A normal dice roll is made.
      else:

         diceResult = DiceResult(roll, nr_of_normal, status, dice_roll_list)

         return diceResult
      