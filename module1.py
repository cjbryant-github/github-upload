# Python practice code - Charlie Bryant - Feb. 2020 
# Modeled after Phoenix's Win32 C application to measure Win 10 NFSC client performance
# print("This line will be printed.")

# Open a filename, supplied as first argument, and returns a file handle in variable <fh>
# Invocation syntax:
#    module1.py <file-to-be-locked-and-read> <number of bytes to read between file locks>
#        Win 10 example:  pything module1.py z:\nfstest\systeminfo.txt 203
#        Linux example : python3 /home/user2/nfsmnt/readme.txt 203

# Code library info:
#    os used for changing current directory
#    timeit used for time calls to keep track of durations
#    sys used for ascii<->integer conversions
#    Conditional code library imports:
#    fcntl used for UNIX locking functions
#    msvcrt used for Windows locking functions


#from datetime import datetime
import timeit, os, sys

# OS specific libraries (i.e locking functions)
try:
    # Posix based file locking (Linux, Ubuntu, MacOS, etc.)
    import fcntl
    def lock_file(f):
        fcntl.lockf(f, fcntl.LOCK_EX)
    def unlock_file(f):
        fcntl.lockf(f, fcntl.LOCK_UN)
except ModuleNotFoundError:
    # Windows file locking
    import msvcrt
    def file_size(f):
        return os.path.getsize( os.path.realpath(f.name) )
    def lock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_RLCK, file_size(f))
    def unlock_file(f):
        msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, file_size(f))





#print("cwd is...")
#print(os.getcwd())

# Define path to the file we will be reading
#workpath="C:\\Users\\CharlesJBryant\\source\\repos\\PythonApplication1"
#os.chdir("C:\\Users\\CharlesJBryant\\source\\repos\\PythonApplication1")

#with open("systeminfo.txt", "rb+") as fh:
#with open(pathlib.Path('":" "/", "Users", "CharlesJBryant", "source", "repos", "PythonApplication1", "systeminfo.txt"), "rb") as fh:
#    bytes = fh.read(203)
#    while bytes:
#        # Do stuff with byte.
#        bytes = fh.read(203)
#        print(bytes)

#while bytes!=0:
# print the file to the screen
#print("Next 203-byte chunk of file ", fh.name, "are:")
#print(fh.read(203))
#print(bytes)


# Variables
#print("try another way...")
file_name = sys.argv[1]
# Convert parm2 value from ASCII to INTEGER
CHUNKSIZE = int(sys.argv[2])
#CHUNKSIZE = 203
##workpath="C:\\Users\\CharlesJBryant\\source\\repos\\PythonApplication1"
chunkn = 1
nolockchunkn = 1

# Change workding dir to path containing file to be read
##os.chdir(workpath)

# Start reading specified chunk size from file until EOF

print("")
print("*** Locking scenario: Opening file in R/O binary mode...")
print("")
print("*** Locking scenario: Now reading/printing file in chunks of specified size of", CHUNKSIZE, "byte(s).")
print("")
#print("time before READS is now:",datetime.now().time())
#starttime = datetime.now().time()
locking_start_time = timeit.default_timer()

##with open("systeminfo.txt", "rb") as fh:  (+ means R/W mode)
# Open file in R/O mode to match WIN32 CreateFile() call with GENERIC_READ
with open(file_name, "rb") as fh:
    
    bytes_read = fh.read(CHUNKSIZE)
    while bytes_read:
        lock_file(fh)
        #for b in bytes_read:            
        print("Reading chunk number:", chunkn," from file, chunk size =", CHUNKSIZE, "byte(s).")
        bytes_read = fh.read(CHUNKSIZE)
        unlock_file(fh)
        chunkn += 1
        #print(bytes_read)

print("")
#endtime = datetime.now().time()
locking_end_time = timeit.default_timer()


print ("")
print("Locking scenario: Now closing file...")
print("")
print("")

fh.close()


print("*** No locking scenario: Opening file in R/O binary mode...")
print("")
print("*** No locking scenario: Now reading/printing file in chunks of specified size of", CHUNKSIZE, "byte(s).")
print("")
#print("time before READS is now:",datetime.now().time())
#starttime = datetime.now().time()
nolocking_start_time = timeit.default_timer()

##with open("systeminfo.txt", "rb+") as fh: (+ means R/W mode)
with open(file_name, "rb") as fh:
    
    bytes_read = fh.read(CHUNKSIZE)
    while bytes_read:
        #lock_file(fh)
        #for b in bytes_read:            
        print("Reading chunk number:", nolockchunkn," from file, chunk size =", CHUNKSIZE, "byte(s).")
        bytes_read = fh.read(CHUNKSIZE)
        #unlock_file(fh)
        nolockchunkn += 1
        #print(bytes_read)

print("")
#endtime = datetime.now().time()
nolocking_end_time = timeit.default_timer()
print("Elapsed locking (file-level) time: {}".format(locking_end_time - locking_start_time),"seconds.")
print("Elapsed nolocking (file-level) time: {}".format(nolocking_end_time - nolocking_start_time),"seconds.")


print ("")
print("No locking scenario: Now closing file...")
print("")

fh.close()