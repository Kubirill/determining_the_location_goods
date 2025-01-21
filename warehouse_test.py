
import random
import math
import pandas as pd
import numpy as np

class TypeOfGoods:
    def __init__(self, name, weight, error_weight):
        self.name = name
        self.weight = weight
        self.error_weight = error_weight*weight

class Goods:
    def __init__(self, type_of_good):
        self.type_of_good = type_of_good
        self.weight = random.uniform((type_of_good.weight -type_of_good.error_weight), 
                                     (type_of_good.weight + type_of_good.error_weight))

class GaussianDistribution:
    def __init__(self, weight, error, count):
        self.mean = weight * count
        self.std_dev = error * math.sqrt(count)

    def init_with_good(self, weight, error, count, new_good):
        if new_good is not None:
            self.mean = weight * count + new_good.weight
            self.std_dev = math.sqrt(count * (error ** 2) + (new_good.type_of_good.error_weight ** 2))
        else:
            self.mean = weight * count
            self.std_dev = error * math.sqrt(count)

    def calculate_probability(self, x):
        if self.std_dev == 0:
            self.std_dev = 0.1
        m = self.mean
        sigma = self.std_dev
        num = 1.47 / (self.std_dev * math.sqrt(2 * math.pi))
        exponent = -((x - self.mean) ** 2) / (2 * (self.std_dev ** 2))
        return num * math.exp(exponent)

class Shelf:
    def __init__(self, number, type_of_good):
        self.number = number
        self.type_of_good = type_of_good
        self.goods_array = []
        self.total_weight = 0
        self.distribution = None
        self.goods_count = 0
        

    def calculate_total_weight(self):
        self.total_weight = sum(good.weight for good in self.goods_array)

    def calculate_distribution(self):
        self.distribution = GaussianDistribution(self.type_of_good.weight, 
                                                 self.type_of_good.error_weight, 
                                                 self.goods_count)

    def move_random_good(self, other_shelves):
        if self.goods_count > 0:
            random_good = random.choice(self.goods_array)
            self.goods_array.remove(random_good)
            self.calculate_total_weight()
            destination_shelf = random.choice([shelf for shelf in other_shelves if shelf.number != self.number])
            destination_shelf.goods_array.append(random_good)
            destination_shelf.calculate_total_weight()
            return random_good, self.number, destination_shelf.number 

    def check_good_probability(self, good):
        new_distribution = GaussianDistribution(0, 0, 0)
        new_distribution.init_with_good(self.type_of_good.weight, 
                                        self.type_of_good.error_weight, 
                                        self.goods_count, good)
        
        sum_prob = self.distribution.calculate_probability(self.total_weight) +  new_distribution.calculate_probability(self.total_weight)
        
        return new_distribution.calculate_probability(self.total_weight) / sum_prob if sum_prob > 0 else 0


def test(num_tests=10000, seed_value=42, detailed_tests=None, 
         num_shelves_range=None, num_types_of_goods_range=None, num_goods_per_shelf=None,
         weight_lower_range=None, weight_upper_range=None, error_range=None):
    random.seed(seed_value)  
    detailed_tests = detailed_tests or []  
    results = []
    
    for test_num in range(num_tests):
        # Если параметры не переданы, устанавливаем их случайные значения
        num_shelves = random.randint(num_shelves_range[0],num_shelves_range[1]) if num_shelves_range is not None else random.randint(10, 100)
        num_types_of_goods = random.randint(num_types_of_goods_range[0],num_types_of_goods_range[1])  if num_types_of_goods_range is not None else random.randint(5, 50)
        weight_range = (random.uniform(weight_lower_range[0],weight_lower_range[1]), random.uniform(weight_upper_range[0],weight_upper_range[1])) if (weight_lower_range is not None and weight_upper_range is not None ) else (random.uniform(0.1, 5), random.uniform(20, 100))
        error_range = error_range if error_range is not None else (0.01, 0.03)
        num_goods_per_shelf = num_goods_per_shelf if num_goods_per_shelf is not None else (random.randint(10, 20), random.randint(30, 100))

        # Генерация типов товаров
        type_of_goods_list = [
            TypeOfGoods(f"Type_{i+1}", 
                        random.uniform(weight_range[0], weight_range[1]), 
                        random.uniform(error_range[0], error_range[1]))
            for i in range(num_types_of_goods)
        ]
        
        # Создание полок и заполнение их товарами
        shelves = []
        for i in range(1, num_shelves + 1):
            shelf_type = random.choice(type_of_goods_list)
            shelf = Shelf(i, shelf_type)
            goods_list = [Goods(shelf_type) for _ in range(1, random.randint(num_goods_per_shelf[0], num_goods_per_shelf[1]))]
            
            shelf.goods_array = goods_list
            shelf.calculate_total_weight()
            shelf.goods_count = len(goods_list)
            shelf.calculate_distribution()
            shelves.append(shelf)
        
        # Перемещение товара
        move_result = shelves[0].move_random_good(shelves)
        if move_result is None:
            continue
        
        missing_good, source_shelf, destination_shelf = move_result
        
        # Расчёт вероятностей
        probabilities = [(shelf, shelf.check_good_probability(missing_good)) for shelf in shelves]
        probabilities.sort(key=lambda x: x[1], reverse=True)

        if test_num + 1 in detailed_tests:
            print(f"Detailed output for Test #{test_num + 1}:")
            print(f"Source Shelf: {source_shelf}, Destination Shelf: {destination_shelf}")
            print("Shelf Probability Table (sorted by probability):")
            
            detail_table = pd.DataFrame([
                {
                    "Shelf Number": shelf.number,
                    "Type of Goods": shelf.type_of_good.name,
                    "Goods Weight": shelf.type_of_good.weight,
                    "Goods Count": shelf.goods_count,
                    "Total Shelf Weight": shelf.total_weight,
                    "Probability": prob
                } for shelf, prob in probabilities
            ]).sort_values(by="Probability", ascending=False)
            print(detail_table.to_string(index=False))
        
        # Сбор данных о результатах
        for rank, (shelf, prob) in enumerate(probabilities, start=1):
            if missing_good in shelf.goods_array:
                target_shelf_rank = rank
                target_shelf_prob = prob
                target_shelf_weight = shelf.type_of_good.weight
                target_shelf_count = shelf.goods_count-1
                target_shelf_std_dev = shelf.distribution.std_dev
                all_goods_weights = [g.weight for sh in shelves for g in sh.goods_array]
                min_weight, max_weight = min(all_goods_weights), max(all_goods_weights)
                target_shelf_all_std_dev = np.std([g.weight for g in shelf.goods_array])
                break

        results.append({
            "Test Number": test_num + 1,
            "Target Shelf Probability": target_shelf_prob,
            "Target Shelf Rank": target_shelf_rank,
            "Missing Good Weight": missing_good.type_of_good.weight,
            "Target Shelf Weight": target_shelf_weight,
            "Target Shelf Goods Count": target_shelf_count-1,
            "Total Shelves": num_shelves,
            "Target Shelf Std Dev": target_shelf_std_dev,
            "Min Weight": min_weight,
            "Max Weight": max_weight,
            "Target Shelf All Std Dev": target_shelf_all_std_dev
        })

    results_df = pd.DataFrame(results)
    return results_df




