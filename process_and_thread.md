# Prcocess and Thread 


### Process

 1. All the runnable software on the computer, sometimes including the operating system, is organized into a number of **sequential processes**, or just processes for short. **A process is just an instance of an executing program**.
 2. Processes must not be programmed with built-in assumptions about timing.
 3. The key idea here is that a process is an activity of some kind. It has a program, input, output, and a state. A single processor may be shared among several processes, with some scheduling algorithm being used to determine when to stop work on one process and service a different one.
 
### Thread

 1. **why need threads?**
    1. threads we add a new element: the ability for the parallel entities to share an address space and all of its data among themselves. This ability is essential for certain applications, which is why having multiple processes (with their separate address spaces) will not work.
    2. threads are lighter weight than processes, they are easier (i.e., faster) to create and destroy than processes.
    3. threads yield no performance gain when all of them are CPU bound, but when there is substantial computing and also substantial I/O, having threads allows these activi- ties to overlap, thus speeding up the application.(only one cpu)
    4. threads are useful on systems with multiple CPUs, where real parallelism is possible.

 2. Prcocess it is a way to group related resources together. A process has an address space containing program text and data, as well as other resources. 

 3. Thread has a program counter that keeps track of which instruc- tion to execute next. It has registers, which hold its current working variables. It has a stack, which contains the execution history, with one frame for each procedure called but not yet returned from. Although a thread must execute in some process, the thread and its process are different concepts and can be treated sepa- rately.

 4. Processes are used to group resources together; threads are the entities scheduled for execution on the CPU.

 5. **Threads vs. processes**
    1. processes are typically independent, while threads exist as subsets of a process.
    2. processes carry considerably more state information than threads, whereas multiple threads within a process share process state as well as memory and other resources. 
    3. processes have separate address spaces, whereas threads share their address space
    4. processes interact only through system-provided inter-process communication mechanisms.
    5. context switching between threads in the same process is typically faster than context switching between processes.

 6. **InterProcess Communication**
    1. where two or more processes are reading or writing some shared data and the final result depends on who runs precisely when, are called **race conditions**. 
    2. That part of the program where the shared memory is accessed is called the **critical region** or **critical section**. If we could arrange matters such that no two processes were ever in their critical regions at the same time, we could avoid races. 
        - No two processes may be simultaneously inside their critical regions.
        - No assumptions may be made about speeds or the number of CPUs.
        - No process running outside its critical region may block other processes.
        - No process should have to wait forever to enter its critical region.
