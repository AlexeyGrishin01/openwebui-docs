## Valves

`Valves` (see the dedicated [Valves & UserValves](../plugin/development/valves.md) page) can also be set for `Pipeline`. In short, `Valves` are input variables that are set per pipeline.

`Valves` are set as a subclass of the `Pipeline` class, and initialized as part of the `__init__` method of the `Pipeline` class.

When adding valves to your pipeline, include a way to ensure that valves can be reconfigured by admins in the web UI. There are a few options for this:

- Use `os.getenv()` to set an environment variable to use for the pipeline, and a default value to use if the environment variable isn't set. An example can be seen below:

```python
self.valves = self.Valves(
    **
)
```

- Set the valve to the `Optional` type, which will allow the pipeline to load even if no value is set for the valve.

```python
class Pipeline:
    class Valves(BaseModel):
        target_user_roles: List[str] = ["user"]
        max_turns: Optional[int] = None
```

If you don't leave a way for valves to be updated in the web UI, you'll see the following error in the Pipelines server log after trying to add a pipeline to the web UI:
`WARNING:root:No Pipeline class found in <pipeline name>`
