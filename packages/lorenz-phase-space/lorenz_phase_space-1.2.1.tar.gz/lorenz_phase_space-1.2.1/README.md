[![PyPI](https://img.shields.io/pypi/v/lorenz-phase-space?label=pypi%20version)](https://pypi.org/project/lorenz-phase-space/)
[![CircleCI](https://circleci.com/gh/daniloceano/lorenz_phase_space.svg?style=shield)](https://app.circleci.com/pipelines/github/daniloceano/lorenz_phase_space)


# Lorenz Phase Space Visualization


<img src="https://github.com/daniloceano/lorenz_phase_space/assets/56005607/862e0916-4960-4658-b7eb-91f7ad57fe9f" width="550">


## Overview

The Lorenz Phase Space (LPS) visualization tool is designed to analyze and illustrate the dynamics of the Lorenz Energy Cycle in atmospheric science.

This tool offers a unique perspective for studying the intricate processes governing atmospheric energetics and instability mechanisms.
It visualizes the transformation and exchange of energy within the atmosphere, specifically focusing on the interactions between kinetic and potential energy forms as conceptualized by Edward Lorenz.

Key features of the tool include:

- Mixed Mode Visualization: Offers insights into both baroclinic and barotropic instabilities, which are fundamental in understanding large-scale atmospheric dynamics. 
This mode is particularly useful for comprehensively analyzing scenarios where both instabilities are at play.

- Baroclinic Mode: Focuses on the baroclinic processes, highlighting the role of temperature gradients and their impact on atmospheric energy transformations.
This mode is vital for studying weather systems and jet stream dynamics.

- Barotropic Mode: Concentrates on barotropic processes, where the redistribution of kinetic energy is predominant. 
This mode is essential for understanding the horizontal movement of air and its implications on weather patterns.


By utilizing the LPS tool, researchers and meteorologists can delve into the complexities of atmospheric energy cycles, gaining insights into how different energy forms interact and influence weather systems and climate patterns. 
The tool's ability to switch between different modes (mixed, baroclinic, and barotropic) allows for a multifaceted analysis of atmospheric dynamics, making it an invaluable resource in the field of meteorology and climate science.

## Features

- Visualization of data in Lorenz Phase Space.
- Support for different types of Lorenz Phase Spaces: mixed, baroclinic, and barotropic.
- Dynamic adjustment of visualization parameters based on data scale.
- Customizable plotting options for detailed analysis.

## Installation

To use this tool, ensure you have Python installed along with the required libraries: pandas, matplotlib, numpy, and cmocean. You can install these packages using pip:


```pip install pandas matplotlib numpy cmocean```

## Usage

# Simple Example with Zoom Disabled

This example demonstrates using the Lorenz Phase Space visualization tool for a single dataset.

```
from lorenz_phase_space.phase_diagrams import Visualizer
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv('your_data.csv')

# Initialize the Lorenz Phase Space plotter without zoom
lps = Visualizer(LPS_type='mixed', zoom=False)

# Plot your data
lps.plot_data(
    x_axis=data['Ck'],
    y_axis=data['Ca'],
    marker_color=data['Ge'],
    marker_size=data['Ke']
)

# Save the visualization
fname = 'samples/sample_1_LPS_mixed'
plt.savefig(f"{fname}.png", dpi=300)
print(f"Saved {fname}.png")
```

# Using Two Datasets with Zoom Enabled

This example shows how to plot data from two datasets with zoom enabled for detailed analysis.

```
from lorenz_phase_space.phase_diagrams import Visualizer
import pandas as pd
import matplotlib.pyplot as plt

# Load your datasets
data1 = pd.read_csv('dataset1.csv')
data2 = pd.read_csv('dataset2.csv')

# Initialize the Lorenz Phase Space plotter with zoom
lps = Visualizer(LPS_type='mixed', zoom=True)

# Plot data from the first dataset
lps.plot_data(
    x_axis=data1['Ck'],
    y_axis=data1['Ca'],
    marker_color=data1['Ge'],
    marker_size=data1['Ke']
)

# Plot data from the second dataset
lps.plot_data(
    x_axis=data2['Ck'],
    y_axis=data2['Ca'],
    marker_color=data2['Ge'],
    marker_size=data2['Ke']
)

# Save the visualization
fname = 'samples/sample_1_LPS_mixed_zoom_multiple'
plt.savefig(f"{fname}.png", dpi=300)
print(f"Saved {fname}.png")
```

# Using Multiple Datasets with Dynamically Updating Limits

This example demonstrates dynamically updating plot limits based on multiple datasets for enhanced visualization with zoom enabled.

```
from lorenz_phase_space.phase_diagrams import Visualizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your datasets
data1 = pd.read_csv('dataset1.csv')
data2 = pd.read_csv('dataset2.csv')

# Dynamically determine plot limits
x_min, x_max = np.min([data1['Ck'].min(), data2['Ck'].min()]), np.max([data1['Ck'].max(), data2['Ck'].max()])
y_min, y_max = np.min([data1['Ca'].min(), data2['Ca'].min()]), np.max([data1['Ca'].max(), data2['Ca'].max()])
color_min, color_max = np.min([data1['Ge'].min(), data2['Ge'].min()]), np.max([data1['Ge'].max(), data2['Ge'].max()])
size_min, size_max = np.min([data1['Ke'].min(), data2['Ke'].min()]), np.max([data1['Ke'].max(), data2['Ke'].max()])

# Initialize Lorenz Phase Space with dynamic limits
lps = Visualizer(
    LPS_type='mixed',
    zoom=True,
    x_limits=[x_min, x_max],
    y_limits=[y_min, y_max],
    color_limits=[color_min, color_max],
    marker_limits=[size_min, size_max]
)

# Plot data from both datasets
lps.plot_data(x_axis=data1['Ck'], y_axis=data1['Ca'], marker_color=data1['Ge'], marker_size=data1['Ke'])
lps.plot_data(x_axis=data2['Ck'], y_axis=data2['Ca'], marker_color=data2['Ge'], marker_size=data2['Ke'])

# Save the visualization
fname = 'samples/sample_1_LPS_mixed_zoom_multiple_dynamic'
plt.savefig(f"{fname}.png", dpi=300)
print(f"Saved {fname}.png")
```

These examples cover a range of scenarios from simple usage to more complex visualizations involving multiple datasets and dynamic adjustment of plot limits, showcasing the flexibility of the Lorenz Phase Space visualization tool.

## Contributing

Contributions to the LPS project are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or further assistance with the Lorenz Phase Space project, please reach out to danilo.oceano@gmail.com.
