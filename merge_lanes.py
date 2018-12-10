import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="File with QBiC codes.")
parser.add_argument("-pR1", "--patternR1", type=str, help="Pattern to find R1 of paired-seq.", default='_R1_')
parser.add_argument("-pR2", "--patternR2", type=str, help="Pattern to find R2 of paired-seq.", default='_R2_')

args = parser.parse_args()

with open(args.file, mode='r') as f:
    lines = f.readlines()

codes = [line.rstrip() for line in lines]

for sample in codes:
    subprocess.call("mkdir %s" % sample, shell=True, stdout=True)
    subprocess.Popen("mv %s* %s" % (sample, sample), shell=True, stdout=True)
    subprocess.Popen("find %s -name '*%s*.fastq.gz' -exec cat {} ';' > %s/%s_R1_.fastq.gz" % (sample, args.patternR1, sample, sample), shell=True, stdout=True)
    subprocess.Popen("find %s -name '*%s*.fastq.gz' -exec cat {} ';' > %s/%s_R2_.fastq.gz" % (sample, args.patternR2, sample, sample), shell=True, stdout=True)



