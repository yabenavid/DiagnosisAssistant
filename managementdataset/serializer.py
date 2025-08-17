# serializers.py
from rest_framework import serializers
from .models import ImgDataset
from django.core.files.base import ContentFile
from zipfile import ZipFile
from django.core.files.storage import default_storage
from vectorization.models import ImageResizer
# from segmentation.apps import segmenter_instance
from segmentation.models import SkimageSegmenter, UnetImageSegmenter, SamImageSegmenter
import shutil
import os

class ImageDatasetSerializer(serializers.ModelSerializer):
    keypoints = serializers.SerializerMethodField()
    descriptors = serializers.SerializerMethodField()

    class Meta:
        model = ImgDataset
        fields = ['id', 'image', 'keypoints', 'descriptors']

    def get_keypoints(self, obj):
        return obj.get_keypoints()

    def get_descriptors(self, obj):
        return obj.get_descriptors()

class MultipleImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        allow_empty=False,
        write_only=True
    )

    def create(self, validated_data):
        images = validated_data.pop('images')
        instances = [ImgDataset(image=image) for image in images]
        return ImgDataset.objects.bulk_create(instances)

class ZipImageUploadSerializer(serializers.Serializer):
    zip_file = serializers.FileField()
    segment_model = serializers.CharField(write_only=True, required=False)

    def validate_zip_file(self, value):
        if not value.name.endswith('.zip'):
            raise serializers.ValidationError("Solo se permiten archivos ZIP.")
        return value

    def create(self, validated_data):
        zip_file = validated_data['zip_file']
        segment_model = validated_data.get('segment_model', '1')  # Default '1'
        images, cont, ex = [], 0, False

        image_resizer = ImageResizer()
        unet_segmenter = UnetImageSegmenter()

        try:
            with ZipFile(zip_file, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    cont = cont + 1
                    print(f'>>>>Imagen {cont} | Nombre: {file_name}')
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        image_file = zip_ref.read(file_name)
                        image_content = ContentFile(image_file, name=file_name)
                        
                        print('INITIALIZING VECTORIZATION')

                        # Vectorization
                        if segment_model == '1' or segment_model == '2':
                            resized_images, resized_images_base64 = image_resizer.procesar_imagenes([image_content])
                            print('VECTORIZATION FINISHED')
                        else:
                            resized_images = [image_content]  # No resizing for UNet

                        resized_image = resized_images[0]
                        original_path = default_storage.save("uploads/" + resized_image.name, ContentFile(resized_image.read()))

                        # Segmentation
                        print('INITIALIZING SEGMENTATION')
                        
                        if segment_model == '1':
                            segmenter_instance = SamImageSegmenter()
                            segmented_images = segmenter_instance.segment_images(resized_images, original_path)
                            segment_type = 'SAM'
                        elif segment_model == '2':
                            skimage_segmenter = SkimageSegmenter()
                            segmented_images = skimage_segmenter.segment_images(resized_images)
                            segment_type = 'ScikitImage'
                        elif segment_model == '3':
                            segmented_images = unet_segmenter.segment_images(resized_images)
                            segment_type = 'UNet'
                        else:
                            raise Exception("Invalid segmentation model param (must be '1', '2' or '3')")

                        print('SEGMENTATION FINISHED')

                        # Save the image instance
                        img_instance = ImgDataset()
                        img_instance.segment_type = segment_type  # Temp attribute
                        img_instance.image = segmented_images[0]
                        img_instance.save()

                        # Extract and save keypoints and descriptors
                        img_instance.extract_and_save_features(default_storage.path(original_path))
                        images.append(img_instance)
        except Exception as e:
            ex = f'Failed reading, segmenting or saving the image. Reason: {e}'
            print(ex)

        # Clean uploads folder
        uploads_path = default_storage.path("uploads")
        for filename in os.listdir(uploads_path):
            file_path = os.path.join(uploads_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        if ex:
            raise Exception(
                f"Error al procesar el archivo ZIP. Asegúrate de que contenga imágenes válidas. Error interno: {ex}"
            )
        return images