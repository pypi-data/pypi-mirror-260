#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Parse the SQLite3 database from NVprof or Nsight and print a dictionary for every kernel.
"""

import sys
import os
import argparse
from tqdm import tqdm

from .db import DB
from .kernel import Kernel
from .nvvp import NVVP
from .nsight import Nsight
from collections import defaultdict
from cofutils import cofcsv

def parseArgs():
    parser = argparse.ArgumentParser(description="Parse SQLite3 DB from NVprof or Nsight.")
    parser.add_argument("--file", '-f', type=str, default=None, help="SQLite3 database.")
    parser.add_argument("--csv", '-c', type=str, default=None, help="dump kernel info into csv file")
    parser.add_argument("--merge", '-m', type=str, default=None, help="merge multiple stream results")
    parser.add_argument("--start", '-s', type=float, default=None, help="profile begin time(s)")
    parser.add_argument("--end", '-e', type=float, default=None, help="profile end time(s)")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        raise parser.error("No such file '{}'.".format(args.file))

    return args


def dbIsNvvp(db):
    cmd = "SELECT * FROM sqlite_master where type='table' AND name='StringTable'"
    result = db.select(cmd)
    return True if len(result) == 1 else False


def main():
    args = parseArgs()

    db = DB(args.file)

    prof_start = -1 if args.start is None else args.start*1e9
    prof_end = float('inf') if args.end is None else args.end*1e9

    nvvp = None
    if dbIsNvvp(db):
        nvvp = NVVP(db)
    else:
        nvvp = Nsight(db)

    kInfo = nvvp.getKernelInfo()
    if len(kInfo) == 0:
        print("Found 0 kernels. Exiting.", file=sys.stderr)
        db.close()
        sys.exit(0)
    else:
        print("Found {} kernels. Getting info for each kernel.".format(len(kInfo)), file=sys.stderr)

    nvvp.createMarkerTable()

    prevSeqId = -1
    prevSubSeqId = -1
    prevOp = "na"

    Kernel.profStart = nvvp.getProfileStart()

    if args.csv:
        table = cofcsv(args.csv)
    else:
        table = None

    if args.merge:
        merge_stream_list = [int(each) for each in args.merge.split(',')]
    else:
        merge_stream_list = None

    fwd_stream_time_dict = defaultdict(int)
    fwd_merge_stream_time_dict = defaultdict(list)
    bwd_stream_time_dict = defaultdict(int)
    bwd_merge_stream_time_dict = defaultdict(list)
    other_stream_time_dict = defaultdict(int)
    other_merge_stream_time_dict = defaultdict(list)

    stream_kernel_table = defaultdict(set)

    for i in tqdm(range(len(kInfo)), ascii=True):
        info = kInfo[i]
        k = Kernel()

        #Calculate/encode object ID
        nvvp.encode_object_id(info)

        #Set kernel info
        k.setKernelInfo(info)
        #Get and set marker and seqid info
        info = nvvp.getMarkerInfo(k.objId, k.kStartTime, k.kEndTime)
        k.setMarkerInfo(info)
        if k.kStartTime < prof_start or k.kEndTime > prof_end or k.device != 0:
            continue

        #Set direction (it uses seq id)
        k.setDirection()

        #Set op
        k.setOp()

        kernel_info = k.print()
        
        nvtx = kernel_info['op'][0] if len(kernel_info['op'])>0 else None
        if table:
            table.write({'stream': kernel_info['stream'], 'Name': kernel_info['kLongName'], 'time(ms)': kernel_info['kDuration']/float(1e6), 'start(s)': kernel_info['kStartTime']/float(1e9), 'end(s)': kernel_info['kEndTime']/float(1e9), 'nvtx': nvtx})
        
        stream_kernel_table[kernel_info['stream']].add(kernel_info['kShortName'])

        if nvtx is not None and 'forward' in nvtx:
            fwd_stream_time_dict[kernel_info['stream']] += kernel_info['kDuration']/float(1e6)
            if merge_stream_list and int(kernel_info['stream']) in merge_stream_list:
                fwd_merge_stream_time_dict[args.merge].append((kernel_info['kStartTime'], kernel_info['kEndTime']))
        elif nvtx is not None and  'backward' in nvtx:
            bwd_stream_time_dict[kernel_info['stream']] += kernel_info['kDuration']/float(1e6)
            if merge_stream_list and int(kernel_info['stream']) in merge_stream_list:
                bwd_merge_stream_time_dict[args.merge].append((kernel_info['kStartTime'], kernel_info['kEndTime']))
        else:
            other_stream_time_dict[kernel_info['stream']] += kernel_info['kDuration']/float(1e6)
            if merge_stream_list and int(kernel_info['stream']) in merge_stream_list:
                other_merge_stream_time_dict[args.merge].append((kernel_info['kStartTime'], kernel_info['kEndTime']))

    def merge_intervals(intervals):
        if not intervals:
            return []

        # 按区间的起始位置进行排序
        intervals.sort(key=lambda x: x[0])

        merged = [intervals[0]]

        for i in range(1, len(intervals)):
            current_interval = intervals[i]
            last_merged_interval = merged[-1]

            # 判断当前区间是否与上一个合并后的区间有交集
            if current_interval[0] <= last_merged_interval[1]:
                # 有交集，合并区间
                merged[-1] = (last_merged_interval[0], max(last_merged_interval[1], current_interval[1]))
            else:
                # 无交集，将当前区间加入结果
                merged.append(current_interval)

        return merged

    def print_dict_timecost(kernel_dict):
        sorted_keys = sorted(kernel_dict.keys())
        for key in sorted_keys:
            print(f"stream-{key}: {kernel_dict[key]} ms")
    def print_dict_name(kernel_dict):
        sorted_keys = sorted(kernel_dict.keys())
        for key in sorted_keys:
            print("="*10, f"short name of kernels in stream-{key}: ", "="*10)
            
            for name in kernel_dict[key]:
                if name:
                    print(name)
            if len(kernel_dict[key]) > 10:
                print("...")
            

    if args.merge:
        fwd_stream_time_merged = sum([end-start for start,end in merge_intervals(fwd_merge_stream_time_dict[args.merge])])
        bwd_stream_time_merged = sum([end-start for start,end in merge_intervals(bwd_merge_stream_time_dict[args.merge])])
        other_stream_time_merged = sum([end-start for start,end in merge_intervals(other_merge_stream_time_dict[args.merge])])
    print("="*10,"forward stage","="*10)
    print_dict_timecost(fwd_stream_time_dict)
    if args.merge:
        print("stream-", args.merge, ": ", fwd_stream_time_merged/float(1e6), "ms")
    print("="*10,"backward stage","="*10)
    print_dict_timecost(bwd_stream_time_dict)
    if args.merge:
        print("stream-", args.merge, ": ", bwd_stream_time_merged/float(1e6), "ms")
    print("="*10,"other stage","="*10)
    print_dict_timecost(other_stream_time_dict)
    if args.merge:
        print("stream-", args.merge, ": ", other_stream_time_merged/float(1e6), "ms")
    print_dict_name(stream_kernel_table)
    if table:
        cofcsv.save('.')
    db.close()


if __name__ == '__main__':
    main()
