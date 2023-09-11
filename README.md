### SCS2205 Computer Networks I - Take Home Assignment 1

Name: W.M.S.L. BANDARA
Registration Number: 2021/CS/020
Index Number: 21000204

# Simple Web Server using Python

This is a simple web server program that can serve both static and PHP files. The server listens on port 2728.

## Instructions for Running the Web Server

Follow these steps to execute the web server:

### 1. Prerequisites

Before running the web server, make sure the following is installed:

- Python
- PHP

### 2. Project Structure

Project directory should have the following structure:

21000204.zip
|-- server.py
|-- htdocs/
| |-- index.php
| |-- multiply.php
| |-- style.css
| |-- ...
|-- README.md (this file)

### 3. Running the Server

1. Extract the contents of `21000204.zip` to a directory of your choice.

2. Open a terminal or command prompt and navigate to the project directory where `server.py` is located.

3. Run the server using the following command:

   ```bash
   python server.py
   ```

The server should start and listen on port 2728.

### 4. Accessing the Web Pages

To access the default web page, open a web browser and enter the following URL:

```
http://localhost:2728
```
