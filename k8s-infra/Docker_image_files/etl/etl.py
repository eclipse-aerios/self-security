import json
import requests
import re
import os
import time
from datetime import datetime

log_file_path = "/var/log/suricata/fast.log"
file_path = "/mnt/shared/mac_address.txt"

try:
    with open(file_path, "r") as f:
        mac_address = f.read().strip()
        print(f"MAC Address: {mac_address}")
except FileNotFoundError:
    print("MAC Address file not found!")

endpoint_url = os.getenv("ENDPOINT_URL")

def transform_line_to_json(line):
    pattern = re.compile(r"(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d{6})\s+\[\*\*\]\s+\[.*?\]\s+(.*?)\s+\[\*\*\]\s+\[Classification:.*?\]\s+\[Priority: (\d+)\]\s+\{(.*?)\}\s+((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))(?:\s+->\s+((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})))?")
    match = pattern.match(line)
    
    if match:
        timestamp_str = match.group(1)
        timestamp = datetime.strptime(timestamp_str, "%m/%d/%Y-%H:%M:%S.%f").isoformat()
        message = match.group(2)
        priority = int(match.group(3))
        protocol = match.group(4)
        src = match.group(5)
        dst = match.group(6) if match.group(6) else ""
        
        node_name = os.getenv("MY_NODE_NAME", "unknown")
        
        data = {
            "timestamp": timestamp,
            "message": message,
            "priority": priority,
            "protocol": protocol,
            "src": src,
            "dst": dst,
            "node_name": node_name,
            "mac": mac_address,
        }
        return json.dumps(data)
    else:
        print(f"Failed to parse line: {line}")
        return None

def send_data_to_endpoint(data):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.put(endpoint_url, data=data, headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to endpoint: {e}")
        return None

def main():
   
    while not os.path.exists(log_file_path):
        print(f"{log_file_path} not found, waiting...")
        time.sleep(10)
    
    with open(log_file_path, "r") as log_file:
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(1)
                continue
            json_data = transform_line_to_json(line)
            if json_data:
                status_code = send_data_to_endpoint(json_data)
                if status_code:
                    print(f"Data sent, received status code: {status_code}")
                else:
                    print("Failed to send data to endpoint")

if __name__ == "__main__":
    main()

