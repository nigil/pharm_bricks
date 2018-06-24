

class EnumBase(object):
    @classmethod
    def get_listed_values(cls, list_):
        return {key: cls.values[key] for key in list_}

    @classmethod
    def get_choices(cls):
        return ((key, val) for key, val in cls.values.items())
