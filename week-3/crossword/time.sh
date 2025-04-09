#! /bin/bash

if [ $# -lt 1 ]; then
  echo "Usage: $0 <ProgramPath>" 
  exit 1  
fi

program_path=$1
array=("$@")
subarray=("${array[@]:1}")
launch_program="$program_path ${subarray[@]}"

# Time is running starting from now
start=$(date +%s.%N)

# We execute the indicated program
$launch_program

# Time has finished
end=$(date +%s.%N)

# We eval the expression
echo "$end - $start" | bc


