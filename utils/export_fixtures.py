import os
import json
from django.core.serializers import serialize
from django.conf import settings

# Django muhitini ishga tushiramiz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')  # Loyihangiz nomini o'zgartiring
import django

django.setup()

# Modelni import qilish
from apps.students.models import Student
from apps.sponsors.models import Sponsor
from apps.donations.models import Donation

# Fixture yoziladigan joyni aniqlaymiz
FIXTURE_DIR = os.path.join(settings.BASE_DIR, 'fixtures')
os.makedirs(FIXTURE_DIR, exist_ok=True)


def export_to_json(model, filename):
    """Berilgan modelni JSON fixture fayliga saqlaydi"""
    file_path = os.path.join(FIXTURE_DIR, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        json_data = serialize('json', model.objects.all())
        f.write(json_data)

    print(f"✅ {filename} fayli yaratildi!")


# Har bir model uchun eksport qilish
export_to_json(Student, 'students.json')
export_to_json(Sponsor, 'sponsors.json')
export_to_json(Donation, 'donations.json')

print("Barcha ma'lumotlar fixture sifatida saqlandi!")
