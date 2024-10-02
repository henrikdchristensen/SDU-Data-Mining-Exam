import sys

def count_lines(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    num_lines = count_lines(file_path)
    print(f'Total number of lines: {num_lines}')