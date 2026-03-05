#include <iostream>
#include <vector>
#include <windows.h>

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
        std::cout << "Вход в функцию backtracking №" << iterations <<
        "\nКоординаты начала поиска: (" << column << ", " << row
        << ")\nПлощадь заполненной части: " << filledPart
        << "\nКоличество квадратов в текущем разбиении: " << currentSplitting.size() << "\n";
        for (int y{row}; y <= size; ++y) {
            for (int x{column}; x <= size; ++x) {
                if (!isUsed(x, y)) {
                    std::cout << "Координаты вставки нового квадрата: (" << column
                    << ", " << row << ")\n";
                    int squareSize = std::min(size - x,  size - y) + 1;
                    for (const Piece& piece : currentSplitting) {
                        if (piece.row + piece.pieceSize > y && piece.column > x)
                            squareSize = std::min(squareSize, piece.column - x);
                    }
                    std::cout << "Максимальный размер квадрата для вставки: " << squareSize << "\n";
                    for (int s{squareSize}; s > 0; --s) {
                        currentSplitting.push_back(Piece(x, y, s));
                        std::cout << "Добавляем в разбиение квадрат: (" << x << ", "
                        << y << ") " << s << "\n";
                        if (filledPart + s * s == size * size) {
                            if (currentSplitting.size() < bestSplitting.size() || bestSplitting.size() == 0) {
                                bestSplitting = currentSplitting;
                                std::cout << "Текущий размер лучшего разбиения: " << currentSplitting.size() << "\n";
                            }
                        }
                        else {
                            if (currentSplitting.size() + 1 < bestSplitting.size() || bestSplitting.size() == 0) {
                                backtracking(x + s, y, filledPart + s * s);
                            }
                        }
                        std::cout << "Возвращаемся назад - удаляем последний квадрат: (" 
                        << x << ", " << y << ") " << s << "\n";
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
            std::cout << "Сторона стола - чётное число, лучшее разбиение - 4 равных квадрата\n";
            bestSplitting.push_back(Piece(1, 1, tableSize/2));
            bestSplitting.push_back(Piece(tableSize/2+1, 1, tableSize/2));
            bestSplitting.push_back(Piece(1, tableSize/2+1, tableSize/2));
            bestSplitting.push_back(Piece(tableSize/2+1, tableSize/2+1, tableSize/2));
        }
        else{
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
    t.findBestSplitting();
    std::cout<< "Количество итераций: " << t.iterations << "\n";
    std::cout << t;
    return 0;
}