#! /bin/bash

if [ $# -lt 1 ]; then
  echo "Usage: $0 <ProgramPath> [Arguments1, Argument2, ...]" 
  exit 1  
fi

# Program path and its arguments
array=("$@")

# Time is running starting from now
start=$(date +%s.%N)

# We execute the specified program with its arguments 
${array[@]}

# Time has finished
end=$(date +%s.%N)

# We eval the expression
calc_output=$(echo "$end - $start" | bc)

echo $calc_output


