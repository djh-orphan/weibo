import appv1
from appv1 import create_app

app = create_app()




if __name__ == "__main__":
    app.run(
        host="172.21.0.12",
        port=8000
    )
