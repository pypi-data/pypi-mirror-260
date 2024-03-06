from distutils.core import setup
import os.path

setup(
    packages=["ps2ff"],
    package_data={
        "ps2ff": [
            os.path.join("tables", "*"),
            os.path.join("config", "*"),
            os.path.join("data", "*"),
        ]
    },
    scripts=[
        os.path.join("bin", "run_ps2ff"),
        os.path.join("bin", "run_ps2ff_single_event"),
        os.path.join("bin", "Cy14HwMeanVar.py"),
    ],
)
