#$ -S /bin/bash
#$ -o /home/el230/SNO+/ftbAnalysis/logs
#$ -e /home/el230/SNO+/ftbAnalysis/logs
#$ -q mps.q

source /mnt/lustre/epp_scratch/neutrino/rat/rat-5.0.3/env_rat-5.0.3.sh;
python /home/el230/SNO+/ftbAnalysis/time_angle_analysis.py
