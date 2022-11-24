import math
import os

from script import convert_script as cs, download_script as ds, merge_script as ms
from research import sub_question_one as sq1

partition_size = 50
threads_merger = 10
threads_sq1 = 1
max_partition_merger = math.ceil(103883/partition_size) + 1
max_partition_sq1 = math.ceil(68980/partition_size) + 1

ds.download_all(os.getcwd())

# for partition in range(1, max_partition_merger):
#     ms.merge_goodreads(threads_merger, partition_size, partition, os.getcwd())
#
# cs.convert_data(os.getcwd())
#
# for partition in range(1, 2):
#     sq1.sub_question_one(threads_sq1, partition_size, partition, os.getcwd())
