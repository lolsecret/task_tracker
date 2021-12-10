from django.db.models import TextChoices


class TaskStatusTypes(TextChoices):
    PLANNED = "PLANNED", "Планируется"
    ACTIVE = "ACTIVE", "Активная"
    CONTROL = "CONTROL", "Контроль"
    COMPLETED = "COMPLETED", "Завершена"
