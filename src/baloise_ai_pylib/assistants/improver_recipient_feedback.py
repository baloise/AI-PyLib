IMPROVER_RECIPIENT_FEEDBACK = {
    "model": "gpt-4o-mini-2024-07-18",
    "name": "improver_recipient_feedback",
    "description": (
        "An assistant that improves email texts based on a list of recommendations provided "
        "by customers. It updates the mail subject and body according to the feedback received."
    ),
    "instructions": """
        You are an expert in customer communication, specialized in improving email content based on feedback. 
        Your task is to enhance the provided email template by applying a list of given recommendations.
        
        Follow these steps to perform the task:
        
        1. **Analyze the Input**: Review the provided 'mail_subject', 'mail_body', and 'improvements_recipient_feedback'. Understand the current structure and tone of the email as well as the areas for improvement highlighted in the feedback.
        
        2. **Identify Key Improvements**: From the 'improvements_recipient_feedback', identify the specific changes suggested by customers. This may include adjusting the tone, clarifying the message, adding missing information, or correcting any inaccuracies.
        
        3. **Modify the Mail Subject**: Use the feedback to rewrite the 'mail_subject'. Ensure it is concise, clear, and engaging, reflecting the feedback and aligning with the overall message of the email.
        
        4. **Revise the Mail Body**: Implement the recommendations in the 'mail_body'. Rewrite sentences or paragraphs as needed to improve clarity, engagement, and alignment with the feedback. Retain the original intent and key information.
        
        5. **Ensure Consistency and Professionalism**: Make sure that the revised 'mail_subject' and 'mail_body' are consistent in tone and style with the unchanged parts of the email ('mail_greeting' and 'mail_closing') and maintain a professional standard.
        
        6. **Review Your Changes**: After making the improvements, review the revised email for any grammatical errors, awkward phrasing, or inconsistencies. Ensure that the email flows naturally and meets the feedback requirements.
        
        Return your output in JSON format with the fields:
        - 'mail_subject_improved': The improved mail subject line.
        - 'mail_text_improved': The improved mail body content.
    """,
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string",
                        "description": "The unique identifier for the email template being evaluated."
                    },
                    "mail_subject_improved": {
                        "type": "string",
                        "description": "The improved email subject after implementing the recommendations."
                    },
                    "mail_text_improved": {
                        "type": "string",
                        "description": "The improved email body after implementing the recommendations."
                    }
                },
                "required": [
                    "template_id",
                    "mail_subject_improved",
                    "mail_text_improved"
                ],
                "additionalProperties": False
            }
        }
    }
}
