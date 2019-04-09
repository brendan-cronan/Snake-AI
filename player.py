#Sources and inspirations: https://tolotra.com/2018/02/23/tutorial-train-a-tensorflow-model-to-control-the-snake-game/#comment-3
# Sentdex youtube video: https://www.youtube.com/watch?v=3zeg7H6cAJw
#modified to fit our self-created observations/input layer and snake game.


from Game import Game as game
import pygame
from pygame.locals import *
import random
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import numpy as np
#env creating the game instance,
env = game()
env.reset()
goal_steps = 300
action = -1
LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 500

def some_random_games_first():

    for episode in range(10):

        env = game()
        env.reset()
        first = True
        for _ in range(goal_steps):

     
            action = random.randrange(0, 4)
      

            if first:
                first = False
                action = 2

  
            env.render()
            observation, reward, done, info = env.step(action)
            a = 0
            if done: break


def generate_population(model):
  
    global score_requirement

    training_data = []

    scores = []
 
    accepted_scores = []
   
    print('Score Requirement:', score_requirement)
    for _ in range(initial_games):
        print('Simulation ', _, " out of ", str(initial_games), '\r', end='')
     
        env.reset()

        score = 0
      
        game_memory = []
     
        prev_observation = []
     
        for _ in range(goal_steps):
        
            if len(prev_observation) == 0:
                action = random.randrange(0, 4)
            else:
                if not model:
                    action = random.randrange(0, 4)
                else:
                    prediction = model.predict(prev_observation.reshape(-1, len(prev_observation), 1))
                    action = np.argmax(prediction[0])

        
            observation, reward, done, info = env.step(action)

       
            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
            prev_observation = observation
            score += reward
            if done: break

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                # output layer
                
                action_sample = [0, 0, 0, 0]
         
                action_sample[data[1]] = 1
                output = action_sample
                # saving our training data
                training_data.append([data[0], output])

 
        scores.append(score)


    print('Average accepted score:', mean(accepted_scores))
    print('Score Requirement:', score_requirement)
    print('Median score for accepted scores:', median(accepted_scores))
    print(Counter(accepted_scores))
    score_requirement = mean(accepted_scores)


    training_data_save = np.array([training_data, score_requirement])
    np.save('saved.npy', training_data_save)

    return training_data


def create_initial_model(training_data):
    shape_second_parameter = len(training_data[0][0])
    x = np.array([i[0] for i in training_data])
    X = x.reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in training_data]
    model = create_neural_network_model(input_size=len(X[0]), output_size=len(y[0]))

    return model


def create_neural_network_model(input_size, output_size):
    network = input_data(shape=[None, input_size, 1], name='input')
    network = tflearn.fully_connected(network, 32)
    network = tflearn.fully_connected(network, 32)
    network = fully_connected(network, output_size, activation='softmax')
    network = regression(network, name='targets')
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs')

    return model


def train_model(training_data, model=False):
    shape_second_parameter = len(training_data[0][0])
    x = np.array([i[0] for i in training_data])
    
    X = x.reshape(-1, shape_second_parameter, 1)
    y = [i[1] for i in training_data]


    model.fit({'input': X}, {'targets': y}, n_epoch=10, batch_size=16, show_metric=True)
    model.save('snake_trained.tflearn')

    return model



def evaluate(model):
  
    scores = []
    choices = []
    for each_game in range(10):
        score = 0
        game_memory = []
        prev_obs = []
        env.reset()
        for _ in range(goal_steps):
            env.render()

            if len(prev_obs) == 0:
                action = random.randrange(0, 4)
            else:
                prediction = model.predict(np.array(prev_obs).reshape(-1, len(prev_obs), 1))
                action = np.argmax(prediction[0])

            choices.append(action)

            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            game_memory.append([new_observation, action])
            score += reward
            if done: break

        scores.append(score)
#     print('Average Score is')
#     print('Average Score:', sum(scores) / len(scores))
     print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))
    print('Score Requirement:', score_requirement)


if __name__ == "__main__":
    
    
    some_random_games_first()
    # initial_population
    training_data = generate_population(None)
    # creating a initial model
    model = create_initial_model(training_data)
    # training with first dataset
    model = train_model(training_data, model)
    # evaluating
    evaluate(model)

    #     recursive learning
    generation = 1
    while generation < 3:
        generation += 1

        print('Generation: ', generation)
        training_data = np.append(training_data, generate_population(None), axis=0)
        print('generation: ', generation, ' initial population: ', len(training_data))
        if len(training_data) == 0:
            break
        model = train_model(training_data, model)
        evaluate(model)
