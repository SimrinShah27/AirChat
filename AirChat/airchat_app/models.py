from airchat import db

class Airlines(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	airline_name = db.Column(db.String(20),nullable=False)
	airline_iata = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f"Airlines('{self.airline_name}','{self.airline_iata}')"

class Airports(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	airport_name = db.Column(db.String(20), nullable=False)
	city = db.Column(db.String(20), nullable=False)
	airport_iata = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f"Airports('{self.airport_name}','{self.city}','{self.airport_iata}')"

class Intent(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	intent_name = db.Column(db.String(20), nullable=False)
	training_data = db.Column(db.String(500), nullable=False)
	score = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Intent('{self.intent_name}','{self.training_data}','{self.score}')"
		
class Ratings(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	airline_sentiment = db.Column(db.String(20), nullable=False)
	airline_sentiment_conf = db.Column(db.Float, nullable=False)
	airline = db.Column(db.String(100), nullable=False)
	text = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Ratings('{self.airline_sentiment}','{self.airline_sentiment_conf}','{self.airline}','{self.text}')"


class MessageHistory(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	message_received = db.Column(db.Text, nullable=False)
	bot_response = db.Column(db.Text, nullable=False)
	intent_name = db.Column(db.String(100), nullable=False)
	intent_identified_flag = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"MessageHistory('{self.message_received}','{self.bot_response}',,'{self.intent_name}','{self.intent_identified_flag}')"
