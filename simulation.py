
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
		if (obs[skill] == 0):
			b = update_belief_wrong_traditional(current_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
		else:
			b = update_belief_right_traditional(current_belief, task.skills[skill].p_slip, task.skills[skill].p_guess)
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
	def __init__(self, p_id, task):
		self.p_id = p_id
		self.mastery = []
		self.initial_belief = []
		self.belief = []
		self.start_b = random.uniform(0.5, 0.5)
		self.prev_obs = []
		for i in range(0, task.number_skills):
			self.prev_obs.append(0)
			m = random.randint(0,1)
			self.mastery.append(m)
			self.initial_belief.append(self.start_b)
		self.belief.append([self.start_b]*task.number_skills) #set to just have the initial belief (complete uncertianty) at the start
			
	def get_obs(self, task, ts):
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
	def __init__(self, name):
		self.name = name
		self.p_guess = random.uniform(0.1, 0.25)
		self.p_slip = random.uniform(0.1, 0.25)
		self.attempted = random.randint(40, 150)
		
	
class Task():
	def __init__(self):
		self.skills = []
		self.number_skills = random.randint(5,10)
		# ~ self.number_skills = 1
		for i in range (0, self.number_skills):
			skill = Skill(i)
			self.skills.append(skill)
		
	
	
	
	
###############################################################################################
##################          MEASURES AND REWARD FUNCTIONS        ##############################
###############################################################################################

def distance_kld(b1, b2):
	d = []
	for ts in range (0, len(b1)):
		d_ts = 0
		for sk in range (0, len(b1[0])):
			d_ts += b1[ts][sk] * math.log(b1[ts][sk]+0.001 / (b2[ts][sk]+0.001)) + (1-b1[ts][sk]+0.001) * math.log((1-b1[ts][sk]+0.001)/ (1-b2[ts][sk]+0.001))
		d.append(d_ts / len(b1[0]))
	return d

	
###############################################################################################
##################          100 ROUNDS OF SIMULATION     ######################################
###############################################################################################

history_rounds = 10 #amount of rounds it will average over
n_timesteps = 180
rounds = 1000

distance_C_BKT = []
distance_I_BKT = []
distance_E_BKT = []
distance_T_BKT = []

TBKT_30 = []
CBKT_30 = []
IBKT_30 = []
EBKT_30 = []
TBKT_80 = []
CBKT_80 = []
IBKT_80 = []
EBKT_80 = []
TBKT_130 = []
CBKT_130 = []
IBKT_130 = []
EBKT_130 = []
TBKT_180 = []
CBKT_180 = []
IBKT_180 = []
EBKT_180 = []

for round_n in range (0, rounds): 
	task = Task()
	p = Person(round_n, task)
	# ~ print (p.mastery)
	p_C_BKT = copy.deepcopy(p)
	# ~ p_T_BKT = copy.deepcopy(p)
	p_I_BKT = copy.deepcopy(p)
	p_E_BKT = copy.deepcopy(p)
	p_T_BKT = copy.deepcopy(p)
	True_State = copy.deepcopy(p)
	True_State.belief = [True_State.mastery]
	history = [ [] for _ in range(n_timesteps) ]
	for ts in range (0, n_timesteps):
		obs = p.get_obs(task, ts)
		# ~ print (obs)
		#update for C-BKT
		b_C_BKT = CBKT_get_new_belief(obs, p_C_BKT, task, ts)
		p_C_BKT.belief.append(b_C_BKT )
		#update for I-BKT
		b_I_BKT = BKT_get_new_belief_from_start(obs, p_I_BKT, task)
		p_I_BKT.belief.append(b_I_BKT)
		#update for E-BKT
		b_E_BKT = BKT_get_new_belief_every_timestep(obs, p_E_BKT, task)
		p_E_BKT.belief.append(b_E_BKT)
		
		b_T_BKT = p_T_BKT.initial_belief
		p_T_BKT.belief.append(b_T_BKT)
		#the true state belief, will be whether they have mastery or not
		True_State.belief.append(p.mastery)

	
	d_C_BKT = distance_kld(p_C_BKT.belief, True_State.belief)
	d_I_BKT = distance_kld(p_I_BKT.belief, True_State.belief)
	d_E_BKT = distance_kld(p_E_BKT.belief, True_State.belief)
	d_T_BKT = distance_kld(p_T_BKT.belief, True_State.belief)
	
	for ts in range (0, len(d_T_BKT)):
		if (ts == 30):
			TBKT_30.append(d_T_BKT[ts])
			CBKT_30.append(d_C_BKT[ts])
			IBKT_30.append(d_I_BKT[ts])
			EBKT_30.append(d_E_BKT[ts])
		if (ts == 80):
			TBKT_80.append(d_T_BKT[ts])
			CBKT_80.append(d_C_BKT[ts])
			IBKT_80.append(d_I_BKT[ts])
			EBKT_80.append(d_E_BKT[ts])
		if (ts == 130):
			TBKT_130.append(d_T_BKT[ts])
			CBKT_130.append(d_C_BKT[ts])
			IBKT_130.append(d_I_BKT[ts])
			EBKT_130.append(d_E_BKT[ts])
		if (ts == 180):
			TBKT_180.append(d_T_BKT[ts])
			CBKT_180.append(d_C_BKT[ts])
			IBKT_180.append(d_I_BKT[ts])
			EBKT_180.append(d_E_BKT[ts])
	
	# ~ print (d_C_BKT)
	
	distance_C_BKT.append(d_C_BKT)
	distance_I_BKT.append(d_I_BKT)
	distance_E_BKT.append(d_E_BKT)
	distance_T_BKT.append(d_T_BKT)


write_file("TBKT_30", TBKT_30 )
write_file("CBKT_30",CBKT_30) 
write_file("IBKT_30",IBKT_30)
write_file("EBKT_30", EBKT_30)
write_file("TBKT_80", TBKT_80)
write_file("CBKT_80", CBKT_80) 
write_file("IBKT_80", IBKT_80) 
write_file("EBKT_80", EBKT_80) 
write_file("TBKT_130", TBKT_130) 
write_file("CBKT_130", CBKT_130)
write_file("IBKT_130", IBKT_130) 
write_file("EBKT_130", EBKT_130) 
write_file("TBKT_180", TBKT_180) 
write_file("CBKT_180", CBKT_180) 
write_file("IBKT_180", IBKT_180) 
write_file("EBKT_180", EBKT_180) 
		
average_C_BKT =  [sum(x)/rounds for x in zip(*distance_C_BKT)]
average_I_BKT =  [sum(x)/rounds for x in zip(*distance_I_BKT)]
average_E_BKT =  [sum(x)/rounds for x in zip(*distance_E_BKT)]
average_T_BKT =  [sum(x)/rounds for x in zip(*distance_T_BKT)]


# ~ print (p_E_BKT.belief)
# ~ print (average_E_BKT)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 15})

# ~ plt.figure(figsize=(8,5))
# ~ plt.gcf().subplots_adjust(bottom=0.15)
# ~ plt.title('KLD Distance to True Skill State')
plt.plot(average_C_BKT, color='#ff1f5b', linewidth = 3)
plt.plot(average_I_BKT, color='#009ade', linewidth = 3)
plt.plot(average_E_BKT, color='#00cd6c', linewidth = 3)
plt.plot(average_T_BKT, color='#ffc61e', linewidth = 3)
# ~ plt.axis([0, n_timesteps, 0, 1])
plt.xlabel('time-steps')
plt.ylabel("Kullback-Leibler Divergence")
plt.show()
	

	
	
	
	
	
