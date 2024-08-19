import subprocess
import csv
import os
from datetime import datetime, timedelta

# TShark command to capture network traffic with protocol
TSHARK_CMD = [
    'tshark', '-i', 'enp0s18', '-a', 'duration:300', '-T', 'fields',
    '-e', 'frame.time_epoch', '-e', 'ip.src', '-e', 'ip.dst',
    '-e', 'tcp.srcport', '-e', 'tcp.dstport', '-e', '_ws.col.Protocol', '-E', 'header=y',
    '-E', 'separator=,'
]

# Output CSV file paths
TEMP_CSV_FILE_PATH = '/home/user/honeypot-matter-thread/tshark/temp_capture.csv'
FINAL_CSV_FILE_PATH = '/usr/share/grafana/csv/capture_filtered.csv'

def capture_and_filter():
    # Start TShark process
    process = subprocess.Popen(TSHARK_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)

    # Open temporary CSV file
    with open(TEMP_CSV_FILE_PATH, mode='w', newline='') as temp_file:
        csv_writer = csv.writer(temp_file)

        csv_writer.writerow(['capture_time', 'frame.time_epoch', 'ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 'protocol'])

        try:
            for line in process.stdout:
                fields = line.strip().split(',')
                if len(fields) != 6:
                    continue

                frame_time_epoch, ip_src, ip_dst, src_port, dst_port, protocol = fields

                # Filter out SSH packets (port 22)
                if src_port == '22' or dst_port == '22' or protocol == '_ws.col.protocol':
                    continue

                # Get the current time
                capture_time = datetime.now().replace(microsecond=0)

                # Write the row to the temporary CSV file
                csv_writer.writerow([capture_time, frame_time_epoch, ip_src, ip_dst, src_port, dst_port, protocol])

                # Flush to ensure data is written to disk
                temp_file.flush()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            process.terminate()

def merge_files():
    if os.path.exists(FINAL_CSV_FILE_PATH):
        with open(FINAL_CSV_FILE_PATH, mode='a', newline='') as final_file:
            csv_writer = csv.writer(final_file)

            # Read from the temporary file and write to the final file
            with open(TEMP_CSV_FILE_PATH, mode='r') as temp_file:
                csv_reader = csv.reader(temp_file)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    csv_writer.writerow(row)
    else:
        os.rename(TEMP_CSV_FILE_PATH, FINAL_CSV_FILE_PATH)

if __name__ == '__main__':
    capture_and_filter()
    merge_files()
