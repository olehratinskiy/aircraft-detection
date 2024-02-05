from django.db import models
from query.models import Query


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    result = models.CharField(blank=True, max_length=255)
    accuracy = models.FloatField()
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    @staticmethod
    def get_by_id(image_id):
        image = Image.objects.filter(id=image_id).first()
        return image if image else None

    @staticmethod
    def get_all_by_query_id(query_id):
        images = Image.objects.filter(query_id=query_id)
        return images

    @staticmethod
    def get_all():
        return Image.objects.all()

    @staticmethod
    def add_image(name, result, accuracy, query):
        image = Image(name=name, result=result, accuracy=accuracy, query=query)
        image.save()
        return image

