# -*- coding: utf-8 -*-
import collections.abc
import datetime
from time import sleep, time

format_duration1 = lambda x:(datetime.datetime.utcfromtimestamp(x) + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
format_duration2 = lambda x:"%02d:%02d:%02d" % (x // 3600, (x % 3600) // 60, x % 60)

def progbar(ls):
    """
    监控任务进度
    :param ls: 可遍历对象
    """
    if isinstance(ls, collections.abc.Iterator):
        ls = [l for l in ls]#解决迭代对象
    len_ls=len(ls)
    decpla=len(str(len_ls))
    start_time=time()
    i=0
    for l in ls:
        if i != 0:
            already_use_time = (time()-start_time) or 0.000000001#已使用时间
            remain_tasks=len_ls-i#剩余任务
            estimate_remain_time=already_use_time/i*remain_tasks#预估剩余时间
        else:
            i += 1
            yield l
            continue
        print("\033[92m"+
              f'总任务数：{len_ls}，'
              f'当前已完成任务数：{i}，'
              f'剩余任务数{remain_tasks}，'
              f'进度：{round(i*100/len_ls,decpla)}%，'
              f'已用时间：{format_duration2(already_use_time)}，'
              f'预估剩余时间：{format_duration2(estimate_remain_time)}，'
              f'速度：{save_speed_decimal(i/already_use_time)}条/秒，'
              f'当前时间：{format_duration1(time())}，'
              f'预估完成时间：{format_duration1(time()+estimate_remain_time)}'
              +"\033[0m")
        i+=1
        yield l
    already_use_time = time() - start_time  # 已使用时间
    print("\033[92m" +
          f'总任务数：{len_ls}，'
          f'当前已完成任务数：{i}，'
          f'剩余任务数{remain_tasks}，'
          f'进度：{round(i * 100 / len_ls, decpla)}%，'
          f'已用时间：{format_duration2(already_use_time)}，'
          f'预估剩余时间：{format_duration2(estimate_remain_time)}，'
          f'速度：{save_speed_decimal(i/already_use_time)}条/秒，'
          f'当前时间：{format_duration1(time())}，'
          f'预估完成时间：{format_duration1(time() + estimate_remain_time)}'
          + "\033[0m")
    print(f'\033[92m任务已完成，总任务数：{len_ls}，总用时：{format_duration2(already_use_time)}，平均速度：{round(i/already_use_time,2)}条/秒\033[0m')

#保留速度小数位
def save_speed_decimal(speed):
    if speed < 0.0001:return "{:.7f}".format(speed)
    i = 0
    for n in str(speed).replace('.', ''):
        if n != '0':return round(speed, i + 2)
        i += 1