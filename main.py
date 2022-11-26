import math
import os

from script import convert_script as cs
from script import download_script as ds
from script import merge_script_child as msc
from script import merge_script_ya as msy
from research import sub_question_one as sq1

partition_size = 50
threads_merger = 10
threads_sq1 = 1
max_partition_merger_child = math.ceil(103883/partition_size) + 1
max_partition_merger_ya = math.ceil(55555/partition_size) + 1
max_partition_sq1 = math.ceil(90656/partition_size) + 1

ds.download_all(os.getcwd())

# for partition in range(1, max_partition_merger_child):
#     msc.merge_goodreads(threads_merger, partition_size, partition, os.getcwd())

# for partition in range(1, max_partition_merger_ya):
#     msy.merge_goodreads(threads_merger, partition_size, partition, os.getcwd())

# cs.convert_data(os.getcwd())

for partition in range(1, 3):
    sq1.sub_question_one(threads_sq1, partition_size, partition, os.getcwd())
