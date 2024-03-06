from typing import Any
from typing import Dict


async def modify(hub, name: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add the 'meta' from the run to the 'ctx' of the state
    """
    # Grab the META from the SLS file this state comes from
    try:
        sls_meta = hub.idem.RUNS[name]["meta"]["SLS"][chunk["__sls__"]]
        chunk["ctx"]["sls_meta"] = sls_meta
    except KeyError:
        chunk["ctx"]["sls_meta"] = None

    # Grab the META from the specific state
    try:
        id_meta = hub.idem.RUNS[name]["meta"]["ID_DECS"][
            f"{chunk['__sls__']}.{chunk['__id__']}"
        ]
        chunk["ctx"]["meta"] = id_meta
    except KeyError:
        chunk["ctx"]["meta"] = None

    return chunk
