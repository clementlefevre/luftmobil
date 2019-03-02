# Luftmobil

## Hardware

- Raspberry Zero W with Raspbian Stretch
- BME280
- SDS011


## Software

- Retrieve the data (timestamp,temperature,pressure,humidity,pm2.5,pm10) every X minutes
- When Wifi is available, store the data into an AWS DynamoDB table.



## Prerequisites

- AWS account set up and credentials & config file in the .aws folder
- Create a Table in dynamo DB
