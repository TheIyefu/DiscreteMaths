import heapq
import zlib

# создает словарь
encoding = {}


# создает класс узлов минимальной кучи
class Node:
    def __init__(self, value, symbol=None):
        self.left = None
        self.right = None
        self.symbol = symbol
        self.value = value

    def __lt__(self, other):
        if self.value < other.value:
            return True
        elif self.value == other.value:
            return self.symbol < other.symbol
        else:
            return False

    def __str__(self):
        return f"{self.symbol} - value {self.value} left - {self.left} right {self.right}"

    def __repr__(self):
        return f"{self.symbol} - value {self.value} left - {self.left} right {self.right}"


def recur(n, code):
    global encoding
    if n.left is None and n.right is None:
        encoding[n.symbol] = code
    if n.left is not None:
        recur(n.left, code + '1')
    if n.right is not None:
        recur(n.right, code + '0')


def encode(word):
    '''кодирование файла в двоичную форму'''
    freq = {}
    for _ in word:
        if _ in freq:
            freq[_] += 1
        else:
            freq[_] = 1

    pq = []
    for symbol in freq:
        pq.append(Node(freq[symbol], symbol))
    heapq.heapify(pq)

    while len(pq) > 1:
        n1 = heapq.heappop(pq)
        n2 = heapq.heappop(pq)
        n3 = Node(n1.value + n2.value, n1.symbol + n2.symbol)
        n3.left = n1
        n3.right = n2
        heapq.heappush(pq, n3)

    recur(pq[0], '')
    print(f"словарь кодов: {encoding}")

    bits = ''
    for _ in word:
        if not _ in encoding:
            raise ValueError("'" + _ + "' не является закодированным символом")
        bits += encoding[_]
    return bits


def decode(str):
    '''декодирование из двоичного кода в алфавиты, основанное на словаре кода'''
    reverse_encoding = {v: k for k, v in encoding.items()}
    window = ''
    result = ''
    for i in str:
        window += i
        value = reverse_encoding.get(window)
        if value is not None:
            result += value  # когда мы нашли совпадение
            window = ''  #сброса window
    # продолжить добавление в window
    return result


with open('input.txt') as f:
    '''кодирует строку, считанную из файла'''
    word = ''.join(f.readlines())
print(f"Текст, прочитанный из input.txt: \n{word}\n\n")
bits = encode(word)
nums = int(bits)
with open("output.txt", "w") as binary_file:
    binary_file.write(f'словарь кодов: {encoding}')
    binary_file.write('%d' % nums)

print(f'Кодированная версия: \n{bits}\n\n')

decoded = decode(bits)

with open('decoded.txt', 'w') as f:
    '''записывает декодированный текст в decoded.txt'''
    f.write(decoded)

print(f'Декодированная версия: \n{decoded}')