from converter import RoundedConverter
from ui import ConverterUI

def main() -> None:
    # Here we pick our specific converter to use in the app.
    # Because of our OOP design, the UI will work perfectly with either 
    # RoundedConverter() or StandardConverter().
    my_converter = RoundedConverter()
    
    app = ConverterUI(converter=my_converter)
    app.mainloop()

if __name__ == "__main__":
    main()
