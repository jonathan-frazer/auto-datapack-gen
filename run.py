import os
import sys
import shutil
from dotenv import load_dotenv

import parameter_assertions

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
from resourcepack.writers.pack_meta_writer import writeResourcepackMeta
from resourcepack.writers.pack_png_writer import writePackPng
from resourcepack.writers.item_definition_writer import writeItemDefinition
from resourcepack.writers.model_file_writer import writeModelFiles
from resourcepack.writers.texture_writer import writeAbilityTextures

load_dotenv()
packParams = parameter_assertions.load_datapack_parameters("parameters/pack_parameters.json")


def deletePrevious():
    datapacks_path = os.getenv("DATAPACK_PATH")
    resourcepacks_path = os.getenv("RESOURCEPACK_PATH")

    if (not datapacks_path or not os.path.exists(datapacks_path)) or (not resourcepacks_path or not os.path.exists(resourcepacks_path)):
        raise RuntimeError("Create .env file with valid DATAPACK_PATH and RESOURCEPACK_PATH")

    # Delete all contents inside datapacks_path
    for folder in os.listdir(datapacks_path):
        folder_path = os.path.join(datapacks_path, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        else:
            os.unlink(folder_path)

    # Delete all contents inside resourcepacks_path
    for folder in os.listdir(resourcepacks_path):
        folder_path = os.path.join(resourcepacks_path, folder)
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
        else:
            os.unlink(folder_path)


def run_pipeline(steps):
    for step in steps:
        step(packParams)


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
    resourcepack_pipeline = [
        writeResourcepackMeta,
        writePackPng,
        writeItemDefinition,
        writeModelFiles,
        writeAbilityTextures,
    ]

    run_pipeline(initialization_pipeline)
    run_pipeline(character_pipeline)
    run_pipeline(resourcepack_pipeline)
