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
codes = [line.split("\t") for line in codes]

for sample in codes:
    p1 = subprocess.call("mkdir %s" % sample[0], shell=True, stdout=True)
    p1.communicate()
    p2 = subprocess.Popen("mv %s*.fastq.gz %s" % (sample[0], sample[1]), shell=True, stdout=True)
    p2.communicate()
    p3 = subprocess.Popen("mv %s* %s" % (sample[1], sample[0]), shell=True, stdout=True)
    p3.communicate()
    p4 = subprocess.Popen("find %s -type f -name '*%s*.fastq.gz' -print0 | sort -z | xargs -0 cat > %s/%s_R1.fastq.gz" % (sample[0], args.patternR1, sample[0], sample[0]), shell=True, stdout=True)
    p4.communicate()
    p5 = subprocess.Popen("find %s -type f -name '*%s*.fastq.gz' -print0 | sort -z | xargs -0 cat > %s/%s_R2.fastq.gz" % (sample[0], args.patternR2, sample[0], sample[0]), shell=True, stdout=True)
    p5.communicate()


