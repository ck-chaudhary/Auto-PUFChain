import serial
import numpy as np
import scipy.io
from struct import pack,unpack
import sys
import time
## TESTING SCP
# %**************************************************************************
# % CHALLENGE AND RESPONSE SETTINGS OF PUF
# %**************************************************************************
nMeas=9 #No. of measurements/challenge
respSize=1 #In Bytes
chalSize=8 #In Bytes
N=chalSize*8 #Challange length in bits

nWord=np.int16(chalSize/8) #No. of 64-bit words
chalGen = -1 #1 if Challenge file is not available then generate it, -1 take challenge file with binary input from SCG, 0 if need to generate the complete CRPDB
nChal=2
#nChal = 32000
#f = open('FPGA_id.txt','r')
#BrNo = f.read()
# print BrNo
BrNo=46
# %**************************************************************************
# % CHALLENGE/ RESPONSE FILES
# %**************************************************************************
#iDir='/home/root/dataset/input/'
oDir='/output/'


respFile=oDir+'resp_APUF_{N}_meas_Br_{BrNo}_all.txt'.format(N=N,BrNo=BrNo)
respGFile=oDir+'respG_APUF_{N}_meas_Br_{BrNo}_all.txt'.format(N=N,BrNo=BrNo)
workspace=oDir+'workspace.txt'

def convertToBinMat(d_i,width):
        arrays=[]
        for e in d_i:
                b=np.binary_repr(e,width=width)
                arr=[int(x) for x in b[:]]
                arrays.append(arr)
        mat=np.matrix(arrays)
        return mat

def arrayToBinVec(D):
        n=len(D)        #returns length of the First Dimension
        m=len(D[1])     #returns length of the Second Dimension
        nBits=m*8
        B=np.zeros((n,nBits))
        for i in xrange(0,m-1):
                s=i*8
                e=(i+1)*8
                d_i=D[:,i]
                b_i=convertToBinMat(d_i,8)
                b_i=np.fliplr(b_i)
                B[:,s:e]=b_i
        return B
def emptyBuffer(ser,logFile):
        s=ser.inWaiting()
        if s:
                ser.read(size=s)

def test_and_clear(ser,logFile):        
        # Open serial port when not yet open        
        if ser.isOpen():
                pass
        else:
                ser.open()
        # Empty receive buffer
        emptyBuffer(ser,logFile)
        # write test command: A = Active ?
        val='A'
        logFile.write('Write_commands: Byte to be written: %s\n'%val)        
        wbs=ser.write(val)
        #print ('test_and_clear: waiting...\n')
        logFile.write('test_and_clear: waiting...\n')
        while ser.inWaiting():
                break
        logFile.write('test_and_clear: Ok.\n')
        #print ('test_and_clear: Ok.\n')

        #check test response: Y = 'Yes'
        test=True
        t=ser.read(size=1)
        logFile.write('test_and_clear: Ok. %s\n'%t)
        test=test and (t=='Y')  
        return test

def write_command(ser,logFile,ch):
        # % write test command: C
        logFile.write("Write_commands: Byte to be written: %s\n"%ch)
        ser.write(ch)

def write_challange(ser,logFile,chal,nWord):    
        # Test if system is active and responding
        if not test_and_clear(ser,logFile):
                test=False
                return test
        # % Empty serial buffer
        emptyBuffer(ser,logFile)

        logFile.write("write_challenge: writing...\n")
        # % Write challenge command C
        logFile.write("command issued is C\n")

        write_command(ser,logFile,'C')
        w=ser.write(pack('<B',nWord))
        #print "size of nWord=%s"%w

        # % chal(length(chal)) contains first challenge byte
        for e in chal:
                #d=np.uint8(chal[i])
                d=ser.write(pack('<B',e))
        test=True
        return test

def read_challange(ser,logFile,chal_size):
        # % Test if system is active and responding

        if not test_and_clear(ser,logFile):
                chal=-1
                return chal
        # % Empty serial buffer
        emptyBuffer(ser,logFile)
        if ser.inWaiting():
                emptyBuffer()
        # % write read_challenge command
        logFile.write("commands to write is V\n")
        write_command(ser,logFile,'V');
        logFile.write("read_challenge: reading...\n")
        while True:
                if ser.inWaiting():
                        t=ser.read(size=1)
                        if t=='B':
                                logFile.write("received challange %s\n"%t)
                                chal=ser.read(size=chal_size)
                                #Modified
                                c=[unpack('<B',e)[0] for e in chal]
                                #print "readed challange=%s\n"%c
                                break
        logFile.write("reading_challange DOne !!!!\n")
        #now exisiting loop
        #print "chal"
        #print chal
        #print "chal"
        return chal


def wait_puf(ser,logFile):
        # % test if system is active and responding
        if not test_and_clear(ser,logFile):
                test=False
                return test
        # % empty serial buffer
        emptyBuffer(ser,logFile)
        # % write wait PUF command and wait for finish
        test=False
        logFile.write("bytes to be written is W\n")
        ser.write('W')
        logFile.write("wait_puf: PUF is being evaluated...\n")
        while True:
                if ser.inWaiting():
                        poll=ser.read(size=1)
                        if poll=='F':
                                logFile.write("received response is %s\n"%poll)
                                test=True
                                break
                        else:
                                if poll=='E':
                                        logFile.write("received response is %s\n")
                                        emptyBuffer(ser,logFile)
                                        ser.write('W')
                                else:
                                        emptyBuffer()
                                        ser.write('W')
        logFile.write("wai_puf evaluation Done!!!!!!!!\n")
        logFile.write("Finished!\n")
        return test

def start_puf(ser,logFile,resp_size):
        # % test if system is active and responding 	      
        if not test_and_clear(ser,logFile):
                logFile.write("start_puf: conn. not active\n")
                print ('start_puf: conn. not active\n')
                r=-1
                return r
        # % empty serial buffer
        emptyBuffer(ser,logFile)
        # % write start PUF evaluation command
        write_command(ser,logFile,'S')
        # % Test response 'Q'
        logFile.write("start_puf: waiting for ack\n")
        while True:
                if ser.inWaiting():
                        t=ser.read(size=1)
                        if t=='Q':
                                logFile.write("received response is %s\n"%t)
                                break
                        else:
                                r=-1
                                logFile.write("start_puf: received wrong respons\n")
                                return r
        logFile.write("ack found !!!!!\n")
        # # %Empty serial buffer
        emptyBuffer(ser,logFile)
        # %Wait for response
        if not wait_puf(ser,logFile):
                logFile.write("start_puf: evaluation is finished an expected way\n")
                r=-1
                return r
        # % read responses bytes
        r=ser.read(size=resp_size)
        logFile.write('start_puf Done !!!!%s\n'%r)
        return r

def puf_eval(ser,logFile,c,chal_size,resp_size,nWord):  
        #Test if system is active and responding 

        if not test_and_clear(ser,logFile):             
                logFile.write("\npuf_eval: conn. is not active.\n")
                r=-1
                return r                
        #% Test challenge length
        if len(c)!=chal_size:           
                logFile.write("puf_eval: wrong challenge length.\n")
                r=-1
                return r        
        #test challenge byte values
        if np.amin(c)<0 or np.amax(c)>255:
                logFile.write("puf_eval: challenge values exceed byte range.\n")
                r=-1
                return r
        # send challenge bytes    

        write_challange(ser,logFile,c,nWord)
        # % test if written challenge is correct
        tc=read_challange(ser,logFile,chal_size)
        #print "tc"+str(tc)
        # % start PUF evaluation and get response.
        r=start_puf(ser,logFile,resp_size)

        #logFile.write("outside function.%s\n"%r)
        try:
                r=unpack('<B',r)
        except Exception,e:
                pass
        logFile.write("puf_eval Finished !!!!!!!!!!!!!!! and tc=%s and response=%s\n"%(tc,r))
        return r

def convert_to_64bit_string(chalArray):
        f_string=''
        for e in chalArray:
                f_string+=str(bin(e)[2:])
        return f_string
def convert_from_string(chalString):
        pass

#main program
if __name__=='__main__':
        logFile=open('logFile.txt','w')
        
        # print response_bin
        # print
        # response_file=open('R_A.txt'.format(nMeas=nMeas),'w')
        f_res=open('f_res.txt','w')
        serialPort = ''
        # serialPort = raw_input("Enter serial port: ")
        BrNo = sys.argv[1] # raw_input("Enter Board Number: ")
        chal_file = sys.argv[2] # raw_input("Enter Challenge Filename: ")
        serialPort='/dev/ttyUSB1'#    #/dev/tty.usbserial-00001014B'
        baudRate=19200
        timeout=1
        #Open the serial port
        ser=serial.Serial(serialPort,baudRate,timeout=1)
        #generate a random	
        if chalGen == -1:
                f = open(chal_file,'r')
                l1=[]
                nChal = 0
                for line in f:
			print(line)
                        nChal = nChal + 1
                        l =[]
                        challenge = ""
                        challenge = bin(int(line,2))[2:].zfill(64)
                        l.append(int(challenge[56:64],2))       #print int(challenge[56:64],2), challenge[56:64] 
                        l.insert(0,int(challenge[48:56],2))     #print int(challenge[48:56],2), challenge[48:56]
                        l.insert(0,int(challenge[40:48],2))     #print int(challenge[40:48],2), challenge[40:48]
                        l.insert(0,int(challenge[32:40],2))     # print int(challenge[32:40],2), challenge[32:40]   
                        l.insert(0,int(challenge[24:32],2))     # print int(challenge[24:32],2), challenge[24:32]
                        l.insert(0,int(challenge[16:24],2))     # print int(challenge[16:24],2), challenge[16:24]
                        l.insert(0,int(challenge[8:16],2))      # print int(challenge[8:16],2), challenge[8:16]
                        l.insert(0,int(challenge[0:8],2))       # print int(challenge[0:8],2), challenge[0:8]
                        l1.append(l)
                #print "array"
                #print l1
                chal = np.array(l1)
                #print nChal
                print chal

        # print chal
        # print len(chal)

        # %*********************************************************************
        # % PUF EVALUATION
        # %*********************************************************************
        resp=np.zeros((nChal,respSize,nMeas))   #Create response matrix
        resp=resp.astype(np.uint32)
        #PUF Evaluation
	start = time.clock()
        for i in range(len(chal)):
                for k in range(nMeas):
        		
                	#Send Challenge and Receive response
                	print "\n(%d,%d)"%(i,k)
                	resp[i,:,k]=puf_eval(ser,logFile,chal[i,:],chalSize,respSize,nWord)
                	print "Challenge =",
                        print "%s"%chal[i,:]
                        print "Response%s = %s"%(k+1,resp[i,:,k])
                	# resp[1,:,k]=puf_eval(ser,logFile,chal[1,:],chalSize,respSize,nWord)
                	#print "Challenge ="
                	#print "%s\n"%chal[0,:]
                	#print "Response%s = %s\n"%(k+1,resp[1,:,k])
                	#print "+"
                	#print len((resp[0]))
	end = time.clock()
	time_taken = end-start
        f_res.write("%s"%time_taken)

        R = []
        for _resp in resp:
                R.append(list(_resp[0]))
        # print
        # print type(R),len(R)
        print R


        #print "R: %s"%(R0)
        #print "R: %s"%(R1)
        resp_bin_list=[]
		
	#print "-------------------------------"
        for i in range(len(R)):
                _resp_bin_list = []
                for j in range(nMeas):
                        resp_bin = ""
                        resp_bin = bin(int(R[i][j]))[2:]#.zfill(4)
                        _resp_bin_list.append(resp_bin)
                resp_bin_list.append(_resp_bin_list)
        
        # print
	#print "-------------------------------"
        maj_resp = []
        for l in resp_bin_list:
                _maj_resp = ""
                for j in range(1):
                        bit = 0
                        for k in range(nMeas):
                                bit = bit + int(l[k][j])        
                        if bit>=(nMeas+1)/2:
                                _maj_resp = _maj_resp + "1";
                        else:
                                _maj_resp = _maj_resp + "0";
                maj_resp.append(_maj_resp)
        # print maj_resp



        for i in range(nMeas):
                k = i+1
                response_bin = open('a_puf_resp_Meas_{k}.txt'.format(k=k),'w')
                for j in range(len(resp_bin_list)):
                        response_bin.write("%s\n"%resp_bin_list[j][i])

        x = []
        for i in maj_resp:
                xi = []
                for j in i:
                        xi.append(int(j))
                x.append(xi)

        
        y=np.array([np.array(xi) for xi in x])
        # print y
        # print

        golden_array=open('a_puf_golden_{BrNo}.txt'.format(BrNo=BrNo),'w')
        for i in maj_resp:
                golden_array.write("%s\n"%i)
        golden_array.close()


        a = {}
        a['golden'] = y
        scipy.io.savemat('golden.mat',a)
        b = scipy.io.loadmat('golden.mat')
        print "----------Done----------"
        ser.close()


