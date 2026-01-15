
def auto_link_methods(methods):
    for m in methods:
        m.setdefault("related_methods", [])
        for other in methods:
            if m["id"] != other["id"] and m["category"] == other["category"]:
                m["related_methods"].append(other["id"])
    return methods
