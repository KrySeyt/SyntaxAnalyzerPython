# S -> TE_END
# E -> +TE|-TE|EPSILON
# T -> PD
# D -> *T|EPSILON
# P -> (TE)|I
# I -> a|b|c
#
# _END - end of string

from typing import Generic, TypeVar, MutableSequence


END_SYMBOL = "\\"
T = TypeVar("T", covariant=False, contravariant=False)


class Stack(Generic[T]):
    def __init__(self, values: MutableSequence | None = None) -> None:
        self.storage = values or list()

    def push(self, value: T) -> None:
        self.storage.append(value)

    def pop(self) -> T | None:
        if len(self.storage) == 0:
            return None
        return self.storage.pop()


class InputSequence:
    def __init__(self, sequence: str) -> None:
        symbols_list = list(sequence)
        symbols_list.append(END_SYMBOL)
        symbols_list.reverse()
        self.sequence = Stack(symbols_list)

    def pop(self) -> str | None:
        return self.sequence.pop()

    def push(self, value: str) -> None:
        self.sequence.push(value)


class Analyzer:
    class WrongSymbol(Exception):
        pass

    def __init__(self, sequence: str) -> None:
        self.sequence = InputSequence(sequence)
        self.current_char = ""
        self.char_index: int = -1
        self.error_found = False
        
    def _get_next_char(self) -> str | None:
        self.char_index += 1
        return self.sequence.pop()

    def _return_char_to_sequence(self) -> None:
        """
        Turns self.current_char to ""
        """
        self.sequence.push(self.current_char)
        self.current_char = ""
        self.char_index -= 1

    def get_first_wrong_char_index(self) -> int | None:
        if self.error_found:
            return self.char_index
        return None

    def _error(self):
        self.error_found = True
        raise self.WrongSymbol

    def _I(self):
        if self.current_char not in ("a", "b", "c"):
            self._error()

    def _P(self):
        if self.current_char == "(":
            self.current_char = self._get_next_char()
            self._T()
            self.current_char = self._get_next_char()
            self._E()

            self.current_char = self._get_next_char()
            if self.current_char != ")":
                self._error()
        else:
            self._I()

    def _D(self):
        if self.current_char == "*":
            self.current_char = self._get_next_char()
            self._T()
        else:
            self._return_char_to_sequence()

    def _T(self):
        self._P()
        self.current_char = self._get_next_char()
        self._D()

    def _E(self):
        if self.current_char == "+" or self.current_char == "-":
            self.current_char = self._get_next_char()
            self._T()
            self.current_char = self._get_next_char()
            self._E()
        else:
            self._return_char_to_sequence()

    def _S(self):
        self._T()
        self.current_char = self._get_next_char()
        self._E()
        self.current_char = self._get_next_char()
        if self.current_char != END_SYMBOL:
            self._error()

    def check(self) -> bool:
        self.error_found = False
        self.current_char = self.current_char = self._get_next_char()

        try:
            self._S()
            return True
        except self.WrongSymbol:
            return False


def main():
    sequence = input("Входная цепочка: ")
    analyzer = Analyzer(sequence)

    if analyzer.check():
        print("Цепочка корректна")
    else:
        print(f"Ошибка: {analyzer.get_first_wrong_char_index() + 1} символ")


if __name__ == "__main__":
    main()
