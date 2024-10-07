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
    ORDER BY conversation_id, created_at ASC
) AS ordered_data
GROUP BY conversation_id
ORDER BY message_count DESC;

