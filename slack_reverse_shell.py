import os
import subprocess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Slack bot token and App-level token
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')
# Define your specific channel ID where the bot will respond
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)
socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=client)

# Function to execute commands
def execute_command(command):
    logging.info(f"Executing command: {command}")
    try:
        # Detect operating system and set the appropriate encoding
        encoding = 'utf-8' if sys.platform != "win32" else 'cp1252'

        # Add errors="ignore" to handle any problematic characters
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding=encoding, errors="ignore")

        if result.returncode == 0:
            logging.info(f"Command executed successfully: {command}")
            return result.stdout
        else:
            logging.error(f"Error executing command: {result.stderr}")
            return f"Error executing command: {result.stderr}"
    except Exception as e:
        logging.exception(f"Failed to run the command: {command}")
        return f"Failed to run the command: {str(e)}"

# Function to handle messages
def handle_message(event):
    channel_id = event["channel"]
    user = event["user"]
    text = event.get("text", "")

    # Ignore bot's own messages
    if "bot_id" in event:
        logging.debug("Ignored bot's own message.")
        return

    # Only respond if the message is in the specific channel
    if channel_id == CHANNEL_ID:
        # If the message starts with "run", treat it as a command
        if text.lower().startswith("run"):
            command = text[3:].strip()
            if command:
                logging.info(f"Command detected: {command}")
                output = execute_command(command)
                try:
                    logging.info(f"Sending command output to channel {channel_id}")
                    client.chat_postMessage(channel=channel_id, text=f"```\n{output}\n```")
                except SlackApiError as e:
                    logging.error(f"Error posting message: {e.response['error']}")
            else:
                logging.warning("No command detected after 'run' keyword.")
        else:
            logging.debug("Message did not start with 'run'.")
    else:
        logging.debug(f"Message received in a different channel: {channel_id}")

def process_slack_events(client, req: SocketModeRequest):
    if req.type == "events_api" and req.payload["event"]["type"] == "message":
        handle_message(req.payload["event"])
        client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
    else:
        logging.debug(f"Received non-message event: {req.type}")


# Start listening to events
if __name__ == "__main__":
    logging.info("Starting Slack bot...")
    socket_client.socket_mode_request_listeners.append(process_slack_events)
    socket_client.connect()

    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        logging.info("Shutting down Slack bot...")