python_sources(
    name="backend",
    dependencies=[
        "pantsbuild.pants.backend.python",
        "aiohttp",
        "asyncpg",
        "websockets",
        "pytest",
    ],
)

python_tests(
    name="backend_tests",
    dependencies=[
        ":backend",
    ],
)
