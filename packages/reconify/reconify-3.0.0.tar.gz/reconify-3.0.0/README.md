# Reconify PIP module

The Reconify module is used for sending data to the Reconify platform at [www.reconify.com](https://www.reconify.com). 

Currently the module supports processing and analyzing Chats, Completions, and Images from:
+ **[OpenAI](#integrate-the-module-with-openai)** 
+ **[Amazon Bedrock](#integrate-the-module-with-amazon-bedrock-runtime)**  (Amazon Titan, AI21 Jurassic, Anthropic Claude, Cohere Command, Meta LLama 2, Mistral, and Stability Stable Diffusion)
+ **[Anthropic](#integrate-the-module-with-anthropic)**
+ **[Cohere](#integrate-the-module-with-cohere)**
+ **[Mistral](#integrate-the-module-with-mistral)**
+ **[Perplexity](#integrate-the-module-with-perplexity)**

Support for additional actions and providers will be added.

## Get started
The first step is to create an account at [app.reconify.com](https://app.reconify.com).

## Generate API and APP Keys
In the Reconify console, add an Application to your account. This will generate both an API_KEY and an APP_KEY 
which will be used in the code below to send data to Reconify.

## Install the module

```
pip install reconify
```

## Integrate the module with OpenAI

The following instructions are for OpenAI's Python SDK v1 or later (released in Nov 2023). For earlier versions of OpenAI's SDK, follow the [legacy instructions](https://www.reconify.com/docs/openai/legacy)

### Import the module
```python
from reconify import reconifyOpenAIHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the OpenaAI module.

```python
from openai import OpenAI
openai_client = OpenAI(api_key = 'YOUR_OPENAI_KEY')
```

Configure the instance of Reconify passing the OpenAi instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyOpenAIHandler.config(openai_client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify when you call openai_client.completions.create, openai_client.chat.completions.create, openai_client.images.generate. 

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyOpenAIHandler.config(openai_client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyOpenAIHandler.setUser ({
   "userId": "ABC123",
   "isAuthenticated": 1,
   "firstName": "Francis",
   "lastName": "Smith",
   "email": "",
   "phone": "",
   "gender": "female"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyOpenAIHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyOpenAIHandler.setSessionTimeout(15)
```

See [Examples with OpenAI](#examples-with-openai)

## Integrate the module with Amazon Bedrock Runtime

### Import the module
```python
from reconify import reconifyBedrockRuntimeHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the Amazon boto3 module.

```python
import boto3
bedrock = boto3.client('bedrock-runtime')
```

Configure the instance of Reconify passing the Bedrock Runtime instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyBedrockRuntimeHandler.config(bedrock, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify when you call bedrock.invoke_model(). 

#### Response handling

When using the Reconify module, the response body from `invoke_model` will be converted from `botocore.response.StreamingBody` to JSON and saved in the response as `parsedBody`. See the examples below for more info. 

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyBedrockRuntimeHandler.config(bedrock, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyBedrockRuntimeHandler.setUser ({
   "userId": "ABC123",
   "firstName": "Francis",
   "lastName": "Smith"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyBedrockRuntimeHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyBedrockRuntimeHandler.setSessionTimeout(15)
```

See [Examples with Amazon Bedrock Runtime](#examples-with-bedrock-runtime)

## Integrate the module with Anthropic

The following instructions are for Anthropic's Python SDK.

### Import the module
```python
from reconify import reconifyAnthropicHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the Anthropic module.

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
anthropic = Anthropic(api_key = 'YOUR_ANTHROPIC_KEY')
```

Configure the instance of Reconify passing the Anthropic instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyAnthropicHandler.config(anthropic, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify. 

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyAnthropicHandler.config(anthropic, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyAnthropicHandler.setUser ({
   "userId": "ABC123",
   "firstName": "Francis",
   "lastName": "Smith"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyAnthropicHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyAnthropicHandler.setSessionTimeout(15)
```

See [Examples with Anthropic](#examples-with-anthropic)

## Integrate the module with Cohere

The following instructions are for Cohere's Python SDK. 

### Import the module
```python
from reconify import reconifyCohereHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the Cohere module.

```python
from cohere import Client
cohere_client = Client('YOUR_COHERE_KEY')
```

Configure the instance of Reconify passing the Cohere instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyCohereHandler.config(cohere_client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify. 

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyCohereHandler.config(cohere_client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyCohereHandler.setUser ({
   "userId": "ABC123",
   "firstName": "Francis",
   "lastName": "Smith"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyCohereHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyCohereHandler.setSessionTimeout(15)
```

See [Examples with Cohere](#examples-with-cohere)

## Integrate the module with Mistral

The following instructions are for Mistral's Python SDK. 

### Import the module
```python
from reconify import reconifyMistralHandler
```

### Initialize the module
Prior to initializing the Reconify module, make sure to import the Mistral module.

```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
client = MistralClient(api_key = 'YOUR_MISTRAL_KEY')
```

Configure the instance of Reconify passing the Mistral instance along with the Reconify API_KEY and APP_KEY created above.

```python
reconifyMistralHandler.config(client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

This is all that is needed for a basic integration. The module takes care of sending the correct data to Reconify. 

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyMistralHandler.config(client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyMistralHandler.setUser ({
   "userId": "ABC123",
   "firstName": "Francis",
   "lastName": "Smith"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyMistralHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyMistralHandler.setSessionTimeout(15)
```

See [Examples with Mistral](#examples-with-mistral)

## Integrate the module with Perplexity

The following instructions are for Perplexity. 

### Import the module
```python
from reconify import reconifyUniversalHandler
```

### Initialize the module

Configure the instance of Reconify passing the Reconify API_KEY and APP_KEY created above.

```python
reconifyUniversalHandler.config( 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key'
)
```

After making a call to the Perplexity, send the input parameters and response data to Reconify, along with the start and end time stamps.

```python
input = {
    "model":"pplx-7b-chat",
    "messages":[
        {"role": "system", "content": "You are a comic"},
        {"role": "user", "content": "Tell a cat joke"},
    ]
}

start = reconifyUniversalHandler.getTimestamp()
response = requests.post("https://api.perplexity.ai/chat/completions", json=input, headers = {
    "accept":"application/json",
    "content-type":"application/json",
    "authorization": "Bearer YOUR_PERPLEXITY_KEY"
})
end = reconifyUniversalHandler.getTimestamp()

reconifyUniversalHandler.logChat(input, response.text, start, end)
```

#### Optional Config Parameters 
There are additional optional parameters that can be passed in to the handler. 

+ debug: (default False) Enable/Disable console logging
+ trackImages: (default True) Turn on/off tracking of createImage 

For example:

```python
reconifyUniversalHandler.config(client, 
   appKey = 'Your_App_Key', 
   apiKey = 'Your_Api_Key',
   debug = True
)
```

### Optional methods

You can optionally pass in a user object or session ID to be used in the analytics reporting. 
The session ID will be used to group interactions together in the same session transcript.

#### Set a user
The user JSON should include a unique userId, all the other fields are optional. 
Without a unique userId, each user will be treated as a new user.

```python
reconifyUniversalHandler.setUser ({
   "userId": "ABC123",
   "firstName": "Francis",
   "lastName": "Smith"
})
```

#### Set a Session ID
The Session ID is an alphanumeric string.
```python
reconifyUniversalHandler.setSession('MySessionId')
```

#### Set Session Timeout
Set the session timeout in minutes to override the default
```python
reconifyUniversalHandler.setSessionTimeout(15)
```

See [Examples with Perplexity](#examples-with-perplexity)

## Examples with OpenAI

### Chat Example

```python
from openai import OpenAI
from reconify import reconifyOpenAIHandler

openai_client = OpenAI(api_key = 'YOUR_OPENAI_KEY')

reconifyOpenAIHandler.config(openai_client, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "isAuthenticated": 1,
   "firstName": "Jim",
   "lastName": "Stand",
   "gender": "male"
})

response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert on commedians."},
        {"role": "user", "content": "Tell a joke about cats"},
    ],
    temperature=0,
)
```

### Completion Example

```python
from openai import OpenAI
from reconify import reconifyOpenAIHandler

openai_client = OpenAI(api_key = 'YOUR_OPENAI_KEY')

reconifyOpenAIHandler.config(openai_client, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "isAuthenticated": 1,
   "firstName": "Jim",
   "lastName": "Stand",
   "gender": "male"
})

response = openai_client.completions.create(
   model = "text-davinci-003",
   prompt = "write a haiku about cats",
   max_tokens = 100,
   temperature = 0,
)
```

### Image Example

```python
from openai import OpenAI
from reconify import reconifyOpenAIHandler

openai_client = OpenAI(api_key = 'YOUR_OPENAI_KEY')

reconifyOpenAIHandler.config(openai_client, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "isAuthenticated": 1,
   "firstName": "Jim",
   "lastName": "Stand",
   "gender": "male"
})

response = openai_client.images.generate(
   model = "dall-e-3",
   prompt = "a cat on the moon",
   n = 1,
   size = "1024x1024",
   quality="standard",
   response_format = "url"
)
```

## Examples with Amazon Bedrock Runtime

### Anthropic Claude example

```python
import boto3
from reconify import reconifyBedrockRuntimeHandler

bedrock = boto3.client('bedrock-runtime')

reconifyBedrockRuntimeHandler.config(bedrock, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "firstName": "Jane",
   "lastName": "Smith"
})

response = bedrock.invoke_model(
    modelId = "anthropic.claude-instant-v1",
    contentType = "application/json",
    accept = "application/json",
    body = "{\"prompt\":\"\\n\\nHuman: Tell a cat joke.\\n\\nAssistant:\",\"max_tokens_to_sample\":300,\"temperature\":1,\"top_k\":250,\"top_p\":0.999,\"stop_sequences\":[\"\\n\\nHuman:\"],\"anthropic_version\":\"bedrock-2023-05-31\"}"
)

#The botocore.response.StreamingBody object will be converted to JSON and saved in parsedBody
print(response.get("parsedBody"))

```

### Stable Diffusion image example

```python
import boto3
from reconify import reconifyBedrockRuntimeHandler

bedrock = boto3.client('bedrock-runtime')

reconifyBedrockRuntimeHandler.config(bedrock, 'Your_App_Key', 'Your_Api_Key')

reconifyOpenAIHandler.setUser({
   "userId": "12345",
   "firstName": "Jane",
   "lastName": "Smith"
})

response = bedrock.invoke_model(
    modelId = "stability.stable-diffusion-xl-v0",
    contentType = "application/json",
    accept = "application/json",
    body = "{\"text_prompts\":[{\"text\":\"a cat drinking boba tea\"}],\"cfg_scale\":10,\"seed\":0,\"steps\":50}"
)
#The botocore.response.StreamingBody object will be converted to JSON and saved in parsedBody
#The following will print out the image result in JSON base64
print(response.get("parsedBody"))

```

## Examples with Anthropic

### Chat Example

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from reconify import reconifyAnthropicHandler

anthropic = Anthropic(api_key = 'YOUR_ANTHROPIC_KEY')

reconifyAnthropicHandler.config(anthropic, 'Your_App_Key', 'Your_Api_Key')

reconifyAnthropicHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith",
})

response = anthropic.messages.create(
    model="claude-2.1",
    max_tokens=300,
    messages = [
      {"role": "user", "content" : "Tell me a cat joke"}
    ]
)
```

### Completions Example

```python
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from reconify import reconifyAnthropicHandler

anthropic = Anthropic(api_key = 'YOUR_ANTHROPIC_KEY')

reconifyAnthropicHandler.config(anthropic, 'Your_App_Key', 'Your_Api_Key')

reconifyAnthropicHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith",
})

response = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"{HUMAN_PROMPT} Tell me a good cat joke{AI_PROMPT}",
)
```

## Examples with Cohere

### Chat Example

```python
from cohere import Client
from reconify import reconifyCohereHandler

cohere_client = Client('YOUR_COHERE_KEY')

reconifyCohereHandler.config(cohere_client, 'Your_App_Key', 'Your_Api_Key')

reconifyCohereHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith"
})

response = cohere_client.chat(
    model="command",
    message="tell me a good cat joke"
)
```

### Generate Example

```python
from cohere import Client
from reconify import reconifyCohereHandler

cohere_client = Client('YOUR_COHERE_KEY')

reconifyCohereHandler.config(cohere_client, 'Your_App_Key', 'Your_Api_Key')

reconifyCohereHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith"
})

response = cohere_client.generate(
    model="command",
    prompt="write a cat haiku",
    max_tokens=300
)
```

## Examples with Mistral

### Chat Example

```python
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from reconify import reconifyMistralHandler

client = MistralClient(api_key = 'YOUR_MISTRAL_KEY')

reconifyMistralHandler.config(client, 'Your_App_Key', 'Your_Api_Key')

reconifyMistralHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith"
})

response = client.chat(
    model="mistral-tiny",
    messages=[
      ChatMessage(role="user", content="Tell me a cat joke")
    ]
)
```

## Examples with Perplexity

### Chat Example

```python
import requests
from reconify import reconifyUniversalHandler

reconifyUniversalHandler.config('Your_App_Key', 'Your_Api_Key')

reconifyUniversalHandler.setUser({
   "userId": "12345",
   "firstName": "Jim",
   "lastName": "Smith"
})

input = {
    "model":"pplx-7b-chat",
    "messages":[
        {"role": "system", "content": "You are a comic"},
        {"role": "user", "content": "Tell a cat joke"},
    ]
}

start = reconifyUniversalHandler.getTimestamp()

response = requests.post("https://api.perplexity.ai/chat/completions", json=input, headers = {
    "accept":"application/json",
    "content-type":"application/json",
    "authorization": "Bearer YOUR_PERPLEXITY_KEY"
})

end = reconifyUniversalHandler.getTimestamp()

reconifyUniversalHandler.logChat(input, response.text, start, end)
```