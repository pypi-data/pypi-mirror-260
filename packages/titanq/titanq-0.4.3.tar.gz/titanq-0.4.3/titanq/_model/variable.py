import enum

class Vtype(str, enum.Enum):
    BINARY = 'binary'
    BIPOLAR = 'bipolar'

    def __str__(self) -> str:
        return str(self.value)

class VariableVector:
    """
    Object That represent a vector of variable to be optimized.
    """
    def __init__(self, name='', size=1, vtype=Vtype.BINARY) -> None:
        if size < 1:
            raise ValueError("Variable vector size cannot be less than 1")

        self._name = name
        self._size = size
        self._vtype = vtype


    def size(self) -> int:
        """
        :return: size of this vector.
        """
        return self._size

    def vtype(self) -> Vtype:
        """
        :return: Type of variable in the vector.
        """
        return self._vtype

    def name(self) -> str:
        """
        :return: Name of this variable vector.
        """
        return self._name