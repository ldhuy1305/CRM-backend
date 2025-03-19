from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        model = self._get_model(view)
        if not model:
            return False

        model_name = model._meta.model_name
        app_label = model._meta.app_label

        permission_all_map = {
            "list": f"viewall_{model_name}",
            "create": f"addall_{model_name}",
        }

        permission_map = {
            "list": f"view_{model_name}",
            "create": f"add_{model_name}",
        }

        request.is_view_all = False

        if self._user_has_permission(user, app_label, permission_all_map.get(view.action)):
            request.is_view_all = True
            return True

        if self._user_has_permission(user, app_label, permission_map.get(view.action)):
            return True

        return False if view.action in ["create",
                                        "list"] else True  # forward to has_object_permission if neither create nor list

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        model = self._get_model(view)
        if not model:
            return False

        model_name = model._meta.model_name
        app_label = model._meta.app_label

        permission_all_map = {
            "retrieve": f"viewall_{model_name}",
            "update": f"changeall_{model_name}",
            "partial_update": f"changeall_{model_name}",
            "destroy": f"deleteall_{model_name}",
        }

        permission_map = {
            "retrieve": f"view_{model_name}",
            "update": f"change_{model_name}",
            "partial_update": f"change_{model_name}",
            "destroy": f"delete_{model_name}",
        }
        if self._user_has_permission(user, app_label, permission_all_map.get(view.action)):
            return True

        if self._user_has_permission(user, app_label, permission_map.get(view.action)):
            return user == obj.created_by

        return False

    @staticmethod
    def _user_has_permission(user, app_label, permission_codename):
        if not permission_codename:
            return False
        return user.has_perm(f"{app_label}.{permission_codename}")

    @staticmethod
    def _get_model(view):
        try:
            return view.get_queryset().model
        except AttributeError:
            return None
