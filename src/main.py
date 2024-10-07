import openai
import json
# Set your OpenAI API key
openai.api_key = 'your-api-key-here'
def send_conversation_to_chatgpt(conversation, prompt):
    # Combine the prompt with the conversation
    input_text = f"{prompt}\n\n{conversation}"

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or another model of your choice
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ]
        )

        # Extract the response text
        reply = response['choices'][0]['message']['content']
        return reply

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def main():
    # Define your prompt
    prompt = "Please analyze the following conversation and provide insights."
    # run logs query

    # Parse the JSON data
    conversations = json.loads(json_data)
    # Number of conversations to send
    n = 2  # or any number you want
    # Send each conversation to ChatGPT
    for i, conversation in enumerate(conversations[:n]):
        conversation_text = "\n".join(
            f"{msg['user_type'].capitalize()} ({msg['sent_by']}): {msg['message_en']}"
            for msg in conversation['conversation_data']
            if msg['message_en'] is not None
        )
        print(f"Sending conversation {i+1} to ChatGPT...")
        response = send_conversation_to_chatgpt(conversation_text, prompt)
        if response:
            print(f"Response for conversation {i+1}:\n{response}\n")
if __name__ == "__main__":
    main()

