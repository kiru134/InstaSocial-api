def string_must_contain_letter(cls, v):
    if not len(v):
        raise ValueError('must contain letter')
    return v
