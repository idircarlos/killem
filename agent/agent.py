import torch
import random
import numpy as np
import shutil
from collections import deque
from game.game import Game
from agent.model import LinearQNet, QTrainer
from util.helper import plot
from util.settings import *
from util.util import TerminalColor

MAX_MEMORY = 200_000
BATCH_SIZE = 2000
LR = 0.001

UP = "\x1B[1A" # Moves up 1 times for \r
CLR = "\x1B[0K" # Clears

def print_state(state_array):
    
    print(f"{UP}{TerminalColor.OKCYAN}{state_array[0]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKCYAN}{state_array[1]}{TerminalColor.ENDC} ",end="  ")
    
    print(f"{TerminalColor.HEADER}{state_array[2]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.HEADER}{state_array[3]}{TerminalColor.ENDC} ",end="  ")

    print(f"{TerminalColor.ENDC}{state_array[4]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKCYAN}{state_array[5]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKGREEN}{state_array[6]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.WARNING}{state_array[7]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.FAIL}{state_array[8]}{TerminalColor.ENDC} ",end=" ")
    
    print(f"{TerminalColor.FAIL}{state_array[9]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.WARNING}{state_array[10]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKGREEN}{state_array[11]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKCYAN}{state_array[12]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.ENDC}{state_array[13]}{TerminalColor.ENDC} ",end="  ")
    
    print(f"{TerminalColor.HEADER}{state_array[14]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.HEADER}{state_array[15]}{TerminalColor.ENDC} ",end="    ")
    
    print(f"{TerminalColor.ENDC}{state_array[16]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKCYAN}{state_array[17]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKGREEN}{state_array[18]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.WARNING}{state_array[19]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.FAIL}{state_array[20]}{TerminalColor.ENDC} ",end=" ")
    
    print(f"{TerminalColor.FAIL}{state_array[21]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.WARNING}{state_array[22]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKGREEN}{state_array[23]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.OKCYAN}{state_array[24]}{TerminalColor.ENDC} ",end="")
    print(f"{TerminalColor.ENDC}{state_array[25]}{TerminalColor.ENDC} ",end="  ")
    

    print(CLR)

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 1 # randomness
        self.gamma = 0.9 # discount rate
        self.lr = LR
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = LinearQNet(26, 128, 128, 5)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.record = 0
        self.total_score = 0


    def get_state(self, game: Game):
        
        # shoot
        bullet_left, bullet_right = game.entity_manager.get_player_shoots_sections()
        enemy_left_danger, enemy_right_danger = game.entity_manager.get_enemies_danger()
        
        # shield
        player_blocking_left, player_blocking_right = game.entity_manager.is_player_blocking()
        shoot_left_danger, shoot_right_danger = game.entity_manager.get_shoots_danger()
        
        # cooldowns
        cds = game.entity_manager.player.get_cooldowns()
        
        # state
        state = [player_blocking_left, player_blocking_right,
                 shoot_left_danger[DANGER_SHOOT_LEFT],shoot_right_danger[DANGER_SHOOT_RIGHT],
                 enemy_left_danger[DANGER_ZONE_LEFT_0],enemy_left_danger[DANGER_ZONE_LEFT_1],enemy_left_danger[DANGER_ZONE_LEFT_2],enemy_left_danger[DANGER_ZONE_LEFT_3],enemy_left_danger[DANGER_ZONE_LEFT_4],
                 enemy_right_danger[DANGER_ZONE_RIGHT_4],enemy_right_danger[DANGER_ZONE_RIGHT_3],enemy_right_danger[DANGER_ZONE_RIGHT_2],enemy_right_danger[DANGER_ZONE_RIGHT_1],enemy_right_danger[DANGER_ZONE_RIGHT_0],
                 cds[1],cds[2],
                 bullet_left[DANGER_ZONE_LEFT_0],bullet_left[DANGER_ZONE_LEFT_1],bullet_left[DANGER_ZONE_LEFT_2],bullet_left[DANGER_ZONE_LEFT_3],bullet_left[DANGER_ZONE_LEFT_4],
                 bullet_right[DANGER_ZONE_RIGHT_4],bullet_right[DANGER_ZONE_RIGHT_3],bullet_right[DANGER_ZONE_RIGHT_2],bullet_right[DANGER_ZONE_RIGHT_1],bullet_right[DANGER_ZONE_RIGHT_0],]
        
        #print(np.array(state, dtype=int))
        #print(f"{UP}{np.array(state, dtype=int)}{CLR}")
        array_state = np.array(state, dtype=int)
        #print_state(array_state)
        return array_state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = max(1 - self.n_games/200,0)
        final_move = [0,0,0,0,0]
        if random.random() < self.epsilon:
            #print(self.epsilon)
            move = random.randint(0, 4)
            final_move[move] = 1
            #print("random",move)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            #print(state0)
            prediction = self.model(state0)
            #print(prediction)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            #print("predicted",move)

        return final_move
    
    def save_checkpoint(self, is_best, checkpoint_dir, best_model_dir):
        state = {
            'epoch': self.n_games + 1,
            'state_dict': self.model.state_dict(),
            'optimizer': self.trainer.optimizer.state_dict(),
            'record': self.record,
            'total_score': self.total_score
        }
        f_path = checkpoint_dir + '/checkpoint.pth'
        torch.save(state, f_path)
        if is_best:
            best_fpath = best_model_dir + '/best_model.pth'
            shutil.copyfile(f_path, best_fpath)
            
    
    def load_checkpoint(self,checkpoint_fpath, model: LinearQNet, optimizer):
        checkpoint = torch.load(checkpoint_fpath)
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        if LEARNING:
            model.train() # TODO: May change this
        else:
            model.eval()
        return checkpoint['epoch'], checkpoint['record'], checkpoint['total_score']


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    agent = Agent()
    game = Game(agent)
    if LEARNING:
        print("Training started!\n")
    agent.n_games, agent.record, agent.total_score = agent.load_checkpoint("./model/best/best_model.pth",agent.model,agent.trainer.optimizer)
    # agent.n_games, agent.record, agent.total_score = agent.load_checkpoint("./model/manual/checkpoint.pth",agent.model,agent.trainer.optimizer)
    
    while True:
    
        # get old state
        state_old = agent.get_state(game)

        # get move  
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        if reward != 0 and reward != -1:
            #print(reward)
            pass

        if LEARNING:
            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)


            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            if LEARNING:
                agent.n_games += 1
                agent.train_long_memory()

                if score > agent.record:
                    agent.record = score
                    agent.save_checkpoint(True, "./model", "./model/best")

                print('Game', agent.n_games, 'Score', score, 'Record:', agent.record)
                print()

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()