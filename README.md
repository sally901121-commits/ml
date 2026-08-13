# CSV Graph Plotter

A lightweight tool to quickly generate graphs from CSV files for experiment analysis and visualization.

## Overview

This project provides a simple and fast way to visualize data from CSV files. Perfect for experimental work, data analysis, and quick visualizations without the need for complex code.

**Main Features:**
- Load CSV files with a single command
- Generate plots instantly
- Support for multiple chart types (line, scatter, bar, histogram, etc.)
- Customizable graph styling
- Export plots as images

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/sally901121-commits/ml.git
cd ml
pip install -r requirements.txt
```

### Dependencies

Common libraries you'll need:
```
pandas>=1.3.0
matplotlib>=3.4.0
numpy>=1.21.0
```

## Usage

### Basic Usage

```bash
python plot.py --csv data.csv
```

### Advanced Usage

```bash
# Plot specific columns
python plot.py --csv data.csv --x column_name --y column_name

# Change plot type
python plot.py --csv data.csv --type scatter

# Save output
python plot.py --csv data.csv --output graph.png

# Add title and labels
python plot.py --csv data.csv --title "My Experiment" --xlabel "Time" --ylabel "Value"
```

## Supported Plot Types

- `line` - Line plot (default)
- `scatter` - Scatter plot
- `bar` - Bar chart
- `hist` - Histogram
- `box` - Box plot

## Project Structure

```
ml/
├── plot.py            # Main plotting script
├── utils.py           # Utility functions for CSV handling
├── requirements.txt   # Project dependencies
├── sample_data/       # Example CSV files
└── README.md          # This file
```

## Example

### Sample CSV Format
```
time,temperature,humidity
1,25.3,60
2,26.1,62
3,25.8,61
```

### Generate Plot
```bash
python plot.py --csv sample_data/experiment.csv --x time --y temperature --type line --output results.png
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Contact

Questions or suggestions? Feel free to reach out!
