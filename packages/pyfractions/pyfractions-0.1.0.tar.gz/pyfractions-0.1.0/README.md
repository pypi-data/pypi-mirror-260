# Fraction Calculator

The Fraction Calculator is a versatile Python library designed for performing various operations in ```numerator/denominator``` format. It enables users to work with fractions seamlessly and includes features like basic arithmetic operations, comparison methods, and more.

## Features

- **Basic Arithmetic Operations:**
  - Addition
  - Subtraction
  - Multiplication
  - Division
  - Floor Division
  - Modulus

- **Comparison Methods:**
  - Compare fractions using the following methods:
    - Less than (`<`)
    - Less than or equal to (`<=`)
    - Equal to (`==`)
    - Not equal to (`!=`)
    - Greater than (`>`)
    - Greater than or equal to (`>=`)

## Usage

To utilize the Fraction Calculator, create instances of the `Fraction` class and perform operations. Here's an example showcasing basic usage:

```python
from pyfractions import Fraction

# Create Fraction objects
fraction1 = Fraction(1, 2)
fraction2 = Fraction(3, 4)

# Perform operations
sum_result = fraction1 + fraction2
difference_result = fraction1 - fraction2
product_result = fraction1 * fraction2
quotient_result = fraction1 / fraction2

# Display results
print(f'Sum: {sum_result}')               # Sum: 5/4
print(f'Difference: {difference_result}') # Difference: -1/4
print(f'Product: {product_result}')       # Product: 3/8
print(f'Quotient: {quotient_result}')     # Quotient: 2/3

# Check if fraction1 is greater than fraction2
is_greater = fraction1 > fraction2

# Display result
print(f'Is fraction1 greater than fraction2? {is_greater}') 
# Is fraction1 greater than fraction2? False
```