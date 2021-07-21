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
A = 1.0
pi = np.pi
phase_list = []
A_list = []
tp_num = 0
levi = 0
#tp_list =  np.arange(0.0,-30.0,-0.5)
tp_list =  np.arange(0.,-30.1,-0.1)
tp_list = np.round(tp_list, 2)
print(tp_list)
np.set_printoptions(precision=1)
for tp in tp_list:

    #filename ='/Users/shota/Documents/klo_lab/matlab/phase/20201105/no'+str(tp)+'.mat'
    filename ='C:/Users/108ga/Documents/laboratory/Documents/klo-lab/210713/OpNoref_7PP'+str(tp)+'.mat'
    #filename ='C:/Users/108ga/Documents/laboratory/Documents/klo-lab/210713/7LSGwNoref_'+str(tp)+'.mat'
    phase_0 = sio.loadmat(filename)
    p = phase_0['phix']
    p_l = np.zeros(10)
    A_l = np.zeros(10)

    #A_sin0 = phase_0['sin_A']   
    #A_l[1:8] = A_sin0.reshape(7)
    #A_l[0] = A_sin0[4]
    #A_l[8] = A_sin0[2]
    #A_l[9] = A_sin0[3]
    phase_list.append(p)

    #A_list.append(A_l)
   
        
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
    outdata[:,0] = np.reshape(amp_L[0] *A*np.sin(phase_list[tp_num][4][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][4][0]),outdata[:,0].shape)
    outdata[:,1] = np.reshape(amp_L[1] *A*np.sin(phase_list[tp_num][0][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][0][0]),outdata[:,0].shape)
    outdata[:,2] = np.reshape(amp_L[2] *A*np.sin(phase_list[tp_num][1][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][1][0]),outdata[:,0].shape)
    outdata[:,3] = np.reshape(amp_L[3] *A*np.sin(phase_list[tp_num][2][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][2][0]),outdata[:,0].shape)
    outdata[:,4] = np.reshape(amp_L[4] *A*np.sin(phase_list[tp_num][3][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][3][0]),outdata[:,0].shape)
    outdata[:,5] = np.reshape(amp_L[5] *A*np.sin(phase_list[tp_num][4][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][4][0]),outdata[:,0].shape)
    outdata[:,6] = np.reshape(amp_L[6] *A*np.sin(phase_list[tp_num][5][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][5][0]),outdata[:,0].shape)
    outdata[:,7] = np.reshape(amp_L[7] *A*np.sin(phase_list[tp_num][6][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][6][0]),outdata[:,0].shape)
    outdata[:,8] = np.reshape(amp_L[8] *A*np.sin(phase_list[tp_num][2][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][2][0]),outdata[:,0].shape)
    outdata[:,9] = np.reshape(amp_L[9] *A*np.sin(phase_list[tp_num][3][1])*np.sin(2 * np.pi * f * t-phase_list[tp_num][3][0]),outdata[:,0].shape)
    
    start_idx += frames
    if levi == 1 and tp_num != len(tp_list)-1:
        tp_num += 1
    else:
        if tp_num != 0 and levi == 0:
            tp_num -= 1
       
with sd.OutputStream(device=38, channels=16, callback=callback,
                              samplerate=fs,blocksize=0):
    
    while True:
        
        key = input()
        if key == '':
            if levi == 0:
                levi = 1
                print('UP')
            else:
                levi = 0
                print('DOWN')