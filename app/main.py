from ansiboard.application import Application
from ansiboard.main_window import MainWindow


def main():
    app = Application()
    
    window = MainWindow()
    window.show()

    app.exec_()


if __name__ == "__main__":
    main()