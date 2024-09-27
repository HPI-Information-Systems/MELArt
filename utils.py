def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def is_named_entiy(obj):
    if isinstance(obj, str):
        return any([char.isupper() for char in obj])
    elif isinstance(obj, list) or isinstance(obj, set):
        return any([is_named_entiy(item) for item in obj])
    elif isinstance(obj, tuple) and len(obj) == 2 and isinstance(obj[0], str) and is_iterable(obj[1]):
        return is_named_entiy(obj[0]) or is_named_entiy(obj[1])
        
if __name__ == '__main__':
    print(is_named_entiy("Hello"))
    print(is_named_entiy("hello"))
    print(is_named_entiy(["Hello", "world"]))
    print(is_named_entiy(["hello", "world"]))
    print(is_named_entiy(("Hello", ["world", "earth"])))
    print(is_named_entiy(("hello", ["world", "earth"])))