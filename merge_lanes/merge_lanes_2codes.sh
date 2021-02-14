#!/bin/bash
# set the number of nodes and processes
#SBATCH --nodes=1

# set the number of tasks per node
#SBATCH --ntasks-per-node=20

# set memory per cpu
#SBATCH --mem=60GB

# set max wallclock time
#SBATCH --time=100:00:00

# set name of job
#SBATCH --job-name=merge_lane

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gisela.gabernet@gmail.com
file="codes.tsv"
while IFS=$'\t' read -r f1 f2
do
    # move files into folders
	mkdir $f1
        printf 'Making folder %s \n' "$f1"
	mv $f2*.fastq.gz $f1/
	mv $f2*.metadata $f1/
	find $f1 -type f -name '*_R1_*.fastq.gz' -print0 | sort -z | xargs -0 cat > "$f1"/"$f1"_R1.fastq.gz
    find $f1 -type f -name '*_R2_*.fastq.gz' -print0 | sort -z | xargs -0 cat > "$f1"/"$f1"_R2.fastq.gz
done <"$file"
