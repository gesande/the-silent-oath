# ============================================================
#  engine/conditions.py
#  Data-driven condition evaluator.
#
#  A condition is either:
#    - None                         → always True
#    - a callable                   → called with state (legacy)
#    - a dict with one of these keys:
#
#  Primitives:
#    {"flag":     "name"}           → state.flags.get("name") is truthy
#    {"memory":   "name"}           → state.has_memory("name")
#    {"has_item": "name"}           → "name" in state.inventory
#    {"equipped": "name"}           → state.equipped["weapon"] == "name"
#    {"stat_gte": "stat", "value": N} → getattr(state, "stat") >= N
#
#  Combinators:
#    {"not": <cond>}
#    {"and": [<cond>, ...]}
#    {"or":  [<cond>, ...]}
# ============================================================


def eval_condition(cond, state) -> bool:
    if cond is None:
        return True
    if callable(cond):
        return bool(cond(state))

    if "flag" in cond:
        return bool(state.flags.get(cond["flag"]))

    if "memory" in cond:
        return state.has_memory(cond["memory"])

    if "has_item" in cond:
        return cond["has_item"] in state.inventory

    if "equipped" in cond:
        return state.equipped.get("weapon") == cond["equipped"]

    if "stat_gte" in cond:
        return getattr(state, cond["stat_gte"]) >= cond["value"]

    if "not" in cond:
        return not eval_condition(cond["not"], state)

    if "and" in cond:
        return all(eval_condition(c, state) for c in cond["and"])

    if "or" in cond:
        return any(eval_condition(c, state) for c in cond["or"])

    raise ValueError(f"Unknown condition: {cond!r}")
