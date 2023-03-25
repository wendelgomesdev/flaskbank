from app_factory import create_app, database

app = create_app()

""" @app.before_first_request
def creat_data_base():
    database.create_all() """
#123
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')