Amazon Shift Finder Bot

🚀 Overview

The Amazon Shift Finder Bot is a powerful automation tool designed to streamline the process of finding and booking desirable shifts on the Amazon hiring portal. It eliminates the need for constant manual checking, helping job seekers secure shifts more efficiently across multiple locations.

✨ Features
Multi-Location Scanning: Automatically cycles through all configured Amazon job locations, checking for available shifts.
Automated Application: Fills in required application details (postal code, city, work hours, time preferences, duration, start time) and attempts to book shifts.
Silent Operation: Runs in a headless browser, meaning no browser window pops up, allowing for background operation without disturbance.
Real-time Status Updates: Provides live feedback on the bot's activities directly within its intuitive Graphical User Interface (GUI).
Configurable Preferences: Easily adjust preferences for weekly hours, time of day, shift duration, and preferred start time via a `job_config.json` file.
Adjustable Retry Interval: The bot retries checking for shifts across all locations at a user-defined interval (currently 2 seconds) if no shifts are found.
No Disturbing Sounds: Operates without any error notification sounds, ensuring a quiet experience.

💻 Technologies Used

This bot is built using a robust stack of Python libraries and tools:

Python: The core programming language orchestrating all bot functionalities, from data processing to web interaction and GUI management.
Selenium WebDriver: Essential for browser automation, allowing the bot to interact with web elements, navigate pages, fill forms, and click buttons on the Amazon hiring website just like a human user.
Tkinter: Python's standard GUI toolkit, used to create the simple, interactive graphical interface for starting, stopping, and monitoring the bot's status.
PyInstaller: Utilized to package the entire Python application and its dependencies into a single, standalone executable (`.exe`), making it easily distributable and runnable without requiring a Python environment installation on the client's machine.

🛠️ Setup and Installation

Follow these steps to set up and run the Amazon Shift Finder Bot:

1. Prerequisites

* Python 3.x installed on your system.
* Google Chrome browser installed (the bot uses ChromeDriver, which Selenium manages).

2. Clone the Repository

git clone [https://github.com/](https://github.com/)[Your GitHub Username]/[Repository Name].git
cd [Repository Name]

3. Install Dependencies
It's recommended to use a virtual environment:

python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

4. Configuration (job_config.json)
The bot's behavior, including locations and job preferences, is controlled via the gui/job_config.json file.

Running the Bot
A. From Source (for developers)

python main.py

B. Building an Executable (.exe) (for clients/distribution)
To create a standalone executable for easy distribution:

pyinstaller --onefile --noconsole --add-data "gui/job_config.json;gui" --add-data "gui/assets;gui/assets" main.py

After successful execution, the main.exe file will be found in the dist/ directory. This executable can be run on any Windows machine without Python installed.
