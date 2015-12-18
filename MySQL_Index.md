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
