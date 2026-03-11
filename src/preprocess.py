import re

def clean_log(line):
    """
    Clean log line by removing numbers and masking block IDs.
    """
    # Remove numbers
    line = re.sub(r'\d+', '', line)
    # Mask block IDs (although redundant if numbers are gone, keeping for safety/specific patterns)
    line = re.sub(r'blk_-?\d+', 'BLK', line)
    return line.lower()

def main():
    # Test
    test_log = "081109 203615 148 INFO dfs.DataNode$PacketResponder: PacketResponder 1 for block blk_38865049064139660"
    print(f"Original: {test_log}")
    print(f"Cleaned: {clean_log(test_log)}")

if __name__ == "__main__":
    main()
