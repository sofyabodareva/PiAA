from collections import deque

class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.is_terminal = False
        self.suff_link = None
        self.exit_link = None
        self.pattern_starts = []
        self.pattern_len = 0


class Trie:
    def __init__(self):
        self.root = Node('')


    def add_word(self, word: str, word_start: int) -> None:
        current = self.root
        for char in word:
            if char not in current.children:
                new_name = current.name + char
                current.children[char] = Node(new_name)
                output_name = current.name if current.name else "root"
                print(f"Добавляем к текущему узлу '{output_name}' дочерний узел с символом '{char}'")
            else:
                print(f"Переходим по существующему узлу '{current.name+char}'")
            current = current.children[char]
        print(f"Слово '{word}' добавлено, узел '{current.name}' помечен как терминальный")
        current.is_terminal = True
        current.pattern_len = len(word)
        current.pattern_starts.append(word_start)

    
    def create_links(self) -> None:
        print("\nСоздаем суффиксные и конечные ссылки:")
        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                print(f"\nОбрабатываем узел '{child.name}'")
                link = current.suff_link
                while link is not None and char not in link.children:
                    output_name = link.name if link.name else 'root'
                    print(f"  Символ '{char}' не найден в '{output_name}', поднимаемся выше")
                    link = link.suff_link
                child.suff_link = link.children[char] if link else self.root
                if child.suff_link is child:
                    child.suff_link = self.root
                suff_name = child.suff_link.name if child.suff_link.name else 'root'
                print(f"  Суффиксная ссылка -> '{suff_name}'")
                if child.suff_link.is_terminal:
                    child.exit_link = child.suff_link
                else:
                    child.exit_link = child.suff_link.exit_link
                exit_name = child.exit_link.name if child.exit_link else "нет"
                print(f"  Выходная ссылка   -> '{exit_name}'")
                queue.append(child)


    def aho_corasick(self, text: str, pattern_len: int, count_word: int) -> list:
        print("\nПроведем поиск вхождений подстрок в текст с помощью алгоритма Ахо-Корасик:")
        match_count = [0] * (len(text)+1)
        current = self.root
        for i in range(len(text)):
            char = text[i]
            print(f"\nТекущий обрабатываемый символ текста '{char}' (позиция в тексте {i+1})")
            while current is not  self.root and char not in current.children:
                print(f"  Символа '{char}' нет в узле '{current.name}', переходим по суффиксной ссылке")
                current = current.suff_link
            if char in current.children:
                current = current.children[char]
                print(f"  Переходим в узел '{current.name}'")
            else:
                print(f"  Символ '{char}' не найден, остаёмся в root")
            node = current
            while node is not self.root:
                if node.is_terminal:
                    for pos in node.pattern_starts:
                        start = i - node.pattern_len - pos + 2
                        if 1 <= start <= len(text) - pattern_len + 1:
                            print(f"  Найдено вхождение части шаблона '{node.name}' (начало шаблона на позиции {start})")
                            match_count[start] += 1
                node = node.exit_link
                if node is None:
                    break
        result = []
        for i in range(1, len(text) + 1):
            if match_count[i] == count_word:
                result.append(i)
        return result



trie = Trie()
text = input()
pattern = input()
wildcard = input()
forbidden = input()
parts = pattern.split(wildcard)
pos = 0
count_word = 0
result = []
print("Добавляем части шаблона в бор:")
for i in range(len(parts)):
    part = parts[i]
    if part:
        print(f"\nДобавляем в бор часть шаблона '{part}' со смещением {pos}")
        trie.add_word(part, pos)
        count_word += 1
    pos += len(part) + 1
trie.create_links()
res = trie.aho_corasick(text, len(pattern), count_word)
print("\nПроверяем позиции на запрещённый символ:")
for start in res:
    flag = True
    for wildcard_pos in range(len(pattern)):
        if pattern[wildcard_pos] == wildcard:
            if text[start - 1 + wildcard_pos] == forbidden:
                print(f"  Позиция {start}: найден запрещённый символ '{forbidden}' на смещении {wildcard_pos}, пропускаем")
                flag = False
                break
    if flag:
        print(f"  Позиция {start}: проверка пройдена")
        result.append(start)
print("\nРезультат:")
for i in result:
    print(i)

