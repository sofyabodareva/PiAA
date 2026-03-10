#include <iostream>
#include <vector>
#include <string>
#include <windows.h>
#include <chrono>

class Piece{
public:
    int column;
    int row;
    int pieceSize;
    Piece(int column, int row, int pieceSize):column(column), row(row), pieceSize(pieceSize){}

    friend std::ostream& operator << (std::ostream& out, const Piece& piece){
        return out << "(" << piece.column << ", " << piece.row << ") " << piece.pieceSize;
    }
};


class Table{
    int tableSize;
    int size;
    int scale;
    std::vector<Piece> bestSplitting;
    std::vector<Piece> currentSplitting;




    int findMinDivisor(int n){
        for(int i{3}; i< n; i+=2){
            if(n % i == 0){
                return i;
            }
        }
        return n;
    }

    bool isUsed(int column, int row){
        for(const Piece& piece : currentSplitting){
            if((row >= piece.row) && (row < piece.row + piece.pieceSize) && (column >= piece.column) && (column < piece.column + piece.pieceSize))
                return true;
        }
        return false;
    }

    void backtracking(int column, int row, int filledPart) {
        ++iterations;
        log.push_back("\nВход в функцию backtracking №" + std::to_string(iterations)
        + "\nКоординаты начала поиска: (" + std::to_string(column) + ", " + std::to_string(row)
        + ")\nПлощадь заполненной части: " + std::to_string(filledPart) 
        + "\nКоличество квадратов в текущем разбиении: " + std::to_string(currentSplitting.size()));
        for (int y{row}; y <= size; ++y) {
            for (int x{column}; x <= size; ++x) {
                log.push_back("Проверяем, можно ли вставить квадрат в точку (" + std::to_string(x) +
                ", " + std::to_string(y) + ")");
                if (!isUsed(x, y)) {
                    log.push_back("Координаты вставки нового квадрата: (" + std::to_string(x)+
                    ", " + std::to_string(y) + ")");
                    int squareSize = std::min(size - x,  size - y) + 1;
                    for (const Piece& piece : currentSplitting) {
                        if (piece.row + piece.pieceSize > y && piece.column > x)
                            squareSize = std::min(squareSize, piece.column - x);
                    }
                    log.push_back("Максимальный размер квадрата для вставки: " + std::to_string(squareSize));
                    for (int s{squareSize}; s > 0; --s) {
                        currentSplitting.push_back(Piece(x, y, s));
                        log.push_back("Добавляем в разбиение квадрат: (" + std::to_string(x) + ", "
                        + std::to_string(y) + ") " + std::to_string(s));
                        if (filledPart + s * s == size * size) {
                            if (currentSplitting.size() < bestSplitting.size() || bestSplitting.size() == 0) {
                                bestSplitting = currentSplitting;
                                log.push_back("Текущий размер лучшего разбиения: " + std::to_string(currentSplitting.size()));
                            }
                        }
                        else {
                            if (currentSplitting.size() + 1 < bestSplitting.size() || bestSplitting.size() == 0) {
                                backtracking(x + s, y, filledPart + s * s);
                            }
                        }
                        log.push_back("Возвращаемся назад - удаляем последний квадрат: (" + std::to_string(x)
                        + ", " + std::to_string(y) + ") " + std::to_string(s));
                        currentSplitting.pop_back();
                    }
                    return;
                }
            }
            column = (size + 1) / 2;
        }
    }

    void scaling(){
        for (Piece& piece : bestSplitting){
            piece.column = (piece.column-1) * scale + 1;
            piece.row = (piece.row-1) * scale + 1;
            piece.pieceSize = piece.pieceSize * scale;
        }
    }

public:
    int iterations;
    std::vector<std::string> log;

    Table(int tableSize):tableSize(tableSize), size(findMinDivisor(tableSize)), scale(tableSize/size), iterations(0){}

    friend std::ostream& operator << (std::ostream& out, const Table& table){
        out << "Минимальное количество квадратов: " << table.bestSplitting.size() << "\n";
        out << "Координаты левых верхних углов использованных квадратов и длины их сторон:\n";
        for(int i{0}; i < table.bestSplitting.size(); ++i){
            out << table.bestSplitting[i] << "\n";
        }
        return out;
    }

    void findBestSplitting(){
        if(tableSize % 2 == 0){
            log.push_back("Сторона стола - чётное число, лучшее разбиение - 4 равных квадрата\n");
            bestSplitting.push_back(Piece(1, 1, tableSize/2));
            bestSplitting.push_back(Piece(tableSize/2+1, 1, tableSize/2));
            bestSplitting.push_back(Piece(1, tableSize/2+1, tableSize/2));
            bestSplitting.push_back(Piece(tableSize/2+1, tableSize/2+1, tableSize/2));
        }
        else{
            log.push_back("Масштаб: " + std::to_string(scale) + "\nРазмер стола для перебора: "
            + std::to_string(tableSize/scale) + "\n");
            currentSplitting.push_back(Piece(1, 1, (size+1)/2));
            currentSplitting.push_back(Piece((size+1)/2+1, 1, (size-1)/2));
            currentSplitting.push_back(Piece(1, (size+1)/2+1, (size-1)/2));
            backtracking((size+1)/2, (size+1)/2, 0.25*(3*size*size-2*size+3));
            scaling();
        }
    }

};


int main(){
    SetConsoleOutputCP(CP_UTF8);
    int n;
    std::cin >> n;
    Table t(n);
    //auto start = std::chrono::steady_clock::now();
    t.findBestSplitting();
    //auto end = std::chrono::steady_clock::now();
    std::cout<< "Количество итераций: " << t.iterations << "\n";
    for(const auto& line : t.log)
        std::cout << line << "\n";
    std::cout << t;
    //std::chrono::duration<double> diff = end - start;
    //std::cout << diff.count();
    return 0;
}