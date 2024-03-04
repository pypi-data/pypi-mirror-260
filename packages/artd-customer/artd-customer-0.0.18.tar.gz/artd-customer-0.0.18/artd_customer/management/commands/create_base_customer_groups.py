from django.core.management.base import BaseCommand
from artd_customer.models import CustomerGroup

CUSTOMER_GROUPS = [
    {
        "group_code": "new",
        "group_name": "New customers",
        "description": "New customers",
    },
    {
        "group_code": "wholesale",
        "group_name": "Wholesale customers",
        "description": "Wholesale customers",
    },
    {
        "group_code": "vip",
        "group_name": "VIP customers",
        "description": "VIP customers",
    },
]

class Command(BaseCommand):
    help = 'Create the base customer groups.'

    def handle(self, *args, **options):
        for group in CUSTOMER_GROUPS:
            if CustomerGroup.objects.filter(group_code=group["group_code"]).count()==0:
                CustomerGroup.objects.create(
                    group_code=group["group_code"],
                    group_name=group["group_name"],
                    group_description=group["description"],
                )
                self.stdout.write(self.style.WARNING(f'Customer group {group["group_code"]} created'))
            else:
                CustomerGroup.objects.filter(group_code=group["group_code"]).update(
                    group_name=group["group_name"],
                    group_description=group["description"],
                )
                self.stdout.write(self.style.ERROR(f'Customer group {group["group_code"]} updated'))
        
