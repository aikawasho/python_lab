#!/usr/bin/env python3
"""Play a sine signal."""
import argparse
import sys
import json
import numpy as np
import sounddevice as sd
import scipy.io as sio

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'frequency', nargs='?', metavar='FREQUENCY', type=float, default=500,
    help='frequency in Hz (default: %(default)s)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-a', '--amplitude', type=float, default=0.2,
    help='amplitude (default: %(default)s)')
args = parser.parse_args(remaining)

start_idx = 0
f = 40000
fs = 192000
A = 1.5
pi = np.pi
phase_list = []
A_list = []
tp_num = 0
levi = 0
LS_on  = 0
#tp_list =  np.arange(-24.0,0.0,0.1)
tp_list1 =  np.arange(-23.3,-18.5,0.1)
tp_list1 = np.insert(tp_list1,0,-100)
#tp_list1 = np.append(tp_list1,-21.01)
tp_list2 =  np.arange(-18.5,0.0,0.1)
tp_list = np.concatenate([tp_list1,tp_list2])
tp_list = np.append(tp_list,100)

tp_list = np.round(tp_list, 2)
print(tp_list)
np.set_printoptions(precision=1)

for tp in tp_list:
    p_l = np.zeros(12)
    A_l = np.zeros(12)
    if -24 < tp <= -18.5:

        if tp == -21.01:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210726/20LSGBottle123468-25-21.0.mat' 
        else:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210726/30LSGBottle123468-25'+str(tp)+'.mat'

        phase_0 = sio.loadmat(filename)
        A_l0 = phase_0['sin_A'].reshape(7)
        p_l0 = phase_0['phix'].reshape(7)

        #1,2段目-1
        p_l[0] = p_l0[0]
        A_l[0] = A_l0[0]
        #1,2段目-2
        p_l[1] = p_l0[0]+np.pi
        A_l[1] = A_l0[0]  
        #3段目-1
        p_l[2] = p_l0[1]
        A_l[2] = A_l0[1]
        #3段目-2
        p_l[8] = p_l0[1]+np.pi
        A_l[8] = A_l0[1]
        #4段目-1
        p_l[3] = p_l0[2]
        A_l[3] = A_l0[2]        
        #4段目-2
        p_l[9] = p_l0[2]+np.pi
        A_l[9] = A_l0[2]  
        #6段目-1
        p_l[5] = p_l0[3]
        A_l[5] = A_l0[3]   
        #6段目-2
        p_l[10] = p_l0[3]+np.pi
        A_l[10] = A_l0[3]  
        #8段目-1
        p_l[7] = p_l0[4]
        A_l[7] = A_l0[4]   
        #8段目-2
        p_l[11] = p_l0[4]+np.pi
        A_l[11] = A_l0[4]  
        A_list.append(A_l)
        phase_list.append(p_l)
    elif  tp == -24 :
        print('optimization')
        if tp == -21.01:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210726/op2tbottle123468-25-21.0.mat' 
        else:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210713/op2tbottle123468-25'+str(tp)+'.mat'

        phase_0 = sio.loadmat(filename)
        p = phase_0['phix']
         #1,2段目-1
        p_l[0] = p[0][0]
        A_l[0] = abs(1.5*np.sin(p[0][1]))
        #1,2段目-2
        p_l[1] = p[0][0]+np.pi
        A_l[1] = abs(1.5*np.sin(p[0][1])) 
        #3段目-1
        p_l[2] = p[1][0]
        A_l[2] = abs(1.5*np.sin(p[1][1]))
        #3段目-2
        p_l[8] = p[1][0]+np.pi
        A_l[8] = abs(1.5*np.sin(p[1][1]))
        #4段目-1
        p_l[3] = p[2][0]
        A_l[3] = abs(1.5*np.sin(p[2][1]))       
        #4段目-2
        p_l[9] = p[2][0]+np.pi
        A_l[9] = abs(1.5*np.sin(p[2][1]))
        #6段目-1
        p_l[5] = p[4][0]
        A_l[5] = abs(1.5*np.sin(p[4][1]))   
        #6段目-2
        p_l[10] = p[4][0]+np.pi
        A_l[10] = abs(1.5*np.sin(p[4][1]))  
        #8段目-1
        p_l[7] = p[6][0]
        A_l[7] = abs(1.5*np.sin(p[6][1]))   
        #8段目-2
        p_l[11] = p[6][0]
        A_l[11] = abs(1.5*np.sin(p[6][1]))  
        A_list.append(A_l)
        phase_list.append(p_l)

        A_list.append(A_l)
        phase_list.append(p_l)
        
    elif tp == 100:

        A_list.append(np.ones(12))
        phase_list.append(np.zeros(12))

               
    else:
        if tp == -100:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210713/7LSGw-25_-21.0.mat'
        elif tp == -18.5:
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210726/7LSGw-25_'+str(tp)+'.mat'
        else:
          
            filename ='/Users/shota/Documents/klo-lab/matlab/phase/210713/7LSGw-25_'+str(tp)+'.mat'
        phase_0 = sio.loadmat(filename)
        p = phase_0['phix']
        A_l[1:8] = phase_0['sin_A'].reshape(7)
        p_l[1:8] = phase_0['phix'].reshape(7)
        p_l[0] = phase_0['phix'][0]
        A_l[0] = phase_0['sin_A'][0]
        A_l[8] = phase_0['sin_A'][1]
        p_l[8] = phase_0['phix'][1]
        A_l[9] = phase_0['sin_A'][2]
        p_l[9] = phase_0['phix'][2]
        A_l[10] = phase_0['sin_A'][4]
        p_l[10] =phase_0['phix'][4]
        A_l[11] = phase_0['sin_A'][6]
        p_l[11] = phase_0['phix'][6]
        A_list.append(A_l)
        phase_list.append(p_l)

    #A_list.append(A_l)
       #filename ='C:/Users/108ga/Documents/laboratory/Documents/klo-lab/210713/7LSGwNoref_'+str(tp)+'.mat'
        
with open('amp_list.json') as g:
    df = json.load(g)  
    
amp_L = df["amp"]  


def callback(outdata, frames, time, status):
   # if status:
    #    print(status, file=sys.stderr)
    global start_idx
    global phase_list
    global tp_num
    global f
    t = (start_idx + np.arange(frames)) / fs
    t = t.reshape(-1, 1)
    outdata[:,:] = 0
    outdata[:,0] = np.reshape(amp_L[0] *A_list[tp_num][0]*np.sin(2 * np.pi * f * t-phase_list[tp_num][0]),outdata[:,0].shape)
    outdata[:,1] = np.reshape(amp_L[1] *A_list[tp_num][1]*np.sin(2 * np.pi * f * t-phase_list[tp_num][1]),outdata[:,0].shape)
    outdata[:,2] = np.reshape(amp_L[2] *A_list[tp_num][2]*np.sin(2 * np.pi * f * t-phase_list[tp_num][2]),outdata[:,0].shape)
    outdata[:,3] = np.reshape(amp_L[3] *A_list[tp_num][3]*np.sin(2 * np.pi * f * t-phase_list[tp_num][3]),outdata[:,0].shape)
    outdata[:,4] = np.reshape(amp_L[4] *A_list[tp_num][4]*np.sin(2 * np.pi * f * t-phase_list[tp_num][4]),outdata[:,0].shape)
    outdata[:,5] = np.reshape(amp_L[5] *A_list[tp_num][5]*np.sin(2 * np.pi * f * t-phase_list[tp_num][5]),outdata[:,0].shape)
    outdata[:,6] = np.reshape(amp_L[6] *A_list[tp_num][6]*np.sin(2 * np.pi * f * t-phase_list[tp_num][6]),outdata[:,0].shape)
    outdata[:,7] = np.reshape(amp_L[7] *A_list[tp_num][7]*np.sin(2 * np.pi * f * t-phase_list[tp_num][7]),outdata[:,0].shape)
    outdata[:,8] = np.reshape(amp_L[8] *A_list[tp_num][8]*np.sin(2 * np.pi * f * t-phase_list[tp_num][8]),outdata[:,0].shape)
    outdata[:,9] = np.reshape(amp_L[9]*A_list[tp_num][9]*np.sin(2 * np.pi * f * t-phase_list[tp_num][9]),outdata[:,0].shape) 
    outdata[:,10] = np.reshape(amp_L[10] *A_list[tp_num][10]*np.sin(2 * np.pi * f * t-phase_list[tp_num][10]),outdata[:,0].shape)
    outdata[:,11] = np.reshape(amp_L[11]*A_list[tp_num][11]*np.sin(2 * np.pi * f * t-phase_list[tp_num][11]),outdata[:,0].shape)   
    
    
    start_idx += frames

       
with sd.OutputStream(device=2, channels=16, callback=callback,
                              samplerate=fs,blocksize=0):
    a = 1
    while True:
        print(tp_list[tp_num])
        
        key = input()
        if key == '':
            if tp_num == len(tp_list)-1:
                tp_num = len(tp_list)-1
                #a = -1
                #tp_num += a
            elif tp_num == 0:
                a = 1
                tp_num += a
            else:
                tp_num += a