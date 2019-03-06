"""Setup for xblock-hl-learning-activities XBlock."""

import os
from setuptools import setup, find_packages


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}

# Constants #########################################################
VERSION = '0.1'

# xblocks  #########################################################
PREREQs = [
    'XBlock',
    'xblock-hl-text',
    'xblock-utils',
]

BLOCKS = [
    # the main learning activity block
    'hl_learning_activities = hl_learning_activities:HL_LearningActivity_XBlock',

    # child blocks
    'la_intro = hl_learning_activities.child_blocks:la_intro',
    'la_step = hl_learning_activities.child_blocks:la_step',
]

setup(
    name='xblock-hl_learning_activities',
    version=VERSION,
    author="cRivet",
    description='Custom Xblock for generating a learning activity for use in HydroLearn platform. (using hl_text)',
    packages=[
        'hl_learning_activities',
    ],

    install_requires=PREREQs,
    entry_points={
        'xblock.v1': BLOCKS,
    },
    package_data=package_data("hl_learning_activities", ["static", "public", "templates"]),
)
