from django.db import models
from user.models import User


class Query(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    datetime = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_by_id(query_id):
        query = Query.objects.filter(id=query_id).first()
        return query if query else None

    @staticmethod
    def get_all():
        return Query.objects.all()

    @staticmethod
    def create_query(user, name, datetime):
        query = Query(user=user, name=name, datetime=datetime)
        query.save()
        return query

