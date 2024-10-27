# Charter Tickets Monitor

This is a Python script designed to monitor selected flight ticket prices from a specified website and send periodic updates via Telegram. It continuously checks ticket prices for specific dates and provides the results directly to your configured Telegram chat.

## Features
- Scrapes flight ticket prices from a target website.
- Sends updates to a Telegram chat.
- Utilizes async features for non-blocking I/O operations.
- Randomized intervals for scraping to reduce likelihood of being detected as a bot.

## Setup

### Prerequisites
- Python 3.7 or later
- A Telegram bot token and chat ID
- Appropriate permissions to install dependencies

### Steps

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd tickets-bot
   ```
2. **Install dependencies**:
Using pip, install all the required packages:


   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Telegram Bot**:
Open `tickets-bot.py` and replace `YOUR_BOT_TOKEN_HERE` and `YOUR_CHAT_ID_HERE` with your bot’s token and chat ID.

4. **Customize Departure and Destination**:
In `tickets-bot.py`  adjust the following constants to customize your desired route:
    ```bash
    DEPARTURE_CITY = "Tehran"  # Replace with your departure city
    DESTINATION_CITY = "Istanbul"  # Replace with your destination city
    ```

5. **Running the Script**:

On Linux: To run in the background, you can use nohup or screen:

- Using nohup:

    ```bash
    nohup python charter-tickets.py &
    ```

- Using screen:

    ```bash
    screen -S tickets-bot
    python charter-tickets.py

    # To detach from the screen session, press Ctrl+A followed by D.
    # To reattach, use:
    screen -r tickets-bot
    ```

- On Windows: To run as a background job, you can use the start command in cmd:

In Command Prompt:

    ```bash
    start python charter-tickets.py
    ```
Alternatively, create a batch script (run.bat):

    ```bash
    @echo off
    start python charter-tickets.py
    exit
    ```

Run run.bat to start the script in a new window.

## Troubleshooting

- Ensure all dependencies are installed correctly.
- If you encounter any errors with invalid tokens or chat IDs, verify them with Telegram's BotFather.
- Check that your system's Python environment is correctly set up to access the necessary web resources.

## License

This project is licensed under the MIT License.