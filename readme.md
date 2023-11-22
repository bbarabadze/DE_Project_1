# Process large csv file with Multiprocessing module

#### This program splits a large data file to chunks and does a parallel computations for each chunk.
#### The file contains some data about trips by NY taxy companies. We need to calculate a total revenue of each company



```mermaid
flowchart LR
    S(Start)
    F{Does files and folders exist?}
    style F fill:blue
    LG(Log to the error file)
    style LG fill:gray
    E(Raise an error)
    style E fill:red
    D(Partitioning files)
    style D fill:orange
    CR{Are original and partition 
    files consistent?}
    style CR fill:blue
    AN5(Find top 10 most common names)
    style AN5 fill:green
    AN6(Find top 5 most active users)
    style AN6 fill:green
    END(End)
    S ----> F
    F -->|yes| D
    F ---->|no| LG
    D --> CR
    CR ----> |yes| AN5
    CR ----> |no| LG
    LG ----> E
    E ----> END
    AN5 ----> AN6
    AN6 ----> END


```