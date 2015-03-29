# Prcocess and Thread 


### Process

 1. All the runnable software on the computer, sometimes including the operating system, is organized into a number of **sequential processes**, or just processes for short. **A process is just an instance of an executing program**.
 2. Processes must not be programmed with built-in assumptions about timing.
 3. The key idea here is that a process is an activity of some kind. It has a program, input, output, and a state. A single processor may be shared among several processes, with some scheduling algorithm being used to determine when to stop work on one process and service a different one.
 
### Thread

 4. **why need threads?**
    1. threads we add a new element: the ability for the parallel entities to share an address space and all of its data among themselves. This ability is essential for certain applications, which is why having multiple processes (with their separate address spaces) will not work.
    2. threads are lighter weight than processes, they are easier (i.e., faster) to create and destroy than processes.
    3. threads yield no performance gain when all of them are CPU bound, but when there is substantial computing and also substantial I/O, having threads allows these activi- ties to overlap, thus speeding up the application.(only one cpu)
    4. threads are useful on systems with multiple CPUs, where real parallelism is possible.

 5. Prcocess it is a way to group related resources together. A process has an address space containing program text and data, as well as other resources. 

 6. Thread has a program counter that keeps track of which instruc- tion to execute next. It has registers, which hold its current working variables. It has a stack, which contains the execution history, with one frame for each procedure called but not yet returned from. Although a thread must execute in some process, the thread and its process are different concepts and can be treated sepa- rately.

 7. Processes are used to group resources together; threads are the entities scheduled for execution on the CPU.

 8. **Threads vs. processes**
    1. processes are typically independent, while threads exist as subsets of a process.
    2. processes carry considerably more state information than threads, whereas multiple threads within a process share process state as well as memory and other resources. 
    3. processes have separate address spaces, whereas threads share their address space
    4. processes interact only through system-provided inter-process communication mechanisms.
    5. context switching between threads in the same process is typically faster than context switching between processes.

 9. **InterProcess Communication**
    1. where two or more processes are reading or writing some shared data and the final result depends on who runs precisely when, are called **race conditions**. 
    2. That part of the program where the shared memory is accessed is called the **critical region** or **critical section**. If we could arrange matters such that no two processes were ever in their critical regions at the same time, we could avoid races. 
        - No two processes may be simultaneously inside their critical regions.
        - No assumptions may be made about speeds or the number of CPUs.
        - No process running outside its critical region may block other processes.
        - No process should have to wait forever to enter its critical region.
        
**Scheduling**

 1. This situation occurs whenever two or more of them are simultaneously in the ready state. If only one CPU is available, a
choice has to be made which process to run next. The part of the operating system that makes the choice is called the **scheduler**, and the algorithm it uses is called the **scheduling algorithm**.

 2. when the CPU copies bits to a video RAM to update the screen, it is computing, not doing I/O, because the CPU is in use. I/O in this sense is when a process enters the blocked state waiting for an external device to complete its work.
 
 3. The basic idea here is that if an I/O-bound process wants to run, it should get a chance quickly so that it can issue its disk request and keep the disk busy. when processes are I/O bound, it takes quite a few of them to keep the CPU fully occupied.

 4. When to Schedule
    
    - when a new process is created, a decision needs to be made whether to run the parent process or the child process.
    - a scheduling decision must be made when a process exits.
    - when a process blocks on I/O, on a semaphore, or for some other reason, another process has to be selected to run. 
    - when an I/O interrupt occurs, a scheduling decision may be made.

 5. Scheduling algorithms can be divided into two categories with respect to how they deal with clock interrupts. 
    - A **nonpreemptive scheduling** algorithm picks a process to run and then just lets it run until it blocks (either on I/O or waiting for another process) or until it voluntarily releases the CPU. 
    - A **preemptive scheduling** algorithm picks a process and lets it run for a maximum of some fixed time.

 6. Scheduling Algorithm Goals
    - All systems
        - Fairness - giving each process a fair share of the CPU            - Policy enforcement - seeing that stated policy is carried         - out Balance - keeping all parts of the system busy
    - Batch systems
        - Throughput - maximize jobs per hour
        - Turnaround time - minimize time between submission and            - termination CPU utilization - keep the CPU busy all the time
    - Interactive systems
        - Response time - respond to requests quickly                       - Proportionality - meet users' expectations
    - Real-time systems
        - Meeting deadlines - avoid losing data
        - Predictability - avoid quality degradation in multimedia systems

 7. Scheduling in Batch Systems
    - First-Come First-Served
    - Shortest Job First
    - Shortest Remaining Time Next
 
 8. Scheduling in Interactive Systems
    - **Round-Robin Scheduling** 
        - Setting the quantum too short causes too many process switches and lowers the CPU efficiency, but setting it too long may cause poor response to short interactive requests. A quantum around 20-50 msec is often a reasonable compromise.
    - **Priority Scheduling**
        - To prevent high-priority processes from running indefinitely, the scheduler may decrease the priority of the currently running process at each clock tick (i.e., at each clock interrupt). If this action causes its priority to drop below that of the next highest process, a process switch occurs. Alternatively, each process may be assigned a maximum time quantum that it is allowed to run. When this quantum is used up, the next highest priority process is given a chance to run. 
    - **Multiple Queues**
        - it was more efficient to give CPU-bound processes a large quantum once in a while, rather than giving them small quanta frequently (to reduce swapping). Giving all processes a large quantum would mean poor response time. The solution was to set up priority classes. Processes in the highest class were run for one quantum. Processes in the next-highest class were run for two quanta. Processes in the next class were run for four quanta, and so on. Whenever a process used up all the quanta allocated to it, it was moved down one class.
    - **Shortest Process Next**
        - The technique of estimating the next value in a series by taking the weighted average of the current measured value and the previous estimate is sometimes called aging. It is applicable to many situations where a prediction must be made based on previous values. 
    - **Guaranteed Scheduling** 
    - **Lottery Scheduling**
        - The basic idea is to give processes lottery tickets for various system resources, such as CPU time. Whenever a scheduling decision has to be made, a lot- tery ticket is chosen at random, and the process holding that ticket gets the re- source. When applied to CPU scheduling, the system might hold a lottery 50 times a second, with each winner getting 20 msec of CPU time as a prize. 
    - **Fair-Share Scheduling** 
        - Based on process owner.
        
 9. **Scheduling in Real-Time Systems**
    - Real-time systems are generally categorized as hard real time, meaning there are absolute deadlines that must be met, or else, and soft real time, meaning that missing an occasional deadline is undesirable, but nevertheless tolerable. 
