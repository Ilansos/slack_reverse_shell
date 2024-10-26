# Reverse Shell on Slack

## Overview

This project demonstrates how a "reverse shell" can be executed via Slack, highlighting potential security vulnerabilities when using chat platforms for command execution. The bot listens for specific messages in a designated Slack channel and executes them as shell commands on the host machine.

This script is intended for cybersecurity research purposes only. It should not be used in production environments or without proper authorization. Misuse of this code could result in severe security risks.

Prerequisites

    Python 3.7+
    Slack API tokens (bot token and app-level token)
    A specific Slack channel to send commands from
    Necessary permissions in your Slack workspace for the bot to read and send messages

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ilansos/slack_reverse_shell.git
cd slack-reverse-shell
```

### 2. Install Dependencies

You can use the provided requirements.txt to install all necessary dependencies. Run the following command:

```bash
pip install -r requirements.txt
```

### 3. Set up Slack App and Bot

**Step 1: Create a Slack App**

    Go to Slack API:
    Navigate to https://api.slack.com/apps and click the Create New App button.

    Choose a Method:
        Select From Scratch.
        Give your app a name (e.g., "MyCommandBot").
        Select the Slack workspace where you want to install the bot.
        Click Create App.

**Step 2: Configure Bot User**

    Enable Bot Features:
        In your app's configuration page, go to the Features section on the left menu and click on OAuth & Permissions.
        Scroll down to Scopes and find Bot Token Scopes. These define what your bot can do.

    Add Bot Token Scopes:
    Here are the key permissions (scopes) you should add:
        channels:history: To read messages in public channels.
        channels:read: To list and access public channels.
        chat:write: To post messages in channels.
        im:history: To read direct messages.
        im:write: To send direct messages.
        groups:history: To read messages in private channels.
        groups:read: To list and access private channels.

    Install Your App to the Workspace:
        After adding the necessary scopes, scroll back to the top and click the Install App to Workspace button.
        Slack will ask you to authorize the app with the permissions you've set. Click Allow.

**Step 3: Retrieve Bot User OAuth Token**

    Get Bot User OAuth Token:
    After installing the app, you'll be redirected to a page where you can find your Bot User OAuth Token. Copy this token as you will use it in your Python script (set it as SLACK_BOT_TOKEN).

**Step 4: Enable Socket Mode for Real-Time Events**

    Enable Socket Mode:
        On the left-hand menu, click Socket Mode under the Features section.
        Enable Socket Mode by clicking the toggle switch.

    Create an App-Level Token:
        You will need an App-Level Token to use Socket Mode.
        Click the Create App-Level Token button.
        Give the token a name (e.g., "SocketModeToken").
        Set the scope to connections
        .
        Click Create and copy the token. This is the App-Level Token that will be used in your script as SLACK_APP_TOKEN.

**Step 5: Subscribe to Events**

    Enable Event Subscriptions:
        On the left-hand menu, click Event Subscriptions under the Features section.
        Toggle Enable Events to On.

    Add Events:
        Under the Subscribe to Bot Events section, click Add Bot User Event.
        Add the following events:
            message.channels: To receive messages from public channels.
            message.groups: To receive messages from private channels.
            message.im: To receive direct messages.
        Save your changes.

    Enable Interaction:
        Go to the Interactivity & Shortcuts section on the left-hand menu.
        Toggle Interactivity to On.
        You can leave the Request URL empty for now, but if you want the bot to respond to button clicks or shortcuts in the future, you'll need this URL.

### 4. Set Your Tokens and Channel ID

Before running the script, you need to export the following environment variables to ensure proper authentication and configuration. These variables are required for the script to communicate with necessary services securely.

It is recommended to use a secrets manager to keep the tokens safe, but for testing purposes they can be exported into the shell:

**Linux:**
```bash
export SLACK_BOT_TOKEN="your-slack-bot-token"
export SLACK_APP_TOKEN="your-slack-app-token"
export CHANNEL_ID="your-channel-id"
```

**Windows:**

#### Using Command Prompt (CMD):
```cmd
set SLACK_BOT_TOKEN=your_slack_bot_token
set SLACK_APP_TOKEN=your_slack_app_token
set CHANNEL_ID=your-channel-id
```
#### Using PowerShell:
```powershell
$env:SLACK_BOT_TOKEN="your_slack_bot_token"
$env:SLACK_APP_TOKEN="your_slack_app_token"
$env:CHANNEL_ID="your-channel-id"
```

### 5. Run the Script

```bash
python slack_reverse_shell.py
```

### 6. Sending Commands via Slack

Once the bot is running, you can send commands in the specified Slack channel. To execute a command, start the message with the keyword run followed by the shell command.

For example:

```bash
run ls -la
```

The bot will respond with the output of the command in the same channel.

## Important Notes

The script currently uses subprocess.run() with shell=True, which poses a command injection vulnerability. It is recommended to use the script for educational purposes only.
Make sure that the bot has only the necessary permissions in your Slack workspace, and avoid adding it to channels where untrusted users may be present.
Security Warning: This bot can execute any command sent to it. Running it in a production environment without safeguards is extremely dangerous and may expose your system to critical vulnerabilities.

## License

This project is licensed under the MIT License. See the LICENSE file for details.