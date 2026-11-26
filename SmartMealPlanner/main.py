from tasks.database import init_database
from UI.app import SmartMealApp


def main():

    # Initialize MariaDB
    init_database()

    # Start SmartMeal UI
    app = SmartMealApp()

    app.mainloop()


if __name__ == "__main__":
    main()