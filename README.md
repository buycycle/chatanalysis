# Chat Analysis
Chat Analysis is a tool that processes Sendbird chat logs within a specified timeframe and batch queries ChatGPT with a predefined prompt. The conversations are split up by a user-defined maximal character length to stay within the context limit. The output consists of two files: the conversations and responses log files.
## Installation
1. **Install Git** (if not already installed):
   - **Windows**: Download the Git installer from the [official Git website](https://git-scm.com/download/win) and run the installer.
   - **macOS**: You can install Git using Homebrew. First, install Homebrew if you haven't already, then run:
     ```bash
     brew install git
     ```
   - **Linux**: Use the package manager specific to your distribution. For example, on Ubuntu, you can run:
     ```bash
     sudo apt update
     sudo apt install git
     ```
2. **Clone the repository**:
   ```bash
   git clone git@github.com:buycycle/chatanalysis.git
   ```
3. **Navigate to the project directory**:
   ```bash
   cd chat-analysis
   ```
4. **Ensure you have Python 3.11 installed**. You can check your Python version with:
   ```bash
   python3 --version
   ```
   If Python 3.11 is not installed, you can download it from the [official Python website](https://www.python.org/downloads/).
5. **Create a virtual environment named `chatanalysis` using Python 3.11**:
   ```bash
   python3.11 -m venv chatanalysis
   ```
6. **Activate the virtual environment**:
   - On Windows:
     ```bash
     chatanalysis\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source chatanalysis/bin/activate
     ```
7. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
## Configuration
- **Secrets**: Store your API keys and other sensitive information in `config/config.ini`.
- **Prompt**: Define the prompt for ChatGPT in `prompt.txt`.
## Usage
1. Ensure your Sendbird chat logs are accessible.
2. Define the timeframe for analysis.
3. Define a prompt in the prompt.txt.
4. Define a summary prompt in prmpt_summary.txt
3. Run the script to process the logs and query ChatGPT:
   ```bash
   python main.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --char-limit int
   ```
   Example for the a specific week and a sensible ChatGPT limit of 140,000 characters:
   ```bash
   python main.py --start-date 2024-10-21 --end-date 2024-10-27 --char-limit 140000
   ```
4. The conversations will be saved in conversations, the responses in responses, and the summary in the summary log files.
## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
## License
This project is licensed under the MIT License.
