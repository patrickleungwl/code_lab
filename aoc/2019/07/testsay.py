# internal_pipe_say_my_name.py
import subprocess
import sys

proc = subprocess.Popen(["python", "say.py"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)


proc.stdin.write("matthew\n")
print(proc.stdout.read())
proc.stdin.write("matthew\n")
print(proc.stdout.read())
proc.stdin.write("exit\n")
proc.stdin.close()

while proc.returncode is None:
    proc.poll()

