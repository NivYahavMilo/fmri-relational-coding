from relational_coding.relational_coding_base import RelationalCodingBase

class FmriRelationalCoding(RelationalCodingBase):

    def run(self, roi):
        subject_gen = self.yield_subject_iterator()
        sub_id = next(subject_gen,None)
        while sub_id:
            roi_sub_data = self.load_roi_data(roi_name=roi,subject=sub_id)




