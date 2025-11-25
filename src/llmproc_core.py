import anthropic
import os
import json
import hashlib
import requests

client = None
no_cache = False

def load_client(api_key: str | None = None) -> anthropic.Anthropic:
    global client
    # If an API key string is provided directly, use it to create the client
    if api_key is not None:
        client = anthropic.Anthropic(api_key=api_key)
    # Otherwise, attempt to load the key from the file
    else:
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
    #print(f"Messages: {messages}")
    #for i, msg in enumerate(messages):
    #    print(f"Message {i}: role='{msg.get('role')}', content='{msg.get('content')}'")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0,
#        system=system,
        messages=messages,
    ).content[0].text
    if prefill:
        response = prefill + response
    return response

def process_with_cache(process_func, article, additional_arg=None):
    cache_dir = f"llm_caches/{process_func.__name__}"
    os.makedirs(cache_dir, exist_ok=True)
    if additional_arg is not None:
        safe_arg = str(additional_arg).replace('/', '_').replace('\\', '_')
        cache_file = f"{cache_dir}/{article['id']}_{safe_arg}.json"
    else:
        cache_file = f"{cache_dir}/{article['id']}.json"
    if os.path.exists(cache_file) and not no_cache:
        print(f"{process_func.__name__} for article {article['id']} (retrieving cache)")
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached_data = json.load(f)
            return cached_data['string_data'] if 'string_data' in cached_data else cached_data
    else:
        print(f"{process_func.__name__} for article {article['id']} (consulting LLM)")
        if additional_arg is not None:
            result = process_func(article, additional_arg)
        else:
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

def describe_image_from_url(image_url, prompt="Please describe this image in detail."):
    import requests
    import base64
    from PIL import Image
    from io import BytesIO
    response = requests.get(image_url)
    response.raise_for_status()
    image_content = resize_image_if_needed(response.content)
    image_data = base64.b64encode(image_content).decode('utf-8')
    try:
        with Image.open(BytesIO(image_content)) as img:
            image_format = img.format.lower()
            format_to_mime = {
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            media_type = format_to_mime.get(image_format, 'image/jpeg')
    except Exception:
        content_type = response.headers.get('Content-Type', 'image/jpeg')
        media_type = content_type.split(';')[0].strip()
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=0,
        messages=messages,
    ).content[0].text
    print(f"\nPrompt: {prompt}\n")
    print(f"Response: {response}\n")
    return response

def resize_image_if_needed(image_content, max_size_mb=3.75, max_dimension=6000):
    from PIL import Image
    from io import BytesIO
    max_size_bytes = max_size_mb * 1024 * 1024
    needs_resize = False
    if len(image_content) > max_size_bytes:
        needs_resize = True
        print(f"Image size ({len(image_content) / 1024 / 1024:.2f}MB) exceeds {max_size_mb}MB limit")
    with Image.open(BytesIO(image_content)) as img:
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            needs_resize = True
            print(f"Image dimensions ({width}x{height}) exceed {max_dimension}px limit")
        if not needs_resize:
            return image_content
        print("Resizing image...")
        if width > height:
            new_width = min(width, max_dimension)
            new_height = int((new_width / width) * height)
        else:
            new_height = min(height, max_dimension)
            new_width = int((new_height / height) * width)
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        output = BytesIO()
        save_format = img.format if img.format else 'JPEG'
        if save_format not in ['JPEG', 'PNG', 'WEBP']:
            save_format = 'JPEG'
        quality = 95
        while quality > 20:
            output.seek(0)
            output.truncate()
            if save_format == 'PNG':
                img_resized.save(output, format=save_format, optimize=True)
            else:
                if img_resized.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img_resized.size, (255, 255, 255))
                    rgb_img.paste(img_resized, mask=img_resized.split()[-1] if img_resized.mode == 'RGBA' else None)
                    rgb_img.save(output, format='JPEG', quality=quality, optimize=True)
                else:
                    img_resized.save(output, format=save_format, quality=quality, optimize=True)
            output_size = len(output.getvalue())
            if output_size <= max_size_bytes:
                print(f"Resized to {new_width}x{new_height}, {output_size / 1024 / 1024:.2f}MB (quality: {quality})")
                return output.getvalue()
            quality -= 10
        print(f"Warning: Could not reduce image below {max_size_mb}MB limit")
        return output.getvalue()