#!/bin/bash +x

script_dir=`dirname $0`

echo $script_dir
                                                                                       
source $script_dir/bin/activate

python3 $script_dir/main.py

#source deactivate
