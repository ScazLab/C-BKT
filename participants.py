
from random import randint
from random import random

import math
import copy
import random

import matplotlib.pyplot as plt

###############################################################################################
##################          CONDITION COMPARISONS        ######################################
###############################################################################################


#####################################################
#########          C-BKT UPDATE        ##############
#####################################################

def probability_attempted(t, time_attempted):
	if t > time_attempted:
		return 1
	else:
		return float(t) / time_attempted
		
def update_belief_right(sk, slip, guess):
	knows_notslipped = sk*(1-slip)
	notknows_guessed = (1-sk)*guess
	top = knows_notslipped
	bottom = knows_notslipped + notknows_guessed
	return top / bottom
	
def update_belief_wrong(sk, slip, guess, t, attempted):
	know_tried_slipped = sk*probability_attempted(t, attempted)*slip
	knows_nottried = sk*(1-probability_attempted(t, attempted))
	notknows_nottried = (1-sk)*(1-probability_attempted(t, attempted))
	notknows_tried_notguessed = (1-sk)*probability_attempted(t, attempted)*(1-guess) 
	top = know_tried_slipped + knows_nottried
	bottom = know_tried_slipped + knows_nottried + notknows_nottried + notknows_tried_notguessed 
	return top / bottom
	
def CBKT_get_new_belief(obs, p, task, ts):
	b_round = []
	for skill in range (0, len(obs)):
		current_skill_obs = obs[skill]
		init_belief = p.initial_belief[skill]
		b = 0
		for i in range (0, history_rounds):
			b_ts = 0
			if (i == 0):

				if (obs[skill] == 0):
					b_ts = update_belief_wrong(init_belief, task.skills[skill].p_slip, task.skills[skill].p_guess,ts, task.skills[skill].attempted)
					history[ts].append(b_ts)
				else:
					b_ts = update_belief_right(init_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
					history[ts].append(b_ts)
			elif (ts - i) < 0:
				b_ts = p.initial_belief[skill]
			else:
				b_ts = history[ts - i][skill]
			b += b_ts
		b = b / history_rounds
		b_round.append(b)
	return b_round
	

	
######################################################
#########          BKT UPDATE FROM START       #######
######################################################

def update_belief_right_traditional(sk, slip, guess):
	knows_notslipped = sk*(1-slip)
	notknows_guessed = (1-sk)*guess
	top = knows_notslipped
	bottom = knows_notslipped + notknows_guessed
	return top / bottom
	
def update_belief_wrong_traditional(sk, slip, guess):
	know_tried_slipped = sk*slip
	notknows_tried_notguessed = (1-sk)*(1-guess) 
	top = know_tried_slipped 
	bottom = know_tried_slipped + notknows_tried_notguessed 
	return top / bottom
	
def BKT_get_new_belief_from_start(obs, p, task):
	b_round = []
	for skill in range (0, len(obs)):
		current_skill_obs = obs[skill]
		init_belief = p.initial_belief[skill]
		# ~ print (p.belief)
		# ~ print (init_belief)
		# ~ print (task.skills[skill].p_slip)
		# ~ print ("------")
		b = 0
		if (obs[skill] == 0):
			b = update_belief_wrong_traditional(init_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
		else:
			b = update_belief_right_traditional(init_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
		b_round.append(b)
	return b_round
	
	
###############################################################################################
##################          BKT UPDATE EVERY TIMESTEP        ##################################
###############################################################################################


def BKT_get_new_belief_every_timestep(obs, p, task):
	b_round = []
	for skill in range (0, len(obs)):
		current_skill_obs = obs[skill]
		current_belief = p.belief[-1][skill]
		b = 0

		# ~ print (p.belief)
		# ~ print (current_belief)
		# ~ print (task.skills[skill].p_slip)
		# ~ print ("------")
		if (obs[skill] == 0):
			b = update_belief_wrong_traditional(current_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
		else:
			b = update_belief_right_traditional(current_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
		# ~ if (skill == 0):
			# ~ print (obs[skill])
			# ~ print (current_belief)
			# ~ print (b)
		b_round.append(b)
	return b_round

###############################################################################################
##################          AUXILIARY FUNCTIONS        ########################################
###############################################################################################
	
def decision(probability):
	v = random.uniform(0.0, 1.0)
	if (v < probability):
		return 1
	else:
		return 0
		
def write_file(name,info):
	f = open(name+".txt", "w")
	for el in info:
		f.write(str(round(el,2)) + "\n")
	f.close()
		
			
###############################################################################################
##################          PERSON, SKILL, AND TASKS        ###################################
###############################################################################################

class Person():
	def __init__(self, p_id, mastery):
		self.p_id = p_id
		self.mastery = []
		self.initial_belief = []
		self.belief = []
		self.prev_obs = []
		for i in range(0, 17):
			self.initial_belief.append(self.start_b)
		self.belief.append([0.5]*17) #set to just have the initial belief (complete uncertianty) at the start
			
	def get_obs(self, p_id, task, ts):
		obs = []
		for i in range (0, task.number_skills):
			p_att = probability_attempted(ts, task.skills[i].attempted)
			has_attempted = decision(p_att)
			can_do = self.mastery[i]

			if (has_attempted == 0):
				obs.append(0)
			else:
				if (can_do == 1):
					probability = 1 - task.skills[i].p_slip
					obs.append(decision(probability))
				else:
					probability = task.skills[i].p_guess
					obs.append(decision(probability))
		return obs
	
		
class Skill():
	def __init__(self, name, guess, slip, att):
		self.name = name
		self.p_guess = guess
		self.p_slip = slip
		self.attempted = att

class Task():
	def __init__(self, t, action):
		# ~ self.skills = []
		# ~ self.number_skills = n_skills
		t_id = t
		self.action = action
		
	
###############################################################################################
##################          MEASURES AND REWARD FUNCTIONS        ##############################
###############################################################################################

def distance(b1, b2):
	d = []
	for ts in range (0, len(b1)):
		d_ts = 0
		for sk in range (0, len(b1[0])):
			d_ts += abs(b1[ts][sk] - b2[ts][sk])
		d.append(d_ts / len(b1[0]))
	return d
	

def distance_squared(b1, b2):
	d = []
	for ts in range (0, len(b1)):
		d_ts = 0
		for sk in range (0, len(b1[0])):
			d_ts += (b1[ts][sk] - b2[ts][sk]) * (b1[ts][sk] - b2[ts][sk])
		d.append(d_ts / len(b1[0]))
	return d
	
def distance_kld(b1, b2):
	d = []
	for ts in range (0, len(b1)):
		d_ts = 0
		for sk in range (0, len(b1[0])):
			d_ts += b1[ts][sk] * math.log(b1[ts][sk]+0.001 / (b2[ts][sk]+0.001)) + (1-b1[ts][sk]+0.001) * math.log((1-b1[ts][sk]+0.001)/ (1-b2[ts][sk]+0.001))
		d.append(d_ts / len(b1[0]))
	return d
		
###############################################################################################
##################          PARTICIPANT DATA     ##############################################
###############################################################################################
	
p1 = Person(1, [1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1])
p2 = Person(1, [1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0])
p3 = Person(1, [1,1,0,0,1,1,1,1,0,1,1,0,0,1,0,0,0]) 
p4 = Person(1, [1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0]) 
p5 = Person(1, [1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1]) 

s1 = (1,0.3, 0.1, 40)
s2 = (2,0.4, 0.1, 100)
s3 = (3,0.3, 0.1, 40)
s4 = (4,0.3, 0.1, 80)
s5 = (5,0.3, 0.1, 40)
s6 = (6,0.3, 0.1, 40)
s7 = (7,0.3, 0.1, 40)
s8 = (8,0.3, 0.1, 60)
s9 = (9,0.3, 0.1, 60)
s10 = (10,0.3, 0.1, 60)
s11 = (11,0.1, 0.3, 120)
s12 = (12,0.1, 0.3, 140)
s13 = (13,0.2, 0.3, 140)
s14 = (14,0.2, 0.3, 140)
s15 = (15,0.2, 0.3, 140)
s16 = (16,0.1, 0.3, 120)
s17 = (17,0.05, 0.3, 120)

skills = [s1, sk2, sk3, sk4, sk5, sk6, sk7, sk8, sk9, s10, sk11, sk12, sk13, sk14, sk15, sk16, sk17]

task1= (1,[1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0 ])
task2= (2,[1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
task3= (3,[0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
task4= (4,[0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
task5= (5,[ 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
task6= (6,[ 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
task7= (7,[ 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task8= (8,[ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task9= (9,[ 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task10= (10,[ 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task11= (11,[ 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task12= (12,[ 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task13= (13,[ 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task14= (14,[ 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task15= (15,[ 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task16= (16,[ 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task17= (17,[ 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task18= (18,[ 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
task19= (19,[ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0])
task20= (20,[ 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])
task23= (23,[ 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0])
task24= (24,[ 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0])
task27= (27,[ 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
task28= (28,[ 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1])
task29= (29,[ 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
task30= (30,[ 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1])
task31= (31,[ 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0])
task32= (32,[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1])
task33= (33,[1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0])
task34= (34[1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1])

all_tasks = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10,
			task11,task12,task13,task14,task15,task16,task17,task18,task19,task20,
			task23,task24,task27,task28,task29,task30,task31,task32,task33,task34]



