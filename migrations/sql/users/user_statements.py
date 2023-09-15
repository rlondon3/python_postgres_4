

GET_USER = "SELECT * FROM users WHERE user_name = %s;"
GET_USERS = "SELECT * FROM users;"
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY, 
                        first_name VARCHAR (100) NOT NULL, 
                        last_name VARCHAR (100) NOT NULL,
                        birthday DATE,
                        city VARCHAR (100) NOT NULL,
                        state VARCHAR (2) NOT NULL, 
                        active BOOLEAN NOT NULL,
                        user_name VARCHAR (50) NOT NULL,
                        email VARCHAR (50) NOT NULL,
                        password VARCHAR (255) NOT NULL
                        )"""
INSERT_INTO_USERS_TABLE_RETURNING_ID = """INSERT INTO users (
                                        first_name, 
                                        last_name,
                                        birthday, 
                                        city, 
                                        state, 
                                        active,
                                        user_name, 
                                        email, 
                                        password
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
UPDATE_USERS_TABLE_RETURNING_USER = """UPDATE users SET 
                                    first_name=(%s), 
                                    last_name=(%s), 
                                    birthday=(%s), city=(%s), 
                                    state=(%s), 
                                    active=(%s),
                                    user_name=(%s), 
                                    email=(%s), 
                                    password=(%s) WHERE id=(%s) RETURNING *;"""
DELETE_FROM_USERS_RETURNING_ID = "SELECT FROM users WHERE id = (%s);"