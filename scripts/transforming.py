import abc
import logging
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from scripts.constants import PROCESS_FOLDER, S3_BUCKET_NAME, ACCESS_ID, ACCESS_KEY

logger = logging.getLogger(__name__)


class AbstractETL(abc.ABC):

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError()


class ETLProcess(AbstractETL):

    def __init__(self, filepath, metadata):
        self.filepath = filepath
        self.output_filepath = None
        self.metadata = metadata

    def process(self):
        self.extract()
        self.transform()
        self.load()

    def extract(self):
        try:
            logging.info("start loading datalab file")
            read_file = pd.read_excel(self.filepath)
            self.metadata["loaded_file"] = self.metadata["file_name"].split(".")[0] + ".csv"
            read_file.to_csv(PROCESS_FOLDER + "\\" + self.metadata["loaded_file"], index=False, header=True)
        except Exception as exp:
            logging.error("Error happened while extracting data file. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done loading datalab file")

    def transform(self):
        try:
            import csv
            logging.info("Start processing data file")
            self.metadata["transformed_file"] = "processed_" + self.metadata["loaded_file"]
            with open(PROCESS_FOLDER + "\\" + self.metadata["loaded_file"], "r", encoding="utf8") as f:
                with open(PROCESS_FOLDER + "\\" + self.metadata["transformed_file"], "w", newline='') as fw:
                    # Skip metadata row, we already have meta_data as arguments
                    # self.metadata['downloaded_file_meta'] = {}
                    for i in range(6):
                        line = f.readline().split(',')
                        # self.metadata[line[0]] = str(line[1:])
                    reader = csv.DictReader(f, delimiter=",")
                    writer = csv.DictWriter(fw, delimiter=",", fieldnames=["date", "keyword", "score"])
                    writer.writeheader()
                    for row in reader:
                        item = {"date": row["날짜"]}
                        for keyword in self.metadata["keyword"].keys():
                            item["keyword"] = keyword
                            item["score"] = row[keyword.strip()]
                            writer.writerow(item)

        except Exception as exp:
            logging.error("Error happened while extracting data file. Stack trace " + str(exp), exc_info=True)
        else:
            logging.info("Done process the file")

    def load(self):
        # to s3 bucket along with metadata
        print(f"Final metadata to bring along to S3 bucket: {self.metadata}")
        logging.info("Transfer the file to S3 bucket")
        from os import path
        # S3 object_name is not specified, use file_name
        object_name = path.basename(self.metadata["transformed_file"])
        for key in self.metadata.keys():
            if type(self.metadata[key]) != 'str':
                self.metadata[key] = str(self.metadata[key])
        # Upload the file
        s3_client = boto3.client('s3',
                                 aws_access_key_id=ACCESS_ID,
                                 aws_secret_access_key=ACCESS_KEY)
        try:
            response = s3_client.upload_file(
                PROCESS_FOLDER + '\\' + self.metadata["transformed_file"],
                S3_BUCKET_NAME,
                object_name,
                ExtraArgs={
                    'Metadata': self.metadata,
                    'ACL': 'public-read'
                },
            )
        except ClientError as e:
            logging.error(e)
        else:
            logging.info("successfully uploaded to s3")
