# MyMark

## Overview

MyMark is a Python package designed to simplify the process of marking 
student code for educators. With MyMark, educators can quickly and 
efficiently grade student assignments without the need to manually access 
and review our entire codebase.

## Features

- Automatically fetches the mark scheme from our server
- Runs the marking process on student code
- Generates feedback and marks for each student submission
- Supports easy installation and configuration

## Installation

You can install MyMark via pip:

```bash
pip install mymarkv2==1.0.1
```

## Usage
To use MyMark, follow these steps:

Ensure you have the necessary environment variables set up:

- SERVER_HOST: usually 146.169.43.198
- API_KEY: Your API key for accessing the server

Run the MyMark extension with the path to the code directory:

```bash
mymark <module name> <exercise name> <code directory>
```
