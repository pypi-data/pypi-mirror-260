# Решаем задачу множественного тестирования
# Хотим выбрать лучшую выборку из k выборок по некоторой целевой метрике
# Пусть гипотеза H_i - iя выборка лучшая, i = 1, ..., k
# Пусть гипотеза H_0 - нет лучшей выборки

# Разработали метод, основанный на предельном распределении
# Он позволяет придерживаться заложенных вероятностей ошибок 1го и 2го рода

# Функции минимального размера выборки и критерия являются основными
# Функция квантиля предельного распределения случайной величины минимума используется в основных функциях


from scipy.stats import norm, bernoulli


# Решаем задачу множественного тестирования
# Хотим выбрать лучшую выборку из k выборок по некоторой целевой метрике
# Пусть гипотеза H_i - iя выборка лучшая, i = 1, ..., k
# Пусть гипотеза H_0 - нет лучшей выборки

# Разработали метод, основанный на предельном распределении
# Он позволяет придерживаться заложенных вероятностей ошибок 1го и 2го рода

# Функции минимального размера выборки и критерия являются основными
# Функция квантиля предельного распределения случайной величины минимума используется в основных функциях

def quantile_of_marginal_distribution(num_samples, quantile_level, variances=[1, 1, 1], equal_variance=True):
    """Функция квантиля предельного распределения минимума

    Parameters
    ----------
    num_samples : int
        Количество выборок, целое число больше 2
    quantile_level : float
        Уровень квантиля предельного распределения минимума
    variances : list of float, optional
        Список дисперсий выборок одинаковой длины. Количество выборок больше 2
    equal_variance : bool, optional
        Равенство дисперсий

    Returns
    -------
    float, если equal_var=True
        Квантиль предельного распределения минимума уровня gamma
    list of float, если equal_var=False
        Набор квантилей предельного распределения минимума для каждого reference_sample_index уровня gamma
    """
    iteration_size = 20000  # Количество итераций теста

    if equal_variance:
        reference_sample_index = 0  # в силу симметрии reference_sample_index по гипотезе H_0 возьмём reference_sample_index = 0 (первая выборка)
        t_values = []
        random_samples = norm.rvs(size=[iteration_size, num_samples], random_state=random_state)
        for sample in random_samples:
            min_t_value = np.inf
            for i in range(num_samples):
                if i != reference_sample_index:
                    t_value = (sample[reference_sample_index] - sample[i]) / np.sqrt(2)
                    min_t_value = min(min_t_value, t_value)
            t_values.append(min_t_value)
        return np.quantile(t_values, quantile_level)
    else:
        quantiles = []
        for j in range(num_samples):
            t_values = []
            random_samples = norm.rvs(size=[iteration_size, num_samples], random_state=random_state)
            for sample in random_samples:
                min_t_value = np.inf
                for i in range(num_samples):
                    if i != j:
                        t_value = sample[j] / np.sqrt(1 + variances[i] / variances[j]) - sample[i] / np.sqrt(
                            1 + variances[j] / variances[i])
                        min_t_value = min(min_t_value, t_value)
                t_values.append(min_t_value)
            quantiles.append(np.quantile(t_values, quantile_level))
        return quantiles


def test_on_marginal_distribution(samples, significance_level=0.05, equal_variance=True, quantiles=None):
    """Функция критерия, основанного на предельном распределении минимума

    Parameters
    ----------
    samples : list of lists
        Список выборок одинаковой длины. Количество выборок больше 2
    significance_level : float, optional
        Уровень значимости, число от 0 до 1
    equal_variance : bool, optional
        Равенство дисперсий
    quantiles : optional
            float, если equal_var=True
                Квантиль предельного распределения минимума уровня 1-alpha/len(X)
            list of float, если equal_var=False
                Набор квантилей предельного распределения минимума для каждого j уровня 1-alpha/len(X)

    Returns
    -------
    int
        Число от 0 до k - номер принятой гипотезы
    """
    num_samples = len(samples)  # Число выборок
    sample_size = len(samples[0])  # Размер выборки

    means = [np.mean(sample) for sample in samples]
    variances = [np.var(sample) * sample_size / (sample_size - 1) for sample in samples]

    if equal_variance:
        if quantiles is None:
            quantiles = quantile_of_marginal_distribution(num_samples=num_samples,
                                                          quantile_level=1 - significance_level / num_samples)  # квантиль предельного распределения
        for j in range(num_samples):
            min_t_value = np.inf
            for i in range(num_samples):
                if i != j:
                    t_value = np.sqrt(sample_size) * (means[j] - means[i]) / np.sqrt(variances[j] + variances[i])
                    min_t_value = min(min_t_value, t_value)
            if min_t_value > quantiles:
                return j + 1
        return 0
    else:
        if quantiles is None:
            quantiles = quantile_of_marginal_distribution(num_samples=num_samples,
                                                          quantile_level=1 - significance_level / num_samples,
                                                          variances=variances,
                                                          equal_variance=False)  # набор квантилей предельного распределения
        for j in range(num_samples):
            min_t_value = np.inf
            for i in range(num_samples):
                if i != j:
                    t_value = np.sqrt(sample_size) * (means[j] - means[i]) / np.sqrt(variances[j] + variances[i])
                    min_t_value = min(min_t_value, t_value)
            if min_t_value > quantiles[j]:
                return j + 1
        return 0


def min_sample_size(number_of_samples, minimum_detectable_effect, variances, significance_level=0.05, power_level=0.2,
                    equal_variance=True, quantile_1=None, quantile_2=None, initial_estimate=None):
    """Функция для подсчёта минимального размера выборки

    Parameters
    ----------
    number_of_samples : int
        Количество выборок, целое число больше 2
    minimum_detectable_effect : float
        Minimum Detectable Effect, положительное число
    variances : list of float, если equal_var=False
          float, если equal_var=True
        Оценка дисперсии выборок одинаковой длины при H(0). Количество выборок больше 2
    significance_level : float, optional
        Уровень значимости, число от 0 до 1
    power_level : float, optional
        1 - мощность, число от 0 до 1
    equal_variance : bool, optional
        Равенство дисперсий
    quantile_1 : optional
            float, если equal_var=True
                Квантиль предельного распределения минимума уровня 1-alpha/len(X)
            list of float, если equal_var=False
                Набор квантилей предельного распределения минимума для каждого sample_index уровня 1-alpha/len(X)
    quantile_2 : optional
            float, если equal_var=True
                Квантиль предельного распределения минимума уровня beta
            None, если equal_var=False
    initial_estimate : int, optional
        Нижняя граница для размера (для более быстрой работы программы)

    # В нашем случае все выборки будут одного размера

    Returns
    -------
    int
        Число sample_size - размер одной выборки
    """
    random_state = 42
    if equal_variance:
        if quantile_1 is None:
            quantile_1 = quantile_of_marginal_distribution(num_samples=number_of_samples,
                                                           quantile_level=1 - significance_level / number_of_samples)  # квантиль предельного распределения 1-alpha/k

        if quantile_2 is None:
            quantile_2 = quantile_of_marginal_distribution(num_samples=number_of_samples,
                                                           quantile_level=power_level)  # квантиль предельного распределения beta
        print(f"{quantile_1 = }, {quantile_2 = }")

        return int(2 * variances * ((quantile_1 - quantile_2) / minimum_detectable_effect) ** 2) + 1
    else:
        iteration_size = 3000  # Количество итераций
        if quantile_1 is None:
            quantile_1 = quantile_of_marginal_distribution(num_samples=number_of_samples,
                                                           quantile_level=1 - significance_level / number_of_samples,
                                                           variances=variances,
                                                           equal_variance=False)  # набор квантилей предельного распределения
        sample_sizes = []  # для размеров выборки
        for sample_index in range(number_of_samples):
            sample_size = initial_estimate or 0
            current_power = 0  # мощность
            while current_power < 1 - power_level:
                sample_size += 100
                current_power = 0
                total_samples = norm.rvs(size=[iteration_size, number_of_samples], random_state=random_state)
                for sample in total_samples:
                    min_t_value = np.inf
                    for i in range(number_of_samples):
                        if i != sample_index:
                            t_value = sample[sample_index] / np.sqrt(1 + variances[i] / variances[sample_index]) - \
                                      sample[i] / np.sqrt(
                                1 + variances[sample_index] / variances[i]) + minimum_detectable_effect * np.sqrt(
                                sample_size / (variances[sample_index] + variances[i]))
                            min_t_value = min(min_t_value, t_value)
                    if min_t_value > quantile_1[sample_index]:
                        current_power += 1
                current_power /= iteration_size
            sample_sizes.append(sample_size)
        return np.max(sample_sizes)


# Применение метода

import numpy as np

# Фиксированный random state
random_state = np.random.RandomState(42)  # Вы можете выбрать любое число в качестве seed

num_samples = 10  # число выборок
minimum_detectable_effect = 0.05  # MDE
assumed_conversion = 0.3  # предполагаемая конверсия
significance_level = 0.05  # уровень значимости
power_level = 0.2  # 1 - мощность

# Считаем минимальный размер выборки
sample_size = min_sample_size(num_samples, minimum_detectable_effect,
                              variances=assumed_conversion * (1 - assumed_conversion),
                              significance_level=significance_level, power_level=power_level, equal_variance=True)
print(f'Размер выборки = {sample_size}')
print("kek")

N = 5

# Все выборки имеют одинаковую конверсию
print('\nВсе выборки имеют одинаковую конверсию')
for _ in range(N):
    samples = bernoulli.rvs(assumed_conversion, size=[num_samples, sample_size], random_state=random_state)
    hypothesis = test_on_marginal_distribution(samples, significance_level=significance_level)
    print(f'\tПринята гипотеза H({hypothesis})')

# Десятая выборка имеет большую на MDE конверсию
print('\nДесятая выборка имеет большую на MDE конверсию')
for _ in range(N):
    samples = [bernoulli.rvs(assumed_conversion, size=sample_size, random_state=random_state) for _ in
               range(num_samples - 1)]
    samples.append(
        bernoulli.rvs(assumed_conversion + minimum_detectable_effect, size=sample_size, random_state=random_state))
    hypothesis = test_on_marginal_distribution(samples, significance_level=significance_level)
    print(f'\tПринята гипотеза H({hypothesis})')

# Пример 2
# Рассмотрим множественный тест для выявления выборки с лучшим доходом на клиента (конверсия * цена)
# В этом случае при гипотезе H_0, равенстве ARPU на всех выборках, дисперсии не равны,
# поскольку при гипотезе H_0 при разных ценах получаем разные конверсии

num_samples = 5  # число выборок
minimum_detectable_effect = 2.5  # MDE
# в среднем ARPU = 15 рублей
prices = [100, 150, 150, 200, 250]  # цены тарифов
conversions = [0.15, 0.1, 0.1, 0.075, 0.06]  # конверсии тарифов
significance_level = 0.05  # уровень значимости
power_level = 0.2  # 1 - мощность
variances = [price ** 2 * conversion * (1 - conversion) for price, conversion in zip(prices, conversions)]

# считаем минимальный размер выборки
sample_size = min_sample_size(num_samples, minimum_detectable_effect, variances=variances, significance_level=significance_level,
                              power_level=power_level, equal_variance=False)
print(f'Размер выборки = {sample_size}')

# Попробуем сгенерировать выборки и посмотреть результат тестирования
N = 5
# все выборки имеют одинаковый ARPU
print('\nВсе выборки имеют одинаковый ARPU')
for _ in range(N):
    samples = []
    for i in range(num_samples):
        samples += [prices[i] * bernoulli.rvs(conversions[i], size=sample_size)]
    hypothesis = test_on_marginal_distribution(samples, significance_level=significance_level)
    print(f'\tПринята гипотеза H({hypothesis})')

# десятая выборка имеет больший на MDE ARPU
print('\nДесятая выборка имеет больший на MDE ARPU')
for _ in range(N):
    samples = []
    for i in range(num_samples - 1):
        samples += [prices[i] * bernoulli.rvs(conversions[i], size=sample_size)]
    samples += [prices[num_samples - 1] * bernoulli.rvs(
        conversions[num_samples - 1] + minimum_detectable_effect / prices[num_samples - 1], size=sample_size)]
    hypothesis = test_on_marginal_distribution(samples, significance_level=significance_level)
    print(f'\tПринята гипотеза H({hypothesis})')
