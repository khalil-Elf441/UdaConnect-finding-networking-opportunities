import logging

DB_USERNAME = "ct_admin"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "geoconnections"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from kafka import KafkaConsumer


TOPIC_NAME = 'locations'
KAFKA_SERVER = 'localhost:9092'

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("LocationProcessor-api")

consumer = KafkaConsumer(TOPIC_NAME)

if __name__ == "__main__":
    while True:
        for location in consumer:
            db.session.add(location)
            db.session.commit()
    time.sleep(86400)