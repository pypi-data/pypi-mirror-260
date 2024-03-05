import os
import subprocess
import pytest
from s3psync.s3cli import S3CLI
from unittest.mock import patch
from s3psync.s3cli import sync_file


@pytest.fixture
def s3cli():
    return S3CLI(aws_profile="test-profile")


def test_get_total_size(s3cli):
    # Setup: Create a mock file list with known sizes
    file_list = [("dir", "file1.txt"), ("dir", "file2.txt")]
    # Mock the os.path.getsize to return a fixed size for any file
    with patch("os.path.getsize", return_value=100):
        # Call the method under test
        total_size = s3cli.get_total_size("/fake/dir", file_list)
        # Assert the expected result
        assert total_size == 200


def test_sync_file(s3cli):
    # Setup: Create a mock file info and other parameters
    file_info = ("dir", "file1.txt")
    parent_dir = "/fake/dir"
    aws_profile = "test-profile"
    s3_bucket = "test-bucket"

    # Mock the subprocess.run to not actually run the command
    with patch("subprocess.run") as mock_run:
        # Call the method under test
        sync_file(file_info, parent_dir, aws_profile, s3_bucket)

    # Assert that subprocess.run was called with the expected command
    expected_cmd = [
        "aws",
        "s3",
        "sync",
        "--profile",
        aws_profile,
        "--exclude",
        "*",
        "--include",
        f"*{file_info[1]}",
        "--quiet",
        os.path.join(parent_dir, file_info[0]),
        f"s3://{s3_bucket}/{file_info[0]}/",
    ]
    mock_run.assert_called_once_with(expected_cmd, check=True,
                                     capture_output=True, text=True)


def test_sync_file_exception(s3cli, capsys):
    # Setup: Create a mock file info and other parameters
    file_info = ("dir", "file1.txt")
    parent_dir = "/fake/dir"
    aws_profile = "test-profile"
    s3_bucket = "test-bucket"
    error_message = (
        "Running command: aws s3 sync --profile test-profile --exclude * "
        "--include *file1.txt --quiet /fake/dir/dir s3://test-bucket/dir/\n"
        "Command failed with exit code 1\n"
        "stdout: Test output\n"
        "stderr: Test error\n"
    )
    # Create a mock exception to simulate subprocess.run failure
    mock_exception = subprocess.CalledProcessError(
        1, 'cmd', output='Test output', stderr='Test error'
    )

    # Mock the subprocess.run to raise the mock exception
    with patch("subprocess.run", side_effect=mock_exception):
        # Call the method under test expecting it to raise an exception
        with pytest.raises(subprocess.CalledProcessError):
            sync_file(file_info, parent_dir, aws_profile, s3_bucket)

    # Capture the output printed to stdout and stderr
    captured = capsys.readouterr()

    # Assert that the expected error message is printed to stdout
    assert error_message in captured.out


def test_get_files(s3cli):
    # Setup: Create a mock directory with files
    parent_dir = "/fake/dir"
    expected_file_list = [
        (".", "file"),
        ("subdir2", "hello_world2"),
        ("subdir1", "hello_world"),
    ]

    # Mock the os.path.isdir to return True
    with patch("os.path.isdir", return_value=True):
        # Mock the os.walk to return a fixed file list for any directory
        # Directory structure
        # /fake/dir
        # ├── file
        # ├── subdir1
        # │   └── hello_world
        # └── subdir2
        #     └── hello_world2
        with patch(
            "os.walk",
            return_value=[
                (parent_dir, ["subdir2", "subdir1"], ["file"]),
                (parent_dir + "/subdir2", [], ["hello_world2"]),
                (parent_dir + "/subdir1", [], ["hello_world"]),
            ],
        ):
            # Call the method under test
            file_list = s3cli.get_files(parent_dir)
            # Assert the expected result
            assert file_list == expected_file_list
