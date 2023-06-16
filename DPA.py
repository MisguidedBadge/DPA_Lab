import csv
import numpy
import os
import sys
from des_cipher import des
from matplotlib import pyplot as plt
from bitstring import BitArray

TRACES_CSV_PATH  = "CSV_TRACES_LAB/"

TRACE_CACHE = {}

'''
	Helper Functions you may use to create basic plots or save differential traces.
	Extend or modify as needed.
'''
def plot_trace(data, title="Trace"):
	plt.clf()	
	plt.title(title)
	plt.xlabel = "Time"
	plt.ylabel = "Current"
	plt.plot(data)
	plt.show()	
	return

'''
	Example for saving matplotlib plots without having to plot them. 
	Extend as needed.
'''
def save_diff_trace(data, title="Trace", path="figs/"):	
	plt.clf()	
	plt.title(title)
	plt.xlabel = "Time"
	plt.ylabel = "Current"
	plt.plot(data)
	plt.savefig(path + title + ".png",bbox_inches="tight")
	return

def DPA(b, s_block, guess, num_traces):
	'''

		ASSIGNMENT: Extend this Function or create your own to perform DPA.
			The goal is to recover the Subkey bits of the First DES SBox by analyzing 
			a set of traces.

		<int> b: Bit used to divide traces into two groups. - Will Always be 0 for this Lab Assignment.
		<int> s_block: the s_block associated with bit b before permutation. - Will Always be 0 for this Lab Assignment.
		<list> guess: 6-Bits of SBox to try.
		<int> num_traces: total amount of traces to perform differential analysis on. More Traces == More Time.
	'''
	# Key is unknown, hence we are performing DPA. Changing this line will not do anything.
	key = b'\x00\x00\x00\x00\x00\x00\x00\x00'	
	d = des(key)
	count = 0
    
	traces = os.listdir(TRACES_CSV_PATH)
    #two lists, one that records traces with a flipped bit, the other records traces without a flipped bit - JACK
	#flipped = []
	#not_flipped = []
    
	t0 = traces[0]
	t0 = numpy.genfromtxt(TRACES_CSV_PATH + t0, delimiter=",")    
	avg_flipped = numpy.zeros( len(t0[:,1]))
	avg_not_flipped = numpy.zeros( len(t0[:,1]))
	n_flip_cnt = 0
	flip_cnt = 0
	for t in traces:
		if t not in TRACE_CACHE.keys():
			TRACE_CACHE[t] = numpy.genfromtxt(TRACES_CSV_PATH + t, delimiter=",")
		data = TRACE_CACHE[t]
		
		# Gets Plaintext M from Filename as bytes
		t_m  = bytes.fromhex(t.split(".")[0])

		# Call First Round of DES, returns R0 & R1.
		# R1 is returning before Permutation and XOR op with LPT.
		R1, R0 = d.crypt(t_m, d.FIRST_ROUND, s_block=s_block, Ks=guess)
		'''
		 	ASSIGNMENT: Create a Selection Function to Extract the Subkey Bits of the First DES SBox
						Focus on the first-bit to find the first SBox subket.
		'''

		if R1[31] == R0[31]:
			#not_flipped+=[data]
			avg_not_flipped += data[:,1]
			n_flip_cnt += 1
		else:
			#flipped+=[data]
			avg_flipped += data[:,1]
			flip_cnt += 1
		count+=1    
		if count == num_traces:
			avg_flipped = avg_flipped / flip_cnt
			avg_not_flipped = avg_not_flipped / n_flip_cnt   
			#avg_flipped = numpy.mean(flipped, axis=0)
			#avg_not_flipped = numpy.mean(not_flipped, axis=0)    
			diff_of_traces = avg_flipped[:] - avg_not_flipped[:]
			#diff_of_traces = avg_flipped - avg_not_flipped
			save_diff_trace(diff_of_traces, title="{}".format(guess), path="traces")
            
			'''
				ASSIGNMENT: Once we reach the last trace, find the difference between 
					the two groups of trace averages found using your selection function. 
			'''			
			return

def main():
	print(os.getcwd())
	'''
		For subkey guess 0 < k < 64, perform DPA analysis on the first SBox in the first round of DES over b = 0.
	'''
	for i in range(0,64):
		guess = list(BitArray(int=i, length=8).bin)[2:]
		guess = [int(x) for x in guess]
		print(guess) # Guess is your 6-Bit Subkey. 2**6 possible Guesses.
		DPA(0, 0, guess, num_traces=60000) 
	

if __name__ == "__main__":
	# Program Entrypoint is main() func.
	main()
