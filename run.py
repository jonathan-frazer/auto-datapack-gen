import os
import sys
import json
import shutil
from dotenv import load_dotenv

# Add the project root to sys.path to enable correct module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from initialization.writers.pack_meta_writer import writePackMeta
from initialization.writers.function_tags_writer import writeFunctionTags
from initialization.writers.predicate_files_initializer import initializePredicateFiles
from initialization.writers.advancement_files_initializer import initializeAdvancementFiles
from initialization.writers.reload_file_writer import writeReloadFile
from initialization.writers.main_function_writers import writeMainFile, writeMainHalfSecFile, writeMainSecFile
from initialization.writers.craft_file_writer import writeCraftFile
from character.writers.item_detect_predicate_creator import createItemDetectPredicate
from character.writers.activation_deactivation_function_writer import writeActivationFunction, writeDeactivationFunction
from character.writers.effect_function_writers import writeTickFunction, writeEffectFunction, writeQuickEffectFunction
from character.writers.ability_slot_writer import createAbilityFiles, createAdvancementFiles


load_dotenv()
datapackParams = json.loads(open("parameters/datapack_parameters.json").read())


def deletePrevious():
    datapacks_path = os.getenv("DATAPACKS_PATH")
    if not datapacks_path or not os.path.exists(datapacks_path):
        return
    for folder in os.listdir(datapacks_path):
        folder_path = os.path.join(datapacks_path, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        else:
            os.unlink(folder_path)


def run_pipeline(steps):
    for step in steps:
        step(datapackParams)


if __name__ == "__main__":
    initialization_pipeline = [
        lambda dp: deletePrevious(),
        writePackMeta,
        writeFunctionTags,
        initializePredicateFiles,
        initializeAdvancementFiles,
        writeReloadFile,
        writeMainFile,
        writeCraftFile,
        writeMainSecFile,
        writeMainHalfSecFile,
    ]
    character_pipeline = [
        createAdvancementFiles,
        createItemDetectPredicate,
        createAbilityFiles,
        writeActivationFunction,
        writeDeactivationFunction,
        writeTickFunction,
        writeQuickEffectFunction,
        writeEffectFunction,
    ]

    run_pipeline(initialization_pipeline)
    run_pipeline(character_pipeline)
