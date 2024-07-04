from app import create_app

TaskManagerApp = create_app()


if __name__ == '__main__':
    TaskManagerApp.run(debug = True)