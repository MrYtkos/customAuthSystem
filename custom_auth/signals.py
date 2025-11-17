# auth/signals.py
import bcrypt
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from custom_auth.models import User, Role, Resource, AccessRules

@receiver(post_migrate)
def create_default_roles_resources(sender, **kwargs):
    user_role, _ = Role.objects.get_or_create(role_name='user')
    admin_role, _ = Role.objects.get_or_create(role_name='admin')

    if not User.objects.filter(email='super@admin.com').exists():
        raw_password = 'admin123'
        hashed = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name='Super',
            last_name='Admin',
            email='super@admin.com',
            password=hashed,
            role=admin_role
        )

    users_res, _ = Resource.objects.get_or_create(name='users')
    orders_res, _ = Resource.objects.get_or_create(name='orders')
    products_res, _ = Resource.objects.get_or_create(name='products')

    AccessRules.objects.get_or_create(
        role=user_role,
        resource=users_res,
        defaults={
            'read_permission': True,
            'update_permission': True
        }
    )

    for res in [users_res, orders_res, products_res]:
        AccessRules.objects.get_or_create(
            role=admin_role,
            resource=res,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True,
            }
        )
