def calculate_score(indicator_values):
    average_value = sum(indicator_values) / len(indicator_values)
    deviation_scores = [100 * (value - average_value) / average_value for value in indicator_values]
    final_score = sum(deviation_scores) / len(deviation_scores)
    return final_score

# 示例数据，用于演示计算过程
market_volatility = 0.8
foreign_investment = 5000
futures_premium = 0.05
price_strength = 0.6
hedging_demand = -0.2
leverage_ratio = 0.3

# 计算每个指标的分值
indicator_scores = []
indicator_scores.append(calculate_score([market_volatility]))
indicator_scores.append(calculate_score([foreign_investment]))
indicator_scores.append(calculate_score([futures_premium]))
indicator_scores.append(calculate_score([price_strength]))
indicator_scores.append(calculate_score([hedging_demand]))
indicator_scores.append(calculate_score([leverage_ratio]))

# 计算最终指标的平均分值
final_score = sum(indicator_scores) / len(indicator_scores)

print("每个指标的分值:", indicator_scores)
print("最终指标的平均分值:", final_score)
