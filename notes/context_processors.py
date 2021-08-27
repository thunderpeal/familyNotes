def groups_processor(request):
    if request.user.is_authenticated:
        groups = request.user.members_groups.all()
        return {'groups': groups}
    return {}
