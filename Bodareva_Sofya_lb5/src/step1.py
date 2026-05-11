from collections import deque

class Node:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.is_terminal = False
        self.suff_link = None
        self.exit_link = None
        self.pattern_nums = []
        self.pattern_len = 0


class Trie:
    def __init__(self):
        self.root = Node('')


    def add_word(self, word: str, word_num: int) -> None:
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
        current.pattern_nums.append(word_num)

    
    def create_links(self) -> None:
        print("\nСоздаем суффиксные и конечные ссылки:")
        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                print(f"\nОбрабатываем узел  '{child.name}'")
                link = current.suff_link
                while link is not None and char not in link.children:
                    output_name = link.name if link.name else 'root'
                    print(f"Символ '{char}' не найден в '{output_name}', поднимаемся выше")
                    link = link.suff_link
                child.suff_link = link.children[char] if link else self.root
                if child.suff_link is child:
                    child.suff_link = self.root
                
                suff_name = child.suff_link.name if child.suff_link.name else 'root'
                print(f"Суффиксная ссылка -> '{suff_name}'")
                
                if child.suff_link.is_terminal:
                    child.exit_link = child.suff_link
                else:
                    child.exit_link = child.suff_link.exit_link
                exit_name = child.exit_link.name if child.exit_link else "нет"
                print(f"Выходная ссылка   -> '{exit_name}'")
                queue.append(child)


    def aho_corasick(self, text: str) -> list:
        print("\nПроведем поиск вхождений подстрок в текст с помощью алгоритма Ахо-Корасик:")
        result = []
        current = self.root
        for i in range(len(text)):
            char = text[i]
            print(f"\nТекущий обрабатываемый символ текста '{char}' (позиция в тексте {i+1})")
            while current is not self.root and char not in current.children:
                print(f"Символа '{char}' нет в узле '{current.name}', переходим по суффиксной ссылке")
                current = current.suff_link
            if char in current.children:
                current = current.children[char]
                print(f"Переходим в узел '{current.name}'")
            else:
                print(f"Символ '{char}' не найден, остаёмся в root")
            node = current
            while node is not self.root:
                if node.is_terminal:
                    pos = i - node.pattern_len + 2
                    for num in node.pattern_nums:
                        print(f"Найдено вхождение шаблона №{num} на позиции {pos}")
                        result.append((pos, num))
                node = node.exit_link
                if node is None:
                    break
        result.sort()
        return result




trie = Trie()
text = input()
n = int(input())
words = []
for i in range(n):
    words.append(input())
print("Добавляем введённые слова в бор:")
for i in range(len(words)):
    print(f"\nДобавляем в бор слово '{words[i]}' под номером {i+1}")
    trie.add_word(words[i], i+1)
trie.create_links()
res = trie.aho_corasick(text)
print("\nРезультат:")
for i in res:
    print(i[0], i[1])
