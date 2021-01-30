#
# IMPORT
#

import tensorflow.compat.v1 as tf
import pygame
import math
import car
import wall
import os
import gym
import random
import numpy as np

from collections import deque
tf.disable_v2_behavior()

# pygame.init()

playerScale = 0.01

def drawGoals():
    for g in goals:
        pygame.draw.line(env.gameDisplay, green, g[0], g[1], 2)

def atGoal(correctK):
    for k in range(len(goals)):
        pos = goals[k]
        for i in range(4):
            if(intersect(player.corners[i], player.corners[(i+1)%4], pos[0], pos[1])):
                poss = line_intersection((player.corners[i], player.corners[(i+1)%4]),(pos[0], pos[1]))
                # pygame.draw.circle(env.gameDisplay, (0,0,0), poss, 5)
                if(k == correctK):
                    env.nextGoal = (env.nextGoal + 1) % env.numGoals
                    return True
    return False

def up():
    player.isAccelerating = True
    player.accelerate(0.2)
def down():
    player.isAccelerating = True
    player.accelerate(-0.1)
def right():
    if abs(player.acc) > 0.1:
        player.turn(-turnAngle)
def left():
    if abs(player.acc) > 0.1:
        player.turn(turnAngle)

def checkKeyboardInput():
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        up()
    if keys[pygame.K_DOWN]:
        down()
    if keys[pygame.K_RIGHT]:
        right()
    if keys[pygame.K_LEFT]:
        left()
    
    if keys[pygame.K_SPACE]:
        player.slowDown(0.06)
    if keys[pygame.K_r]:
        changeStartPos(pygame.mouse.get_pos())
        player.x, player.y = pygame.mouse.get_pos()

def changeStartPos(pos):
    with open('start_pos.txt', 'w') as F:
        F.write('%d %d\n' % (pos[0], pos[1]))

def loadGoals():
    goals = []
    if os.path.exists('goals.txt'):
        with open('goals.txt', 'r') as F:
            for line in F:
                txt = line[:-1]
                t = txt.split(' ')
                l = []
                for num in t:
                    l.append(int(num))
                g = [(l[0], l[1]), (l[2], l[3])]
                goals.append(g)
    return goals

def loadWalls():
    walls = []
    if os.path.exists('walls.txt'):
        with open('walls.txt', 'r') as F:
            for line in F:
                txt = line[:-1]
                t = txt.split(' ')
                l = []
                for num in t:
                    l.append(int(num))
                w = wall.Wall(l[0], l[1], l[2], l[3])
                walls.append(w)
    return walls

def drawWalls(wallWidth):
    for w in walls:
        pygame.draw.line(env.gameDisplay, black, (w.x1, w.y1), (w.x2, w.y2), wallWidth)

def debugMode():
    drawWalls(2)
    # for cor in player.corners:
    #     pygame.draw.circle(env.gameDisplay, (0,0,0), cor, 3)
    # debugBorder()
    # checkForCollisionWithWalls(player, walls)

def debugBorder():
    pygame.draw.line(env.gameDisplay, black, player.corners[0], player.corners[1], 2)
    pygame.draw.line(env.gameDisplay, black, player.corners[1], player.corners[2], 2)
    pygame.draw.line(env.gameDisplay, black, player.corners[2], player.corners[3], 2)
    pygame.draw.line(env.gameDisplay, black, player.corners[3], player.corners[0], 2)

def checkForCollisionWithWalls(obj, wallList):
        for wall in wallList:
            for i in range(4):
                if(intersect(obj.corners[i], obj.corners[(i+1)%4],(wall.x1, wall.y1), (wall.x2, wall.y2))):
                    pos = line_intersection((obj.corners[i], obj.corners[(i+1)%4]),((wall.x1, wall.y1), (wall.x2, wall.y2)))
                    # pygame.draw.circle(env.gameDisplay, (0,0,0), pos, 5)
                    return killPlayer()

def killPlayer():
    # player.__init__(startPos[0], startPos[1], playerScale)
    return True

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return 0, 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


display_width, display_height = 1000, 500
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)

class CustomEnv(gym.Env):
    def __init__(self,env_config={}):
        self.crashed = False
        self.startPos = (display_width / 2, display_height / 2)
        self.player = car.Car(startPos[0], startPos[1], playerScale)
        self.nextGoal = 1
        self.numGoals = len(goals)
        self.state = []
        self.time = 0
        self.isDead = False
        self.reward = 0
    
    def init_render(self):
        import pygame
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Game")

    def step(self, action):
        self.time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crashed = True
            # print(event)

        player.isAccelerating = False
        if userInputOn:
            checkKeyboardInput()
        else:
            if action==0:
                up()
            if action==1:
                left()
            if action==2:
                down()
            if action==3:
                right()
        if not player.isAccelerating:
            player.slowDown(0.5)
        
        self.isDead = checkForCollisionWithWalls(player, walls)

        player.updatePos()
        done = False

        self.state = []
        dists = player.vision(walls, self.gameDisplay)
        for i in dists:
            self.state.append(i)
        self.state.append(player.acc)
        self.state.append(player.angle)
        self.state.append(self.time)
        # print("{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7]))
        # reward = 0
        self.reward -= 0.05
        if atGoal(self.nextGoal):
            print("HIT GOAL")
            self.time = 0
            self.reward += 100

        if self.time > 550:
            done = True

        if self.isDead:
            done = True
            self.reward -= 300
            print("died")
        return np.array(self.state), self.reward, done, {}
    
    def reset(self):
        self.isDead = False
        self.nextGoal = 1
        self.reward = 0
        player.__init__(startPos[0], startPos[1], playerScale)
        dists = player.vision(walls, self.gameDisplay)
        self.time = 0
        self.state = []
        for i in dists:
            self.state.append(i)
        self.state.append(player.acc)
        self.state.append(player.angle)
        self.state.append(self.time)
        return np.array(self.state)

    def render(self):
        self.gameDisplay.fill(white)
        drawGoals()
        debugMode()
        # player.visionDraw(env.gameDisplay)
        player.draw(self.gameDisplay)
        pygame.display.update()
        self.clock.tick(60)

if os.path.exists('start_pos.txt'):
    with open('start_pos.txt', 'r') as F:
        for line in F:
            txt = line[:-1]
            t = txt.split(' ')
            l = []
            for num in t:
                l.append(int(num))
            startPos = tuple(l)

crashed = False
userInputOn = False
turnAngle = 5.5

player = car.Car(startPos[0], startPos[1], playerScale)
walls = loadWalls()
goals = loadGoals()

move_ticker = 0

x1, y1, x2, y1 = (0, 0, 0, 0)
firstWallPos, secondWallPos = (0, 0)

env = CustomEnv()
env.init_render()

# while not crashed:
    
#     if pygame.mouse.get_pressed() == (1,0,0):
#         if firstWallPos == 0:
#             x1, y1 = pygame.mouse.get_pos()
#             #print("SET 1")
#             firstWallPos = 1
#         elif secondWallPos == 1:
#             x2, y2 = pygame.mouse.get_pos()
#             #print("SET 2")
#             secondWallPos = 2
    
#     if pygame.mouse.get_pressed() == (0, 0, 0) and firstWallPos == 1 and secondWallPos == 0:
#         secondWallPos = 1

#     if secondWallPos == 2:
#         #print("CREATED WALL")
#         w = wall.Wall(x1,y1,x2,y2)
#         walls.append(w)
#         with open('walls.txt', 'a') as F:
#             F.write('%d %d %d %d\n' % (x1, y1, x2, y2))
#         x1, y1 = x2, y2
#         secondWallPos = 0

#     if pygame.mouse.get_pressed() == (0, 0, 1):
#         #print("DELETE SAVED WALL POS")
#         x1, y1, x2, y2 = (0,0,0,0)
#         firstWallPos = 0
#         secondWallPos = 0

#     if pygame.mouse.get_pressed() == (0, 1, 0):
#         #print("DELETE ALL WALLS")
#         x1, y1, x2, y2 = (0,0,0,0)
#         firstWallPos = 0
#         secondWallPos = 0
#         walls = []
#         open("walls.txt", "w").close()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             crashed = True
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 crashed = True
#         print(event)

##################

print("Gym:", gym.__version__)
print("Tensorflow:", tf.__version__)

class QNetwork():
    def __init__(self):
        self.state_in = tf.placeholder(tf.float32, shape=[None, 10])
        self.action_in = tf.placeholder(tf.int32, shape=[None])
        self.q_target_in = tf.placeholder(tf.float32, shape=[None])
        action_one_hot = tf.one_hot(self.action_in, depth=4)

        self.hidden1 = tf.layers.dense(self.state_in, 100, activation=tf.nn.relu)
        self.q_state = tf.layers.dense(self.hidden1, 4, activation=None)
        self.q_state_action = tf.reduce_sum(tf.multiply(self.q_state, action_one_hot), axis=1)

        self.loss = tf.reduce_mean(tf.square(self.q_state_action - self.q_target_in))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)

    def update_model(self, session, state, action, q_target):
        feed = {self.state_in: state, self.action_in: action, self.q_target_in: q_target}
        session.run(self.optimizer, feed_dict=feed)

    def get_q_state(self, session, state):
        q_state = session.run(self.q_state, feed_dict={self.state_in: state})
        return q_state

class ReplayBuffer():
    def __init__(self, maxlen):
        self.buffer = deque(maxlen=maxlen)
        
    def add(self, experience):
        self.buffer.append(experience)
        
    def sample(self, batch_size):
        sample_size = min(len(self.buffer), batch_size)
        samples = random.choices(self.buffer, k=sample_size)
        return map(list, zip(*samples))

class DQNAgent():
    def __init__(self, env):
        # self.state_dim = env.observation_space.shape
        # self.action_size = env.action_space.n
        self.q_network = QNetwork()
        self.replay_buffer = ReplayBuffer(maxlen=10000)
        self.gamma = 0.97
        self.eps = 0.05

        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())
            
    def get_action(self, state):
        q_state = self.q_network.get_q_state(self.sess, [state])
        action_greedy = np.argmax(q_state)
        action_random = np.random.randint(4)
        action = action_random if random.random() < self.eps else action_greedy
        return action
    
    def train(self, state, action, next_state, reward, done):
        self.replay_buffer.add((state, action, next_state, reward, done))
        states, actions, next_states, rewards, dones = self.replay_buffer.sample(50)
        q_next_states = self.q_network.get_q_state(self.sess, next_states)
        q_next_states[dones] = np.zeros([4])
        q_targets = rewards + self.gamma * np.max(q_next_states, axis=1)
        self.q_network.update_model(self.sess, states, actions, q_targets)

        if done: self.eps = max(0.005, 0.99 * self.eps)

    def __del__(self):
        self.sess.close()

agent = DQNAgent(env)
num_episodes = 4000
highest_reward = -1000
saver = tf.train.Saver(var_list=None, name='saved-model', max_to_keep=0, keep_checkpoint_every_n_hours=1, save_relative_paths=True)

saver.restore(agent.sess, 'car-model/model-540')

for ep in range(540, num_episodes):
    state = env.reset()
    total_reward = 0
    done = False
    while not done:
        action = agent.get_action(state)
        next_state, reward, done, info = env.step(action)
        agent.train(state, action, next_state, reward, done)
        env.render()
        total_reward = reward
        state = next_state
        if env.crashed:
            ep = 9999
            break

    # agent.update_model(total_reward)
    
    if ep % 10 == 0 or total_reward > highest_reward:
        saver.save(agent.sess, 'car-model/model', global_step=ep)

    if total_reward > highest_reward:
        highest_reward = total_reward
    print("Episode: {}, total_reward: {:.2f}, highest_reward: {:.2f}, eps: {:.2f}".format(ep, total_reward, highest_reward, agent.eps))

    # env.close()

pygame.quit()