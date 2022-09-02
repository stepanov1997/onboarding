import os
import mysql.connector
import time
import pandas as pd
import boto3

class AdvertiserReport:
    def __init__(self, advertiser_ids):
        self.advertiser_ids = advertiser_ids

    def wait_mysql_to_be_ready(self):
        stop = False
        while not stop:
            time.sleep(1)
            try:
                self.mydb = mysql.connector.connect(
                    host=os.environ["MYSQL_HOST"],
                    user=os.environ["MYSQL_USER"],
                    password=os.environ["MYSQL_PASSWORD"],
                    database=os.environ["MYSQL_DATABASE"]
                )
                stop = True
            except:
                print("Wait for database to be initialized...")

    def execute_query(self):
        mycursor = self.mydb.cursor()
        mycursor.execute(f"""
            SELECT ad.id, ad.name, ad.type, a.name, o.name
            FROM AD ad
            JOIN ADVERTISER a on a.id = ad.advertiserId
            JOIN ORGANISATION o on a.organisationId = o.id
            WHERE advertiserId IN ({self.advertiser_ids})
        """)
        myresult = mycursor.fetchall()
        return pd.DataFrame(data=myresult, columns=[
            "Ad id", "Ad name", "Ad type", "Advertiser name", "Organisation name"
        ])

    def upload_to_aws(self, local_file, bucket, s3_file, access_key, secret_key, endpoint_url=None):
        s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")

    def send_results(self, dataframe):
        dataframe.to_csv("report.csv")
        try:
            self.upload_to_aws(
                local_file="report.csv",
                bucket=os.environ["S3_BUCKET"],
                s3_file="report_s3.csv",
                access_key=os.environ["S3_ACCESS_KEY"],
                secret_key=os.environ["S3_SECRET_KEY"],
                endpoint_url=os.environ.get("S3_ENDPOINT", None)
            )
        except Exception as ex:
            print(f"Error: {ex}")
            return False
        return True

    def create_report(self):
        try:
            self.wait_mysql_to_be_ready()
            df = self.execute_query()
            return self.send_results(df)
        except Exception as ex:
            print(ex)
            return False


if __name__ == "__main__":
    report = AdvertiserReport(os.environ["ADVERTISER_IDS"])
    if report.create_report():
        print("Success: report is created.")
    else:
        print("Error: report is not created.")
