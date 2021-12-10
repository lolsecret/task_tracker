from rest_framework import permissions


class CanViewTasks(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.can_view_board(obj)


class IsAuthorOrReadOnly(CanViewTasks):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return super().has_object_permission(request, view, obj.item.list.board)
        else:
            return request.user == obj.author
