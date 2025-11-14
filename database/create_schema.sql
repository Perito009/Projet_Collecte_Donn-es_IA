CREATE TABLE IF NOT EXISTS turbines (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	location TEXT
);

CREATE TABLE IF NOT EXISTS sensors (
	id SERIAL PRIMARY KEY,
	turbine_id INTEGER REFERENCES turbines(id),
	sensor_type TEXT,
	unit TEXT
);

CREATE TABLE IF NOT EXISTS measurements (
	id SERIAL PRIMARY KEY,
	sensor_id INTEGER REFERENCES sensors(id),
	timestamp TIMESTAMP,
	value DOUBLE PRECISION
);
