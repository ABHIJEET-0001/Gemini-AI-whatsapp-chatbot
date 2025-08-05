# Twilio-OpenAI-WhatsApp-Bot

This repo contains code to build a chatbot in Python that runs in WhatsApp and answers user messages using OpenAI API. Developed with FastAPI and we use Twilio for Business WhatsApp integration. The source code is available on GitHub under an open-source license.

## Tech stack:
- Python
- Docker
- FastAPI
- Twilio
- OpenAI API
- Redis

## Getting Started

To get started, follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:Shakurova/Twilio-OpenAI-WhatsApp-Bot.git
   cd Twilio-OpenAI-WhatsApp-Bot/
   ```

2. Setting up Twilio

   - **Twilio Sandbox for WhatsApp**: Start by setting up the Twilio Sandbox for WhatsApp to test your application. This allows you to send and receive messages using a temporary WhatsApp number provided by Twilio. Follow the steps in the Twilio Console under the "Messaging" section to configure the sandbox. You can find detailed instructions in the [Twilio Blog Guide](https://www.twilio.com/en-us/blog/ai-chatbot-whatsapp-python-twilio-openai).

   - **Moving to Production**: Once you have tested your application in the sandbox environment and are ready to go live, you can set up a Twilio phone number for production use. This involves purchasing a Twilio number and configuring it to handle WhatsApp messages. Refer to [Twilio Guide](https://www.twilio.com/docs/whatsapp) for more information on transitioning to a production environment.

3. Make sure you have docker and redis installed on your machine.

   For macOS:
   Install Redis using Homebrew:
   ```bash
   brew install redis
   ```
   Start Redis:
   ```bash
   brew services start redis
   ```

   Install Docker via Homebrew:
   ```bash
   brew install --cask docker
   Open Docker Desktop and make sure it’s running.
   ```
   Verify installation:
   ```bash
   docker --version
   ```

4. Create a `.env` file in the project directory and set your OpenAI API key and Twilio account details as environment variables:
   ```plaintext
    TWILIO_WHATSAPP_NUMBER=<your Twilio phone number>
    TWILIO_ACCOUNT_SID=<your Twilio account SID>
    TWILIO_AUTH_TOKEN=<your Twilio auth token>
    OPENAI_API_KEY=<your OpenAI API key>
    REDIS_HOST=<your redis host>
    REDIS_PORT=<your redis port>
    REDIS_PASSWORD=<your redis password>
   ```

5. Build and start the chatbot containers by running:
   ```bash
   docker-compose up --build -d
   ```