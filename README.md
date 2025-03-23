# Sample API FastAPI

![Tests Status](https://img.shields.io/github/actions/workflow/status/Lucho00Cuba/sample-api/tests.yaml?label=Tests%20Status&logo=github)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

This is a sample API built with FastAPI and Authentication and Authorization using JWT.

## Requirements

- DevContainers (VSCode)
- Python 3.12
- Docker

## Setup

1. Clone the repository

    ```bash
    git clone https://github.com/Lucho00Cuba/sample-api.git
    cd sample-api
    ```
2.a. **Using DevContainers (Recommended)**

   - VSCode should prompt you to open the project in a DevContainer. The necessary environment will be set up automatically.

2.b. **Without DevContainers**

   - Create a virtual environment:

     ```
     python3 -m venv venv
     ```

   - Activate the virtual environment:
   
     **On Linux/MacOS:**
        ```
        source venv/bin/activate
        ```
     **On Windows:**
        ```
        .\venv\Scripts\activate
        ```

   - Install dependencies:
        ```
        pip install -r requirements.txt
        ```

   - Run the API:

      ```bash
      API_IS_DEV=true src/entrypoint.sh
      ```

## Features

- 🔐 Authorization and Authentication using JWT
- 🔄 Automatic loading routes from the `src/routes` folder
   - 📝 Manually set an endpoint if needed
- 📊 Custom response formatting for consistent API responses
- 📑 Swagger and Redoc auto-generated API documentation
- 📦 Docker support

## TODO

- [ ] ✅ Improve unit and integration test coverage
- [ ] 🔗 Integrate with a third-party user system such as Rancher-Manager (Local)
- [ ] 🚀 Implement rate-limiting to prevent abuse
- [ ] 🔄 Implement a refresh token mechanism for better security
- [ ] 📂 Improve database handling, possibly integrating SQLAlchemy or another ORM
