import os
import pandas as pd
import argparse
import configparser
from buycycle.data import sql_db_read
import openai
import json
from datetime import datetime
# Read configuration
config = configparser.ConfigParser()
config.read("config/config.ini")
# Set your OpenAI API key from the config file
openai.api_key = config.get("openai", "api_key")
model = config.get("openai", "model")
def build_query(start_date, end_date):
    """Build the SQL query for fetching chat logs."""
    return f"""
SELECT
    conversation_id,
    JSON_ARRAYAGG(
        JSON_OBJECT(
            'sent_by', ordered_data.sent_by,
            'user_type',
                CASE
                    WHEN ordered_data.sent_by = ordered_data.buyer_id THEN 'buyer'
                    WHEN ordered_data.sent_by = ordered_data.seller_id THEN 'seller'
                END,
            'message_type', ordered_data.message_type,
            'message_en',
                CASE
                    WHEN ordered_data.message_type = 'message' THEN ordered_data.message_en
                    WHEN ordered_data.message_type = 'offer' AND ordered_data.sent_by = ordered_data.seller_id THEN CONCAT('offer seller: ', ordered_data.current_seller_offer)
                    WHEN ordered_data.message_type = 'offer' AND ordered_data.sent_by = ordered_data.buyer_id THEN CONCAT('offer buyer: ', ordered_data.current_buyer_offer)
                    ELSE NULL
                END,
            'character_count',
                CASE
                    WHEN ordered_data.message_type = 'message' THEN CHAR_LENGTH(ordered_data.message_en)
                    ELSE NULL
                END,
            'offer',
                CASE
                    WHEN ordered_data.message_type != 'message' AND ordered_data.sent_by = ordered_data.seller_id THEN ordered_data.current_seller_offer
                    WHEN ordered_data.message_type != 'message' AND ordered_data.sent_by = ordered_data.buyer_id THEN ordered_data.current_buyer_offer
                    ELSE NULL
                END,
            'sent_at', ordered_data.created_at
        )
    ) AS conversation_data,
    COUNT(*) AS message_count,
    SUM(
        CASE
            WHEN ordered_data.message_type = 'message' THEN CHAR_LENGTH(ordered_data.message_en)
            ELSE 0
        END
    ) AS total_character_count
FROM (
    SELECT * FROM sendbird_message_logs
    WHERE created_at BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY conversation_id, created_at ASC
) AS ordered_data
GROUP BY conversation_id
HAVING total_character_count >= 50
ORDER BY created_at DESC
    """
def get_chat_logs(start_date, end_date):
    """Fetch chat logs from the database."""
    query = build_query(start_date, end_date)
    df = sql_db_read(
        query=query,
        DB="DB_LOG",
        config_paths="config/config.ini",
        index_col="conversation_id",
    )
    return df
def send_conversation_to_chatgpt(conversation, prompt):
    input_text = f"{prompt}\n\n{conversation}"
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text},
            ],
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def send_summary_request_to_chatgpt(responses, prompt):
    input_text = f"{prompt}\n\n{responses}"
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text},
            ],
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"An error occurred while summarizing: {e}")
        return None
def main(start_date, end_date, char_limit):
    with open("prompt.txt", "r") as file:
        prompt = file.read().strip()
    with open("prompt_summary.txt", "r") as file:
        prompt_summary = file.read().strip()
    df = get_chat_logs(start_date, end_date)
    total_conversations = len(df)
    print(f"Total conversations to process: {total_conversations}")
    # Create log files for conversations, responses, and summary
    conversation_log_filename = f"conversations_{start_date}_to_{end_date}.log"
    response_log_filename = f"responses_{start_date}_to_{end_date}.log"
    summary_log_filename = f"summary_{start_date}_to_{end_date}.log"
    with open(conversation_log_filename, "w") as conv_log_file, open(
        response_log_filename, "w"
    ) as resp_log_file:
        conv_log_file.write(f"Total conversations: {total_conversations}\n\n")
        resp_log_file.write(f"prompt: {prompt}\n\n")
        resp_log_file.write(f"Total conversations: {total_conversations}\n\n")
        current_bundle = []
        current_char_count = 0
        all_responses = []
        # Check if df is a DataFrame
        if isinstance(df, pd.DataFrame):
            for i, row in df.iterrows():
                conversation_data = json.loads(row["conversation_data"])
                conversation_text = "\n".join(
                    f"{msg['user_type'].capitalize()} ({msg['sent_by']}): {msg['message_en']}"
                    for msg in conversation_data
                    if msg["message_en"] is not None
                )
                conv_log_file.write(
                    f"Conversation {i+1}/{total_conversations}:\n{conversation_text}\n\n"
                )
                print(
                    f"Processing conversation {i+1}/{total_conversations} with {row['total_character_count']} characters."
                )
                if current_char_count + row["total_character_count"] <= char_limit:
                    current_bundle.append(conversation_text)
                    current_char_count += row["total_character_count"]
                else:
                    # Send the current bundle to ChatGPT
                    if current_bundle:
                        bundled_text = "\n\n".join(current_bundle)
                        print(f"Sending bundled conversations to ChatGPT...")
                        response = send_conversation_to_chatgpt(bundled_text, prompt)
                        if response:
                            print(f"Response for bundled conversations:\n{response}\n")
                            resp_log_file.write(
                                f"Response for bundled conversations:\n{response}\n\n"
                            )
                            all_responses.append(response)
                    # Reset the bundle and add the current conversation
                    current_bundle = [conversation_text]
                    current_char_count = row["total_character_count"]
        else:
            print(
                "Unexpected data structure for df. Please check the output of get_chat_logs."
            )
        # Send any remaining conversations in the last bundle
        if current_bundle:
            bundled_text = "\n\n".join(current_bundle)
            print(f"Sending final bundled conversations to ChatGPT...")
            response = send_conversation_to_chatgpt(bundled_text, prompt)
            if response:
                print(f"Response for final bundled conversations:\n{response}\n")
                resp_log_file.write(
                    f"Response for final bundled conversations:\n{response}\n\n"
                )
                all_responses.append(response)
        # Send all responses to ChatGPT for summarization
        if all_responses:
            responses_text = "\n\n".join(all_responses)
            print("Sending responses to ChatGPT for summarization...")
            summary = send_summary_request_to_chatgpt(responses_text, prompt_summary)
            if summary:
                print(f"Summary:\n{summary}\n")
                with open(summary_log_filename, "w") as summary_file:
                    summary_file.write(f"prompt_summary: {prompt_summary}\n\n")
                    summary_file.write(f"Total responses: {len(all_responses)}\n\n")
                    summary_file.write(summary)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process chat logs within a date range."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        required=True,
        help="The start date in YYYY-MM-DD format",
    )
    parser.add_argument(
        "--end-date", type=str, required=True, help="The end date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--char-limit",
        type=int,
        required=True,
        help="Character limit for bundling messages",
    )
    args = parser.parse_args()
    # Validate date format
    try:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(args.end_date, "%Y-%m-%d").date()
    except ValueError as e:
        print(f"Invalid date format: {e}")
        exit(1)
    main(start_date, end_date, args.char_limit)

