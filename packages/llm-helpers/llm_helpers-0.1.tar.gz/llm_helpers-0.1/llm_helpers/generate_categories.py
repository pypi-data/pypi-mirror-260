from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage

def get_llm_model(llm, endpoint, key, api_version=None, deployment_name=None):
    if llm == 'azure':
        try:
            # Attempt to create the AzureChatOpenAI object
            return AzureChatOpenAI(
                azure_endpoint=endpoint,
                openai_api_version=api_version,
                deployment_name=deployment_name,
                openai_api_key=key,
                openai_api_type="azure",
            )
        except Exception as e:
            # Handle or log the exception as needed
            raise ValueError(f"Failed to create the AzureChatOpenAI model: {str(e)}")
    else:
        raise ValueError(f"Unsupported language model: {llm}")

def generate_categories(text, llm, endpoint, key, api_version=None, deployment_name=None, max_tokens=200, temperature=0.0, frequency_penalty=0.0, presence_penalty=0.0, max_token_size=4092, system_prompt="Generate the top categories into which the below text can be grouped, just print the categories, do not add any examples, put them to Others category if they dont fit in any category: "):
    if not text:
        raise ValueError("The 'text' parameter cannot be blank or None.")
    # Get the llm_model using the new function
    llm_model = get_llm_model(llm, endpoint, key, api_version, deployment_name)
    current_length = 0
    categories = []

    length = len(text)
    start = 0
    end = int(max_token_size * 2.5)  # Adjusted according to your request

    while start < length:
        text_segment = text[start:end]
        start = end
        end += int(max_token_size * 2.5)  # Keep the same increment as initially set
        if end > length:
            end = length

        promptx = system_prompt + text_segment

        ans = llm_model(
                [HumanMessage(content=promptx)],
                max_tokens=max_tokens,
                temperature=temperature,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )

        categories += ans.content.split('\n')

        current_length += sum(len(category) for category in categories)

        if current_length >= 200:
            break

    if current_length < 200:
        combined_categories_text = ' '.join(categories)
        # Call generate_categories recursively with correct parameters
        more_categories = generate_categories(combined_categories_text, llm, endpoint, key, api_version, deployment_name, max_tokens, temperature, frequency_penalty, presence_penalty, max_token_size, system_prompt)
        categories += more_categories

    return categories
