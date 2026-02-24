FROM python:3.11-buster
ARG _workdir=/app
WORKDIR ${_workdir}

RUN pip install poetry

COPY src/poetry.lock src/pyproject.toml ${_workdir}/
RUN poetry install --no-root

COPY src/ ${_workdir}/

ENTRYPOINT [ "poetry", "run", "python3", "main.py" ]
CMD ["-h"]