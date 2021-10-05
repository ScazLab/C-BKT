#!/usr/bin/env python
import matplotlib.pyplot as plt 

belief = 0.50
updated_belief = 0.5
guess = 0.1
slip = 0.1
time_learn = 60
obs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# ~ obs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# ~ obs = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
obs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
hist = 10
ts = 0
traditional = []
traditional_every = []
history = []
average = []
history_average = []
end_bkt = []


	


def update_belief_right(sk, slip, guess):
	knows_notslipped = sk*(1-slip)
	notknows_guessed = (1-sk)*guess
	top = knows_notslipped
	bottom = knows_notslipped + notknows_guessed
	return top / bottom
	
def update_belief_wrong(sk, slip, guess, t):
	know_tried_slipped = sk*probability_attempted(t)*slip
	knows_nottried = sk*(1-probability_attempted(t))
	notknows_nottried = (1-sk)*(1-probability_attempted(t))
	notknows_tried_notguessed = (1-sk)*probability_attempted(t)*(1-guess) 
	top = know_tried_slipped + knows_nottried
	bottom = know_tried_slipped + knows_nottried + notknows_nottried + notknows_tried_notguessed 
	return top / bottom
	
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
	
	
def probability_attempted(t):
	if t > time_learn:
		return 1
	else:
		return float(t) / time_learn
	

	
for t in range (0, len(obs)):
	b = 0
	o = obs[t]
	for i in range (0, hist):
		b_ts = 0
		if (i == 0):
			if (o == 0):
				b_ts = update_belief_wrong(belief, slip, guess,t)
			else:
				b_ts = update_belief_right(belief, slip, guess)
			history.append(b_ts)
		elif (t - i) < 0:
			b_ts = belief
		else:
			b_ts = history[t - i]
		b += b_ts
	b = b / hist
	history_average.append(b)
	
history2 = []
for t in range (0, len(obs)):
	b = 0
	o = obs[t]
	for i in range (0, hist):
		b_ts = 0
		if (i == 0):
			if (o == 0):
				b_ts = update_belief_wrong_traditional(belief, slip, guess)
			else:
				b_ts = update_belief_right_traditional(belief, slip, guess)
			history2.append(b_ts)
		elif (t - i) < 0:
			b_ts = belief
		else:
			b_ts = history2[t - i]
		b += b_ts
	b = b / hist
	average.append(b)
	
for t in range(0, len(obs)):
	o = obs[t]
	if (o == 0):
		b_ts = update_belief_wrong_traditional(belief, slip, guess)
	else:
		b_ts = update_belief_right_traditional(belief, slip, guess)
	traditional.append(b_ts)
	if (t > 58):
		end_bkt.append(b_ts)
	else:
		end_bkt.append(0.5)

	
for t in range(0, len(obs)):
	o = obs[t]
	if (o == 0):
		updated_belief = update_belief_wrong_traditional(updated_belief, slip, guess)
	else:
		updated_belief = update_belief_right_traditional(updated_belief, slip, guess)
	traditional_every.append(updated_belief)
			
			
# ~ obs.append(obs[-1])
print (len(obs))
print (len(history))
print (len(history_average))
print (len(traditional))
print (len(traditional_every))

# ~ n_ts = len(obs)
n_ts = []
for i in range (0, len(obs)):
	n_ts.append(i)
	
	# ~ ax1 = plt.subplot(131)
# ~ ax1.scatter([1, 2], [3, 4])
# ~ ax1.set_xlim([0, 5])
# ~ ax1.set_ylim([0, 5])

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 10})

fig, (ax1, ax2, ax3, ax4, ax5, ax6, ax7) = plt.subplots(7)
# ~ fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=2.0)
# ~ fig.tight_layout()
# ~ fig.suptitle('Vertically stacked subplots')
# ~ ax1.set_title("observation")
ax1.set_ylim([-0.1, 1.1])
ax1.plot(n_ts, obs, color = '#f28522', linewidth = 2)
ax1.set_title("Observation")
ax1.axes.xaxis.set_visible(False)

ax2.set_ylim([-0.1, 1.1])
ax2.plot(n_ts, end_bkt, color = '#ffc61e' , linewidth = 2)
ax2.set_title("T-BKT")
ax2.axes.xaxis.set_visible(False)

ax3.set_ylim([-0.1, 1.1])
ax3.plot(n_ts, traditional, color = '#009ade', linewidth = 2)
ax3.set_title("I-BKT")
ax3.axes.xaxis.set_visible(False)

ax4.set_ylim([-0.1, 1.1])
ax4.plot(n_ts, traditional_every, color = '#00cd6c', linewidth = 2)
ax4.set_title("E-BKT")
ax4.axes.xaxis.set_visible(False)

ax5.set_ylim([-0.1, 1.1])
ax5.plot(n_ts, history, color = '#ff6c93', linewidth = 2)
ax5.set_title("C-BKT-AT")
ax5.axes.xaxis.set_visible(False)

ax6.set_ylim([-0.1, 1.1])
ax6.plot(n_ts, average, color = '#ff5280', linewidth = 2)
ax6.set_title("I-BKT-AV")
ax6.axes.xaxis.set_visible(False)

ax7.set_ylim([-0.1, 1.1])
ax7.plot(n_ts, history_average, color = '#ff1f5b', linewidth = 2)
ax7.set_title("C-BKT")
# ~ ax7.axes.xaxis.set_visible(False)

plt.show()


	

# ~ print (update_belief_right(0.5, 0.1, 0.1))
# ~ print (update_belief_wrong(0.5, 0.1, 0.1, 0.1))
# ~ print (update_belief_wrong(0.5, 0.1, 0.1, 0.4))
# ~ print (update_belief_wrong(0.5, 0.1, 0.1, 0.9))
# ~ print (update_belief_wrong(0.5, 0.1, 0.1, 1.0))
