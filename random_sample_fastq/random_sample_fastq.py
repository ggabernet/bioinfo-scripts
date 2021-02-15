## Original script by mojones https://raw.githubusercontent.com/mojones/random_scripts/14218de511d24b6450df4dc98ca15752626b6797/sample_fastq.py
## ported to python 3 and added option for paired-end files

import random
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("output", help="output FASTQ filename")
parser.add_argument("-f", "--fraction", type=float, help="fraction of reads to sample")
parser.add_argument("-n", "--number", type=int, help="number of reads to sample")
parser.add_argument("-s", "--sample", type=int, help="number of samples to take", default=1)
parser.add_argument("-R1", "--R1", type=str, help="R1 mate filename")
parser.add_argument("-R2", "--R2", type=str, help="R2 mate filename")
args = parser.parse_args()


if args.fraction and args.number:
   sys.exit("give either a fraction or a number, not both")


if not args.fraction and not args.number:
   sys.exit("you must give either a fraction or a number")

if not args.R1:
    sys.exit("you must provide at least a fastq file with the R1 argument")

if args.R2:
    print("sampling paired-end reads...")
    output_files_R2 = []
else:
    print("sampling single-end reads...")


print("counting records....")
with open(args.R1) as input:
    num_lines = sum([1 for line in input])
total_records = int(num_lines / 4)


if args.fraction:
    args.number = int(total_records * args.fraction)


print("sampling " + str(args.number) + " out of " + str(total_records) + " records")


output_files = []
output_sequence_sets = []
for i in range(args.sample):
    output_files.append(open(args.output + "_R1." + str(i) + ".fastq", "w"))
    output_sequence_sets.append(set(random.sample(range(total_records + 1), args.number)))
    if args.R2:
        output_files_R2.append(open(args.output + "_R2." + str(i) + ".fastq", "w"))

record_number = 0
with open(args.R1, "r+") as input:
    for line1 in input:
        line2 = next(input)
        line3 = next(input)
        line4 = next(input)
        for i, output in enumerate(output_files):
            if record_number in output_sequence_sets[i]:
                    output.write(line1)
                    output.write(line2)
                    output.write(line3)
                    output.write(line4)
        record_number += 1
        if record_number % 100000 == 0:
            print("R1 file " + str((record_number / total_records) * 100)  + " % done")

if args.R2:
    record_number = 0
    with open(args.R2, "r+") as input:
            for line1 in input:
                line2 = next(input)
                line3 = next(input)
                line4 = next(input)
                for i, output in enumerate(output_files_R2):
                    if record_number in output_sequence_sets[i]:
                            output.write(line1)
                            output.write(line2)
                            output.write(line3)
                            output.write(line4)
                record_number += 1
                if record_number % 100000 == 0:
                    print("R2 file " + str((record_number / total_records) * 100)  + " % done")

for output in output_files:
    output.close()

if args.R2:
    for output in output_files_R2:
        output.close()
print("done!")