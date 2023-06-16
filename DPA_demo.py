import csv
import numpy
import os
import sys
from des_cipher import des
from matplotlib import pyplot as plt
from bitstring import BitArray

CSV_FILES_PATH = "CSV_TRACES_LAB/"

## main
if __name__ == '__main__':
    
    traces = os.listdir(CSV_FILES_PATH)

    #
    # demonstrate a single power trace
    #

    t0 = traces[0]
    t0 = numpy.genfromtxt(CSV_FILES_PATH + t0, delimiter=",")
    plt.clf()	
    plt.plot(t0[:,0], t0[:,1], color='orange', alpha=0.75, label='Trace 0')
    plt.title('Power Trace 0 ')
    plt.xlabel('Time (s)')
    plt.ylabel('Current')
    plt.legend()
    plt.show()


    #
    # demo two traces
    # 
    t1 = traces[1]
    t1 = numpy.genfromtxt(CSV_FILES_PATH + t1, delimiter=",")

    plt.clf()	
    plt.plot(t0[:,0], t0[:,1], color='orange', alpha=0.5, label = 'Trace 0')
    plt.plot(t1[:,0], t1[:,1], color='blue', alpha=0.5, label='Trace 1')
    plt.title('Power Trace 0 & 1')
    plt.xlabel('Time (s)')
    plt.ylabel('Current')
    plt.legend()
    plt.show()

    #
    # show difference in power traces
    #

    plt.clf()	
    plt.plot(t0[:,0], t0[:,1], color='orange', alpha=0.5, label='Trace 0')
    plt.plot(t1[:,0], t1[:,1], color='blue', alpha=0.5, label='Trace 1')
    plt.plot(t0[:,0], t0[:,1] - t1[:,1], color='red', alpha=0.75, label='Difference')
    plt.title('Difference in Power Traces')
    plt.xlabel('Time (s)')
    plt.ylabel('Current')
    plt.legend()
    plt.show()

   
    #
    # compute an average power trace
    #
    print ('Averaging')

    avg = numpy.zeros(len(t0[:,1] ))
    for i in range(0,10):
        print (i)
        data = numpy.genfromtxt(CSV_FILES_PATH + traces[i], delimiter=",")
        avg += data[:,1]
    avg = avg / 10

    plt.clf()	
    for i in range(0,10):
        print (i)
        data = numpy.genfromtxt(CSV_FILES_PATH + traces[i], delimiter=",")
        plt.plot(data[:,0], data[:,1], alpha=0.25, label='Trace '+str(i) )
    plt.plot(t0[:,0], avg[:], color='red', alpha=0.75, label='Average')
    plt.title('Average Power Trace')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Power')
    plt.legend()
    plt.show()

    #
    # Compute two averages, even and odd
    #
    print ("Computing Even/Odd Averages")

    avg_odd = numpy.zeros( len(t0[:,1]))
    avg_even = numpy.zeros( len(t0[:,1]))

    for i in range(0,10):
        print (i)
        data = numpy.genfromtxt(CSV_FILES_PATH + traces[i], delimiter=",")
        if (i %2 ):
            print ('odd')
            avg_odd += data[:,1]
        else:
            avg_even += data[:,1]

    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.75, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.75, label='Even')
    plt.title('Average Power Traces')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Power')
    plt.legend()
    plt.show()

    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.25, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.25, label='Even')
    plt.plot(t0[:,0], avg_odd[:] - avg_even[:], color='orange', alpha=0.75)
    plt.title('Average Power Difference ')
    plt.xlabel('Time (s)')
    plt.ylabel('Average Power')
    plt.legend()
    plt.show()

    #
    # Inflated Trace 
    #
    print ('inflated trace')

    t0 = traces[0]
    t0 = numpy.genfromtxt(CSV_FILES_PATH + t0, delimiter=",")
    inflate_index = numpy.where( (t0[:,0] > 2.4E-7) & (t0[:,0] < 2.5E-7) )

    new_t0 = t0.copy()
    new_t0[inflate_index,1] *= 1.10

    plt.clf()	
    plt.plot(t0[:,0], t0[:,1], color='red', alpha=0.5, label='Origional')
    plt.plot(new_t0[:,0], new_t0[:,1], color='blue', alpha=0.5, label='Inflated')
    plt.title('Inflated Power Trace')
    plt.xlabel('Time')
    plt.ylabel('Current')
    plt.legend()
    plt.show()

    # 
    # Inflated equally across even and odd
    #
    print ('inflate equally')

    t0 = traces[0]
    t0 = numpy.genfromtxt(CSV_FILES_PATH + t0, delimiter=",")
    inflate_index = numpy.where( (t0[:,0] > 2.4E-7) & (t0[:,0] < 2.5E-7) )

    avg_odd = numpy.zeros( len(t0[:,1]))
    avg_even = numpy.zeros( len(t0[:,1]))

    for i in range(0,10):
        print (i)
        data = numpy.genfromtxt(CSV_FILES_PATH + traces[i], delimiter=",")

        if (i < 5 ):
            print ('artifically inflating first half')
            data[inflate_index,1] *= 1.10

        if (i % 2):
            print ('odd')
            avg_odd += data[:,1]
        else:
            avg_even += data[:,1]

    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.75, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.75, label='Even')
    plt.title('Average Power Traces')
    plt.xlabel('Time')
    plt.ylabel('Average Current')
    plt.legend()
    plt.show()

    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.25, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.25, label='Even')
    plt.plot(t0[:,0], avg_odd[:] - avg_even[:], color='orange', alpha=0.75, label='Difference')
    plt.title('Average Power Difference ')
    plt.xlabel('Time')
    plt.ylabel('Average Current')
    plt.legend()
    plt.show()

    # 
    # Now only inflate the odds
    #
    print ('inflating odds')

    t0 = traces[0]
    t0 = numpy.genfromtxt(CSV_FILES_PATH + t0, delimiter=",")
    inflate_index = numpy.where( (t0[:,0] > 2.4E-7) & (t0[:,0] < 2.5E-7) )
 
    avg_odd = numpy.zeros( len(t0[:,1]))
    avg_even = numpy.zeros( len(t0[:,1]))

    for i in range(0,10):
        print (i)
        data = numpy.genfromtxt(CSV_FILES_PATH + traces[i], delimiter=",")
        if (i %2 ):
            print ('artifically inflating only odds')
            data[inflate_index,1] *= 1.10

        if (i %2):
            print ('odd')
            avg_odd += data[:,1]
        else:
            avg_even += data[:,1]

    
    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.75, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.75, label='Even')
    plt.title('Average Power Traces')
    plt.xlabel('Time')
    plt.ylabel('Average Current')
    plt.legend()
    plt.show()

    plt.clf()	
    plt.plot(t0[:,0], avg_odd[:], color='red', alpha=0.25, label='Odd')
    plt.plot(t0[:,0], avg_even[:], color='blue', alpha=0.25, label='Even')
    plt.plot(t0[:,0], avg_odd[:] - avg_even[:], color='orange', alpha=0.75, label='Difference')
    plt.title('Average Power Difference ')
    plt.xlabel('Time')
    plt.ylabel('Average Current')
    plt.legend()
    plt.show()


