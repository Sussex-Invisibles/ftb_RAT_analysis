#$ -S /bin/bash
#$ -o /home/el230/SNO+/ftbAnalysis/stability/logs
#$ -e /home/el230/SNO+/ftbAnalysis/stability/logs
#$ -q mps.q

source /mnt/lustre/epp_scratch/neutrino/rat/rat-5.0.3/env_rat-5.0.3.sh;
source /home/el230/SNO+/ftbAnalysis/env.sh;

python /home/el230/SNO+/ftbAnalysis/stability/stability_analysis.py
