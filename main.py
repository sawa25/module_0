import numpy as np
import time

# глобальная переменная является списком, значит передается в декораторы по ссылке.
# сделана попытка исключить обращение по глобальному имени где-то внутри кода
# может это и не имеет смысла????.....,а следует напрямую обращаться по глобальному имени
totalcount = [0]  # хранить количество протестированных алгоритмов


def decorator_maker_with_arguments(algo_count):
    # внешний декоратор для цели передачи переменной хранения количества вызовов внутреннего декоратора
    # algo_count - фактически ссылка на глобальную переменную хранения количества тестируемых алгоритмов
    # но исключается обращение по глобальному имени totalcount
    def decorator_scoretime_game(game_core):  # внутренний декоратор
        def wrapper(*args, **kwargs):
            nonlocal algo_count
            algo_count[0] = algo_count[0] + 1
            np.random.seed(1)  # фиксируем RANDOM SEED, чтобы эксперимент был воспроизводим!
            # если переданы параметры для диапазона случайных чисел, то использовать их
            if "init_min" in kwargs.keys():
                init_min = kwargs.get("init_min")
            else:
                init_min = 1
            if "init_max" in kwargs.keys():
                init_max = kwargs.get("init_max")
            else:
                init_max = 101
            probes_count = 5000  # количество случайных чисел для определения средних показателей
            random_array = np.random.randint(init_min, init_max, size=probes_count)  # массив случайных чисел
            result_array = np.zeros(probes_count)  # массив числа попыток угадывания каждого из чисел в random_array

            t0 = time.time_ns()  # начальное время старта
            '''Запускаем игру probes_count раз, чтобы узнать средние показатели скорости работы алгоритма'''
            for i in range(probes_count):
                result_array[i] = game_core(random_array[i])
            dt = time.time_ns() - t0  # время, затраченное на выполнение числа угадываний, равного probes_count

            # среднее число попыток и среднее время одного угадывания
            score, perform_time = result_array.mean(), dt / probes_count
            print(f"    '{game_core.__name__}' угадывает в среднем за {round(score)} попыток, "
                  f"\n       среднее время одного угадывания составляет {perform_time} наносекунд.")
            return None  # неявный возврат только измененного totalcount, переданного по ссылке

        return wrapper

    return decorator_scoretime_game


@decorator_maker_with_arguments(algo_count=totalcount)
def game_core_v1(number):  # оригинальная функция из примера skillfactory, оставлена для сравнения
    '''Просто угадываем на random, никак не используя информацию о больше или меньше.
    Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    while True:
        count += 1
        predict = np.random.randint(1, 101)  # предполагаемое число
        if number == predict:
            return count  # выход из цикла, если угадали


@decorator_maker_with_arguments(algo_count=totalcount)
def game_core_v2(number):  # оригинальная функция из примера skillfactory, оставлена для сравнения
    '''Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того,
    больше оно или меньше нужного.
    Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    predict = np.random.randint(1, 101)
    while number != predict:
        count += 1
        if number > predict:
            predict += 1
        elif number < predict:
            predict -= 1
    return (count)  # выход из цикла, если угадали


@decorator_maker_with_arguments(algo_count=totalcount)
def game_core_v3(number, init_min=1, init_max=101):  # функция, реализованная в качестве задания
    '''Функция принимает загаданное число number из заданного диапазона init_min÷init_max
    и возвращает число попыток угадывания:
    Для каждой очередной попытки угадать number вплоть до момента успешного сравнения predict и number
    выбираем число predict, определенное методом деления текущего диапазона(отрезка) пополам на
    поддиапазоны, один из которых (левый или правый) принимается для последующих итераций в
    зависимости от результата сравнения number и очередного predict.
    (слева или справа находится number по отношению к predict)'''

    count = 0  # количество попыток угадать
    # диапазон возможных чисел
    left_boundary = init_min
    right_boundary = init_max
    while True:
        count += 1
        predict = (right_boundary + left_boundary) // 2  # выбрать число в середине текущего диапазона
        if number == predict:
            return (count)  # выход из цикла, если угадали
        if number > predict:  # выбрать для последующей итерации правый поддиапазон
            left_boundary = predict
        elif number < predict:  # выбрать для последующей итерации левый поддиапазон
            right_boundary = predict


if __name__ == '__main__':
    # для собственной функции game_core_v3 можно задать диапазон случайных чисел
    init_min = 1
    init_max = 101
    print(f"Выполняется тестирование алгоритмов угадывания случайного целого чиса в диапазоне <{init_min}÷{init_max}>:")
    # оригинальные функции game_core_v1,game_core_v2 из примера skillfactory не модифицированы,
    # диапазон в них принимается от 1 до 101
    game_core_v1()
    game_core_v2()
    game_core_v3(init_min=init_min, init_max=init_max)  # собственная функция
    dend = int(
        str(totalcount[0])[-1])  # последняя цифра числа протестированных алгоритмов для установки окончания слова
    print(f"\nПротестирован(о) {totalcount[0]} алгоритм{'' if dend == 1 else 'а' if 1 < dend <= 4 else 'ов'}.")
