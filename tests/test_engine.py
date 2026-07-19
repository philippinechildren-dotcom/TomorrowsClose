"""
tests/test_engine.py

Simple test for the Tomorrow's Close engine.
"""

from engine.engine import process_request


def main():
    result = process_request("QQQ")
    print(result)


if __name__ == "__main__":
    main()
