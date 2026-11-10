import json
from typing import Annotated, Literal

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Location event mock server")

FiniteFloat = Annotated[float, Field(allow_inf_nan=False)]


class LocationPoint(BaseModel):
    latitude: Annotated[FiniteFloat, Field(ge=-90, le=90)]
    longitude: Annotated[FiniteFloat, Field(ge=-180, le=180)]
    accuracy: FiniteFloat | None
    altitude: FiniteFloat | None
    speed: FiniteFloat | None
    heading: FiniteFloat | None
    timestamp: Annotated[int, Field(ge=0)]


class LocationEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["location"]
    platform: Literal["ios", "android", "web"]
    sessionId: Annotated[str, Field(min_length=1)]
    sentAt: Annotated[str, Field(min_length=1)]
    locations: Annotated[list[LocationPoint], Field(min_length=1, max_length=100)]


class LocationReceipt(BaseModel):
    received: int


@app.post("/locations", response_model=LocationReceipt)
def receive_locations(event: LocationEvent) -> LocationReceipt:
    print(json.dumps(event.model_dump(), indent=2), flush=True)
    return LocationReceipt(received=len(event.locations))


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()