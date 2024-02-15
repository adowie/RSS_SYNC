import os
import subprocess

# # Start Prefect
# prefect_process = subprocess.Popen(["prefect", "server", "start"])
# prefect_process.wait()

# Start Kafka
kafka_process = subprocess.Popen(["kafka-server-start.sh", "/app/kafka/config/server.properties"])
# Wait for both processes to finish
kafka_process.wait()