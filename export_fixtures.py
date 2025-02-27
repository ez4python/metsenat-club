import os
import json
from django.core.serializers import serialize
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
import django

django.setup()

from apps.students.models import Student
from apps.sponsors.models import Sponsor
from apps.donations.models import Donation
from apps.shared.models import University

FIXTURE_DIR = os.path.join(settings.BASE_DIR, 'fixtures')
os.makedirs(FIXTURE_DIR, exist_ok=True)


def export_to_json(model, filename, exclude_fields=None):
    """
    Model ma'lumotlarini JSON fixture sifatida saqlaydi (formatlangan),
    lekin exclude_fields ro‘yxatidagi maydonlarni saqlamaydi.
    """
    exclude_fields = exclude_fields or []

    file_path = os.path.join(FIXTURE_DIR, filename)
    raw_json = serialize('json', model.objects.all())

    formatted_json = json.loads(raw_json)

    # Unwanted fields removal
    for item in formatted_json:
        for field in exclude_fields:
            item["fields"].pop(field, None)

    formatted_json_str = json.dumps(formatted_json, indent=4, ensure_ascii=False)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(formatted_json_str)

    print(f"{filename} fayli yaratildi!")


# There we can exclude fields, which are not needle for fixtures
try:
    export_to_json(Student, 'students.json', exclude_fields=['updated_at', 'created_at'])
    export_to_json(Sponsor, 'sponsors.json', exclude_fields=['updated_at', 'created_at'])
    export_to_json(Donation, 'donations.json', exclude_fields=['updated_at', 'created_at'])
    export_to_json(University, 'universities.json')
    print("Barcha kerakli ma'lumotlar JSON formatida saqlandi!")
except Exception as e:
    print(f"Error: {e}")
