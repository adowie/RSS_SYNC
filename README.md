# RSS FEED SYNC PROJECT

## Spin up Docker Container

- Modify the `docker-compose.yml` to set the following ENVs in container
  1. RSS_FEED_URL="<https://news.google.com/rss>" # set feed to consume
  2. QUEUE="SS_RSS_SYNC" # queue topic / group
  3. KAFKA_BOOTSTRAP_SERVERS="localhost:9092" # this is the kakfa instance that this Sync should queue to

- ```bash
  docker-compose up -d --build
  ```

### After Docker Container is up and running, you can access the following services

- **Activate virtual environment**

```bash
.\venv\Scripts\activate
```

- **Run Sync Flow**
  - To run the main flow of the project use this command in your terminal:
  - If you are using Prefect Cloud run before the sync command: prefect cloud login

    - ```python
         python app/rss_sync.py
      ```
