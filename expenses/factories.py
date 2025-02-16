import factory
from factory import Faker
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory

from .models import Expense, Group, GroupMember


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    type = factory.Iterator([Group.COUPLE, Group.FAMILY, Group.FRIENDS])
    created_at = Faker("date_time")
    updated_at = Faker("date_time")


class GroupMemberFactory(DjangoModelFactory):
    class Meta:
        model = GroupMember

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
    income = Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    income_currency = "ARS"
    income_frequency = factory.Iterator(
        [
            GroupMember.MONTHLY,
            GroupMember.BIWEEKLY,
            GroupMember.WEEKLY,
            GroupMember.YEARLY,
        ]
    )
    share_percentage = Faker(
        "pydecimal", left_digits=2, right_digits=2, min_value=0, max_value=100
    )
    role = factory.Iterator([GroupMember.ADMIN, GroupMember.MEMBER])
    joined_at = Faker("date_time")


class ExpenseFactory(DjangoModelFactory):
    class Meta:
        model = Expense

    name = Faker("sentence", nb_words=3)
    amount = Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    date = Faker("date")
    group = factory.SubFactory(GroupFactory)
    created_at = Faker("date_time")
    updated_at = Faker("date_time")
