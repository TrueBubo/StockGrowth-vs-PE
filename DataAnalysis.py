import scipy

from CompanyStats import CompanyStats
import numpy as np
import matplotlib.pyplot as plt

stats2022: dict = CompanyStats("Common Stocks — USA — TradingView - 2022.html", 2022).getStats()
stats2024: dict = CompanyStats("All US Stocks on One Page — TradingView - 2024.html", 2024).getStats()

number_of_years_between = 22 / 12

ignore_companies = {}

common_companies = stats2022.keys() & stats2024.keys()

companies = [stats2022[company] for company in common_companies if (stats2022[company].pe
             is not None and company not in ignore_companies)]


previous_pe = np.array([company.pe for company in companies])
growth_rates = np.array([((stats2024[company.ticket].price / stats2022[company.ticket].price) - 1) * 100 for company in companies])
growth_rates = np.sign(growth_rates) * (np.abs(growth_rates) ** (1 / number_of_years_between)) # Deals with negative growth rates

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(previous_pe, growth_rates)

plt.title("Relationship between growth rate and P/E")
plt.xlabel("P/E")
plt.ylabel("Growth rate per year")
plt.scatter(previous_pe, growth_rates)
plt.plot(previous_pe, slope*previous_pe+intercept)
print(f"growth_rate = {slope}*PE + {intercept}")
print(f"r^2 = {round(r_value ** 2, 4)}")
print(f"p = {round(p_value, 4)}")
plt.savefig("growth_pe_graph.png")
plt.show()
