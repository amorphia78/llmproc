import anthropic

def load_llm_client(api_key) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)

def llm_prompt(prompt, client, llm_task_type="summariser", prefill="" ):
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