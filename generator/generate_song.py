import importlib


def generate_section(section_name, section_type, bars, file_rg, file_d):
    rhythm_guitar = f"rhythm_guitar.{section_name}.{section_type}"
    try:
        module = importlib.import_module(rhythm_guitar)
        data = module.generate(file_rg, bars, 4)
    except ImportError:
        print(f"Module {rhythm_guitar} not found.")
    except AttributeError:
        print(f"Module {rhythm_guitar} does not have a generate function.")

    drums = f"drums.{section_name}.{section_type}"
    try:
        module = importlib.import_module(drums)
        module.generate(file_d, data)
    except ImportError:
        print(f"Module {drums} not found.")
    except AttributeError:
        print(f"Module {drums} does not have a generate function.")


def generate_song(structure):
    for section, element, bars in structure:
        generate_section(section, element, bars)

