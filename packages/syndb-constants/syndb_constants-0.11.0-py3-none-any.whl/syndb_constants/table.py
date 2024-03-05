from enum import Enum, auto
from typing import Literal

ID_COLUMN_NAME = "cid"
DATASET_ID_COLUMN_NAME = "dataset_id"
PARENT_ID_COLUMN_NAME = "parent_id"
PARENT_ENUM_COLUMN_NAME = "parent_enum"


SyndbTableNames = Literal[
    "neuron",
    "dendrite",
    "axon",
    "pre_synaptic_terminal",
    "synapse",
    "dendritic_spine",
    "endoplasmic_reticulum",
    "nucleus",
    "vesicle",
    "mitochondria",
]


class SyndbTable(Enum):
    # Neuro data hierarchy ==================
    NEURON = auto()

    # Neurites
    DENDRITE = auto()
    AXON = auto()
    PRE_SYNAPTIC_TERMINAL = auto()
    SYNAPSE = auto()
    DENDRITIC_SPINE = auto()

    # Cellular structures
    ENDOPLASMIC_RETICULUM = auto()
    NUCLEUS = auto()

    # Smaller organelles
    VESICLE = auto()
    MITOCHONDRIA = auto()


syndb_table_name_to_enum = {e.name.lower(): e for e in SyndbTable}

syndb_table_to_table_name = {st: st.name.lower() for st in SyndbTable}
syndb_table_supported_str = ", ".join(syndb_table_to_table_name.values())

table_name_to_syndb_table = {n: s for s, n in syndb_table_to_table_name.items()}


COMPARTMENT_HIERARCHY: list[tuple[SyndbTable, ...]] = [
    (SyndbTable.NEURON,),
    (SyndbTable.DENDRITE, SyndbTable.AXON),
    (SyndbTable.PRE_SYNAPTIC_TERMINAL, SyndbTable.SYNAPSE, SyndbTable.DENDRITIC_SPINE),
    (
        SyndbTable.MITOCHONDRIA,
        SyndbTable.ENDOPLASMIC_RETICULUM,
        SyndbTable.NUCLEUS,
        SyndbTable.VESICLE,
    ),
]

_max_line = 0
compartment_to_valid_parents: dict[SyndbTable, tuple[SyndbTable, ...]] = {}
for level in range(1, len(COMPARTMENT_HIERARCHY)):
    parents = []
    for parent_group in COMPARTMENT_HIERARCHY[:level]:
        parents.extend(parent_group)

    level_tables = COMPARTMENT_HIERARCHY[level]

    # For centering `syndb_table_hierarchy_print`
    _total_line_length = sum(len(table.name) for table in level_tables) + (len(level_tables) - 1) * 2
    _max_line = max(_max_line, _total_line_length)

    ascending_parents = tuple(reversed(parents))
    for l_comp in level_tables:
        compartment_to_valid_parents[l_comp] = ascending_parents

syndb_table_hierarchy_print = "\n".join(
    ", ".join(syndb_table.name.lower() for syndb_table in level).center(_max_line) for level in COMPARTMENT_HIERARCHY
)
syndb_table_hierarchy_descending = [SyndbTable.NEURON, *compartment_to_valid_parents]
