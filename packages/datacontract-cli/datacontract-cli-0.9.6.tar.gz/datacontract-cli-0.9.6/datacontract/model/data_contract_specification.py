import os
from typing import List, Dict

import pydantic
import yaml
from pydantic import BaseModel


class Contact(BaseModel):
    name: str = None
    url: str = None
    email: str = None


class Server(BaseModel):
    type: str = None
    format: str = None
    project: str = None
    dataset: str = None
    path: str = None
    delimiter: str = None
    endpointUrl: str = None
    location: str = None
    account: str = None
    database: str = None
    schema_: str = pydantic.fields.Field(default=None, alias='schema')
    host: str = None
    port: int = None
    catalog: str = None
    topic: str = None
    http_path: str = None # Use ENV variable
    token: str = None     # Use ENV variable
    dataProductId: str = None
    outputPortId: str = None


class Terms(BaseModel):
    usage: str = None
    limitations: str = None
    billing: str = None
    noticePeriod: str = None


class Field(BaseModel):
    ref: str = None
    type: str = None
    format: str = None
    required: bool = None
    unique: bool = None
    description: str = None
    pii: bool = None
    classification: str = None
    pattern: str = None
    minLength: int = None
    maxLength: int = None
    minimum: int = None
    minimumExclusive: int = None
    maximum: int = None
    maximumExclusive: int = None
    enum: List[str] = []
    tags: List[str] = []
    fields: Dict[str, 'Field'] = {}

    @property
    def ref(self):
        return self.schema.get("$ref")


class Model(BaseModel):
    description: str = None
    type: str = None
    fields: Dict[str, Field] = {}


class Info(BaseModel):
    title: str = None
    version: str = None
    description: str = None
    owner: str = None
    contact: Contact = None


class Example(BaseModel):
    type: str = None
    description: str = None
    model: str = None
    data: str | object = None


class Quality(BaseModel):
    type: str = None
    specification: str | object = None


class DataContractSpecification(BaseModel):
    dataContractSpecification: str = None
    id: str = None
    info: Info = None
    servers: Dict[str, Server] = {}
    terms: Terms = None
    models: Dict[str, Model] = {}
    # schema: Dict[str, str]
    examples: List[Example] = []
    quality: Quality = None

    @classmethod
    def from_file(cls, file):
        if not os.path.exists(file):
            raise(f"The file '{file}' does not exist.")
        with open(file, 'r') as file:
            file_content = file.read()
        return DataContractSpecification.from_string(file_content)

    @classmethod
    def from_string(cls, data_contract_str):
        data = yaml.safe_load(data_contract_str)
        return DataContractSpecification(**data)

    def to_yaml(self):
        return yaml.dump(self.model_dump(exclude_defaults=True, exclude_none=True), sort_keys=False)
