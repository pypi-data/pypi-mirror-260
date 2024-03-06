# MarkPlus

## Overview

MarkPlus is a Python package designed to simplify the process of marking 
student code for educators. With MarkPlus, educators can quickly and 
efficiently grade student assignments without the need to manually access 
and review our entire codebase.

## Features

- Automatically fetches the mark scheme from our server
- Runs the marking process on student code
- Generates feedback and marks for each student submission
- Supports easy installation and configuration

## Installation

You can install MarkPlus via pip:

```bash
pip install markplus==1.0
```

## Usage
To use MarkPlus, follow these steps:

Ensure you have the necessary environment variables set up:

- EXERCISE_NAME: The name of the assignment
- API_KEY: Your API key for accessing the server

Run the MarkPlus extension with the path to the code directory:

```bash
markplus <path to student code directory>
```
