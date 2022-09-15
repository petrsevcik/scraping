import csv
import json

import scrapy


class DeveloperprojectsSpider(scrapy.Spider):
    name = 'developerprojects'
    allowed_domains = ['www.immobilienscout24.at']
    start_urls = ['http://www.immobilienscout24.at/']

    def start_requests(self):
        projects = self.load_developer_projects()

        for project, meta_data in projects:
            url = 'https://www.immobilienscout24.at/portal/graphql'
            params = f'?operationName=findChildrenByParams&variables=%7B%22params%22%3A%7B%22estateType%22%3A%22APARTMENT%22%2C%22region%22%3A%22009001%22%2C%22transferType%22%3A%22RENT%22%2C%22useType%22%3A%22RESIDENTIAL%22%7D%2C%22parentId%22%3A%22{project}%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22e48e50e9e417c7be84896449c3b5473ff25c7476418cc4a78af950acfe3fe86a%22%7D%7D'
            property_url = url + params
            yield scrapy.http.Request(url=property_url, meta=meta_data)

    def parse(self, response):
        raw_data = json.loads(response.body)
        properties = raw_data["data"]["findChildrenByParams"]["hits"]
        for property in properties:
            yield {
                "data": property,
                "meta_data": response.meta
            }

    def load_developer_projects(self, csv_file="vienna_data.csv"):
        developer_projects_ids = []
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row[2]) > 1 and row[2] != "error":
                    property_id = row[6].split("/")[-1]
                    meta_data = {"full_address": row[0],
                                 "description": row[1],
                                 "devproject_link": row[6],
                                 "contact": row[7],
                                 "company": row[8]}
                    developer_projects_ids.append((property_id, meta_data))
        return developer_projects_ids
