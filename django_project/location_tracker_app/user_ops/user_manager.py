from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_by_natural_key(self, email_id):
        return super(UserManager, self).get(email=email_id)

    def create_superuser(self, email, password, **kwargs):
        superuser = self.model(email=email, is_superuser=True)
        superuser.set_password(password)
        superuser.save()
        return superuser

    def get_query_set(self):
        return

    def get_user_by_email(self, email):
        return self.get_queryset().get(email=email.lower())

    def get_users_for_organization(self, organization_id):
        return self.get_queryset().filter(organization_id=organization_id)

