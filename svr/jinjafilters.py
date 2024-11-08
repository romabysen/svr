import inflect

inflect_engine = inflect.engine()


def plural(value: str) -> str:
    return inflect_engine.plural(value)
