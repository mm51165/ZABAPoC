# Generated by Django 5.0.7 on 2024-08-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Chunk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("embedding", models.BinaryField()),
                ("embedding_size", models.IntegerField()),
                ("url", models.URLField()),
                ("last_update", models.DateTimeField()),
                ("keywords", models.CharField(max_length=2000)),
            ],
        ),
    ]