import os
import sys
from dotenv import load_dotenv

# Add the project root to sys.path to enable correct module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import shutil
from collections import deque

# Initialization Pipeline Imports
from initialization.writers.pack_meta_writer import writePackMeta
from initialization.writers.function_tags_writer import writeFunctionTags
from initialization.writers.predicate_files_initializer import initializePredicateFiles
from initialization.writers.reload_file_writer import writeReloadFile
from initialization.writers.main_file_writer import writeMainFile
from initialization.writers.main_halfsec_file_writer import writeMainHalfSecFile
from initialization.writers.main_sec_file_writer import writeMainSecFile
from initialization.writers.craft_file_writer import writeCraftFile

# Character Pipeline Imports
from character.writers.item_detect_predicate_creator import createItemDetectPredicate
from character.writers.activation_function_writer import writeActivationFunction
from character.writers.deactivation_function_writer import writeDeactivationFunction
from character.writers.tick_function_writer import writeTickFunction
from character.writers.effect_function_writer import writeEffectFunction
from character.writers.quick_effect_function_writer import writeQuickEffectFunction

load_dotenv()
datapackParams = json.loads(open('parameters/datapack_parameters.json').read())

def deletePrevious():
	datapacks_path = os.getenv('DATAPACKS_PATH')
	if os.path.exists(datapacks_path):
		for folder in os.listdir(datapacks_path):
			folder_path = os.path.join(datapacks_path, folder)
			if os.path.isdir(folder_path):
				shutil.rmtree(folder_path)
			else:
				os.unlink(folder_path)

if __name__ == "__main__":
	intializationPipeline = deque([
        lambda dp: deletePrevious(),
		writePackMeta,
		writeFunctionTags,
		initializePredicateFiles,
        writeReloadFile,
		writeMainFile,
		writeCraftFile,
		writeMainSecFile,
		writeMainHalfSecFile
	])
	characterPipeline = deque([
		createItemDetectPredicate,
		writeActivationFunction,
		writeDeactivationFunction,
		writeTickFunction,
		writeQuickEffectFunction,
		writeEffectFunction
	])

	finalPipeline = deque([intializationPipeline,characterPipeline])
	def runPipeline(pipeline):
		for item in pipeline:
			if isinstance(item, deque):	runPipeline(item)
			else:						item(datapackParams)

	runPipeline(finalPipeline)
