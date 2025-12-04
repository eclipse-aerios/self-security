from flask import Flask
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
        return data
    else:
        print(f"Failed to parse line: {line}")
        return None

app = Flask(__name__)

@app.route('/events')
def get_suricata_events():
    events_list=[]
    status_code=200
    try:
        if os.path.exists(log_file_path):
            print(f"INFO: Event file found: {log_file_path}")
            with open(log_file_path, "r") as log_file:
                lines = log_file.readlines()
                for line in lines:
                    json_data = transform_line_to_json(line)
                    if json_data:
                        events_list.append(json_data)
        else:
            print(f"ERROR: File does not exist: {log_file_path}")
    except Exception as e:
        status_code=500
        print(f"ERROR: {e}")

    response = app.response_class(
        response=json.dumps(events_list),
        status=status_code,
        mimetype='application/json'
    )
    return response
#        return json.dumps(events_list)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
