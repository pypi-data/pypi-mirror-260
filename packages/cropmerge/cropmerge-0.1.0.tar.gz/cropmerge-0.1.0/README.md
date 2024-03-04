# cropmerge
Library for cropping point clouds in blocks and merge them with semantic and instance labels.

## Overview
Points in hte overlap area are repeated betweeen blocks.
For merging semantic labels it is used the probability of each class as input. The output probability of a point is the mean of the probabilities of that points in each block.
For merging instance labels the are not merged point by point, bt instance by instance. Instance j of block J and instance i of block I are merge if and only if the maximum IoU of instane j with all the instances of block I is with the instance i, and vice versa.  

## Citation


## Licence
cropmerge

Copyright (C) 2023 GeoTECH Group <geotech@uvigo.gal>

Copyright (C) 2023 Daniel Lamas Novoa <daniel.lamas.novoa@uvigo.gal>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program in ![COPYING](https://github.com/GeoTechUVigo/cropmerge/blob/main/COPYING). If not, see <https://www.gnu.org/licenses/>.

## Installation
To install cropmerge (available in test.pypi):
```
python3 -m pip install --extra-index-url https://test.pypi.org/simple/ cropmerge==0.0.2
```