# RestApiServerMS

The **Rest API Server Microservice** serves as an interface for interacting
with the InfluxDB and provides a foundation for analytics and future system
interactions. It offers REST endpoints to allow users to query, add, and remove
data in the InfluxDB, enabling in-depth analysis of the underlying battery
data (BESS).

While currently focused on data analytics, this microservice is envisioned to
evolve in the next development stage to directly interact with the BESS,
potentially via MQTT topics, for more advanced control and monitoring.

## Key Responsibilities

1. **Data Querying**: Provides a `GET /query` endpoint to retrieve data from
   InfluxDB, facilitating analysis of time-series metrics.
2. **Data Insertion**: Offers a `POST /add` endpoint to add new data to the
   InfluxDB, supporting updates to the dataset.
3. **Data Deletion**: Enables a `DELETE /remove` endpoint to remove data from
   the InfluxDB, ensuring data management flexibility.
4. **Future BESS Interaction**: Serves as a foundation for the next development
   stage, where it may interact directly with BESS devices via MQTT or similar
   protocols for enhanced monitoring and control.

Here is a visualization of the WebsocketServerMS's role within the Pipeline
architecture:

![Pipeline Diagram](assets/images/RestApiServerMS_in_Pipeline.png "Pipeline
Diagram")

## Installation

**Note**: This guide is for local installation. You may need `sudo`
privileges to execute some of these commands.

### Prerequisites

1. A Linux system (developed and tested on Ubuntu).
2. InfluxDB installed and active.
3. Postman or equivalent, or a basic html file (to test the REST API
   endpoints).
4. Docker installed and active.
5. A Python virtual environment:
    - Create and activate a virtual environment (`venv`).
    - Run `pipenv install` to install dependencies.
    - Run `pipenv install --dev` to install development dependencies.

### Environment Variables

Ensure in the root directory there is an `.env` file with the following
parameters:

```plaintext
# Influx Configuration Settings
INFLUX_URL=
INFLUX_TOKEN=
INFLUX_ORG=
INFLUX_BUCKET=

# Restful Server Configuration Settings
REST_HOST=
REST_PORT=
```

### Setup

- Make the CI/CD simulation script executable:
   ```bash
   chmod +x simulate_cicd.sh
    ```
- Run the simulation script to create the Docker container:
    ```bash 
    ./simulate_cicd.sh 
    ```
  This will create and start the Docker container.

**Note**: This script is intended to simulate a CI/CD deployment. The
actual `.github/workflows/deploy.yml` is simply a placeholder and would
be the next stage in the development process. Hence, this script will do
the following:

- stop and remove all previously running docker containers and images
  with the same image name and same container name (ensures a clean build)
- lint the project in accordance with PEP 8 standards with `pylint .`
- run unit tests with `pytest -v`
- build the docker image
- then run a docker container with that same image

For the purpose of the demo, I figured simulating a CI/CD deployment
pipeline via bash script would be easier to show/explain in a
limited amount of time, especially since the Pipeline is intended to run
"on-premise".

### Teardown

- Make the teardown script executable:
  ```bash
  chmod +x teardown.sh
  ```
- Run the teardown script:

    ```bash
    ./teardown.sh
    ```

- This will simply remove any docker images and containers associated with
  this specific Microservice.

## Usage

- To view the logs of the running Docker container, use the
  following command:
  ```bash
    docker logs -f rest_server_ms_simulation_container_1
    ```

**Note:** In a production environment, the logs would typically be redirected
to a
file and integrated with an ELK stack (Elasticsearch, Logstash, and Kibana) to
enable visualization and analysis on a dashboard. However, for the purposes of
this demo, I opted against introducing additional overhead to the Docker
container to minimize latency as much as possible.

### Endpoints

#### GET: /query

`http://localhost:8000/batteryData/query`

#### Description

This endpoint retrieves data for a specific battery based on the given query
parameters.

#### Query Parameters

- `battery_id`: (Required) The ID of the battery you want to query.
    - Example: `1`

- `start_time`: (Required) The start time for the query. Use relative
  times (e.g., `-5h` for 5 hours ago) or absolute timestamps.
    - Example: `-5h`

- `stop_time`: (Required) The stop time for the query. Use relative times (
  e.g., `-1m` for 1 minute ago) or absolute timestamps.
    - Example: `-1m`

- `field`: (Required) The specific field of the battery data to retrieve.
    - Example: `latency_ms`

#### Example request

`GET` `http://localhost:8000/batteryData/query?
battery_id=1&start_time=-5h&stop_time=-1m&field=latency_ms`

#### Example response

```json
[
  ...,
  {
    "time": "2024-11-17T00:01:53.238000Z",
    "value": 7
  },
  {
    "time": "2024-11-17T00:01:52.648000Z",
    "value": 7
  },
  ...
]
```

---

#### POST: /add

`http://localhost:8000/batteryData/add`

#### Description

This endpoint allows adding new battery data to the system. The request
requires a JSON payload containing the battery details.

#### JSON Payload

The request body should be a JSON object with the following fields:

- `battery_id`: (Required) The unique identifier for the battery.
  Example: `"100"`
- `voltage`: (Required) The voltage reading of the battery.
  Example: `450`
- `current`: (Required) The current reading of the battery.
  Example: `50`
- `temperature`: (Required) The temperature reading of the battery in degrees
  Celsius.
  Example: `25`
- `state_of_charge`: (Required) The state of charge (SOC) of the battery, as a
  percentage.
  Example: `80`
- `state_of_health`: (Required) The state of health (SOH) of the battery, as a
  percentage.
  Example: `90`

#### Example request

`POST` `http://localhost:8000/batteryData/add`

`Content-Type: application/json`

```json
{
  "battery_id": "100",
  "voltage": 450,
  "current": 50,
  "temperature": 25,
  "state_of_charge": 80,
  "state_of_health": 90
}
```

#### Example response

```json
{
  "status": "success"
}
```

---

#### DELETE: /remove

`http://localhost:8000/batteryData/remove`

#### Description

This endpoint allows the removal of battery data for a specific battery ID
within a specified time range.

#### Query parameters

- `battery_id`: (Required) The unique identifier of the battery whose data you
  want to delete.
  Example: `"100"`

- `start_time`: (Required) The start time of the range for which the data
  should
  be deleted. Use relative times (e.g., -5h for 5 hours ago) or absolute
  timestamps.
  Example: `-5h`

- `stop_time`: (Required) The stop time of the range for which the data should
  be
  deleted. Use relative times (e.g., -1ms for 1 millisecond ago) or absolute
  timestamps.
  Example: `-1ms`

#### Example request

`DELETE` `/batteryData/remove?battery_id=100&start_time=-5h&stop_time=-1ms`

#### Example response

```json
{
  "status": "deleted"
}
```

---

## Testing

There is no need to explicitly run the linter or unit tests, since the
script `simulate_cicd.sh` already takes care of this.

## MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
