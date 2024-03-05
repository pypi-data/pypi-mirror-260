import os
import subprocess
import time
from multiprocessing import Pool


"""
A function defined at the module level is picklable.
This allows child processes to import the module and access the function.
"""


def sync_file(file_info, parent_dir, aws_profile, s3_bucket):
    """
    Synchronizes a single file to an S3 bucket using the AWS CLI.

    Constructs and executes the AWS CLI command to sync a single file
    from a local directory to an S3 bucket using the subprocess module.

    Parameters:
    - file_info (tuple): Contains the relative path and the file name.
    - parent_dir (str): The parent directory for file syncing.
    - aws_profile (str): The AWS profile for the sync command.
    - s3_bucket (str): The target S3 bucket for file syncing.

    Prints and executes the command, checking for successful completion.
    """
    relative_path, file = file_info
    abs_path = (
        os.path.join(parent_dir, relative_path)
        if relative_path != "."
        else parent_dir + "/"
    )
    s3_path = (
        f"s3://{s3_bucket}/{relative_path}/"
        if relative_path != "."
        else f"s3://{s3_bucket}/"
    )
    cmd = [
        "aws",
        "s3",
        "sync",
        "--profile",
        aws_profile,
        "--exclude",
        "*",
        "--include",
        f"*{file}",
        "--quiet",
        abs_path,
        s3_path,
    ]
    print(f"Running command: {' '.join(cmd)}")
    try:
        # Execute command with output capture
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        # Print stdout and stderr if an exception is raised
        print(f"Command failed with exit code {e.returncode}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        raise


class S3CLI:
    def __init__(self, aws_profile):
        self.aws_profile = aws_profile

        self._check_awscli()

    def _check_awscli(self):
        try:
            subprocess.check_output(["aws", "--version"])
        except Exception as e:
            print(f"Exception occurred: {e}")

    def get_files(self, parent_dir):
        file_list = []
        if not os.path.isdir(parent_dir):
            print(f"{parent_dir} is not a directory.")
            return file_list
        for root, dirs, files in os.walk(parent_dir):
            if not os.path.isdir(root):
                print(f"{root} is not a directory.")
                continue
            for file in files:
                relative_path = os.path.relpath(root, parent_dir)
                file_list.append((relative_path, file))
        return file_list

    def get_total_size(self, parent_dir, file_list):
        """
        Calculates total size of all files in bytes.
        Files are represented as tuples (relative_path, file_name).
        Iterates over the list, calculates each file's size, and sums them.

        :param parent_dir: Directory where files are located
        :param file_list: List of tuples (relative_path, file_name)
        :return: Total size of files in bytes
        """
        total_size = 0
        for relative_path, file in file_list:
            if relative_path == ".":
                relative_path = ""
            abs_path = os.path.join(parent_dir, relative_path, file)
            total_size += os.path.getsize(abs_path)
        return total_size

    def _check_s3_bucket_name(self, s3_bucket):
        # Remove any trailing "/" from s3_bucket
        return s3_bucket.rstrip("/")

    def sync(self, parent_dir, s3_bucket, parallel_instances):
        s3_bucket = self._check_s3_bucket_name(s3_bucket)
        file_list = self.get_files(parent_dir)
        total_size = self.get_total_size(parent_dir, file_list)
        start_time = time.time()

        # Use a partial function to pass the extra arguments to sync_file
        from functools import partial

        sync_file_with_args = partial(
            sync_file,
            parent_dir=parent_dir,
            aws_profile=self.aws_profile,
            s3_bucket=s3_bucket,
        )

        with Pool(parallel_instances) as p:
            p.map(sync_file_with_args, file_list)
            p.close()
            p.join()

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_size_mb = total_size / (1024 * 1024)
        total_size_gb = total_size_mb / 1024
        average_rate = total_size_mb / elapsed_time
        print(f"Total size: {total_size_mb} MB or {total_size_gb} GB")
        print(f"Number of files: {len(file_list)}")
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"Average rate: {average_rate} MB/sec")
