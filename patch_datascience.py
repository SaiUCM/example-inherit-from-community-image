import re, pathlib

p = pathlib.Path("/opt/conda/lib").glob("python3.*/site-packages/datascience/maps.py")
path = next(p)
txt = path.read_text()
txt = txt.replace("import pkg_resources", "import importlib.resources as _ir")
txt = re.sub(
    r'pkg_resources\.resource_filename\(__name__,\s*("geodata/geocode_states\.csv")\)',
    r'str(_ir.files(__name__) / \1)',
    txt,
)
path.write_text(txt)
print("patched", path)
