# MediSearch API Client

[MediSearch](https://medisearch.io/) API Client provides a Python interface for the MediSearch API. Easily send user messages and receive LLM responses, articles, and handle any errors that might arise.

## Installation

```bash
pip install medisearch_client
```

## Usage

### Initialization

Initialize the client with your API key (obtain one from the [MediSearch API page](https://medisearch.io/developers)):

```python
from medisearch_client import MediSearchClient

client = MediSearchClient(api_key="your_api_key")
```

### Sending User Messages and Making Follow-Up Queries

To send a user message, first generate a unique conversation id (`your_conversation_id` below) for your conversation. Then, you may call the client as:

```python
responses = client.send_user_message(
    conversation=["By how much does sport increase life expectancy?"],
    conversation_id="your_conversation_id",
    should_stream_response=True
)

for response in responses:
    print(response)
```

#### Conversation Structure

The `conversation` parameter is a list of strings where user and chatbot messages alternate. For follow-up queries, append the user's new message to the end of the list.

Example:

```python
conversation=[
    "What is diabetes?",
    "Diabetes is...",
    "How is it treated?"
]
```

Always ensure the last message in the conversation is from the user.

#### Streaming Option

The `should_stream_response` flag controls how the client receives responses:

- `True`: Stream the responses as they arrive. This is useful if you want to process each part of the response separately or if you want to display it to the user piece by piece.
- `False`: Wait until all parts of the response are collected and then return them as a list.

### Supported Languages

MediSearch supports:

- English
- French
- Spanish
- German
- Hindi
- Chinese
- Japanese
- Slovak
- Arabic

Set the `language` parameter in `send_user_message` accordingly.

## Output structure

In the following call to our API

```
responses = client.send_user_message(
    conversation=["By how much does sport increase life expectancy?"],
    conversation_id="your_conversation_id",
    should_stream_response=True
)
```

`responses` will be a list of MediSearch events. Please see [our docs](https://medisearch.io/developers) for a detailed description of all the events.

## Error Handling

If there is an error in the call to our API

```
responses = client.send_user_message(
    conversation=["By how much does sport increase life expectancy?"],
    conversation_id="your_conversation_id",
    should_stream_response=True
)
```

then `responses` will contain an error event. This will be in the form of an element such as

```
{
	event: "error",
	error_code: "error_not_enough_articles",
	id: "your_conversation_id"
}
```

Some errors are part of how MediSearch API works. For example:

- If we do not find enough relevant articles to a question, we will return `error_not_enough_articles`. For example, if the question is non-medical or does not make sense, MediSearch will throw this error.
- If the conversation is too long, then we will return `error_out_of_tokens`. This happens rarely in practice. It can start happening if you ask MediSearch approximately 8 questions and get 8 responses in one conversation.

Therefore, you should have at least some basic error handling mechanism to show your users a sensible message on your frontend when an error happens.

Please see [our docs](https://medisearch.io/developers) for a detailed description of all the error events.

If you ever think that there is a problem **do not hesitate to contact us: founders@medisearch.io.**
