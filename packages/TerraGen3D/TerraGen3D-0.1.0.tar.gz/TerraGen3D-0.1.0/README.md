# TerraGen3D

TerraGen3D is an innovative Python library designed for geological modeling, enabling users to create, analyze, and visualize complex 3D geological structures with ease. From simulating sediment layers and modeling geological deformation to exploring mineral deposits, TerraGen3D brings your geological data to life.

## Features

- **3D Geological Modeling**: Generate and visualize complex 3D geological structures.
- **Fault Simulation**: Create realistic fault models within your geological data.
- **Data Visualization**: Utilize powerful visualization tools to explore your models.
- **Export Capabilities**: Export your geological data to CSV for further analysis.

## Installation

Install TerraGen3D using pip:

```bash
pip install TerraGen3D


Ensure you have Python 3.x installed on your system.
```
## Quick Start
Here's a simple example to get you started with TerraGen3D. This example demonstrates how to generate a geological model with faults and visualize it:

import TerraGen3D as tg

# Define parameters
num_points = 500  # Number of data points
num_faults = 3    # Number of faults to generate
fault_length = 0.3
fault_width = 0.05

# Generate data with faults
data_with_faults = tg.generate_fault(num_points, num_faults, fault_length, fault_width)

# Visualize the generated data
tg.plot_3d_data_realistic_with_noise_and_contour(data_with_faults)


## Contributing
We welcome contributions to TerraGen3D! Whether you're interested in fixing bugs, adding new features, or improving documentation, your help is appreciated.

Please check out our Contributing Guidelines for more information.


## License
TerraGen3D is licensed under the MIT License.


## Contact
For questions or feedback, please reach out to Olanrewaju Muili at olanrewaju.muili@gmail.com.