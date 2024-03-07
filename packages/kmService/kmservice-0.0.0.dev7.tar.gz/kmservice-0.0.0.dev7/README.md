<p align="center">
   <em><h1>kmService</h1></em>
</p>

[![build](https://github.com/Hazedd/kmService/workflows/Build/badge.svg)](https://github.com/Hazedd/kmService/actions)
[![codecov](https://codecov.io/gh/Hazedd/kmService/branch/master/graph/badge.svg)](https://codecov.io/gh/Hazedd/kmService)
[![PyPI version](https://badge.fury.io/py/kmService.svg)](https://badge.fury.io/py/kmService)

---

**Documentation**: <a href="https://Hazedd.github.io/kmService/" target="_blank">https://Hazedd.github.io/kmService/</a>

**Source Code**: <a href="https://github.com/Hazedd/kmService" target="_blank">https://github.com/Hazedd/kmService</a>

---



## Install

```batch
pip install kmService
```

## Usage

```py
import asyncio
from kmService import KmService, get_km_service

if async:
    km_service_instance = await KmService.factory()
else:
    km_service_instance = get_km_service(url)

km_service_instance._get_km_async(x, y)

km_service_instance.get_point()


```

###
<script src="https://embed.github.com/view/geojson/Hazedd/kmService/current-coverage-km-server.geojson"></script>


### arcGisFeatureCache
**arcGisFeatureCache**: <a href="https://github.com/Hazedd/ArcGisFeatureCache" target="_blank">https://github.com/Hazedd/ArcGisFeatureCache</a>


## License

This project is licensed under the terms of the MIT license.
