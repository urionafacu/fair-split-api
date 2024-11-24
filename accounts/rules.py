import rules

@rules.predicate
def is_owner(user, obj):
    return obj.id == user.id if obj else False
