import os
import sys

import mysql.connector
import time
import pandas as pd
import boto3
from metaflow import FlowSpec, step, Parameter, retry, catch, timeout


class AdvertiserReport(FlowSpec):
    advertiser_ids = Parameter(name="advertiserIds", required=True, separator=",")

    @step
    def start(self):
        self.next(self.create_report, foreach="advertiser_ids")

    @retry(times=3)
    @timeout(minutes=1)
    @step
    def create_report(self):
        self.advertiser_id = self.input
        mysql_client = self.wait_mysql_to_be_ready()
        mysql_cursor = mysql_client.cursor()
        mysql_cursor.execute(f"""
                    SELECT ad.id, ad.name, ad.type, a.name, o.name
                    FROM AD ad
                    JOIN ADVERTISER a on a.id = ad.advertiserId
                    JOIN ORGANISATION o on a.organisationId = o.id
                    WHERE advertiserId = ({self.advertiser_id})
                """)
        results = mysql_cursor.fetchall()
        df = pd.DataFrame(data=results, columns=[
            "Ad id", "Ad name", "Ad type", "Advertiser name", "Organisation name"
        ])
        self.report_filename = f"report_{self.advertiser_id}.csv"
        
        df.to_csv(self.report_filename)
        self.next(self.join_upload_results)

    @retry(times=3)
    @catch(var="s3_exception")
    @step
    def join_upload_results(self, inputs):
        for input_element in inputs:
            self.upload_to_aws(
                local_file=input_element.report_filename,
                bucket=os.environ["S3_BUCKET"],
                s3_file=input_element.report_filename,
                access_key=os.environ["S3_ACCESS_KEY"],
                secret_key=os.environ["S3_SECRET_KEY"],
                endpoint_url=os.environ.get("S3_ENDPOINT", None)
            )
            print(f"{input_element.report_filename} has successfully uploaded on S3!")
        self.next(self.end)

    @step
    def end(self):
        if self.s3_exception:
            print(f"Error: {self.s3_exception}")
            sys.exit("S3 error")
        print("Report sent successfully!!")

    def wait_mysql_to_be_ready(self):
        while True:
            time.sleep(1)
            try:
                return mysql.connector.connect(
                    host=os.environ["MYSQL_HOST"],
                    user=os.environ["MYSQL_USER"],
                    password=os.environ["MYSQL_PASSWORD"],
                    database=os.environ["MYSQL_DATABASE"]
                )
            except:
                print("Wait for database to be initialized...")

    def upload_to_aws(self, local_file, bucket, s3_file, access_key, secret_key, endpoint_url=None):
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")


if __name__ == "__main__":
    AdvertiserReport()
