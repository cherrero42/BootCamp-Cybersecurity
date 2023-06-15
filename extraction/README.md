# extraction

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
    e  x  t  r  a  c  t  i  o  n
_____________________________________


In this project we familiarize with the MFT (Master File Table) of the NTFS file system (New Technology Filesystem). The objective of this project is to develop a tool that is able to recover deleted files on NTFS. As we all know in most filesystems when you delete a file it is not really deleted, it stays there unless its overwritten, because of this reason in a lot of cases you will be able to recover deleted files when performing a forensics analysis. We always work on a Win10 VM. We are allowed to use any programming language.

You are allowed to use any library that helps you develop this tool for recovering deleted files on NTFS using Python; we need to understand the structure of the Master File Table (MFT) and implement the necessary logic to identify and recover deleted files. Here's a basic outline of the steps involved:

    Read the raw disk data: To access the NTFS file system, we need to read the raw disk data. This can be achieved using Python's built-in open() function in binary mode to read the disk device directly (e.g., open("\\\\.\\PhysicalDrive0", "rb")).

    Locate the MFT: The MFT is typically located at the beginning of the NTFS partition. You can search for the MFT signature ("FILE") within the raw disk data to find its offset.

    Parse the MFT entries: The MFT contains records for each file and directory in the NTFS partition. Each record is called a "File Record Segment" (FRS) and is identified by a unique MFT entry number. Parse the MFT entries to extract relevant information like the file name, size, attributes, timestamps, etc.

    Identify deleted files: Deleted files in NTFS are marked as "unused" in the MFT. By analyzing the flags and attributes of each MFT entry, you can determine if a file is deleted or active. Deleted files are good candidates for recovery.

    Recover deleted files: For each deleted file, you can retrieve its content by analyzing the clusters associated with the file. The MFT entry provides the cluster runs that represent the file's data on the disk. You can read these clusters and reconstruct the file content.

    Save recovered files: As you recover the deleted files, you can save them to a different location to avoid overwriting any existing data. You can create a new directory to store the recovered files or modify the original file names to differentiate them from the existing ones.

It's important to note that working with raw disk data and implementing file system analysis can be complex and potentially risky. It's recommended to thoroughly test and validate the tool on non-production environments or disk image copies to ensure data integrity and prevent accidental data loss.

The above steps provide a high-level overview of the process, and each step involves multiple subtasks. We need to delve into the details of the NTFS file system specification to implement the parsing and recovery logic accurately.


## Documentation

[Documentation](http://dubeyko.com/development/FileSystems/NTFS/ntfsdoc.pdf)

<p align="center"> <img src="./extraction.jpeg" alt="image" width="456"/> </p>

Jun 2023