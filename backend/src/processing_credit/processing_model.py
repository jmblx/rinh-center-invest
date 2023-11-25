import joblib
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.compose import ColumnTransformer

def use_model(data: dict):
  preprocessor = joblib.load('preprocessor.pkl')
  df_to_predict = pd.DataFrame(data)

  # Загрузка модели
  model = load_model('model.h5')

  # Предобработка данных для предсказания
  X_to_predict = preprocessor.transform(df_to_predict)

  # Делаем предсказание
  predicted_credit_score = model.predict(X_to_predict)
  return predicted_credit_score
