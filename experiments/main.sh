#!/usr/bin/env bash
# Wenchang Yang (wenchang@princeton.edu)
# Thu Nov 16 16:06:42 EST 2023
##SBATCH --nodes=1                # node count
##SBATCH --ntasks-per-node=1      # number of tasks per node
# 
#SBATCH --ntasks=1               # total number of tasks across all nodes = nodes x ntasks-per-node
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=16G         # memory per cpu-core (4G is default)
#SBATCH --time=24:00:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=all          # send email when job begins/ends/fails
#SBATCH --mail-user=wenchang@princeton.edu
# 
##SBATCH --array=1-100#%32        # job array with index values 1, 2, ...,; max job # is 32 if specified
##SBATCH --output=slurm-%A.%a.out # stdout file
##SBATCH --error=slurm-%A.%a.err  # stderr file
set -e #v
##env settings
#export PATH=/tigress/wenchang/miniconda3/bin:$PATH
#export PYTHONPATH=/tigress/wenchang/wython
#export PYTHONUNBUFFERED=TRUE # see https://stackoverflow.com/questions/230751/how-to-flush-output-of-print-function
#export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK #for multi-threaded job
#ii_job=$SLURM_ARRAY_TASK_ID #for job array

model=all
modeler=all
modelers_all="wenchang gvecchi gr7610 cw55 bosongz maofeng"
if [ $# -ge 1 ]; then
    model=$1 #the first arg as model
fi
if [ $# -ge 2 ]; then
    modeler=$2 #the second arg as modeler
fi

#python /tigress/wenchang/bin/make_html_exps.py model=all
#python /tigress/wenchang/bin/make_html_exps_accordion.py model=$model modeler=$modeler #use the accordion component from Bootstrap 5
#python /tigress/wenchang/bin/make_html_bs5.py
if [ $modeler == "all" ]; then
    for m in $modelers_all; do
        python make_html_exps_accordion.py model=$model modeler=$m #use the accordion component from Bootstrap 5
    done
else
    python make_html_exps_accordion.py model=$model modeler=$modeler #use the accordion component from Bootstrap 5
fi

#webpage of models
python make_html_models.py
