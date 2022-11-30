from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase

class FmriRelationalCoding(RelationalCodingBase):

    def run(self, roi):
        sub = next(self.yield_subject_iterator())
        roi_sub_data = self.load_roi_data(roi_name=roi,subject=sub)




