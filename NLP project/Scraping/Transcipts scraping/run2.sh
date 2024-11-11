#!/bin/bash

# Define the number of runs
total_runs=20

# Define the initial argument value
arg_value=0

# Loop through the runs
for (( i=1; i<=$total_runs; i++ ))
do
    # Run the Python script with the current argument value
    nohup python3 main.py -n $arg_value &
    
    # Capture the PID of the last background process
    pid=$!
    
    # Wait for the process to finish
    wait $pid
    
    # Kill the process
    kill $pid
    
    # Increment the argument value for the next run
    ((arg_value+=1000))
    
    # Pause for 1 minute
    sleep 60
done

