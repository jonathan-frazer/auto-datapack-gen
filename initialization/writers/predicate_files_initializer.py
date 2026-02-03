import os
from ..basic_predicates_builder import get_basic_predicate_content


def initializePredicateFiles(datapackParams):
    predicate_file_path = os.path.join(
        os.getenv("DATAPACKS_PATH"),
        datapackParams["pack_name"],
        "data",
        datapackParams["namespace"],
        "predicate",
    )
    os.makedirs(predicate_file_path, exist_ok=True)

    for filename in ["is_sneaking.json", "is_sprinting.json", "is_on_ground.json"]:
        with open(os.path.join(predicate_file_path, filename), "w") as f:
            f.write(get_basic_predicate_content(filename.split(".")[0]))
