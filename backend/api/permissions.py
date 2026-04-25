from rest_framework import permissions


def get_resume_owner(obj):
    if hasattr(obj, "owner"):
        return obj.owner
    if hasattr(obj, "resume"):
        return obj.resume.owner
    if hasattr(obj, "section"):
        return obj.section.resume.owner
    return None


class IsOwnerOrPublicReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = get_resume_owner(obj)

        if request.method in permissions.SAFE_METHODS:
            is_public = getattr(obj, "is_public", None)
            if is_public is None and hasattr(obj, "resume"):
                is_public = obj.resume.is_public
            if is_public is None and hasattr(obj, "section"):
                is_public = obj.section.resume.is_public
            return bool(is_public) or owner == request.user or request.user.is_staff

        return request.user.is_authenticated and (
            owner == request.user or request.user.is_staff
        )
