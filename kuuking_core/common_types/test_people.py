from dataclasses import dataclass

@dataclass
class TestPeople:
    name: list[str]
    age: list[str]
    profession: list[str]

@dataclass
class Person:
    name: str
    age: str
    profession: str
