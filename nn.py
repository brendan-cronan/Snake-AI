# neural network class

from SnakeAI import Game as game
import pygame
from pygame.locals import *
import random

import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import median, mean
from collections import Counter
import numpy as np

env = game()
env.reset()

LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 3000


def some_random_games_first():
    # plays 5 games to show what it looks like
    for episode in range(5):
        
        env = game()
        env.reset()
        #    first = True
        for _ in range(goal_steps):
            # to go faster, dont render. Shows the game.
            env.render()
            #randomize movement of the snake.
            #need to figure out what the range of this is
            action = random.randrange(-1, 2)

            observation, reward, done, info = env.step(action)
            if done: break



def generate_population(model):
    
    global score_requirement
    training_data = []
    scores = []
    accepted_scores = []
    
    print('Score Requirement for AI ', score_requirement)

    for _ in range(initial_games):
        print('Simulation ', _, " out of ", str(initial_games), '\r', end='')
        
        score = 0
        game_memory = []
        prev_observation = []

        for _ in range(goal_steps):

            if len(prev_observation) == 0:
                action = random.randrange(-1, 2)
            else:
                if not model:
                    action = random.randrange(-1, 2)
                else:
                    prediction = model.predict(prev_observation.reshape(-1, len(prev_observation), 1))
                    action = np.argmax(prediction[0])

            observation, reward, done, info = env.step(action)

            #storing the previous game into game memory.
            # previous observation gets matched with action made

            if len(prev_observation) > 0:
                game_memory.append([prev_observation, action])
                prev_observation = observation
                score += reward
            if done: break

            #if score beats the score requirement, save every move made.

        if score >= score_requirement:
            accepted_scores.append(score)

            # output layer for the network, one-hot output.
            for data in game_memory:
                
                action_sample = [0, 0, 0]
                action_sample[data[1]] = 1
                output = action_sample
                # saving the training data
                training_data.append([data[0], output])
        
        # save overall scores
        env.reset();
        scores.append(score)


    # saving the training data to np array
    training_data_save = np.array([training_data, score_requirement])
    np.save('saved.npy', training_data_save)
    
    # stats from the network
    print('Score Requirement:', score_requirement)
    print('Average accepted score:', mean(accepted_scores))
    print('Median score for accepted scores:', median(accepted_scores))
    print(Counter(accepted_scores))
    #increasing the score requirement
    score_requirement = mean(accepted_scores)

    return training_data


def neural_network_model(input_size, output_size):
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
    model.save('trained_snake.tflearn')
    
    return model


def evaluate_trained_model(model):
    score = []
    choices = []

    for each_game in range(10):
        score = 0
        game_memory = []
        prev_obs = []
        env.reset();

        for _ in range(goal_steps):
            env.render();

            if len(prev_obs) == 0:
                actions.random.randrange(-1,2)
            else:
                prediction = model.predict(prev_obs.reshape(-1, len(prev_obs), 1))
                action = np.argmax(prediction[0])

            choices.append(action)

            new_observation, reward, done, info = env.step(action)
            prev_obs = new_observation
            game_memory.append([new_observation, action])
            score += reward
            if done: break
        
            scores.append(score)
        print('Average Score is')
        print('Average Score:', sum(scores) / len(scores))
        print('choice 1:{}  choice 0:{}'.format(choices.count(1) / len(choices), choices.count(0) / len(choices)))
        print('Score Requirement:', score_requirement)



if __name__ == "__main__":
    
    
    some_random_games_first()
    # initial_population
    training_data = generate_population(None)
    
    #train with initial population data first

    model = train_model(training_data, model)

    #evaluating the model
    evaluate_trained_model(model)
    


    #recursive calls to train the AI
    
#    generation = 1
#    while True:
#        generation += 1
#
#        print('Generation: ', generation)
#        # training_data = initial_population(model)
#        training_data = np.append(training_data, generate_population(None), axis=0)
#        print('generation: ', generation, ' initial population: ', len(training_data))
#        if len(training_data) == 0:
#            break
#        model = train_model(training_data, model)
#        evaluate(model)
