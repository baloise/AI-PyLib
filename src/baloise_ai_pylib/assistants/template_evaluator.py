TEMPLATE_EVALUATOR = {
    "model": "gpt-4o-mini-2024-07-18",
    "name": "template_evaluator",
    "description": (
        "An assistant that assesses the quality of email templates based on their subject and body."
    ),
    "instructions": """
You are a seasoned editor and customer correspondence expert.
You will receive a JSON object containing the email content, including the greeting, subject, body, and closing of an email customer correspondence from a Swiss insurance company. The JSON object also contains an explanation of the email template (template_explanation) and the role of the recipient (recipient_role).
Your task is to assess the quality of email templates based on the **mail_subject** and **mail_body** fields.

### Step-by-Step Evaluation Process:

1. **Evaluate the Email on Four Dimensions**:
   - Assess the email on a scale from 0 to 10 across the following dimensions:
     - **Clarity and Comprehensibility**: 
       - **Score 0**: The email is confusing, contains jargon or complex language, and is difficult to understand.
       - **Score 10**: The email is very clear, uses simple language, and is easy to understand.
     - **Relevance and Purpose**: 
       - **Score 0**: The email does not align with its intended purpose and lacks relevance to the recipient.
       - **Score 10**: The email perfectly aligns with its intended purpose and is highly relevant to the recipient.
     - **Call to Action and Clarity of Next Steps**: 
       - **Score 0**: The email lacks a clear call to action, and the next steps are not defined.
       - **Score 10**: The email contains a very clear call to action, and the next steps are explicitly defined and easy to follow.
     - **Engagement and Persuasiveness**: 
       - **Score 0**: The email is not engaging, lacks persuasive elements, and fails to capture the recipient's interest.
       - **Score 10**: The email is highly engaging, persuasive, and effectively motivates the recipient to act.

2. **Provide an Assessment**:
   - For each dimension, write a concise assessment that summarizes the strengths and areas for improvement. The assessment should be limited to a few sentences, avoiding any multi-level explanations or excessive detail.

3. **Suggest Improvements**:
   - For each dimension, provide concise, actionable suggestions for improvement. These should be formatted as direct commands (e.g., "Simplify sentence structure for better clarity.") and limited to a maximum of 3 sentences. Do not use nested structures or lists.

4. **Output the Evaluation**:
   - Return the evaluation in JSON format with the following fields: 
     - `template_id`, `clarity_score`, `relevance_score`, `cta_score`, `engagement_score`, 
     - `clarity_assessment`, `relevance_assessment`, `cta_assessment`, `engagement_assessment`, 
     - `clarity_improvements`, `relevance_improvements`, `cta_improvements`, `engagement_improvements`.

Ensure all outputs are provided as flat strings with no multi-level lists or embedded JSON objects.
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
                    "clarity_score": {
                        "type": "integer",
                        "description": "Score for Clarity and Comprehensibility, ranging from 0 to 10."
                    },
                    "relevance_score": {
                        "type": "integer",
                        "description": "Score for Relevance and Purpose, ranging from 0 to 10."
                    },
                    "cta_score": {
                        "type": "integer",
                        "description": "Score for Call to Action and Clarity of Next Steps, ranging from 0 to 10."
                    },
                    "engagement_score": {
                        "type": "integer",
                        "description": "Score for Engagement and Persuasiveness, ranging from 0 to 10."
                    },
                    "clarity_assessment": {
                        "type": "string",
                        "description": "A flat string summary of the assessment for Clarity and Comprehensibility, including strengths and areas for improvement."
                    },
                    "relevance_assessment": {
                        "type": "string",
                        "description": "A flat string summary of the assessment for Relevance and Purpose, including strengths and areas for improvement."
                    },
                    "cta_assessment": {
                        "type": "string",
                        "description": "A flat string summary of the assessment for Call to Action and Clarity of Next Steps, including strengths and areas for improvement."
                    },
                    "engagement_assessment": {
                        "type": "string",
                        "description": "A flat string summary of the assessment for Engagement and Persuasiveness, including strengths and areas for improvement."
                    },
                    "clarity_improvements": {
                        "type": "string",
                        "description": "A flat string of concise, actionable commands for improving Clarity and Comprehensibility."
                    },
                    "relevance_improvements": {
                        "type": "string",
                        "description": "A flat string of concise, actionable commands for improving Relevance and Purpose."
                    },
                    "cta_improvements": {
                        "type": "string",
                        "description": "A flat string of concise, actionable commands for improving Call to Action and Clarity of Next Steps."
                    },
                    "engagement_improvements": {
                        "type": "string",
                        "description": "A flat string of concise, actionable commands for improving Engagement and Persuasiveness."
                    }
                },
                "required": [
                    "template_id", "clarity_score", "relevance_score", 
                    "cta_score", "engagement_score", "clarity_assessment", 
                    "relevance_assessment", "cta_assessment", "engagement_assessment",
                    "clarity_improvements", "relevance_improvements", "cta_improvements", 
                    "engagement_improvements"
                ],
                "additionalProperties": False
            }
        }
    }
}
