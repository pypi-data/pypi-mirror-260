# spectra_dio

Python Module for PowerBox / PowerTwin digital I/O 

# Installation

`pip install spectra_dio`

# Example Usage

```python
import spectra_dio

dio = spectra_dio.DIO(spectra_dio.IOConfig.from_dmi())
dio.initialize()

# Read digital input status
print(dio.read_di())

# Set digital output DO0 on
dio.write_do(0, True)
```