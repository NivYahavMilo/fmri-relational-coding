import json
from typing import List, Optional


ROI_NAMES = []
SUBJECTS = ['100610',
            '102311']

class StaticData:
    ROI_NAMES:Optional[List]
    SUBJECTS: Optional[List]

    @classmethod
    def inhabit_class_members(cls):
        """
        load json file
        set class attr
        """
        f = open('data.json')
        data = json.load(f)

        for attr, values in data.items():
            setattr(cls, attr, values)
