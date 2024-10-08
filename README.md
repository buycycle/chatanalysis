# Chat Analysis
Chat Analysis is a tool that processes Sendbird chat logs within a specified timeframe and batch queries ChatGPT with a predefined prompt. The conversations are split up by a user defined maximal character length to stay in the context limit. The output are two files, the conversations and responses log files.

## Chat Analysis
Chat Analysis is a tool that processes Sendbird chat logs within a specified timeframe and batch queries ChatGPT with a predefined prompt. The conversations are split up by a user defined maximal character length to stay in the context limit. The output are two files, the conversations and responses log files.

## Installation (Updated)
1. Clone the repository:
   ```bash
   git clone git@github.com:buycycle/chatanalysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd chat-analysis
   ```
3. Ensure you have Python 3.11 installed. You can check your Python version with:
   ```bash
   python3 --version
   ```
   If Python 3.11 is not installed, you can download it from the [official Python website](https://www.python.org/downloads/).
4. Create a virtual environment named `chatanalysis` using Python 3.11:
   ```bash
   python3.11 -m venv chatanalysis
   ```
5. Activate the virtual environment:
   - On Windows:
     ```bash
     chatanalysis\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source chatanalysis/bin/activate
     ```
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Usage
1. Ensure your Sendbird chat logs are accessible.
2. Define the timeframe for analysis.
3. Run the script to process the logs and query ChatGPT:
   ```bash
   python main.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --char-limit int
   ```
# example for the last 2 days and a sensible chatGPT limit of 140000 characters
   ```bash
   python main.py --start-date $(date -d "2 days ago" +%Y-%m-%d) --end-date $(date +%Y-%m-%d) --char-limit 140000
   ```
4. The conversations will be saved in conversionts and the responses in responses log files.
## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

