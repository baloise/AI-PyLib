import os
import time
import json
from openai import OpenAI
from typing import Optional, Dict, Any, List
import logging
from tqdm import tqdm
from baloise_ai_pylib.config import TEMPERATURE, TOP_P, RATE_LIMIT, PARALLEL_REQUEST_LIMIT, RUN_WAIT_TIME, RUN_MAX_RETRIES
from concurrent.futures import ThreadPoolExecutor, as_completed
from.helpers import get_nested_field

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.getLogger("openai").setLevel(logging.
# WARNING)

def apply_assistant(assistant:dict[str, Any], input_data_path:str, input_fields:List[str], output_data_path:str, sleep_time:int=60, rate_limit:int=RATE_LIMIT, use_parallel:bool=True) -> None:
    """
    Apply an AI assistant to process input data and save the raw results.
    Can operate in both sequential and parallel modes.

    Args:
        assistant: dictionary describing the assistant.
        input_data_path (str): The file path of the input JSON data.
        input_fields (list): A list of fields from the input data to be used in the assistant's content.
        output_data_path (str): The file path where the raw processed data will be saved.
        sleep_time (int): Time to sleep between rate-limited requests in sequential mode.
        rate_limit (int): Number of requests after which to apply rate limiting in sequential mode.
        use_parallel (bool): Whether to use parallel processing (True) or sequential processing (False).

    Returns:
        None
    """

    if not isinstance(assistant,dict):
        raise TypeError("assistant parameter must be of type dict")


    client = OpenAI()

    with open(input_data_path, 'r', encoding='utf-8-sig') as file:
        input_data = json.load(file)

    def process_example(example):
        content = {field: get_nested_field(example, field) for field in input_fields}
        content_json = json.dumps(content)
        
        return use_assistant(
            client, 
            **assistant, 
            temperature=TEMPERATURE, 
            top_p=TOP_P, 
            content=content_json
        )

    with open(output_data_path, 'w', encoding='utf-8') as output_file:
        if use_parallel:
            with ThreadPoolExecutor(max_workers=PARALLEL_REQUEST_LIMIT) as executor:
                futures = []
                for example in input_data:
                    futures.append(executor.submit(process_example, example))

                for future in tqdm(as_completed(futures), total=len(input_data), desc=f"Processing with {assistant['name']}"):
                    response = future.result()
                    output_file.write(response)
                    output_file.write("\n")
        else:
            for i, example in enumerate(tqdm(input_data, desc=f"Processing with {assistant['name']}")):
                response = process_example(example)
                output_file.write(response)
                output_file.write("\n")
                
                if (i + 1) % rate_limit == 0:
                    time.sleep(sleep_time)

    print(f"Processing complete. Raw results saved to {output_data_path}")


def create_assistant(
    client: OpenAI, 
    model: str, 
    name: str, 
    description: str, 
    instructions: str, 
    temperature: float,
    top_p: float,
    response_format: Optional[Dict[str, Any]] = None,
    logging_enabled: bool = False
):
    """
    Creates an assistant with specific instructions.

    Returns:
        dict: The created assistant object.
    """
    if logging_enabled:
        logging.info(f"Creating assistant: {name}")
    
    assistant_params : Dict[str, Any] = {
        "model": model,
        "name": name,
        "description": description,
        "instructions": instructions,
    }
    
    if response_format:
        if response_format.get("type") == "json_object":
            assistant_params["tools"] = [{"type": "function", "function": {"name": "response_formatter", "parameters": response_format["schema"]}}]
        elif response_format.get("type") == "text":
            assistant_params["response_format"] = {"type": "text"}

    response = client.beta.assistants.create(**assistant_params)
    if logging_enabled:
        logging.info(f"Created assistant: {name} (ID: {response.id})")
    return response

def create_thread(client: OpenAI, logging_enabled: bool = False):
    """
    Creates a new thread.
    """
    if logging_enabled:
        logging.info("Creating new thread")
    response = client.beta.threads.create()
    if logging_enabled:
        logging.info(f"Created thread with ID: {response.id}")
    return response

def delete_assistant(client: OpenAI, assistant_id: str, logging_enabled: bool = False):
    """
    Deletes an assistant with the specified ID.

    Args:
        client: The OpenAI client object.
        assistant_id (str): The ID of the assistant to delete.

    Returns:
        dict: The deleted assistant object.

    Raises:
        Exception: If there's an error deleting the assistant.
    """
    try:
        if logging_enabled:
            logging.info(f"Deleting assistant: {assistant_id}")
        response = client.beta.assistants.delete(assistant_id=assistant_id)
        if logging_enabled:
            logging.info(f"Deleted assistant: {assistant_id}")
        return response
    except Exception as e:
        logging.error(f"Error deleting assistant: {e}")
        raise

def create_message(client: OpenAI, thread_id: str, content: str, logging_enabled: bool = False):
    """
    Creates a new message in the specified thread.
    """
    if logging_enabled:
        logging.info(f"Creating message in thread: {thread_id}")
    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    if logging_enabled:
        logging.info(f"Created message with ID: {response.id}")
    return response

def run_assistant(client: OpenAI, thread_id: str, assistant_id: str, logging_enabled: bool = False):
    """
    Runs the assistant in the specified thread.
    """
    try:
        if logging_enabled:
            logging.info(f"Running assistant: {assistant_id} in thread: {thread_id}")
        response = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        if logging_enabled:
            logging.info(f"Run response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error running assistant: {e}")
        raise

def retrieve_run(client: OpenAI, thread_id: str, run_id: str, wait_time: int = 5, max_retries: int = 10, logging_enabled: bool = False):
    """
    Retrieves the status of a run, waiting for it to complete if necessary.
    """
    retries = 0
    while retries < max_retries:
        try:
            response = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if logging_enabled:
                logging.info(f"Retrieve run attempt {retries + 1}. Status: {response.status}")

            if response.status == "completed":
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                content = last_message.content[0].text.value
                if logging_enabled:
                    logging.info(f"Run completed. Last message content: {content[:100]}...")  # Log first 100 chars
                return content
            elif response.status == "failed":
                logging.error(f"Run failed. Error: {response.last_error}")
                raise Exception(f"Run failed: {response.last_error}")
            else:
                if logging_enabled:
                    logging.info(f"Run not yet completed. Waiting {wait_time} seconds before next attempt.")
                time.sleep(wait_time)
                retries += 1
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

    logging.error(f"Maximum retries ({max_retries}) reached. The run did not complete in the expected time.")
    raise TimeoutError("Maximum retries reached. The run did not complete in the expected time.")


def delete_thread(client: OpenAI, thread_id: str, logging_enabled: bool = False):
    """
    Deletes a thread with the specified ID.

    Args:
        client: The OpenAI client object.
        thread_id (str): The ID of the thread to delete.

    Returns:
        The response from the API after deleting the thread.

    Raises:
        Exception: If there's an error deleting the thread.
    """
    try:
        if logging_enabled:
            logging.info(f"Deleting thread: {thread_id}")
        response = client.beta.threads.delete(thread_id)
        if logging_enabled:
            logging.info(f"Deleted thread: {thread_id}")
        return response
    except Exception as e:
        logging.error(f"Error deleting thread: {e}")
        raise

def get_or_create_assistant(
    client: OpenAI,
    model: str,
    name: str,
    description: str,
    instructions: str,
    temperature: float,
    top_p: float,
    response_format: Optional[Dict[str, Any]] = None,
    logging_enabled: bool = False
) -> str:
    """
    Retrieves an existing assistant or creates a new one if it doesn't exist.
    
    Returns:
        str: The assistant ID.
    """
    if logging_enabled:
        logging.info(f"Getting or creating assistant: {name}")
    
    # List existing assistants
    assistants = client.beta.assistants.list(order="desc", limit=100)
    
    # Check if an assistant with the given name already exists
    for assistant in assistants.data:
        if assistant.name == name:
            if logging_enabled:
                logging.info(f"Using existing assistant: {name} (ID: {assistant.id})")
            return assistant.id
    
    # If no matching assistant is found, create a new one
    assistant = create_assistant(client, model, name, description, instructions, temperature, top_p, response_format, logging_enabled=False)
    return assistant.id

def use_assistant(
    client: OpenAI,
    model: str,
    name: str,
    description: str,
    instructions: str,
    temperature: float,
    top_p: float,
    content: str,
    wait_time=RUN_WAIT_TIME,
    max_retries=RUN_MAX_RETRIES,
    response_format: Optional[Dict[str, Any]] = None,
    logging_enabled: bool = False
):
    if logging_enabled:
        logging.info(f"Starting use_assistant for {name}")
    
    assistant_id = get_or_create_assistant(client, model, name, description, instructions, temperature, top_p, response_format, logging_enabled=False)
    if logging_enabled:
        logging.info(f"Assistant ID: {assistant_id}")
    
    thread = create_thread(client, logging_enabled=False)
    if logging_enabled:
        logging.info(f"Created thread with ID: {thread.id}")
    
    message = create_message(client, thread.id, content, logging_enabled=False)
    if logging_enabled:
        logging.info(f"Created message with ID: {message.id}")
    
    run = run_assistant(client, thread.id, assistant_id, logging_enabled=False)
    if logging_enabled:
        logging.info(f"Started run with ID: {run.id}")
    
    try:
        if logging_enabled:
            logging.info(f"Attempting to retrieve run. Wait time: {wait_time}, Max retries: {max_retries}")
        response = retrieve_run(client, thread.id, run.id, wait_time, max_retries, logging_enabled=False)
        if logging_enabled:
            logging.info(f"Assistant {name} (ID: {assistant_id}) completed task")
        
        return response
    except TimeoutError as e:
        if logging_enabled:
            logging.error(f"Timeout error occurred: {str(e)}")
        raise
    except Exception as e:
        if logging_enabled:
            logging.error(f"Unexpected error occurred: {str(e)}")
        raise
    finally:
        if logging_enabled:
            logging.info(f"Deleting thread {thread.id}")
        delete_thread(client, thread.id, logging_enabled=False)

def process_tasks_with_assistant(client: OpenAI, assistant_id: str, tasks: List[str], wait_time: int = RUN_WAIT_TIME, max_retries: int = RUN_MAX_RETRIES, logging_enabled: bool = False) -> List[Dict[str, Any]]:
    results = []
    for task in tasks:
        if logging_enabled:
            logging.info(f"Processing task: {task}")
        try:
            result = use_assistant(client, assistant_id, task, wait_time, max_retries, logging_enabled=False)
            results.append({"task": task, "result": result})
            if logging_enabled:
                logging.info(f"Task completed: {task}")
        except TimeoutError as e:
            results.append({"task": task, "error": str(e)})
            logging.error(f"Task failed: {task}. Error: {str(e)}")
    return results

def delete_all_assistants(logging_enabled: bool = False):
    """
    Retrieves all existing assistants and deletes them.

    Returns:
        int: The number of assistants deleted.

    Raises:
        Exception: If there's an error retrieving or deleting assistants.
    """
    try:
        client = OpenAI()
        assistants = client.beta.assistants.list(order="desc", limit=100)
        deleted_count = 0

        for assistant in assistants.data:
            delete_assistant(client, assistant.id, logging_enabled=False)
            deleted_count += 1

        if logging_enabled:
            logging.info(f"Deleted {deleted_count} assistants")
        return deleted_count
    except Exception as e:
        logging.error(f"Error deleting all assistants: {e}")
        raise