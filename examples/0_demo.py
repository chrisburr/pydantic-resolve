import asyncio
from pydantic import BaseModel
from pydantic_resolve import Resolver

async def query_age(name):
    print(f'query {name}')
    await asyncio.sleep(1)
    _map = {
        'kikodo': 21,
        'John': 14,
        '老王': 40,
    }
    return _map.get(name)

class Person(BaseModel):
    name: str

    age: int = 0
    async def resolve_age(self):
        return await query_age(self.name)

    is_adult: bool = False
    def post_is_adult(self):
        return self.age > 18

async def simple():
    p = Person(name='kikodo')
    p = await Resolver().resolve(p)
    print(p)
    # Person(name='kikodo', age=21, is_adult=True)

    people = [Person(name=n) for n in ['kikodo', 'John', '老王']]
    people = await Resolver().resolve(people)
    print(people)
    # issue of N+1 query
    # [Person(name='kikodo', age=21, is_adult=True), Person(name='John', age=14, is_adult=False), Person(name='老王', age=40, is_adult=True)]

asyncio.run(simple())
