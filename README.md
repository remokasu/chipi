# CHIPI - Comprehensive History and Interactive Python Interface

CHIPI is a flexible and easy-to-use Python package for managing and manipulating data in buffers. It provides a comprehensive history tracking system and an interactive Python interface for handling data operations in buffers.

## Features

- Create and manage multiple buffers
- Flexible buffer size with optional maximum length
- Built-in methods for data manipulation and analysis
- Extendable with custom methods
- Import and export data from JSON and CSV files

## Installation

To install CHIPI, simply run:

```sh
pip install chipi
```

## Quick Start

```python
from chipi import Buffer, BufferManager

# Create a buffer and add some data
buf = Buffer("my_data")
buf.add(1)
buf.add(2)
buf.add(3)

# Retrieve data
print(buf.current_value)  # Output: 3
print(buf.previous_value)  # Output: 2
print(buf.data)  # Output: [1, 2, 3]

# Create a BufferManager for managing multiple buffers
labels = ["data1", "data2", "data3"]
buff_mgr = BufferManager(labels)

# Add data to the managed buffers
buff_mgr.d["data1"].add(10)
buff_mgr.d["data2"].add(20)
buff_mgr.d["data3"].add(30)

# Get data from a managed buffer
print(buff_mgr.get_data("data1"))  # Output: [10]
```