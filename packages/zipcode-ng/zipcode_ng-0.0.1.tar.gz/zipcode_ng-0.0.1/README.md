# Nigerian Zip Codes (zipcode-ng)

The `zipcode-ng` library provides information about states, local government areas (LGAs) towns and zip codes in Nigeria.

## Installation

You can install the package via pip:

```bash
pip install zipcode-ng
```

## Usage

### Importing

```python
from zipcode_ng import (
    get_state_data,
    get_all_state_data
)

# Retrieve data for a specific state
lagos_state_data = get_state_data("Lagos")
print("Lagos State Data:", lagos_state_data)

# Retrieve data for all states
all_states_data = get_all_state_data()
print("All States Data:", all_states_data)
```

### Functions

- `get_state_data(identifier: Union[str, StateName]) -> StateInfo`: Returns information about a specific state based on its name or postal code.

- `get_all_state_data() -> List[StateInfo]`: Returns information about all states in Nigeria.

### Type Definitions

- `StateInfo`: Represents the data structure for information about a state, including its name, language, tribe, description, region, etc.

- `StateName`: Literal type representing the names of Nigerian states.

### JSON Data

The state information returned by the library is sourced from a JSON file included with the package. The JSON file contains details about each state, including local government areas and towns within them.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## GitHub Repository

You can find the source code and contribute to this project on GitHub: [Nigerian Zip Codes on GitHub](https://github.com/awesomegoodman/zipcode-ng)
