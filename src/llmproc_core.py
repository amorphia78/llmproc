import anthropic
import os
import json
import hashlib

client = None

def load_client(api_key: str | None = None) -> anthropic.Anthropic:
    global client
    # If an API key string is provided directly, use it to create the client
    print("In load_client() api_key is: " + api_key)
    if api_key is not None:
        client = anthropic.Anthropic(api_key=api_key)
    # Otherwise, attempt to load the key from the file
    try:
        with open('key.txt', 'r') as file:
            file_api_key = file.read().strip()
        client = anthropic.Anthropic(api_key=file_api_key)
    except FileNotFoundError:
        print("key.txt file not found")
        raise
    except Exception as e:
        print(f"Error loading API key: {str(e)}")
        raise

def send_prompt(prompt, llm_task_type="summariser", prefill="", prior_prompt="", prior_llm ="" ):
    global client
    if prior_prompt != "":
        messages = [
            { 'role': "user",
              'content': [ {'type': "text", 'text': prior_prompt} ]
            }, {
              'role': "assistant",
              'content': [ {'type': "text", 'text': prior_llm } ]
            }, {
              'role': "user",
              'content': [ {'type': "text", 'text': prompt } ]
        } ]
        if prefill:
            messages.append( {
                'role': "assistant",
                'content': [ {'type': "text", 'text': prefill} ]
            } )
    else:
        messages = [ {
                'role': "user",
                'content': [ {'type': "text", 'text': prompt} ]
        } ]
        if prefill:
            messages.append( {
                'role': "assistant",
                'content': [ {'type': "text", 'text': prefill} ]
            } )
    system = ""
    if llm_task_type == "summariser":
        system = ""
    elif llm_task_type == "processor":
        system = ""
    else:
        system = llm_task_type
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=system,
        messages=messages,
    ).content[0].text
    if prefill:
        response = prefill + response
    return response

def process_with_cache(process_func, article):
    cache_dir = f"llm_caches/{process_func.__name__}"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/{article['id']}.json"
    if os.path.exists(cache_file):
        print(f"{process_func.__name__} for article {article['id']} (retrieving cache)")
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
            return cached_data['string_data'] if 'string_data' in cached_data else cached_data
    else:
        print(f"{process_func.__name__} for article {article['id']} (consulting LLM)")
        result = process_func(article)
        if isinstance(result, str):
            data_to_store = {'string_data': result}
        else:
            data_to_store = result
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_store, ensure_ascii=False, indent=2, fp=f)  # type: ignore
        return result

def process_url_with_cache(process_func, url):
    # Create a hash of the URL to use as cache ID
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()

    cache_dir = f"llm_caches/{process_func.__name__}"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/{url_hash}.json"

    if os.path.exists(cache_file):
        print(f"{process_func.__name__} for URL {url} (retrieving cache)")
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
            return cached_data['string_data'] if 'string_data' in cached_data else cached_data
    else:
        print(f"{process_func.__name__} for URL {url} (consulting LLM)")
        result = process_func(url)
        if isinstance(result, str):
            data_to_store = {'string_data': result}
        else:
            data_to_store = result
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data_to_store, ensure_ascii=False, indent=2, fp=f)  # type: ignore
        return result
