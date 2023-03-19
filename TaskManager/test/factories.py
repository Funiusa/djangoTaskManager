import factory
from main.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: "Task %d" % n)
    description = factory.Faker("text")
    deadline_date = factory.Faker("future_datetime", end_date="+30d")
    state = Task.States.NEW
    priority = Task.Priority.LOW

