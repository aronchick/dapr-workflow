import os
import sys
import subprocess

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(str(nextline, "utf8"))
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise Exception(command, exitCode, output)

import step_1
import step_2
import step_3
execute('dapr run --app-id step_4 --app-protocol grpc --app-port 50051 -d ./components --log-level error python3 step_4.py')
exit()