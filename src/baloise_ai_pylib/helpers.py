import json
import re
import os

def get_nested_field(data, field):
    """Helper function to get nested fields."""
    keys = field.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, {})
        else:
            return None
    return data

def find_json_objects(s):
    """Find JSON objects in a string, handling nested structures."""
    objects = []
    stack = []
    start = 0
    for i, c in enumerate(s):
        if c == '{':
            if not stack:
                start = i
            stack.append(i)
        elif c == '}':
            if stack:
                stack.pop()
                if not stack:
                    objects.append(s[start:i+1])
    return objects

def extract_json_objects(s):
    """Extract JSON objects from a string, handling both wrapped and unwrapped JSON."""
    # First, extract JSON objects wrapped in ```json ... ``` blocks
    wrapped_jsons = re.findall(r'```json\n(.*?)\n```', s, re.DOTALL)
    
    # Then, find standalone JSON objects
    standalone_jsons = re.findall(r'(?<=\n)\s*(\{.*?\})\s*(?=\n)', s, re.DOTALL)
    
    # Combine both types of JSON objects
    all_jsons = wrapped_jsons + standalone_jsons
    
    return all_jsons

def string_to_json(input_file_path, output_file_path=None):
    """
    Transform the string output from apply_assistant into JSON format.

    Args:
        input_file_path (str): Path to the input file containing string output.
        output_file_path (str, optional): Path to save the transformed JSON output.
            If not provided, it will be set to input_file_path + "_clean".

    Returns:
        str: The path of the output JSON file.
    """
    # Set default output path if not provided
    if output_file_path is None:
        file_name, file_extension = os.path.splitext(input_file_path)
        output_file_path = f"{file_name}_clean{file_extension}"

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract all JSON objects
    json_blocks = extract_json_objects(content)
    
    transformed_data = []

    for json_str in json_blocks:
        json_str = json_str.strip()
        if json_str:
            try:
                # Try to parse as JSON
                json_data = json.loads(json_str)
                transformed_data.append(json_data)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {json_str}")
                transformed_data.append({
                    "raw_text": json_str,
                    "parsing_error": "Unable to parse JSON structure"
                })

    # Write the transformed data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(transformed_data, file, indent=2, ensure_ascii=False)

    print(f"Transformation complete. JSON output saved to {output_file_path}")
    return output_file_path

def join_analyzed_data(core_data_path, analyzed_path, output_path):
    """
    Join the analyzed data with the core data and save the result.

    Args:
        core_data_path (str): Path to the core JSON file.
        analyzed_path (str): Path to the analyzed JSON file.
        output_path (str): Path to save the joined JSON output.

    Returns:
        None
    """
    with open(core_data_path, 'r', encoding='utf-8') as file:
        core_data = json.load(file)

    with open(analyzed_path, 'r', encoding='utf-8') as file:
        analyzed_data = json.load(file)

    # Create a dictionary of analyzed data for easy lookup
    analyzed_dict = {item['template_id']: item for item in analyzed_data}

    # Join the data
    joined_data = []
    for item in core_data:
        template_id = item['template_id']
        if template_id in analyzed_dict:
            joined_item = {**item, **analyzed_dict[template_id]}
            joined_data.append(joined_item)
        else:
            print(f"Warning: No analyzed data found for template_id {template_id}")
            joined_data.append(item)

    # Write the joined data to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(joined_data, file, indent=2, ensure_ascii=False)

    print(f"Joined data saved to {output_path}")
