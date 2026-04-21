def connect(parent: dict[str, object], child: dict[str, object]) -> None:
    if (not child["parent"] is parent) and (not child in parent["childs"]): 
        child["parent"] = parent
        parent["childs"].append(child)

def deconnect(parent: dict[str, object], child: dict[str, object]) -> None:
    if (child["parent"] is parent) and (child in parent["childs"]):
        child["parent"] = None
        parent["childs"].remove(child)