#!/usr/bin/env python

from __future__ import print_function
import multiprocessing


def run(amount_process, function, parameters):
    pool = multiprocessing.Pool(processes=amount_process)
    results = []
    for x in pool.imap(function, parameters):
        results.append(x)
    return results

"""
import signal
import Queue
import sys


# based on code from Bryce Boe, available at: bryceboe.com/2010/08/26/python-multiprocessing-and-keyboardinterrupt/
def _manual_function(job_queue, result_queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while not job_queue.empty():  # PROCESSES ARE FINISHING WITHOUT ENDING THE OTHER JOBS
        try:
            job = job_queue.get(block=False)
            # print(job, result_queue.qsize(), job_queue.qsize())
            result = job[0](job[1])
            result_queue.put(result)
        except Queue.Empty:
            pass
    # print(os.getpid(), "going home", job_queue.empty()) ## <<------------------- JOBS ENDING BEFORE


def run2(amount_process, function, parameters):
#    Returns the execution of a function from a given set of parameters.
    
#    Args:
#        amount_process (int): the amount of processes.
#        function (func): the function.
#        parameters (list): the list of arguments for the function.
    job_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue(len(parameters))
    for i in parameters:
        job_queue.put((function, i))
    workers = []
    for i in range(amount_process):
        tmp = multiprocessing.Process(target=_manual_function,
                                      args=(job_queue, result_queue))
        tmp.start()
        workers.append(tmp)
    try:
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        print("Stopped from command", file=sys.stderr)
        for worker in workers:
            worker.terminate()
            worker.join()
    result = []
    while not result_queue.empty():
        result.append(result_queue.get(block=False))
    return result
"""
