import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def getData():
    data = pd.read_csv("test_results.csv")
    data['Относительный вес товара к весу товара на стеллаже'] = data['Missing Good Weight'] / data['Target Shelf Weight']
    data['Относительный вес товара к весу всех товаров на стеллаже'] = data['Missing Good Weight'] / (data['Target Shelf Weight'] * data['Target Shelf Goods Count'])
    data['Кол-во товаров на стеллаже'] = data['Target Shelf Goods Count']
    data['Кол-во стеллажей'] = data['Total Shelves']
    data['Минимальный вес товаров '] = data['Min Weight']
    data['Максимальный вес товаров'] = data['Max Weight']
    return data
 

# Параметры для анализа
analysis_params = [
    'Кол-во товаров на стеллаже', 
    'Кол-во стеллажей',  
    'Минимальный вес товаров ', 
    'Максимальный вес товаров'
    #'Относительный вес товара к весу товара на стеллаже', 
    #'Относительный вес товара к весу всех товаров на стеллаже'
]

def categorize_param(data, param, bins=None):
    if pd.api.types.is_integer_dtype(data[param]) or pd.api.types.is_bool_dtype(data[param]):
        return data[param]  # Возвращаем как есть для дискретных параметров
    if bins is None:
        bins = np.histogram_bin_edges(data[param], bins='auto')
    return pd.cut(data[param], bins=bins)

def plot_analysis():
    data = getData()
    params=analysis_params
    for param in params:
        categorized_param = categorize_param(data, param, bins=20)

        # Средняя вероятность и стандартное отклонение ранга полки
        mean_prob = data.groupby(categorized_param)['Target Shelf Probability'].mean()
        rank_std = data.groupby(categorized_param)['Target Shelf Rank'].std()

        plt.figure(figsize=(15, 5))

        # Линейный график для средней вероятности
        plt.subplot(1, 3, 1)
        mean_prob.plot(kind='line', marker='o', title='Средняя вероятность нахождения товара на полке')
        plt.xlabel(param)
        plt.xticks(rotation=45, ha="right")

        # Столбчатая диаграмма для стандартного отклонения ранга полки
        plt.subplot(1, 3, 2)
        rank_std.plot(kind='bar', color='teal', title='Стандартное отклонение позиции полки')
        plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.xlabel(param)
        plt.xticks(rotation=45, ha="right")

        # Подготовка данных для нормированной столбчатой диаграммы с накоплением
        stacked_data = data.copy()
        stacked_data['Correct Shelf Prediction'] = stacked_data['Target Shelf Rank'] == 1
        stacked_counts = stacked_data.groupby([categorized_param, 'Correct Shelf Prediction']).size().unstack(fill_value=0)
        stacked_normalized = stacked_counts.div(stacked_counts.sum(axis=1), axis=0).iloc[:, ::-1]

        # Столбчатая диаграмма с накоплением для правильности предсказаний
        plt.subplot(1, 3, 3)
        stacked_normalized.plot(kind='bar', stacked=True, color=['mediumseagreen', 'lightcoral'], ax=plt.gca())
        plt.locator_params(axis='x', nbins=10)
        plt.title('Верные и неверные предсказания')
        plt.xlabel(param)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel('Доля')
        plt.legend(['Верно', 'Неверно'], title='Результат предсказания', loc='upper left', bbox_to_anchor=(1, 1))

        plt.tight_layout()
        plt.show()

#plot_analysis()
