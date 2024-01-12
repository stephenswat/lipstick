import pydantic
import typing


class DataType(pydantic.BaseModel):
    size: int
    count: int


class Interconnect(pydantic.BaseModel):
    source: str
    destination: str
    bandwidth: int
    bidirectional: typing.Optional[bool] = False

    @pydantic.validator("bandwidth")
    def bandwidth_positive(v):
        if v <= 0:
            raise ValueError("Interconnect bandwidth must be positive and non-zero")
        return v


class Implementation(pydantic.BaseModel):
    device: str
    throughput: float


class Algorithm(pydantic.BaseModel):
    in_type: str
    out_type: str
    implementations: typing.List[Implementation]


class TaskGraph(pydantic.BaseModel):
    datatypes: typing.Dict[str, DataType]
    devices: typing.List[str]
    interconnects: typing.List[Interconnect]
    algorithms: typing.Dict[str, Algorithm]
    source: str
    sink: str

    @pydantic.model_validator(mode="after")
    def datatype_names_valid(self):
        types = self.datatypes.keys()
        devices = self.devices

        for i in self.interconnects:
            if i.source not in devices:
                raise ValueError(
                    'Interconnect source device "%s" does not exist.' % (i.source)
                )

            if i.destination not in devices:
                raise ValueError(
                    'Interconnect destination device "%s" does not exist.'
                    % (i.destination)
                )

        for a in self.algorithms.values():
            if a.in_type not in types:
                raise ValueError(
                    'Algorithm input type "%s" does not exist.' % (a.in_type)
                )

            if a.out_type not in types:
                raise ValueError(
                    'Algorithm output type "%s" does not exist.' % (a.out_type)
                )

        if self.source not in types:
            raise ValueError('Source type "%s" does not exist.' % (self.source))

        if self.sink not in types:
            raise ValueError('Sink type "%s" does not exist.' % (self.sink))

        return self
