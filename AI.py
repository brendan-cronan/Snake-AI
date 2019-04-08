from Game import Game

instance = Game()
instance.reset()

while True:
    observations = instance.step([1,0])
