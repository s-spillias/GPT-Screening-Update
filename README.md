# GPT-Screening-Update: Collaborative Intelligence Paper Review System

A web-based system for automated paper screening using various AI models. This system allows you to upload papers, define screening criteria, and use AI agents to assess papers based on those criteria.

## Table of Contents
1. [Introduction to Python](#introduction-to-python)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Detailed Setup Guide](#detailed-setup-guide)
5. [Usage](#usage)
6. [Using the Pilot](#using-the-pilot)
7. [Key Components](#key-components)
8. [File Structure](#file-structure)
9. [Input Format](#input-format)
10. [Output Format](#output-format)
11. [Resume Capability](#resume-capability)
12. [Error Handling](#error-handling)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)

## Introduction to Python

This project is built using Python, a high-level programming language known for its simplicity and readability. If you're new to Python, here are some key points:

- Python is interpreted, meaning you don't need to compile your code before running it.
- It uses indentation to define code blocks, which contributes to its clean and readable syntax.
- Python has a large standard library and an even larger ecosystem of third-party packages, which we'll be using in this project.

In this project, Python is used to handle the backend logic, process data, and interact with AI models.

## Features

- Web interface for paper screening management
- Support for multiple AI models (OpenAI, Gemini, Mixtral, Llama3, Claude)
- Resume capability - continues from last processed paper
- Multiple AI agents per paper for consensus
- Excel-based output with detailed assessments
- Pilot mode for initial screening and criteria refinement

## Requirements

- Python 3.x
- Required Python packages (installed via requirements.txt):
  - Flask (2.3.3) - Web server
  - pandas (2.1.0) - Data handling
  - python-dotenv (1.0.0) - Environment management
  - openai (1.12.0) - OpenAI API integration
  - groq (0.4.2) - Groq API for Mixtral/Llama3
  - boto3 (1.34.34) - AWS integration
  - openpyxl (3.1.2) - Excel file handling
  - xlrd (2.0.1) - Excel reading
  - PyPDF2 (3.0.1) - PDF processing
  - requests (2.31.0) - HTTP requests
  - anthropic (0.18.1) - Claude API
  - google-generativeai (0.3.2) - Gemini API

## Detailed Setup Guide

### 1. Install Python

If you don't have Python installed:

a. Visit the [official Python website](https://www.python.org/downloads/).
b. Download the latest version of Python 3 for your operating system.
c. Run the installer and follow the installation wizard. Make sure to check the box that says "Add Python to PATH" during installation.

To verify the installation, open a command prompt or terminal and type:
```bash
python --version
```
You should see the Python version number.

### 2. Install Git

If you don't have Git installed:

a. Visit the [official Git website](https://git-scm.com/downloads).
b. Download the version for your operating system.
c. Run the installer and follow the installation wizard.

To verify the installation, open a command prompt or terminal and type:
```bash
git --version
```
You should see the Git version number.

### 3. Clone the Repository

Open a command prompt or terminal and run:

```bash
git clone https://github.com/s-spillias/GPT-Screening-Update.git
cd GPT-Screening-Update
```

This downloads the project to your computer and navigates into the project directory.

### 4. Set Up a Virtual Environment (Optional but Recommended)

A virtual environment is an isolated Python environment that helps manage dependencies for different projects. To create and activate a virtual environment:

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see (venv) at the beginning of your command prompt, indicating the virtual environment is active.

### 5. Install Dependencies

With your virtual environment activated (if you're using one), run:

```bash
pip install -r requirements.txt
```

This command reads the requirements.txt file and installs all the necessary Python packages for the project.

### 6. Set Up API Keys

The system supports various AI models. Create a `.env` file in the root directory of the project and add your API keys:

```env
# For OpenAI
OPENAI_API_KEY=your_key_here

# For Gemini
GOOGLE_API_KEY=your_key_here

# For Mixtral/Llama3/Gemma2
GROQ_API_KEY=your_key_here

# For Claude
ANTHROPIC_API_KEY=your_key_here

# For AWS Claude
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_key_here
```

Note: The `.env` file is not included in the repository for security reasons. Make sure to create it locally and never commit it to version control.

To obtain these API keys, you'll need to sign up for accounts with the respective AI service providers and generate API keys through their developer portals. Note, you can get a free Google and Groq account which could cover smaller screens. Whereas OpenAI and Antrhopic accounts will require setting up credit card details and likely cost ~ 100 USD for a 1000 paper screen.

## Usage

1. Start the server:
```bash
python server.py
```
This will automatically open your default web browser to the screening interface. If it doesn't, you can manually open a browser and go to `http://localhost:5000` (or the URL displayed in the terminal).

2. In the web interface:
   - Upload your papers file (Excel or CSV format): Click on the "Choose File" button and select your file.
   - Add screening criteria: Enter your criteria in the provided text area, one per line, or you can upload a csv/excel file.
   - Select AI model: Choose from OpenAI, Gemini, Mixtral, Llama3, or Claude using the dropdown menu.
   - Set number of agents: Enter the number of AI agents you want to use for consensus.
   - Click "Start Screening": This will begin the screening process.

3. Results will be saved in the output directory specified in the configuration. You can find the Excel file with the screening results in this directory once the process is complete.

### Screening Criteria Format

To upload your screening criteria, use the following Excel template format:

| A | B | C |
|-----------------|----------|----------|
| Criteria type:  | Included: | Excluded: |
| E.g. Geographic location | If the study area includes the ... | Studies that do not include... |
| ... | ... | ... |

Save this as an Excel file (.xlsx) and upload it in the web interface. Here's what each column represents:

- Column A (Criteria type): Specifies the type of criterion (e.g., Geographic location, Study type, etc.)
- Column B (Included): Describes the inclusion criteria for this type
- Column C (Excluded): Describes the exclusion criteria for this type

Each row after the header represents a different criterion. You can add as many criteria as needed.

## Using the Pilot

The pilot mode allows for an initial review of a subset of papers to help fine-tune your screening criteria. Here's how to use it:

1. Start the server as described in the Usage section.

2. In the web interface, locate the "Use Pilot" option.

3. Set a percentage of papers for the AI to review. This determines how many papers will be screened in the pilot mode.

4. Start the screening process. The AI will review the specified percentage of papers using your initial screening criteria.

5. After the pilot screening is complete, review the results to gain insights into how well your criteria are working.

6. Based on these initial results, you can refine your screening criteria to improve accuracy and relevance.

7. Once you're satisfied with the adjusted criteria, you can proceed with screening the full set of papers.

The pilot mode is particularly useful for:
- Getting a quick overview of how your screening criteria perform on a sample of papers
- Identifying potential issues or ambiguities in your criteria
- Making informed adjustments to your criteria before running a full screening

This approach helps ensure that your full screening process is as effective and efficient as possible.

## Key Components

- `server.py`: Flask server handling web interface and configuration. This is the main entry point of the application.
- `screening_logic.py`: Core screening logic and AI interaction. This file contains the main algorithms for paper screening.
- `file_operations.py`: Helper functions for file operations, such as reading and writing Excel files.
- `static/index.html`: Web interface that users interact with in their browser.
- `ai_interaction.py`: AI model interaction layer, handling communication with various AI APIs.

## File Structure

```
GPT-Screening-Update/
├── server.py           # Web server
├── screening_logic.py  # Core screening logic
├── file_operations.py  # Helper functions
├── ai_interaction.py   # AI interaction
├── data_processing.py  # Data processing functions
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── static/            
│   ├── index.html     # Web interface
│   └── script.js      # Frontend JavaScript
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Input Format

The input file (Excel/CSV) should contain at least:
- Title column: Paper titles
- Abstract column: Paper abstracts

Additional columns are preserved in the output but not used in screening. Make sure your input file follows this format to ensure proper functioning of the system.

## Output Format

The screening results Excel file contains multiple sheets:
- `screening_results_summary`: Overview with paper numbers, titles, and final decisions
- Agent sheets (0-N): Detailed assessments from each AI agent including:
  - Initial decisions
  - Final decisions
  - Detailed reasoning for each screening criterion

You can open this Excel file to view the results after the screening process is complete.

## Resume Capability

The system automatically detects the last processed paper and continues from there when restarted. This allows for:
- Interruption and resumption of screening
- Adding more papers to existing screenings
- Running multiple sessions over time

The resume point is determined by:
1. Reading the existing output Excel file
2. Finding the highest paper number processed
3. Continuing from the next paper

This feature is particularly useful for large screening tasks that may take multiple sessions to complete.

## Error Handling

The system includes several error handling mechanisms to ensure smooth operation:
- Invalid file formats are rejected with clear error messages
- Missing API keys are caught and reported
- Failed AI calls are logged and retried
- Incomplete papers are marked for review
- JSON serialization errors are handled gracefully

If you encounter an error, check the console output for more information about what went wrong.

## Troubleshooting

Here are some common issues you might encounter and how to resolve them:

1. "API key not found" 
   - Check your `.env` file to ensure it contains the correct keys for your chosen model.
   - Make sure the `.env` file is in the root directory of the project.
   - Double-check that you've spelled the API key names correctly in the `.env` file.

2. "File format not supported" 
   - Ensure your input file is in .xlsx, .xls, or .csv format.
   - Check that your file contains at least a 'Title' and an 'Abstract' column.

3. "Object not JSON serializable" 
   - This is handled internally, but if you see this error, try restarting the server.
   - If the error persists, check your input data for any unusual characters or formatting.

4. Excel file access errors 
   - Close the output Excel file if it's open in another program.
   - Ensure you have write permissions in the directory where the output file is being saved.

5. "ModuleNotFoundError" when running the server
   - This usually means a required package is not installed. Make sure you've run `pip install -r requirements.txt`.
   - If using a virtual environment, ensure it's activated before running the server.

6. The web interface doesn't open automatically
   - Try manually opening a web browser and navigating to `http://localhost:5000`.
   - Check the console output for any error messages or a different URL.

7. AI model not responding
   - Verify that you have a stable internet connection.
   - Check that your API keys are correct and have sufficient credits/quota.

If you encounter any other issues, feel free to open an issue on the GitHub repository with a detailed description of the problem and any error messages you're seeing.

## Contributing

Feel free to submit issues and enhancement requests! If you're new to contributing to open source projects, here are some steps to get started:

1. Fork the repository on GitHub.
2. Clone your fork to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them with a clear commit message.
5. Push your changes to your fork on GitHub.
6. Create a pull request from your fork to the original repository.

We appreciate all contributions, whether it's code, documentation, or bug reports!
