from enums import Mode
from relational_coding.relational_coding_base import RelationalCodingBase


class FmriRelationalCoding(RelationalCodingBase):

    def single_tr_correlation(self, timepoint):
        pass

    def rest_between_iteration(self):
        rest_tr_gen = self.rest_between_tr_generator()
        _tr = next(rest_tr_gen, None)
        while _tr:
            self.single_tr_correlation(timepoint=_tr)

    def run(self, roi):
        subject_gen = self.yield_subject_generator()
        sub_id = next(subject_gen, None)
        while sub_id:
            roi_sub_data_task = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.CLIPS)
            roi_sub_data_rest = self.load_roi_data(roi_name=roi, subject=sub_id, mode=Mode.REST)


