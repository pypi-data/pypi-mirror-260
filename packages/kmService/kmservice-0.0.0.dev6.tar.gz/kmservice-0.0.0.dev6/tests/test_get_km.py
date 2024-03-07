import asyncio

import pytest

from kmService.km_service import KmService

feature_service_instance_km = asyncio.run(KmService.factory())


@pytest.mark.parametrize(
    "feature_service_instance_km",
    [
        (feature_service_instance_km),
    ],
)
@pytest.mark.asyncio
async def test_km_service(feature_service_instance_km: KmService):
    assert len(feature_service_instance_km._value_objects_dict.keys()) == 670

    _ = [
        [176186.3034, 362277.276],
        [176167.4443, 362276.1518],
        [176290.652, 362255.5943],
        [176267.8789, 362260.7968],
        [176248.7935, 362269.5774],
    ]
    for item in _:
        response = await feature_service_instance_km._get_km_async(item[0], item[1])
        print(response[0].km_value_str)
