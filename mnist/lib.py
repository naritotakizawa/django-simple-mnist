import pickle
from sklearn import datasets, svm
from sklearn.model_selection import train_test_split


def read():
    """予測モデルを読み込む"""
    with open('mnist.pickle', 'rb') as file:
        clf = pickle.load(file)
    return clf


def create_and_save():
    """予測モデルを作成し、保存する"""
    # サンプル画像データのロード
    mnist = datasets.fetch_mldata('MNIST original', data_home='image/')
    X = mnist.data / 255
    y = mnist.target

    # 訓練用データとテスト用データに分ける
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=5000, test_size=0
    )

    # 訓練用データで学習
    clf = svm.SVC()
    clf.fit(X_train, y_train)

    # 予測モデルの保存
    with open('mnist.pickle', 'wb') as file:
        pickle.dump(clf, file)
    return clf


# pickleで保存したデータがなければ、新しく作る
try:
    clf = read()
except FileNotFoundError:
    clf = create_and_save()


def predict(img_array):
    """手書き文字を判別した結果を返す"""
    result = clf.predict(img_array)
    return str(int(result[0]))
