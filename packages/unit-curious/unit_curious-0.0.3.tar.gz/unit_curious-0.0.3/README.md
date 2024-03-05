# UnitCurious

Explore historical, quirky, and unconventional units of measurement with this easy-to-use Python library.

## Installation

```bash
$ pip install unit_curious
```

## Usage

`UnitCurious` lets you convert between several unusual units. 

```python
import unitcurious

# Calculate length in ancient Egyptian cubits
result_feet = unitcurious.cubit(1.8)  # Assumes ~1.8 cubits for a forearm
print(f"Result in feet: {result_feet}") 

# Smoots are serious business at MIT... 
bridge_length = unitcurious.smoot(364.4, to="meter") 
print(f"That's {bridge_length} meters in smoots!")  

# How many barleycorns fit in an inch?
inch_in_barleycorns = unitcurious.barleycom(1, to="inches")
print(inch_in_barleycorns)
```

## Currently supported units:

Cubit (ancient length)

Barleycorn (English length)

Smoot (humorous MIT unit)

Stone (British weight)

## Coming Soon to UnitCurious

We're always exploring new horizons at UnitCurious, and we've got some exciting features and functions in the pipeline designed to make your experience even more fascinating and fun.

## Contributing

Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## License

`UnitCurious` was created by Rajaa Lebchiri. It is licensed under the terms
of the MIT license.
