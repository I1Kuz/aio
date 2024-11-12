import configparser
import redis
import uuid
 
 
class RedisRepository:
    redisclient = None
    server = None
    port = None
    database = None
 
    # method used to get the parameters to connect to Redis
    def _get_redis_parameters(self):
        # definition of the object used to read the config file
        configfile = configparser.ConfigParser()
        configfile.read("config.ini")
 
        rediscache = configfile["redis"]
        self.server = rediscache["server"]
        self.port = rediscache["port"]
        self.database = rediscache["db"]
 
    def __init__(self):
        # get Redis paramters
        self._get_redis_parameters()
 
    def insert_user(self, name, age, city):
        """
        Creates a new user in Redis with a GUID as the user ID.
        :param name: Name of the user.
        :param age: Age of the user.
        :param city: City of the user.
        :return: The GUID of the created user.
        """
        user_id = str(uuid.uuid4())  # Generate a GUID for the user ID
        user_key = f"user:{user_id}"
        user_data = {
            "name": name,
            "age": age,
            "city": city
        }
 
        try:
            # Using a context manager to handle the Redis connection
            # This ensures that the connection is properly closed after
            # the block of code is executed, even if an exception occurs:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                #  Hset is a command in Redis that is used to set the value of one or more
                # fields in a hash. It's a very versatile and commonly used command in Redis,
                # especially when dealing with objects or entities that have multiple attributes
                client.hset(user_key, mapping=user_data)
                # Add the user key to the set of users
                client.sadd("users", user_key)
                return user_id
        except Exception as error:
            print(f"Error during the insert operation, because of: {error}")
            return 0
 
    def select_all_users(self):
        """
        Retrieves all users from Redis.
        :return: A list of user data dictionaries.
        """
        all_users = []
        try:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                # Retrieve all user keys from the set
                user_keys = client.smembers("users")
                for user_key in user_keys:
                    # Fetch each user's data
                    user_data = client.hgetall(user_key.decode('utf-8'))
                    # Convert bytes to string for each field
                    user_data = {k.decode('utf-8'): v.decode('utf-8')
                                 for k, v in user_data.items()}
                    all_users.append(user_data)
        except Exception as error:
            print(f"Error during the select all users operation: {error}")
 
        return all_users
 
    def select_user_by_name(self, nameinput):
        """
        Finds a user in Redis by their name.
        :param nameinput: The name of the user to find.
        :return: User data if found, else None.
        """
        try:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                # Retrieve all user keys from the set
                user_keys = client.smembers("users")
                for user_key in user_keys:
                    # Fetch each user's data
                    user_data = client.hgetall(user_key.decode('utf-8'))
                    # Convert bytes to string for each field
                    user_data = {k.decode('utf-8'): v.decode('utf-8')
                                 for k, v in user_data.items()}
 
                    if user_data.get("name") == nameinput:
                        return user_data
        except Exception as error:
            print(f"Error during the select users by name operation: {error}")
 
        return None
 
    def delete_user_by_name(self, nameinput):
        """
        Deletes a user in Redis by their name.
        :param nameinput: The name of the user to delete.
        :return: True if the user was deleted, False otherwise.
        """
        try:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                user_keys = client.smembers("users")
                for user_key in user_keys:
                    user_data = client.hgetall(user_key.decode('utf-8'))
                    user_data = {k.decode('utf-8'): v.decode('utf-8')
                                 for k, v in user_data.items()}
                    if user_data.get("name") == nameinput:
                        # Delete the user's hash
                        client.delete(user_key.decode('utf-8'))
                        # Remove the user key from the set of users
                        client.srem("users", user_key)
                        return True
        except Exception as error:
            print(f"Error during user deletion: {error}")
 
        return False
 
    def update_user(self, user_id, updated_data):
        """
        Updates a user in Redis.
        :param user_id: The ID of the user to update.
        :param updated_data: A dictionary with the updated user data.
        :return: True if the update was successful, False otherwise.
        """
        user_key = f"user:{user_id}"
        try:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                # Check if the user exists
                if not client.exists(user_key):
                    print(f"No user found with ID: {user_id}")
                    return False
 
                # Update user data
                client.hset(user_key, mapping=updated_data)
                return True
        except Exception as error:
            print(f"Error during user update: {error}")
            return False
 
    def select_all_users_with_id(self):
        """
        Retrieves all users from Redis, including their IDs.
        :return: A list of dictionaries, each containing user data along with the user ID.
        """
        all_users_with_id = []
        try:
            with redis.Redis(host=self.server, port=self.port, db=self.database) as client:
                user_keys = client.smembers("users")
                for user_key in user_keys:
                    # Extract user ID from the key
                    user_id = user_key.decode('utf-8').split(":")[1]
                    user_data = client.hgetall(user_key.decode('utf-8'))
                    user_data = {k.decode('utf-8'): v.decode('utf-8')
                                 for k, v in user_data.items()}
                    # Include the user ID in the data dictionary
                    user_data['id'] = user_id
                    all_users_with_id.append(user_data)
        except Exception as error:
            print(f"Error during the retrieval operation: {error}")
 
        return all_users_with_id