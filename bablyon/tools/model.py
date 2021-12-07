class BablyonModel:
    def __init__(self,**kawrgs) -> None:
        for key,value in kawrgs.items():
            if not hasattr(self,key):
                setattr(self,key,value)