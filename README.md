# Chat Analysis
Chat Analysis is a tool that processes Sendbird chat logs within a specified timeframe and batch queries ChatGPT with a predefined prompt. The output is a JSON file containing the responses from ChatGPT.
## Features
- Extracts chat logs from Sendbird within a defined timeframe.
- Batch processes conversations and queries ChatGPT.
- Outputs responses in a structured JSON format.
## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:buycycle/chatanalysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd chat-analysis
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage
1. Ensure your Sendbird chat logs are accessible.
2. Define the timeframe for analysis.
3. Run the script to process the logs and query ChatGPT:
   ```bash
   python main.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD
   ```
4. The output JSON file with ChatGPT responses will be saved in the specified directory.
## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

