import pandas as pd

def GetFile(file):
    with open(file) as f:
        logs = []
        lines = f.readlines()
        lines = [line.rstrip().split(' ', 5) for line in lines]
    return lines


        
if(__name__ == "__main__"):
    lines = GetFile("test.txt")
    df = pd.DataFrame(lines, columns=['Date', 'Time', 'Context', 'Key', 'Agent', 'Message'])
    df.to_csv('csv/matter_logs.csv', index=False)

