import math
import os

import download_script as ds
import merge_script as ms
import convert_script as cs
import research.sub_question_one as sq1

threads = 10
partition_size = 10
max_partition_merger = math.ceil(103883/partition_size) + 1
max_partition_sq1 = math.ceil(68980/partition_size) + 1

# Initialize the folders and files & Download the data
# ds.download_all()

# Next partition: 1476
# Merge the data into 1 coherent set
# First parameter: the amount of threads, 10-50 recommended, >100 discouraged
# Second parameter: the partition to be processed, 2080 partitions of 50 books
# for partition in range(1, max_partition_merger):
#     ms.merge_goodreads(threads, partition_size, partition)

cs.convert_data()

for partition in range(1, 2):
    sq1.sub_question_one(threads, partition_size, partition, os.getcwd())
