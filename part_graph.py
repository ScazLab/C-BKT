
from random import randint
from random import random

import math
import copy
import random
import numpy as np


import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 15})


figure(figsize=(6, 6), dpi=80)
plt.plot([0,1], [6,13], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [5,5], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [6,8], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [1,4], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [3,12], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [8,13], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [4,14], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [10,16], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [4,6], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [2,1], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [11,15], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [6,5], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [5,11], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [9,12], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [3,4], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [8,10], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [2,11], color='#ff1f5b', linewidth = 2, marker ="o")
plt.plot([0,1], [12,14], color='#ff1f5b', linewidth = 2, marker ="o")
# ~ plt.plot([1, 2, 3], marker=11)

plt.plot(1, 9)


# ~ plt.title('')
# ~ plt.xlabel('Year')
plt.ylabel('Pretest/Posttests Scores')
plt.show()


# ~ print (av_TBKT)
# ~ print (av_CBKT)
# ~ print (av_IBKT)
# ~ print (av_EBKT)
# ~ print (av_Opt)

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
	

heights =  [5.83, 9.67]
bars = np.arange(len(heights))
objects = ('Pre-Test', 'Post-Test')
y_pos = np.arange(len(objects))

plt.figure()
figure(figsize=(6, 6), dpi=80)
barlist = plt.bar(y_pos, heights, align='center')
barlist[0].set_color('#757575')
barlist[1].set_color('#ff1f5b')

plt.ylim(0, 12)
plt.xticks(y_pos, objects)
plt.ylabel('Number of Skills')
# ~ plt.title('Average Number of Skills Demontrated')
barplot_annotate_brackets(0, 1, 'p < 0.05', bars, heights)
plt.show()





# ~ fig.suptitle('Horizontally stacked subplots')
# ~ ax1.plot(x, y)
# ~ ax2.plot(x, -y)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams.update({'font.size': 10})

obs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,
1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1]

cbkt = [0.5,0.5,0.499,0.498,0.497,0.496,0.495,0.493,0.49,0.488,0.485,0.482,0.479,0.477,0.473,0.47,0.467,0.464,0.461,0.457,0.454,0.45,0.447,0.443,0.439,0.435,0.431,0.427,0.423,0.418,0.414,0.446,0.478,
0.51,0.543,0.576,0.61,0.644,0.679,0.714,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.75,0.765,0.78,0.795,0.81,0.825,0.84,0.855,0.87,0.885,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.84,0.78,
0.72,0.66,0.66,0.666,0.673,0.679,0.686,0.692,0.759,0.825,0.891,0.958,0.964,0.964,0.964,0.924,0.884,0.844,0.804,0.804,0.804,0.804,0.804,0.804,0.804,0.844,0.884,0.924,0.964,0.924,0.884,0.844,0.804,
0.763,0.723,0.683,0.643,0.603,0.563,0.563,0.563,0.563,0.563,0.603,0.643,0.683,0.683,0.683,0.683,0.723,0.763,0.804,0.844,0.844,0.844,0.844,0.967]

n_ts = []
for i in range (0, len(obs)):
	n_ts.append(i)
	
# ~ 
fig, (ax1, ax2) = plt.subplots(2)
ax1.set_ylim([-0.1, 1.1])
ax1.plot(n_ts, obs, color = '#757575', linewidth = 2)
# ~ ax1.set_title("Observation")
ax1.axes.xaxis.set_visible(False)

ax2.set_ylim([-0.1, 1.1])
# ~ figure(figsize=(6, 6), dpi=80)
ax2.plot(n_ts, cbkt, color = '#ff1f5b' , linewidth = 2, )
ax2.plot([53,53], [0,1], color = '#000000', linewidth = 1, linestyle='dashed')
ax2.plot([75,75], [0,1], color = '#000000', linewidth = 1, linestyle='dashed')
ax2.plot([129,129], [0,1], color = '#000000', linewidth = 1, linestyle='dashed')
# ~ ax2.set_title("C-BKT")
ax2.axes.xaxis.set_visible(True)
# ~ plt.rcParams["figure.figsize"] = (20,3)


plt.show()
