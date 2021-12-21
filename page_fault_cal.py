class PageFaultCal:

    def __init__(self, alg: str):
        self.alg = alg

    def calculate(self, num_of_frames, ref_list):
        if self.alg == 'lru'.lower():
            return self._lru(num_of_frames, ref_list)
        if self.alg == 'fifo'.lower():
            return self._fifo(num_of_frames, ref_list)
        if self.alg == 'optimal'.lower():
            return self._optimal(num_of_frames, ref_list)
        else:
            raise ValueError('please give alg value from lru, fifo, optimal')

    @staticmethod
    def _fifo(num_of_frames, ref_list):
        if num_of_frames == 1:
            return len(ref_list)
        tlb = [None] * num_of_frames
        replace_i = 0
        page_fault_count = 0
        for ref in ref_list:
            if ref in tlb:
                continue
            page_fault_count += 1
            tlb[replace_i] = ref
            replace_i += 1
            if replace_i == num_of_frames:
                replace_i = 0
        return page_fault_count

    @staticmethod
    def _lru(num_of_frames, ref_list):
        if num_of_frames == 1:
            return len(ref_list)
        page_fault_count = 0
        tlb = [None] * num_of_frames
        for i, ref in enumerate(ref_list):
            if ref in tlb:
                continue
            last_tlb = tlb.copy()
            for j in reversed(range(i)):
                if ref_list[j] in last_tlb:
                    last_tlb.remove(ref_list[j])
                if len(last_tlb) == 1:
                    break
            if None in tlb:
                for x in range(len(tlb)):
                    if tlb[x] is None:
                        tlb[x] = ref
                        break
            else:
                tlb = [ref if x == last_tlb[0] else x for x in tlb]
            # print(tlb)
            page_fault_count += 1
        return page_fault_count

    @staticmethod
    def _optimal(num_of_frames, ref_list):
        if num_of_frames == 1:
            return len(ref_list)
        page_fault_count = 0
        tlb = [None] * num_of_frames
        for i, ref in enumerate(ref_list):
            if ref in tlb:
                continue
            last_tlb = tlb.copy()
            for j in range(i + 1, len(ref_list)):
                if ref_list[j] in last_tlb:
                    last_tlb.remove(ref_list[j])
                if len(last_tlb) == 1:
                    break
            if None in tlb:
                for x in range(len(tlb)):
                    if tlb[x] is None:
                        tlb[x] = ref
                        break
            else:
                tlb = [ref if x == last_tlb[0] else x for x in tlb]
            # print(tlb)
            page_fault_count += 1
        return page_fault_count


if __name__ == "__main__":
    alg = 'optimal'
    lru_cal = PageFaultCal(alg)
    ref_list = [1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6, 3, 2, 1, 2, 3, 6]
    num_of_frames = 7
    page_fault_count = lru_cal.calculate(num_of_frames, ref_list)
    print(page_fault_count)