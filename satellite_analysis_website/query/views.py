from django.utils import timezone

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from fractalnet.predict import preprocess_image, make_predictions
from image.models import Image
from query.models import Query
from user.models import User
from data_management.s3_functions import save_image_to_directory, load_image_from_directory


def get_analysis_page(request, user_id=-1):
    ###################################
    return render(request, 'analysis.html')


def get_summary_page(request, query_id):
    query = Query.get_by_id(query_id)
    if query:
        images = Image.get_all_by_query_id(query_id)
        images_files = [load_image_from_directory(image.name) for image in images]
        images_data = [{'info': image, 'file': file} for image, file in zip(images, images_files)]

        result = {
            'query_name': query.name,
            'query_time': query.datetime,
            'images_data': images_data
        }

        return render(request, 'summary.html', {'result': result})

    return redirect('get_analysis_page')


def create_analysis(request):
    if request.method == 'POST':
        data_identifier = request.POST.get('data_identifier')
        images = request.FILES.getlist('images')
        user_id = request.session.get('user_id', -1)

        if len(images) > 0 and user_id != -1:
            user = User.get_by_id(user_id)
            query = Query.create_query(user=user, name=data_identifier, datetime=timezone.now())
            for img in images:
                updated_img = preprocess_image(img)
                aircraft_type, accuracy = make_predictions(updated_img)
                Image.add_image(name=img.name, result=aircraft_type, accuracy=accuracy, query=query)

                # In future save to S3
                save_image_to_directory(img.name, updated_img)

            return redirect('summary', query_id=query.id)

    return render(request, 'analysis.html')


def get_all_results(request):
    queries = Query.get_all()
    print(queries)
    if len(queries) > 0:
        return render(request, 'history.html', {'queries': queries})

    return redirect('get_analysis_page')
