from django import forms


class ImageUploadForm(forms.Form):
    file = forms.ImageField(label='画像ファイル')
