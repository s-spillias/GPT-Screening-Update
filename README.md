# GPT-Screening-Update: Collaborative Intelligence Paper Review System

A web-based system for automated paper screening using various AI models. The system allows you to upload papers, define screening criteria, and use AI agents to assess papers based on those criteria.

## Features

- Web interface for paper screening management
- Support for multiple AI models (OpenAI, Gemini, Mixtral, Llama3, Claude)
- Resume capability - continues from last processed paper
- Multiple AI agents per paper for consensus
- Excel-based output with detailed assessments

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

## Setup

1. Clone the repository:
```bash
git clone https://github.com/s-spillias/GPT-Screening-Update.git
cd GPT-Screening-Update
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys:
The system supports various AI models. Create a `.env` file in the root directory and add your API keys:
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

## Usage

1. Start the server:
```bash
python server.py
```
This will automatically open your default web browser to the screening interface.

2. In the web interface:
   - Upload your papers file (Excel or CSV format)
   - Add screening criteria
   - Select AI model (OpenAI, Gemini, Mixtral, Llama3, Claude) and number of agents
   - Click "Start Screening"

3. Results will be saved in the output directory specified in the configuration.

## Key Components

- `server.py`: Flask server handling web interface and configuration
- `screening_logic.py`: Core screening logic and AI interaction
- `file_operations.py`: Helper functions for file operations
- `static/index.html`: Web interface
- `ai_interaction.py`: AI model interaction layer

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

Additional columns are preserved in the output but not used in screening.

## Output Format

The screening results Excel file contains multiple sheets:
- `screening_results_summary`: Overview with paper numbers, titles, and final decisions
- Agent sheets (0-N): Detailed assessments from each AI agent including:
  - Initial decisions
  - Final decisions
  - Detailed reasoning for each screening criterion

## Resume Capability

The system automatically detects the last processed paper and continues from there when restarted. This allows for:
- Interruption and resumption of screening
- Adding more papers to existing screenings
- Running multiple sessions over time

The resume point is determined by:
1. Reading the existing output Excel file
2. Finding the highest paper number processed
3. Continuing from the next paper

## Error Handling

- Invalid file formats are rejected with clear error messages
- Missing API keys are caught and reported
- Failed AI calls are logged and retried
- Incomplete papers are marked for review
- JSON serialization errors are handled gracefully

## Troubleshooting

Common issues:
1. "API key not found" - Check your .env file has the correct keys for your chosen model
2. "File format not supported" - Ensure input file is .xlsx, .xls, or .csv
3. "Object not JSON serializable" - This is handled internally, but if seen, restart the server
4. Excel file access errors - Close the output Excel file if it's open in another program

## Contributing

Feel free to submit issues and enhancement requests!


