import signal
TIMEOUT = 5 # number of seconds your want for timeout
'''
def interrupted(signum, frame):
    "called when read times out"
    print 'interrupted!'
signal.signal(signal.SIGALRM, interrupted)
'''
def input(s):
    try:
            print s
            foo = raw_input()
            return foo
    except:
            # timeout
            return 

# set alarm
signal.alarm(TIMEOUT)
s = input("please inpout the string:")
# disable the alarm after success
signal.alarm(0)
print 'You typed', s

def raw_input_with_timeout(s, t):
	input_content = 
	#set alarm
	signal.alarm(TIMEOUT)
	input_content = input(s)
	signal.alarm(0)
	return 


