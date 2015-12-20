# MySQL Index

1. **What are indexes for ?** 
    *   Speed up access in the database
    *   Help to enforce constraints (UNIQUE, FOREIGN
KEY)

2. **Indexes in MyISAM vs Innodb**
    * In MyISAM data pointers point to physical
offset in the data file
        *   All indexes are essentially equivalent 
    * In Innodb
        *   PRIMARY KEY (Explicit or Implicit) - stores data in
the leaf pages of the index, not pointer
        *   Secondary Indexes – store primary key as data
pointer

3. **Multiple Column Indexes**
    *   Sort Order is defined, comparing leading
column, then second etc
    *   It is still one BTREE Index; not a separate BTREE
index for each level
4. **Overhead of The Indexing**
    *   Indexes are costly; Do not add more than you
need
        *   In most cases extending index is better than
adding new one
    *   **Writes** - Updating indexes is often major cost
of database writes
    *   **Reads** - Wasted space on disk and in memory;
additional overhead during query optimization
5.  **Indexing Innodb Tables**
    *   Data is clustered by Primary Key
        *   Pick PRIMARY KEY what suites you best
    *   PRIMARY KEY is implicitly appended to all indexes
        *   KEY (A) is really KEY (A,ID) internally
        *   Useful for sorting, Covering Index.
6.  **Multi Column indexes for efficient sorting**
    *   It becomes even more restricted!
    *   KEY(A,B)
    *   Will use Index for Sorting
        *   **ORDER BY A** - sorting by leading column
        *   **A=5 ORDER BY B** - EQ filtering by 1st and sorting by 2nd
        *   **ORDER BY A DESC, B DESC** - Sorting by 2 columns in same order
        *   **A>5 ORDER BY A** - Range on the column, sorting on the same
    *   Will NOT use Index for Sorting
        *   **ORDER BY B** - Sorting by second column in the index
        *   **A>5 ORDER BY B** – Range on first column, sorting by second
        *   **A IN(1,2) ORDER BY B** - In-Range on first column
        *   **ORDER BY A ASC, B DESC** - Sorting in the different order
    *   MySQL Using Index for Sorting Rules
        *   You can’t sort in different order by 2 columns
        *   You can only have Equality comparison (=) for
columns which are not part of ORDER BY
7.  **Avoiding Reading The data**
    *   Reading Index ONLY and not accessing the “data”
        *   EXAMPLE: SELECT STATUS FROM ORDERS WHERE CUSTOMER_ID=123
        *   KEY(CUSTOMER_ID,STATUS)
    *   Access is a lot more sequential
        *   Access through data pointers is often quite “random”
8.  **Using Multiple Indexes for the table**
    *   MySQL Can use More than one index
        *   “Index Merge”
    *   SELECT * FROM TBL WHERE A=5 AND B=6
        *   Can often use Indexes on (A) and (B) separately
        *   Index on (A,B) is much better
    *   SELECT * FROM TBL WHERE A=5 OR B=6 
        *   2 separate indexes is as good as it gets
        *   Index (A,B) can’t be used for this query
