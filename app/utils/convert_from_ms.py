from fastapi import Query


async def convert_from_ms(
    timeout: float = Query(..., description="Timeout in ms", example=1500, gt=0)
):
    return timeout / 1000
