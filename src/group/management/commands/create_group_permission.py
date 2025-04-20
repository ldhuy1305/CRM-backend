from typing import Any

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from account.models import Account
from api.constants import ActionEnum, GroupNameEnum
from authentication.models import User
from call.models import Call
from campaign.models import Campaign
from contact.models import Contact
from deal.models import Deal
from lead.models import Lead
from meeting.models import Meeting
from task.models import Task


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # add other permission
        self.create_other_permission()

        # Create group permission for admin, manager, salesman, marketer
        self.create_group_permission()

        # Add permission to groups
        self.assign_permission_to_groups()

    def create_other_permission(self):
        list_permission_data = [
            (ActionEnum.CONVERT.value, Lead),
            (ActionEnum.ASSIGN_TO_OTHER.value, Contact),
            (ActionEnum.ASSIGN_TO_OTHER.value, Account),
            (ActionEnum.CLOSE.value, Deal),
            (ActionEnum.COMPLETE.value, Task),
        ]

        for action, model in list_permission_data:
            codename = self._get_codename_permission_by_model(action, model)
            name = self._get_name_permission_by_model(action, model)
            content_type = ContentType.objects.get_for_model(model)

            Permission.objects.get_or_create(
                codename=codename, content_type=content_type, defaults={"name": name}
            )

    def assign_permission_to_groups(self):
        permissions = {
            GroupNameEnum.ADMIN.value: [
                *self._get_full_permission_for_all(Lead),
                (ActionEnum.CONVERT.value, Lead),
                *self._get_full_permission_for_all(Contact),
                (ActionEnum.ASSIGN_TO_OTHER.value, Contact),
                *self._get_full_permission_for_all(Account),
                (ActionEnum.ASSIGN_TO_OTHER.value, Account),
                *self._get_full_permission_for_all(Deal),
                (ActionEnum.CLOSE.value, Deal),
                *self._get_full_permission_for_all(Campaign),
                *self._get_full_permission_for_all(Task),
                (ActionEnum.COMPLETE.value, Task),
                *self._get_full_permission_for_all(Meeting),
                *self._get_full_permission_for_all(Call),
                *self._get_full_permission_for_all(User),
            ],
            GroupNameEnum.MANAGER.value: [
                *self._get_full_permission_for_all(Lead),
                (ActionEnum.CONVERT.value, Lead),
                *self._get_full_permission_for_all(Contact),
                (ActionEnum.ASSIGN_TO_OTHER.value, Contact),
                *self._get_full_permission_for_all(Account),
                (ActionEnum.ASSIGN_TO_OTHER.value, Account),
                *self._get_full_permission_for_all(Deal),
                (ActionEnum.CLOSE.value, Deal),
                *self._get_full_permission_for_all(Campaign),
                *self._get_full_permission_for_all(Task),
                (ActionEnum.COMPLETE.value, Task),
                *self._get_full_permission_for_all(Meeting),
                *self._get_full_permission_for_all(Call),
                (ActionEnum.VIEW.value, User),
            ],
            GroupNameEnum.SALESMAN.value: [
                *self._get_full_permission(Lead),
                (ActionEnum.CONVERT.value, Lead),
                *self._get_full_permission(Contact),
                (ActionEnum.VIEW.value, Account),
                *self._get_full_permission(Deal),
                (ActionEnum.CLOSE.value, Deal),
                (ActionEnum.VIEW.value, Campaign),
                *self._get_full_permission(Task),
                (ActionEnum.COMPLETE.value, Task),
                *self._get_full_permission(Meeting),
                *self._get_full_permission(Call),
                (ActionEnum.VIEW.value, User),
            ],
            GroupNameEnum.MARKETER.value: [
                (ActionEnum.VIEW.value, Lead),
                (ActionEnum.ADD.value, Lead),
                (ActionEnum.CHANGE.value, Lead),
                *self._get_full_permission(Campaign),
                *self._get_full_permission(Task),
                (ActionEnum.COMPLETE.value, Task),
                *self._get_full_permission(Meeting),
                (ActionEnum.VIEW.value, User),
            ],
        }
        for group_name, permissions in permissions.items():
            group = Group.objects.get(name=group_name)
            group.permissions.clear()
            for action, model in permissions:
                codename = f"{action}_{model._meta.model_name}"
                permission = Permission.objects.filter(codename=codename).first()
                if not permission:
                    permission = Permission.objects.create(
                        codename=codename,
                        content_type=ContentType.objects.get_for_model(model),
                        name=self._get_name_permission_by_model(action, model),
                    )

                group.permissions.add(permission)

    @staticmethod
    def _get_full_permission_for_all(model):
        return [
            (ActionEnum.VIEW.value + "all", model),
            (ActionEnum.ADD.value + "all", model),
            (ActionEnum.CHANGE.value + "all", model),
            (ActionEnum.DELETE.value + "all", model),
        ]

    @staticmethod
    def _get_full_permission(model):
        return [
            (ActionEnum.VIEW.value, model),
            (ActionEnum.ADD.value + "all", model),
            (ActionEnum.CHANGE.value, model),
            (ActionEnum.DELETE.value, model),
        ]

    @staticmethod
    def create_group_permission():
        names = [
            GroupNameEnum.ADMIN.value,
            GroupNameEnum.MANAGER.value,
            GroupNameEnum.SALESMAN.value,
            GroupNameEnum.MARKETER.value,
        ]
        for name in names:
            Group.objects.get_or_create(name=name)

    @staticmethod
    def _get_name_permission_by_model(action: str, model: Any) -> str:
        action = action.replace("all", " all")
        model_name = model._meta.model_name
        return f"Can {action} {model_name}"

    @staticmethod
    def _get_codename_permission_by_model(action: str, model: Any) -> str:
        action = action.replace("all", "")
        model_name = model._meta.model_name
        return f"{action}_{model_name}"
