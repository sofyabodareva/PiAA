#include <iostream>
#include <vector>

class Piece{
public:
    int column;
    int row;
    int pieceSize;
    Piece(int column, int row, int pieceSize):column(column), row(row), pieceSize(pieceSize){}

    friend std::ostream& operator << (std::ostream& out, const Piece& piece){
        return out << piece.column << " " << piece.row << " " << piece.pieceSize;
    }
};


class Table{
    int tableSize;
    int size;
    int scale;
    std::vector<Piece> bestSplitting;
    std::vector<Piece> currentSplitting;



    int findMinDivisor(int n){
        for(int i{2}; i< n; ++i){
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
        for (int y{row}; y <= size; ++y) {
            for (int x{column}; x <= size; ++x) {
                if (!isUsed(x, y)) {
                    int squareSize = std::min(size - x,  size - y) + 1;
                    for (const Piece& piece : currentSplitting) {
                        if (piece.row + piece.pieceSize > y && piece.column > x)
                            squareSize = std::min(squareSize, piece.column - x);
                    }
                    for (int s{squareSize}; s > 0; --s) {
                        currentSplitting.push_back(Piece(x, y, s));
                        if (filledPart + s * s == size * size) {
                            if (currentSplitting.size() < bestSplitting.size() || bestSplitting.size() == 0) {
                                bestSplitting = currentSplitting;
                            }
                        }
                        else {
                            if (currentSplitting.size() + 1 < bestSplitting.size() || bestSplitting.size() == 0) {
                                backtracking(x + s, y, filledPart + s * s);
                            }
                        }
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
        out << table.bestSplitting.size() << "\n";
        for(int i{0}; i < table.bestSplitting.size(); ++i){
            out << table.bestSplitting[i] << "\n";
        }
        return out;
    }

    void findBestSplitting(){
        if(tableSize % 2 == 0){
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
    int n;
    std::cin >> n;
    Table t(n);
    t.findBestSplitting();
    std::cout << t;
    std::cout<< t.iterations;
    return 0;
}