
from random import randint
from random import random

import math
import copy
import random

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
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
		self.task = task
		for i in range(0, task.number_skills):
			m = random.randint(0,1)
			# ~ if (m == 0):
				# ~ self.start_b = random.uniform(0.1, 0.6)
			# ~ else:
				# ~ self.start_b = random.uniform(0.4, 0.9)
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
	
	def teach_skill(self, round_belief):
		min_belief = 100
		min_i = -1
		for i in range(0, len(round_belief)):
			if (round_belief[i] < min_belief):
				min_belief = round_belief[i]
				min_i = i
		if (self.mastery[min_i] == 0):
			p_learning = self.task.skills[min_i].teaching
			has_learned = decision(p_learning)
			# ~ print ("has learned" + str(has_learned))
			if (has_learned):
				self.mastery[min_i] = 1
				
	def teach_skill2(self, round_belief):
		less_04 = []
		for i in range(0, len(round_belief)):
			if (round_belief[i] < 0.3):
				less_04.append(i)
		if (less_04 != []):
			min_i = random.choice(less_04)
			if (self.mastery[min_i] == 0):
				p_learning = self.task.skills[min_i].teaching
				has_learned = decision(p_learning)
				# ~ print ("has learned" + str(has_learned))
				if (has_learned):
					self.mastery[min_i] = 1
				
	def skills_known(self):
		count = 0
		for s in self.mastery:
			if s == 1:
				count +=1
		return count
		
	
class Skill():
	def __init__(self, name):
		self.name = name
		self.p_guess = random.uniform(0.1, 0.25)
		self.p_slip = random.uniform(0.1, 0.25)
		self.attempted = random.randint(40, 150)
		self.teaching = random.uniform(0.15, 0.35)


	
class Task():
	def __init__(self):
		self.skills = []
		self.number_skills = random.randint(5,10)
		for i in range (0, self.number_skills):
			skill = Skill(i)
			self.skills.append(skill)
		
	
	
	
	
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
	
	
###############################################################################################
##################          100 ROUNDS OF SIMULATION     ######################################
###############################################################################################

	
history_rounds = 10 #amount of rounds it will average over
n_timesteps = 180
rounds = 1000

skills_learned_CBKT = []
skills_learned_IBKT = []
skills_learned_EBKT = []
skills_learned_TBKT = []
skills_learned_TS = []

for round_n in range (0, rounds): 
	task = Task()
	p = Person(round_n, task)
	# ~ print (p.mastery)
	count_skills_known_before = p.skills_known()
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
		# ~ print (p_T_BKT.start_b)
		#the true state belief, will be whether they have mastery or not
		True_State.belief.append(p.mastery)
		
		# ~ print (ts % n_timesteps)
		if (ts % 20 == 19):
			# ~ print ("TEACHING")
			p_C_BKT.teach_skill(b_C_BKT)
			p_I_BKT.teach_skill(b_I_BKT)
			p_E_BKT.teach_skill(b_E_BKT)
			p_T_BKT.teach_skill(b_T_BKT)
			True_State.teach_skill(True_State.mastery)
	
		# ~ print (p_C_BKT.skills_known())
	skills_learned_CBKT.append(p_C_BKT.skills_known() - count_skills_known_before)
	skills_learned_IBKT.append(p_I_BKT.skills_known() - count_skills_known_before)
	skills_learned_EBKT.append(p_E_BKT.skills_known() - count_skills_known_before)
	skills_learned_TBKT.append(p_T_BKT.skills_known() - count_skills_known_before)
	skills_learned_TS.append(True_State.skills_known() - count_skills_known_before)
	

av_CBKT = (sum(skills_learned_CBKT) / len(skills_learned_CBKT))
av_IBKT = (sum(skills_learned_IBKT) / len(skills_learned_IBKT))
av_EBKT = (sum(skills_learned_EBKT) / len(skills_learned_EBKT))
av_TBKT = (sum(skills_learned_TBKT) / len(skills_learned_TBKT))
av_Opt = (sum(skills_learned_TS) / len(skills_learned_TS))

write_file("Learned_TBKT", skills_learned_TBKT) 
write_file("Learned_CBKT", skills_learned_CBKT) 
write_file("Learned_IBKT", skills_learned_IBKT) 
write_file("Learned_EBKT", skills_learned_EBKT) 
write_file("Learned_Opt", skills_learned_TS) 

print (av_TBKT)
print (av_CBKT)
print (av_IBKT)
print (av_EBKT)
print (av_Opt)

def barplot_annotate_brackets(num1, num2, data, center, height, yerr=None, dh=.05, barh=.05, fs=None, maxasterix=None):
	""" 
	Annotate barplot with p-values.

	:param num1: number of left bar to put bracket over
	:param num2: number of right bar to put bracket over
	:param data: string to write or number for generating asterixes
	:param center: centers of all bars (like plt.bar() input)
	:param height: heights of all bars (like plt.bar() input)
	:param yerr: yerrs of all bars (like plt.bar() input)
	:param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
	:param barh: bar height in axes coordinates (0 to 1)
	:param fs: font size
	:param maxasterix: maximum number of asterixes to write (for very small p-values)
	"""

	if type(data) is str:
		text = data
	else:
		# * is p < 0.05
		# ** is p < 0.005
		# *** is p < 0.0005
		# etc.
		text = ''
		p = .05

		while data < p:
			text += '*'
			p /= 10.

			if maxasterix and len(text) == maxasterix:
				break

		if len(text) == 0:
			text = 'n. s.'

	lx, ly = center[num1], height[num1]
	rx, ry = center[num2], height[num2]

	if yerr:
		ly += yerr[num1]
		ry += yerr[num2]

	ax_y0, ax_y1 = plt.gca().get_ylim()
	dh *= (ax_y1 - ax_y0)
	barh *= (ax_y1 - ax_y0)

	y = max(ly, ry) + dh

	barx = [lx, lx, rx, rx]
	bary = [y, y+barh, y+barh, y]
	mid = ((lx+rx)/2, y+barh)

	plt.plot(barx, bary, c='black')

	kwargs = dict(ha='center', va='bottom')
	if fs is not None:
		kwargs['fontsize'] = fs

	plt.text(*mid, text, **kwargs)


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 15})

heights =  [av_TBKT,av_IBKT,av_EBKT,av_CBKT,av_Opt]
bars = np.arange(len(heights))
objects = ('T-BKT', 'I-BKT', 'E-BKT', 'C-BKT', 'Optimal')
y_pos = np.arange(len(objects))

# ~ plt.figure()
# ~ figure(figsize=(6, 6), dpi=80)
barlist = plt.bar(y_pos, heights, align='center')
barlist[0].set_color('#ffc61e')
barlist[1].set_color('#009ade')
barlist[2].set_color('#00cd6c')
barlist[3].set_color('#ff1f5b')
barlist[4].set_color('#757575')

plt.ylim(0, 2.5)
plt.xticks(y_pos, objects)
plt.ylabel('Number of Skills Learned')
# ~ plt.title('Average Number of Skills Demontrated')
barplot_annotate_brackets(0, 1, 'p < 0.05', bars, heights)
barplot_annotate_brackets(0, 2, 'p < 0.05', bars, heights, dh=.16)
barplot_annotate_brackets(0, 3, 'p < 0.05', bars, heights, dh=.11)
barplot_annotate_brackets(0, 4, 'p < 0.05', bars, heights)
plt.show()

