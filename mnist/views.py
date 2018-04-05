import base64
from io import BytesIO
from django.shortcuts import render
from django.views import generic
from .forms import ImageUploadForm
from .lib import predict
import numpy as np
from PIL import Image


class UploadView(generic.FormView):
    template_name = 'mnist/upload.html'
    form_class = ImageUploadForm

    def form_valid(self, form):
        # アップロードファイル本体を取得
        file = form.cleaned_data['file']
        # ファイルを、28*28にリサイズし、グレースケール(モノクロ画像)
        img = Image.open(file).resize((28, 28)).convert('L')

        # 学習時と同じ形に画像データを変換する
        img_array = np.asarray(img) / 255
        img_array = img_array.reshape(1, 784)

        # 推論した結果を、テンプレートへ渡して表示
        context = {
            'result': predict(img_array),
        }
        return render(self.request, 'mnist/result.html', context)


class PaintView(generic.TemplateView):
    template_name = 'mnist/paint.html'

    def post(self, request):
        base_64_string = request.POST['img-src'].replace(
            'data:image/png;base64,', '')
        file = BytesIO(base64.b64decode(base_64_string))

        # ファイルを、28*28にリサイズし、グレースケール(モノクロ画像)
        img = Image.open(file).resize((28, 28)).convert('L')

        # 学習時と同じ形に画像データを変換する
        img_array = np.asarray(img) / 255
        img_array = img_array.reshape(1, 784)

        # 推論した結果を、テンプレートへ渡して表示
        context = {
            'result': predict(img_array),
        }
        return render(self.request, 'mnist/result.html', context)
