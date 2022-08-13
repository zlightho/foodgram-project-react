# Generated by Django 4.1 on 2022-08-13 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("food", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="recipe",
            options={"ordering": ("-pub_date",)},
        ),
        migrations.AddField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
