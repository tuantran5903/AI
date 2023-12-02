import numpy as np
import random
import matplotlib.pyplot as plt

# 3.1 Khởi tạo các món hàng 
def generate_random_items(num_items, max_Value, max_Weight):
    values = []
    weights = []
    result="Danh sách các món hàng:\n"
    for i in range(0, num_items):
        values.append(np.random.randint(1, max_Value))
        weights.append(np.random.randint(1, max_Weight))
        item = "Tên: " + f"Món hàng {i+1}, " + "Trọng lượng: " + f"{weights[i]}, " + "Giá trị: " + f"{values[i]}\n"
        result+=item
    return values, weights, result

# 3.2 Khởi tạo giải pháp ngẫu nhiên 
def Random_Initial_solution(initial_prop_of_items, num_items):
    x = np.random.binomial(1, initial_prop_of_items, size=num_items)
    return x

# 3.3 Tạo hàm tính giá trị value và weight 
def evaluate(solution, capacity, values, weights):
    array_solution = np.array(solution)
    array_value = np.array(values)
    array_weight = np.array(weights)
    value = np.dot(array_solution, array_value)  
    weight = np.dot(array_solution, array_weight)  
    if weight > capacity:
        return [weight-capacity, weight]
    else:
        return [value, weight]

def getNeighbours(solution, num_items):
    nbrhood = []
    for i in range(0, num_items):
        temp=list(solution)
        nbrhood.append(temp)
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    return nbrhood

class HillClimbing():
    def __init__(self, num_items, capacity, max_Value, max_Weight):
        self.values = None
        self.weights = None
        self.current_solution = None
        self.result = None
        self.num_items = num_items        
        self.capacity = capacity
        self.max_Value = max_Value
        self.max_Weight = max_Weight
        self.iterPro = {}

    def plotOutput(self):
        plt.figure(figsize=(7, 5))
        plt.xticks(np.arange(0, 100 + 10, 10), fontsize=5)
        plt.yticks(np.arange(0, 1000+100,100), fontsize=5)
        plt.plot(*zip(*self.iterPro.items()))
        plt.xlabel('Restarts', fontsize=7)
        plt.ylabel('Optimal choice', fontsize=7)
        plt.title('Solving Knapsack using HillClimbing', fontsize=8)
        plt.show()
      
    def solve(self):  
        initial_prop_of_items=0.2
        restarts=100
        solutionsChecked=0
        evaluate_super_best= [0,0]
        self.values, self.weights, self.result = generate_random_items(self.num_items, self.max_Value, self.max_Weight)
        for restart in range(restarts):
            done = 0
            self.current_solution = Random_Initial_solution(initial_prop_of_items, self.num_items)  # current_solution sẽ giữ giải pháp hiện tại 
            best_solution = self.current_solution[:]  # best_solution sẽ giữ giải pháp tốt nhất
            evaluate_current = evaluate(self.current_solution, self.capacity, self.values, self.weights)[:]  # evaluate_current sẽ giữ việc đánh giá giải pháp hiện tại
            evaluate_best = evaluate_current[:]   

            while done == 0:
                Neighborhood = getNeighbours(self.current_solution, self.num_items)  # tạo danh sách tất cả giải pháp lân cận của current_solution
                for s in Neighborhood:  
                    solutionsChecked = solutionsChecked + 1
                    if ((evaluate(s, self.capacity, self.values, self.weights)[0] > evaluate_best[0]) and (evaluate(s, self.capacity, self.values, self.weights)[1] <= self.capacity)):  
                        best_solution = s[:] 
                        evaluate_best = evaluate(s, self.capacity, self.values, self.weights)[:]

                if evaluate_best == evaluate_current:  # nếu không có giải pháp hàng xóm nào tốt hơn best_solution 
                    done = 1
                else:
                    self.current_solution = best_solution[:] 
                    evaluate_current = evaluate_best[:] 

            self.iterPro[restart] = evaluate_best[0]
            if (evaluate_best[0] > evaluate_super_best[0]):
                evaluate_super_best = evaluate_best[:]     # value tốt nhất cho đến hiện tại 
                solution_super_best = best_solution[:]     # giải pháp tốt nhất cho đến hiện tại 

        self.result += "\nSố lượng hàng xóm được duyệt qua: " + str(solutionsChecked) + "\n"
        self.result += "Giải pháp tốt nhất: " + str(solution_super_best) + "\n"
        self.result += "Value của giải pháp tốt nhất: " + str(evaluate_super_best) + "\n"
        return self.result, self.current_solution, self.values, self.iterPro

if __name__ == "__main__":
    Hill = HillClimbing(20,50,100,20)
    Hill.solve()
    result, current_solution, values, iterPro=Hill.solve()
    print(result)
    Hill.plotOutput()
