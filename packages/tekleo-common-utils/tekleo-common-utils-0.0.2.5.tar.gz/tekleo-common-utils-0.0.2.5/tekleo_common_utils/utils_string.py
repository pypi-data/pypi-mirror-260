from typing import List, Tuple

from injectable import injectable


@injectable
class UtilsString:
    def remove_mixed_spaces(self, text: str) -> str:
        words = text.split(' ')
        new_words = [word.strip() for word in words if len(word.strip()) > 0]
        return ' '.join(new_words)

    def find_all(self, text: str, slice: str) -> List[int]:
        if text == '':
            return []
        if slice == '':
            return []

        indexes = []
        start = 0
        while start != -1:
            start = text.find(slice, start)
            if start != -1:
                indexes.append(start)
                start = start + len(slice)
        return indexes

    def find_all_as_start_end_indexes(self, text: str, slice: str) -> List[Tuple[int, int]]:
        result = []
        start_indexes = self.find_all(text, slice)
        for start_index in start_indexes:
            start_end_tuple = (start_index, start_index + len(slice))
            result.append(start_end_tuple)
        return result
