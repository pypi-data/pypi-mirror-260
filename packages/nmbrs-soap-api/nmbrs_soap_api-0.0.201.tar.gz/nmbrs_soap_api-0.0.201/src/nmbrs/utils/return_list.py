def return_list(func):
    """
    Decorator ensuring the decorated function always returns a list.

    If result is None, returns an empty list.
    If result is not a list, wraps it in a list before returning.

    :param func: The function to be decorated.
    :return: The decorated function.
    """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            if result is None:
                return []
            if not isinstance(result, list):
                return [result]
            return result
        except Exception as e:
            # If error is this:
            if str(e) == "TypeError: 'NoneType' object is not iterable":
                # return list
                return []
            raise e

    return wrapper
