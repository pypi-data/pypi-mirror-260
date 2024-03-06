# PyPRYCD
This module provides a simple unofficial wrapper for working with the PRYCD APIs for real estate analysis.

## Getting Started
To install, simply execute the following command in the command line:

```shell
pip install pyprycd
```

### Obtaining API Keys
Once you have installed the module, you can now make API calls, however you will have to purchase API keys from PRYCD at (www.prycd.com)  Pyrcd has two separate API keys for the pricing and comps API which must be purchased separately.  When you initialize the constructor, you can set either of them, or set the keys later using one of the setter methods.

## Methods
* `get_comps()`:  Returns PRYCD comparables in a requested region.
* `get_counties_in_state(<state>)`:  Returns a list of counties in a state. Accepts either a state name or code.
* `get_fips_code(<county>)`: Returns the FIPS code for a county. Note that you must spell out the full county name and state. IE: `Maricopa County AZ`
* `get_pricing()`:  Returns PRYCD estimated values for a requested property.  Supports all options for the PRYCD API.
* `set_pricing_api_key(<api_key>)`: Sets or resets the pricing API key. 
* `set_comp_api_key(<api_key>)`  Sets or resets the comp API key.  Supports all options for the PRYCD API.


## Example Usage
```python
from pyprycd import PyPrycd

PRICING_API_KEY = '1234'
COMPS_API_KEY = '5678'

# Initialize the PyPrycd Object
pyrcd = PyPrycd(pricing_api_key=PRICING_API_KEY, comp_api_key=COMPS_API_KEY)

# Get a FIPS code
fips = PyPrycd.get_fips_code('Autauga County AL')

# Get pricing data about a property
pricing_data = pyrcd.get_pricing()

```
