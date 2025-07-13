# agent-toolCall-getTemperature

This project demonstrates how to use OpenAI's function calling (tool calling) capabilities to fetch the current temperature for a given city using a simple Python script. The code interacts with a local OpenAI-compatible API (such as Ollama) and defines a custom tool for temperature retrieval.

## Features

- Integrates with OpenAI-compatible APIs using the `openai` Python package.
- Defines a custom tool (`get_temperature`) that can be called by the assistant.
- Handles tool calls and returns results to the assistant.
- Maintains a conversation history for context-aware responses.

## How It Works

1. **Tool Definition**:  
    The `get_temperature` function is defined and described in the `tools` list. This allows the assistant to call it when needed.

2. **Tool Call Handling**:  
    When the assistant requests a tool call, the code parses the function name and arguments, executes the corresponding Python function, and appends the result to the conversation history.

3. **Conversation Loop**:  
    The `main()` function runs a loop where user input is sent to the assistant. If a tool call is requested, it is executed and the result is provided back to the assistant for a follow-up response.

4. **API Interaction**:  
    The script uses the `OpenAI` client to send messages and tool definitions to the API endpoint (`http://localhost:11434/v1`).

## Usage

1. **Install dependencies**:
    ```bash
    pip install openai
    ```

2. **Run a compatible API server** (e.g., Ollama) locally.

3. **Run the script**:
    ```bash
    python your_script.py
    ```

4. **Interact with the assistant**:  
    Type your questions (e.g., "What is the temperature in Nairobi?"). The assistant may call the `get_temperature` tool and respond with the result.

5. **Exit**:  
    Type `exit` to end the conversation.

## Example

```
Your Message (type 'Exit' to end the conversation): What is the temperature in Mombasa?
Tool call requested: get_temperature
Assistant: The current temperature in Mombasa is 20.0ºC.
Overall Assistant Reply Message: The current temperature in Mombasa is 20.0ºC.
```

## Notes

- The `get_temperature` function currently returns a static value (`20.0`). You can modify it to fetch real data from a weather API.
- The script is configured to use the `qwen3:4b` model. Adjust the model name as needed.
- Make sure your API server is running and accessible at the specified `base_url`.

## License

This project is provided for educational purposes.