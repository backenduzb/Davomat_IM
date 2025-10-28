from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=1024, verbose_name="O'quvchining toliq ismi")
    class_type  = models.ForeignKey("teachers.Class", on_delete=models.CASCADE, verbose_name="Sinfi")
    status = models.CharField(default="Bor", verbose_name="Statusi", blank=True)
    sababi = models.TextField(verbose_name="Sababi", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.class_type:
            self.class_type.students.add(self)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"  
