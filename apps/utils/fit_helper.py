import datetime
import httpx


class FitnessDataFetcher:
    def __init__(self):
        self.base_url = (
            "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        )

    async def normalize_datetime(self, date: str):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        end_of_day = (
            date_obj + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
        )
        return int(end_of_day.timestamp()) * 1000

    async def fetch_steps_data(self, start_time, end_time, access_token: str):
        data = {
            "aggregateBy": [
                {
                    "dataTypeName": "com.google.step_count.delta",
                    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps",
                }
            ],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": await self.normalize_datetime(start_time),
            "endTimeMillis": await self.normalize_datetime(end_time),
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=data, headers=headers)
            response.raise_for_status()
            return await self.process_steps_data(response.json())

    async def fetch_heart_rate_data(
        self, start_time: str, end_time: str, access_token: str
    ):
        data = {
            "aggregateBy": [
                {
                    "dataTypeName": "merge_heart_rate_bpm",
                    "dataSourceId": "derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm",
                }
            ],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": await self.normalize_datetime(start_time),
            "endTimeMillis": await self.normalize_datetime(end_time),
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, json=data, headers=headers)
            response.raise_for_status()
            return await self.process_heart_rate_data(response.json())

    async def process_steps_data(self, data):
        labels = []
        values = []
        for bucket in data["bucket"]:
            start_time = bucket["startTimeMillis"]
            end_time = bucket["endTimeMillis"]
            dataset = bucket["dataset"][0]

            if "point" in dataset and dataset["point"]:
                point = dataset["point"][0]
                value = point["value"][0]["intVal"]
                labels.append(
                    f"{ datetime.datetime.fromtimestamp(int(start_time) / 1000.0).date()} - { datetime.datetime.fromtimestamp(int(end_time) / 1000.0).date()}",
                )
                values.append(value)

        return {"labels": labels, "values": values}

    async def process_heart_rate_data(self, data):
        labels = []
        values = []
        for bucket in data["bucket"]:
            start_time = bucket["startTimeMillis"]
            end_time = bucket["endTimeMillis"]
            dataset = bucket["dataset"][0]

            if "point" in dataset and dataset["point"]:
                point = dataset["point"][0]
                value = point["value"][0]["fpVal"]
                labels.append(
                    f"{ datetime.datetime.fromtimestamp(int(start_time) / 1000.0).date()} - { datetime.datetime.fromtimestamp(int(end_time) / 1000.0).date()}",
                )
                values.append(value)

        return {"labels": labels, "values": values}

    async def validate_google_access_token(self, access_token: str):
        url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={access_token}"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
        except Exception as e:
            return ValueError("Invalid access token")
