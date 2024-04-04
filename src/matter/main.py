import filter
import parser
import report
import plot
import pandas as pd

def DoParser():
    lines = parser.GetFile("test.txt")
    df = pd.DataFrame(lines, columns=['Date', 'Time', 'Context', 'Key', 'Agent', 'Message'])
    df.to_csv('csv/matter_logs.csv', index=False)

def DoFilter():
    filter.filter("matter_logs.csv", "subscription", 5, "Subscription.csv")
    filter.filter("Subscription.csv", "succeed", 5, "succeeded.csv")
    filter.filter("Subscription.csv", "fail", 5, "failed.csv")
    filter.filter("failed.csv", "node", 4, "failed.csv")
    filter.filter("matter_logs.csv", "commissioning", 5, "commissioning.csv")

def DoReport():
    report.nodeSubscription("succeeded.csv", "failed.csv", "commissioning.csv", "node.csv")

def DoPlot():
    plot.GetGraphNode(1, "succeeded.csv", "failed.csv", "commissioning.csv")

if __name__ == "__main__":
    DoParser()
    DoFilter()
    DoReport()
