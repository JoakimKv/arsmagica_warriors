
# warrior_class.py

class Warrior:
    
   def __init__(self, id, name, attack, defense, damage, body_size, 
                armour, stance, rating, comments):
        
      self.id = id
      self.name = name
      self.attack = attack
      self.defense = defense
      self.damage = damage
      self.body_size = body_size
      self.armour = armour
      self.stance = stance
      self.rating = rating
      self.comments = comments

   def getRating(self):

      return self.rating
   
   def setRating(self, newRating):

      self.rating = newRating
   
   def copyWarriorDataFromObject(self, warriorCopy):
        
      self.id = warriorCopy.id
      self.name = warriorCopy.name
      self.attack = warriorCopy.attack
      self.defense = warriorCopy.defense
      self.damage = warriorCopy.damage
      self.body_size = warriorCopy.body_size
      self.armour = warriorCopy.armour
      self.stance = warriorCopy.stance
      self.rating = warriorCopy.rating
      self.comments = warriorCopy.comments

   def makeCopyOfWarriorObject(self):
      
      warriorCopy = Warrior(id = self.id, name = self.name, attack = self.attack,
                            defense = self.defense, damage = self.damage, 
                            body_size = self.body_size, armour = self.armour,
                            stance = self.stance, rating = self.rating, 
                            comments = self.comments)
      
      return warriorCopy
   
   def __repr__(self):
        
      return (f"Warrior(Id={repr(self.id)}, Name={repr(self.name)}, Attack={repr(self.attack)}, "
              f"Defense={repr(self.defense)}, Damage={repr(self.damage)}, "
              f"BodySize={repr(self.body_size)}, Armour={repr(self.armour)}, "
              f"Stance={repr(self.stance)}, Rating={repr(self.rating)}, "
              f"Comments={repr(self.comments)})")
