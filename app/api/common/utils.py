import random
import string


# TODO: Method naming rule: verb
def random_digit_with_number(length_of_values: int=7) -> str:
    choices = string.ascii_uppercase + string.digits + string.ascii_lowercase
    random_value = ''.join(random.SystemRandom().choice(choices) for _ in range(length_of_values))
    return random_value


# TODO: Method naming rule: verb
def random_number(length_of_values: int=6) -> str:
    choices = string.digits
    random_value = ''.join(random.SystemRandom().choice(choices) for _ in range(length_of_values))
    return random_value
