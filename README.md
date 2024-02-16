# RSS FEED SYNC PROJECT

## Spin up Docker Container

- Modify the `docker-compose.yml` to set the following ENVs in container
  1. RSS_FEED_URL="<https://news.google.com/rss>" # set feed to consume
  2. FEED_INGESTOR="default" # set feed to consume
  3. QUEUE="SS_RSS_SYNC" # queue topic / group
  4. KAFKA_BOOTSTRAP_SERVERS="localhost:9092" # this is the kakfa instance that this Sync should queue to

- ```bash
  docker-compose up -d --build
  ```

### After Docker Container is up and running, you can access the following services

- **Activate virtual environment**

```bash
.\venv\Scripts\activate
```

- You may also need to run
  
  ```bash
  pip install --no-cache-dir -r requirements.txt
  ```

- **Run Sync Flow**
  - To run the main flow of the project use this command in your terminal:
  - If you are using Prefect Cloud run before the sync command: prefect cloud login

  ```bash
  python app/rss_sync.py
  ```

- View Kafka Topic Messages by opening the kakfa container
- i.e. open using docker terminal

```shell
  kafka-console-consumer --bootstrap-server localhost:9092 --topic SS_RSS_SYNC --from-beginning
```
