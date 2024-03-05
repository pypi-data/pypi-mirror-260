# Fourch-api

Fourch-api is a Python library for interacting with the 4chan API. It provides a simple interface to retrieve posts and attachments from 4chan boards.

## Installation

Install the library using pip:

```bash
pip install Fourch-api
```

## Usage

```python
from enum import Enum
from Fourch_api.const import Board, Category, Special, Other, International
from Fourch_api import FourCH

# Initialize FourCH object with a specific board
board = Board.A
fourch = FourCH(board)

# Get posts from a specific page
posts = await fourch.get_post(page=1)

# Get attachments from a specific page
attachments = await fourch.get_attachments(page=1)
```

## API Reference

### FourCH Class

```python
from Fourch_api import FourCH
```

#### Initialization

```python
# Initialize FourCH object with a specific board
board = Board.A
fourch = FourCH(board)
```

#### Methods

##### `get_post(page: int = 1) -> Model`

Get posts from a specific page.

- `page`: The page number to retrieve posts from (default is 1).

```python
posts = await fourch.get_post(page=1)
```

##### `get_attachments(page: int = 1) -> Model`

Get attachments from a specific page.

- `page`: The page number to retrieve attachments from (default is 1).

```python
attachments = await fourch.get_attachments(page=1)
```

### Constants

#### Boards Enum

```python
from Fourch_api.const import Board
```

- Represents the available 4chan boards.

#### Categories Enum

```python
from Fourch_api.const import Category
```

- Represents the available categories on 4chan.

#### Special Enum

```python
from Fourch_api.const import Special
```

- Represents special categories on 4chan.

#### Other Enum

```python
from Fourch_api.const import Other
```

- Represents other categories on 4chan.

#### International Enum

```python
from Fourch_api.const import International
```

- Represents international boards on 4chan.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
