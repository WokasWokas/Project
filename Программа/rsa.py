"""
    Импорт нужных библиотек.
    1. Настройки
    2. Модуль для получения рандомных значение длиной в k бит
    3. Модуль получения времени, для обновления сида относительно текущего времени
"""
from preference import preference
import random 
import time

# Функция обновления сида для метода random
UpdateSeed = lambda: random.seed(version=int(time.time())) 

# Инициализация настроек программы
__KEY_LENGTH__ = preference.get('__KEY_LENGTH__')
__EXPONENT_KEY_LENGTH__ = preference.get('__EXPONENT_KEY_LENGTH__')
__BLOCK_LENGTH__ = preference.get('__BLOCK_LENGTH__')
__ENCODE__ = preference.get('__ENCODE__')

# Функция проверки числа на простоту
def IsPrime(number: int) -> bool: 
    if (number == 2 or number == 3):
        return True
    if (number % 2 == 0 or number % 3 == 0 or number == 1):
        return False
    i = 5
    while (i*i < number):
        if (number % i == 0 or number % (i + 2) == 0):
            return False
        i += 4
    return True

# Деление строки на блоки
def SplitString(text: str) -> tuple[str]:
    return [text[i:i+__BLOCK_LENGTH__] for i in range(0, len(text), __BLOCK_LENGTH__)]

# Получение наибольшего общего делителя
def gcd(value1: int, value2: int) -> int:
    while ((value1 != 0) and (value2 != 0)):
        if (value1 > value2):
            value1 -= value2
        else:
            value2 -= value1
    return max(value1, value2)

# Генерация числа
def GenerateNumber(exponent: bool = False) -> int:
    if exponent: 
        length = __EXPONENT_KEY_LENGTH__ 
    else: 
        length = __KEY_LENGTH__
    return random.getrandbits(length)

# Функция получения простого числа
def GetRandomPrimeNumber(exponent: bool = False) -> int:
    number = GenerateNumber(exponent)
    while not IsPrime(number):
        number = GenerateNumber(exponent)
    return number

class RSA: # Основной класс программы
    def __init__(self) -> None: # Инициализация программы
        status = self.Generate()
        while not status:
            status = self.Generate()
    
    # Фунция инициализации генерации ключей и экспоненты
    def Generate(self):
        UpdateSeed()
        self.FirstKey = GetRandomPrimeNumber() # получение первого и второго простого числа 
        self.SecondKey = GetRandomPrimeNumber()
        self.PublicKey = self.FirstKey * self.SecondKey # получение публичного числа
        self.Euler = (self.FirstKey - 1) * (self.SecondKey - 1) # получение числа эйлера
        self.Exponent = self.GetExponent() # генерация экспоненты
        self.PrivateKey = self.GetPrivateKey() # генерация приватного ключа
        if self.PrivateKey is None: # проверка на правильность генерации
            return False
        self.pubkey  = (self.Exponent, self.PublicKey)
        self.privkey = (self.PrivateKey, self.PublicKey)
        status = self.CheckKeys() # проверка работоспрособности ключей
        if not status:
            return False
        return True

    # функция получения экспоненты
    def GetExponent(self) -> int: 
        Exponent = GetRandomPrimeNumber(True)
        # пока число больше публичного ключа или наибольший делитель не равен 1, ищет экспоненту
        while Exponent > self.PublicKey or gcd(Exponent, self.Euler) != 1:
            Exponent = GetRandomPrimeNumber(True)
        return Exponent

    # Функция получения приватного ключа
    def GetPrivateKey(self) -> int:
        PrivateKey = GetRandomPrimeNumber()
        # счётчик попыток
        count, ucount = 0, 0
        # пока произведение приватного ключа и экспоненты минус 1 
        # обратно взаимно число эйлеру, ищем приватный ключ
        while (PrivateKey * self.Exponent - 1) % self.Euler != 0:
            if count % 25 == 0: # обновление сида
                if ucount == 20: # возврат ошибки поиска
                    return None
                UpdateSeed()
                self.Exponent = self.GetExponent()
                ucount += 1
            PrivateKey = GetRandomPrimeNumber()
            count += 1
        return PrivateKey

    # Проверка правильности ключей
    def CheckKeys(self) -> bool:
        try:
            decoded = self.Decode('test')
            encoded = self.Encode(decoded)
            # Если после шифрования и расшифровки данные одинаковые, то ключи правильные
            if encoded.replace('\0', '').encode('utf-8') != 'test'.encode('utf-8'):
                raise ValueError('Wrong Keys')
            return True
        except:
            return False

    # Функция зашифровки
    def Decode(self, text: str) -> str:
        blocks = SplitString(text) # разделения данных на блоки
        decodedblocks = [] # зашифрованные блоки
        for block in blocks:
            value = int.from_bytes(bytes(block, __ENCODE__), byteorder='little', signed=True)
            # зашифровка блока по формуле: (value ^ exponent) % pubkey
            decodedblocks.append(pow(value, self.pubkey[0], self.pubkey[1]))
        return ' '.join(str(block) for block in decodedblocks)

    # Функция расшифровки
    def Encode(self, text: int) -> str:
        try:
            decodedblocks = text.split(' ') 
            blocks = []
            for block in decodedblocks:
                # Расшифровка блока по формуле: (value ^ privkey) % pubkey
                value = pow(int(block), self.privkey[0], self.privkey[1])
                blocks.append(value.to_bytes(value.bit_length(), byteorder='little', signed=True))
            return (''.join(block.decode(__ENCODE__) for block in blocks)).replace('\0', '')
        except ValueError:
            return 'Wrong Value!'

    def GetData(self) -> str: # получение данных ключей
        data = f"First Prime    | {self.FirstKey}\nSecond Prime   | {self.SecondKey}\nPublicKey      | {self.pubkey[1]}\n"
        data += f"Euler          | {self.Euler}\nExponent       | {self.pubkey[0]}\nPrivate Key    | {self.privkey[0]}"
        return data