class DataProcessor:
    def __init__(self, data):
        self.data = data

    def transform_data(self):
        transformed_data = []
        for entry in self.data:
            print(f"Transforming feed entry->{entry.title}")
            # Define your transformation logic here (e.g., extract specific fields, format text)
            transformed_entry = {
                "title": entry.title,
                "summary": entry.summary,
                # Add more transformed fields as needed
                # note these fields will be sent to the queuing system
            }
            transformed_data.append(transformed_entry)
        return transformed_data


class Ingestor:
    def __init__(self, data_processor: DataProcessor):
        self.data_processor = data_processor

    def digest(self):
        # Override this method in specific ingestors
        return self.data_processor.transform_data()


class CustomIngestor(Ingestor):
    def digest(self):
        # Add your custom ingestion logic based on the specified ingestor
        #  use self.data_processor.data to access feed.entries
        transformed_data = []  # Your specific transformation logic
        return transformed_data


def select_ingestor(feed, ingestor_name="default"):
    # initialize the default ingestor
    ingestor = Ingestor(DataProcessor(feed.entries))
    # add conditional flow for alternate Ingestors
    # if ingestor_name == "custom":
    #   ingestor = CustomIngestor(DataProcessor(feed.entries))
    return ingestor.digest()
