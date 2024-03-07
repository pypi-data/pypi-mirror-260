# aeroet
Surface energy balance and atmospheric profiling algorithms for calculating 
evapotranspiration from thermal imagery.

See Morgan, B.E. & Caylor, K.K. (2023). Estimating fine-scale transpiration from
UAV-derived thermal imagery and atmospheric profiles. *Water Resources Research*,
59, e2023WR035251. [https://doi.org/10.1029/2023WR035251](https://doi.org/10.1029/2023WR035251)

Note: The API and documentation are under development. Please contact Bryn Morgan
(brynmorgan@ucsb.edu) with any questions.




## Installation
1. Create a new conda environment.
```bash
$ conda create -n aeroet python=3.10
$ conda activate aeroet
```
*Note: I'm not sure whether specifying the version of python is necessary, but likely depends the version of python install in your `base` environment. Better to specify.*

2. `pip` install.
```bash
$ pip install aeroet
```
3. Use as desired!

## Usage
See [https://github.com/brynemorgan/uavet-wrr](https://github.com/brynemorgan/uavet-wrr) 
for example usage.