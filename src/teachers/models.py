from django.db import models

class ClassName(models.Model):
    name = models.CharField(max_length=10, verbose_name="Sinf nomi")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Sinf nomi"
        verbose_name_plural = "Sinflar nomi"


class Class(models.Model):
    class_teacher_full_name = models.CharField(max_length=512, verbose_name="Rahbarni toliq ismi", null=True, blank=True)
    class_teacher_tg_id = models.CharField(max_length=156, verbose_name="Rahbarni telegram idsi", null=True, blank=True)
    class_name = models.OneToOneField(ClassName, on_delete=models.CASCADE, verbose_name="Sinf nomi")
    students = models.ManyToManyField("students.Student")

    this_updated = models.BooleanField(default=False, null=True, blank=True, verbose_name="Yangilanganmi")

    def __str__(self):
        return f"{self.class_name}"

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"
    