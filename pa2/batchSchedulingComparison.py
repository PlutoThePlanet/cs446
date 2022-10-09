# batchSchedulingComparison.py
# Paige Mortensen
# CS 446 PA2 - compare, contrast, and simulate process management algorithms

# FCFS is an extremely straightforward algorithm and therefore easy to implement. The downsides of this algorithm is
# that if longer processes are first "in line", this may cause a long wait time. This long wait may also lead to fewer
# processes being able to run and, if our system crashes in this time, we may lose all the shorter processes that didn't
# get a chance to run.
# Shortest Job First is a more complicated program, but helps ensure that all short program are run as soon as possible,
# and as quickly as possible. Downsides may occur, however, if a longer process gets put off for too long (all other
# processes are shorter and therefore always run first). Similar to the FCFS algorithm, if our system crashes before our
# longer processes are run, we may lose these longer processes, or they may simply end up never being run.
# Using the Priority algorithm ensures that our most important processes are always run first; for example, we always
# want our system to boot before we allow the user to begin making requests. But, if we define a long or many long
# processes as having higher priority, we may have shorter processes stuck waiting for a long time. If they are
# important short processes we can define them as such, but this may be inconvenient for the user as it is possible for
# not as many processes to be completed in the same amount of time a longer process may take.


import sys
import copy


def avg_turnaround(process_completion_times, process_arrival_times):
    turnaround_times = []
    total = 0
    for elem in range(0, len(process_completion_times)):
        turnaround_time = process_completion_times[elem] - process_arrival_times[elem]          # calc turnaround
        turnaround_times += [turnaround_time]                                                   # add time to list
        total += turnaround_time                                                                # add to turnTotal
    avg_turn_time = total / len(turnaround_times)                                               # calc average
    return [turnaround_times, avg_turn_time]


def avg_wait(process_turnaround_times, process_burst_times):
    wait_total = 0
    for elem in range(0, len(process_turnaround_times)):
        wait_time = process_turnaround_times[elem] - process_burst_times[elem]      # take the difference
        wait_total += wait_time                                                     # add to total
    wait_avg = wait_total / (len(process_turnaround_times))                         # calc average
    return wait_avg


def first_come_first_served_sort(data):
    completion_list = []
    current_time = 0
    data.sort(key=lambda x: x[0])                       # sort by PID so edge case is set up
    data.sort(key=lambda x: x[1])                       # sort by arrival time
    for elem in range(0, len(data)):                    # find completion times
        completion = current_time + data[elem][2]       # completion = currentTime + burstTime
        completion_list += [completion]                 # add to list
        current_time += data[elem][2]                   # new current time
    return [data, completion_list]


def shortest_job_first_sort(data):
    pid_list = []
    exit_queue = []                         # basically a sorted 'data' list, w/ completion times added to each process
    current_time = 0
    data.sort(key=lambda x: x[0])           # sort by PID so edge case is set up
    data.sort(key=lambda x: x[1])           # sort by arrival time - active process should be at front
    queue = copy.deepcopy(data)             # deep copy so original data is maintained
    pid_list += [queue[0][0]]               # add first process to PID list

    while not queue == []:                                  # while there are still processes waiting to be run,
        if len(queue) == 1:
            pid_list += [queue[0][0]]                       # list final process
            current_time += queue[0][2]                     # update the final burst time
            queue[0].append(current_time)                   # track exit time of final process
            exit_queue.append(queue[0])                     # add final process to exit queue (to be returned)
            queue.pop(0)
        else:
            for j in range(0, len(queue)-1):                # check that all processes have remaining time
                if queue[j][2] <= 0:                        # if a process has reached 0 time remaining
                    pid_list += [queue[0][0]]               # list process when removed
                    queue[0].append(current_time)           # track exit time
                    exit_queue.append(queue[0])             # add entire process to exit queue (to be returned)
                    queue.pop(0)                            # remove from the queue (process finished).
            for index in range(1, len(queue)):              # iterate through the remaining waiting processes.
                if queue[index][2] < queue[0][2]:           # if the next process has a shorter burst than the current
                    if current_time == 0:                   # if this isn't the first process being swapped,
                        queue[0][2] -= queue[index][1]      # decrement the burst of active process by arrival of next
                        current_time += queue[index][1]     # update cur. time by arrival of next (that time had passed)
                    queue.insert(0, queue[index])           # place new active process at front
                    queue.pop(index+1)                      # remove process from old location
            queue[0][2] -= 1                                # decrement remaining time of active
            current_time += 1                               # increment current time

    for i in range(0, len(exit_queue)):           # for every process in exit_queue
        for j in range(0, len(data)):             # look through original 'data'
            if exit_queue[i][0] == data[j][0]:    # and find the process w/ matching PID
                exit_queue[i][2] = data[j][2]     # then restore the old burst time of the process
    return [pid_list, exit_queue]


def priority_sort(data):
    completion_list = []
    current_time = 0
    data.sort(key=lambda x: x[0])                     # sort by PID
    data.sort(key=lambda x: x[1])                     # sort by arrival time
    data.sort(key=lambda x: x[3])                     # sort by priority
    for elem in range(0, len(data)):                  # find completion times
        completion = current_time + data[elem][2]     # completion = currentTime + burstTime
        completion_list += [completion]               # add to list
        current_time += data[elem][2]                 # new current time
    return [data, completion_list]


def calculate_times(data_2d, pid_list, arrival_time_list, burst_time_list, priority_list, completion_list):
    for elem in range(0, 4):
        pid_list += [int(data_2d[elem][0])]                                 # update arrays - sorted
        arrival_time_list += [int(data_2d[elem][1])]
        burst_time_list += [int(data_2d[elem][2])]
        priority_list += [int(data_2d[elem][3])]
    turnaround_ret = avg_turnaround(completion_list, arrival_time_list)     # calculate times
    turnaround_list = turnaround_ret[0]
    avg_turnaround_time = turnaround_ret[1]
    wait = avg_wait(turnaround_list, burst_time_list)
    return [avg_turnaround_time, wait]


def main():
    sorting = {"FCFS", "ShortestFirst", "Priority"}
    pid_list = []
    arrival_time_list = []
    burst_time_list = []
    priority_list = []
    completion_time_list = []
    data_2d = []
    arg_list = []

    if len(sys.argv) != 3:                                                                  # check num of arguments
        arg_list += [sys.argv[0]]
        print("you did not enter the correct number of arguments")
        print("what is the name of your process file?")
        file = input()
        arg_list += [file]
        print("what sort type would you like to use?")
        sort = input()
        arg_list += [sort]
    elif len(sys.argv) == 3:
        arg_list += [sys.argv[0]]
        arg_list += [sys.argv[1]]
        arg_list += [sys.argv[2]]
    if not any(ele in arg_list for ele in sorting):                                         # did you provide a sort
        print("your process scheduling options are FCFS, ShortestFirst, or Priority")
        quit()
    try:                                                                                    # does the file exist
        open(arg_list[1], 'r')
    except OSError:
        print("your file doesn't exist")
        quit()
    else:                                                                                   # then parse the input
        with open(arg_list[1], 'r') as f:
            index = 0
            for line in f:
                pid, arrival_time, burst_time, priority = line.split(', ')
                data_list = [int(pid), int(arrival_time), int(burst_time), int(priority)]   # 2D array of all data
                data_2d.insert(index, data_list)
                index += 1

    if arg_list[2] == "FCFS":  # ###################################################### FCFS ###########################
        fcfs_ret = first_come_first_served_sort(data_2d)
        data_2d = fcfs_ret[0]
        completion_list = fcfs_ret[1]
        print("PID ORDER OF EXECUTION")
        for elem in range(0, len(data_2d)):
            print(data_2d[elem][0])
        time_ret = calculate_times(data_2d, pid_list, arrival_time_list, burst_time_list, priority_list, completion_list)
        avg_turnaround_time = time_ret[0]
        wait = time_ret[1]
        print("Average Process Turnaround Time: " + str(avg_turnaround_time))
        print("Average Process Wait Time: " + str(wait))
    elif arg_list[2] == "ShortestFirst":  # ########################################### ShortestFirst ##################
        sjf_ret = shortest_job_first_sort(data_2d)
        ret_pid_list = sjf_ret[0]
        ret_exit_data = sjf_ret[1]
        for elem in range(0, len(ret_exit_data)):                                    # update individual data lists
            pid_list += [ret_exit_data[elem][0]]
            arrival_time_list += [ret_exit_data[elem][1]]
            burst_time_list += [ret_exit_data[elem][2]]
            priority_list += [ret_exit_data[elem][3]]
            completion_time_list += [ret_exit_data[elem][4]]
        print("PID ORDER OF EXECUTION")
        for elem in range(0, len(ret_pid_list)):                                     # print process list
            print(ret_pid_list[elem])
        turnaround_ret = avg_turnaround(completion_time_list, arrival_time_list)     # calculate times
        turnaround_list = turnaround_ret[0]
        avg_turnaround_time = turnaround_ret[1]
        wait = avg_wait(turnaround_list, burst_time_list)
        print("Average Process Turnaround Time: " + str(avg_turnaround_time))        # print
        print("Average Process Wait Time: " + str(wait))
    elif arg_list[2] == "Priority":  # ################################################ Priority #######################
        prio_ret = priority_sort(data_2d)
        data_2d = prio_ret[0]
        completion_list = prio_ret[1]
        print("PID ORDER OF EXECUTION")
        for elem in range(0, len(data_2d)):
            print(data_2d[elem][0])
        time_ret = calculate_times(data_2d, pid_list, arrival_time_list, burst_time_list, priority_list, completion_list)
        avg_turnaround_time = time_ret[0]
        wait = time_ret[1]
        print("Average Process Turnaround Time: " + str(avg_turnaround_time))
        print("Average Process Wait Time: " + str(wait))


if __name__ == "__main__":
    main()
