# llm_helpers Package

## Overview

The `llm_helpers` package provides utilities for interacting with language learning models (LLMs), including generating categories from text using recursrive calls to services like Azure's version of OpenAI. This package simplifies the process of sending requests to and interpreting responses from these models for large data which may not fit in the context of the target model.

## Installation

To install `llm_helpers`, download the package and install it using pip:

```
pip install llm_helpers
```

Or, if the package is hosted in a repository:

```
pip install git+https://github.com/sonnylaskar/llm_helpers.git
```

## Usage

To use the `llm_helpers` package in your project, simply import it and call the available functions. The primary function, `generate_categories`, allows you to generate category tags for a given text input using a specified language learning model. 
Currently only OpenAI and Azure OpenAI is supported.

### Example

#### Recursive Category Generation from Text

When dealing with a large corpus of text from which we aim to generate categories, we often encounter the challenge that the text size exceeds the target model's context limit. One effective strategy to overcome this limitation is to segment the text into smaller portions that the model can process. The initial step involves chunking the text to fit within the model's context and generating categories for each segment. Subsequently, these categories are amalgamated and subjected to another round of category generation. This process may not suffice in a single iteration if the combined output still exceeds the model's context limit, necessitating further chunking and category generation. The `generate_categories` function facilitates this intricate process recursively, enabling streamlined category generation from extensive text data.

**Parameters:**
- **txt:** The input text for category generation.
- **llm:** The language model to use, choices include 'azure' or 'openai'.
- **endpoint:** If using 'azure', specify the Azure endpoint.
- **key:** The authentication key for the language model API.
- **api_version:** Specifies the API version of the chosen model.

**Optional Parameters (with defaults):**
- **max_tokens=200:** The maximum number of tokens to generate.
- **temperature=0.0:** Controls the randomness in the output generation.
- **frequency_penalty=0.0:** Adjusts the likelihood of repeating information.
- **presence_penalty=0.0:** Influences the introduction of new concepts.
- **max_token_size=4092:** Set to maximum token capacity of the target language model.
- **system_prompt="Generate the top categories into which the below text can be grouped, just print the categories, do not add any examples, put them to Others category if they don't fit in any category:":** Customizable prompt that guides the model in generating relevant categories.

**Note:** 
- The `system_prompt` serves as a guideline for the model to ensure the categories generated align with the specified criteria.
- Adjust the `max_token_size` according to the maximum token capacity of the target language model to optimize the chunking process.  

The following script demonstrates how to use the `llm_helpers` package to generate categories from text stored in a file named `sample_text.txt`:

```python
import llm_helpers

# Open the file in read mode
with open('sample_text.txt', 'r') as file:
    # Read the entire contents of the file into a string
    txt = file.read()

# Update the <> below with the correct values
categories = llm_helpers.generate_categories(txt, 
                                             llm = 'azure', 
                                             endpoint = "<azure_endpoint>", 
                                             key = "<azure_key>", 
                                             api_version="<api_version>", 
                                             deployment_name="<deployment_name>", 
                                             max_tokens=200, 
                                             temperature=0.0, 
                                             frequency_penalty=0.0, 
                                             presence_penalty=0.0, 
                                             max_token_size=4092, 
                                             system_prompt="Generate the top categories into which the below text can be grouped, just print the categories, do not add any examples, put them to Others category if they dont fit in any category: "
                                            )
print(categories)
```

Replace the placeholders (`<>`) with your actual Azure endpoint, key, API version, and deployment name to run the script.

## License

This project is licensed under the Apache License, Version 2.0. For more details, see the [LICENSE](LICENSE) file in the root directory of this project. 

## Contributing

We welcome contributions to the `llm_helpers` package! If you'd like to contribute, please follow these steps:

1. Fork the repository on GitHub.
2. Make your changes in your forked repository.
3. Submit a Pull Request back to the main repository.

We encourage you to discuss any substantial changes through a GitHub issue before you start working on your contribution. This allows us to provide feedback, suggest any necessary adjustments, and help you determine the best approach.
