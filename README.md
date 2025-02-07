# LessonGenerator
POC demonstrating the detection of objects in images; and then generate a bunch of activities that children can do using those objects. 

> **Note:** Guardrails are not included.

---

## Pre-Requisites
1. Docker
2. Docker Compose
3. Make (Optional)

## Usage
1. Create `.env` file in the project root. Use `.env.example` as the template.
2. Use `make` to run this project:

```shell
# If this is your first time running the project:
make fresh

# Otherwise, run:
make run
```

For more handy shortcuts, check out the `Makefile`

## Stack
1. Flask as Backend
2. Streamlit as Frontend
