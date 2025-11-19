
# rating_calculator_class.py



class RatingCalculator:
   
   k_constant = 20

   # s is warrior A's score (s_A). 
   def __init__(self, ratingA = 1000, ratingB = 1000, k_A = k_constant, k_B = k_constant, s = 0):
      
      self.ratingA = ratingA
      self.ratingB = ratingB
      self.k_A = k_A
      self.k_B = k_B
      self.s_A = s
      self.s_B = 1 - self.s_A
  
   # This method calculates the new ratings and returns the tuple (new_rating A, new_rating_B). 
   # s has the value s = 0 (warrior A loose), s = 0.5 (draw) and s = 1 (Warrior A wins).
   # s is warrior A's score (s_A).
   def calculateNewRatings(self, ratingA, ratingB, s):

      # Note that s_A + s_B = 1
      self.s_A = s
      self.s_B = 1 - self.s_A 
      self.ratingA = ratingA
      self.ratingB = ratingB

      # Note that e_A +_e_B = 1.
      e_A = 1 / (1 + 10 ** ((self.ratingB - self.ratingA) / 400))
      e_B = 1 / (1 + 10 ** ((self.ratingA - self.ratingB) / 400))

      dRatingA = self.k_A * (self.s_A - e_A)
      dRatingB = self.k_B * (self.s_B - e_B)

      newRatingA = round(self.ratingA + dRatingA)
      newRatingB = round(self.ratingB + dRatingB)

      return newRatingA, newRatingB
       
   def getInitialRatingsAndScore(self):
      
      return self.ratingA, self.ratingB, self.s_A

   def setInitialRatingsAndScore(self, ratingA, ratingB, s):
      
      self.ratingA = ratingA
      self.ratingB = ratingB
      self.s_A = s
      self.s_B = 1 - self.s_A

   def getInitialRatings(self):
      
      return self.ratingA, self.ratingB

   def setKFactors(self, k_A, k_B):
      
      self.k_A = k_A
      self.k_B = k_B

   def getKFactors(self):
      
      return self.k_A, self.k_B
   
   def copyRatingCalculatorDataFromObject(self, ratingCalculatorCopy):
        
      self.ratingA = ratingCalculatorCopy.ratingA
      self.ratingB = ratingCalculatorCopy.ratingB
      self.k_A = ratingCalculatorCopy.k_A
      self.k_B = ratingCalculatorCopy.k_B
      self.s_A = ratingCalculatorCopy.s_A
      self.s_B = ratingCalculatorCopy.s_B 

   def makeCopyOfRatingCalculatorObject(self):

      ratingCalculatorCopy = RatingCalculator(ratingA = self.ratingA, ratingB = self.ratingB, 
                                              k_A = self.k_A, k_B = self.k_B, s = self.s_A)
      
      return ratingCalculatorCopy
