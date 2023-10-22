from django.http import JsonResponse
from django.views import View

from media.methods import upload_to_s3, create_thumbnail
from media.models import Media


class MediaAPI(View):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No image supplied"}, status=400)

        # Use the upload_to_s3 function to get the file URL
        thumbnail_url = upload_to_s3(create_thumbnail(file))
        file.seek(0)
        s3_url = upload_to_s3(file)

        # Extract user from request (assuming user is authenticated and request.user exists)
        user = request.user if request.user.is_authenticated else None

        # Save the image details to the Media model
        Media.objects.create(
            actor=user,
            file_type=file.content_type,
            file_name=file.name,
            file_size=file.size,
            file_url=s3_url,
            thumbnail_url=thumbnail_url,
        )

        # Return the file's URL in the response
        return JsonResponse({"url": s3_url, "thumbnail_url": thumbnail_url})
