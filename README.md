# LLM-based Automation Agent

## Overview
This project is an automation agent that executes plain-English tasks using an LLM (GPT-4o-Mini) and integrates them into a Continuous Integration (CI) pipeline. The agent is designed to handle various operational tasks efficiently and verifiably.

## Features
- Accepts plain-English tasks via API
- Uses an LLM to interpret and execute multi-step tasks
- Reads and writes files for verification
- Provides error handling with appropriate HTTP responses
- Supports automation tasks such as formatting files, sorting data, extracting information, and running scripts

## API Endpoints
### `POST /run?task=<task description>`
- Executes a given task based on the description.
- Returns:
  - `200 OK` if successful
  - `400 Bad Request` for task errors
  - `500 Internal Server Error` for agent errors

### `GET /read?path=<file path>`
- Returns the content of the specified file.
- Returns:
  - `200 OK` with file content if successful
  - `404 Not Found` if the file does not exist

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/user-name/repo-name.git
   cd repo-name
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```sh
   export AIPROXY_TOKEN=<your_token>
   ```
4. Run the application:
   ```sh
   python app.py
   ```

## Running with Docker
1. Build the Docker image:
   ```sh
   docker build -t user-name/repo-name .
   ```
2. Run the container:
   ```sh
   docker run -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 user-name/repo-name
   ```

## Contributing
Feel free to submit issues and pull requests to improve the project.

## License
This project is licensed under the MIT License.

