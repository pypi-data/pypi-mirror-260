"""
The main entry point.
"""


def main():
    from s3psync.core import main

    main()


if __name__ == "__main__":
    import sys

    sys.exit(main())
