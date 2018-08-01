from peewee import Model, DoesNotExist, TextField
import config

class State(Model):
    user_id = TextField(unique=True)
    state = TextField()
    class Meta:
        database = config.db

def crt():
    State.create_table()
    
def get_current_state(user_id):
    try:
        instance = State.get(State.user_id == user_id)
        return instance.state
    except DoesNotExist:
        return config.States.S_START_BOOKING.value
    except Exception as ex:
    	print('~get_state(): ' + str(ex))


def set_state(userId, value):
    try:
        instance = State.get(State.user_id == userId)
        instance.state = value
        instance.save()
        return True
    except DoesNotExist:
        instance = State.create(user_id=userId, state=config.States.S_START_BOOKING.value)
        instance.save()
        return True
    except Exception as ex:
    	print('~set_state(): ' + str(ex))