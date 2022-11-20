import math

import download_script as ds
import merge_script as ms

threads = 10
partition_size = 50
max_partition = math.ceil(103883/partition_size) + 1

# Initialize the folders and files & Download the data
ds.download_all()

# Merge the data into 1 coherent set
# First parameter: the amount of threads, 10-50 recommended, >100 discouraged
# Second parameter: the partition to be processed, 208 partitions of 500 books
for partition in range(1, max_partition):
    ms.merge_goodreads(threads, partition_size, partition)
