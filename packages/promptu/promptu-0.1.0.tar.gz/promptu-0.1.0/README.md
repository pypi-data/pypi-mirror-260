# Promptu

> Write dynamic LLM prompts as natural language

Promptu provides a suite of natural language generation utilities for prompt
engineers, such as truncation, pluralization and natural language list
formatting.

## Project Status

:warning: This project is currently in its infancy. Please report bugs and
expect breaking changes.

## Installation

```sh
pip install promptu
```

## Example

```py
from promptu import join

def find_matching_color(existing_colors):
    return f'What color goes well with {join(items=existing_colors, conjunction="and")}?'

# Prints "What color goes well with blue, purple and white?"
print(find_matching_color(['blue', 'purple', 'white']))
```

## Using in Langchain

```py
runnable = (
    {'prompt': RunnableLambda(find_matching_color)}
    | PromptTemplate.from_template('{prompt}')
    | model
)
runnable.invoke(['blue', 'purple', 'white'])
```

## Prompting Utilities

### `join()`

Formats a list of items as a natural language list.

**Syntax:**

```py
join(items: Iterable, conjunction: str) -> str
```

### `pluralize()`

Selects the singular or plural form of a word based on the number of items.

**Syntax:**

```py
pluralize(singular: str, plural: str, items: Iterable) -> str
```

### `truncate()`

Truncates a string to a maximum length. If the text is longer than the maximum
length, all characters after the maximum length are replaced with the suffix.

**Syntax:**

```py
truncate(
    text: str, max_length: int, mode=TruncateMode.CHARACTER, suffix="..."
) -> str
```
