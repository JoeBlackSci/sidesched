from sidesched.classes import Side

class TestSide:
    
    def __init__(self) -> None:
        names = ["bbb", "aaa"]
        sizes = [1, 2]
        
        self.side1 = Side(names[0], size=sizes[0])
        self.side2 = Side(names[1], size=sizes[1])
    
    def test_name(self) -> None:
        assert self.side1.name == "bbb"
    
    def test_size_1(self) -> None:
        assert self.side1.size == 1
    
    def test_size_2(self) -> None:
        assert self.side2.size == 2
        
    def test_sorting(self) -> None: 
        assert sorted([self.side1, self.side2]) == [self.side2, self.side1]
        
        
        
        
