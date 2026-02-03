import os
from ..basic_predicates_builder import get_basic_predicate_content


def initializePredicateFiles(packParams):
    predicate_file_path = os.path.join(
        os.getenv("DATAPACK_PATH"),
        packParams["pack_name"],
        "data",
        packParams["namespace"],
        "predicate",
    )
    os.makedirs(predicate_file_path, exist_ok=True)

    for filename in ["is_sneaking.json", "is_sprinting.json", "is_on_ground.json"]:
        with open(os.path.join(predicate_file_path, filename), "w") as f:
            f.write(get_basic_predicate_content(filename.split(".")[0]))
