import java.util.ArrayList;
import java.util.List;

/**
 * Created by Patrick on 7/5/17.
 */
public class Board {
    private int[][] board;





    public Board(int numRows, int numCols) {

        board = new int[numRows][numCols];
        /**
        board[0][0]=1;
        board[0][1]=1;
        board[0][2]=1;
        board[0][3]=1;
        board[0][4]=1;
        board[0][6]=1;
        board[1][0]=1;
        board[1][1]=1;
        board[1][2]=1;
        board[1][3]=1;
        board[1][4]=1;
        board[1][6]=1;
         */
    }


    public BoardCoord[] determineDropLoc(Piece piece) {
        int pieceLength = piece.length();
        int minHeight = piece.getBottomBoundary();
        BoardCoord[] pieceCoord = piece.getCoords();
        int height = minHeight;

        thisWhile:
        while (height > 0 ) {
            height--;
            for (int i = 0; i < pieceLength; i++) {
                if (pieceCoord[i].row-minHeight+height<board.length&&pieceCoord[i].row-minHeight+height>=0) {
                    if (board[pieceCoord[i].row -minHeight+ height][pieceCoord[i].col] != 0) {
                        height++;
                        break thisWhile;
                    }
                }
            }

        }

        BoardCoord[] dropLoc = new BoardCoord[pieceLength];
        for (int i = 0; i < pieceLength; i++) {
            dropLoc[i] = new BoardCoord(height + pieceCoord[i].row - minHeight, pieceCoord[i].col);
           // System.out.println(dropLoc[i].row + " " + dropLoc[i].col);
        }
        return dropLoc;
    }

    public int dropPiece(Piece piece) {
        int scoreDiff=-1;
        if(piece.dropped==false) {
            piece.dropped = true;
            BoardCoord[] dropLoc = piece.getDropLoc();
            piece.updateCoords(dropLoc);
            boolean flag = updateBoard(piece);
            if(!flag){
                return -999;
            }
            if (flag) {
                scoreDiff=checkRowsForFull(piece);
            }

        }
        return scoreDiff;
    }


    public int checkRowsForFull(Piece piece){
        int[] full=new int[board.length];
        full[board.length-1]=-1;
        int total=0;
        for(int i=0;i<board.length;i++){

            full[i]=checkRow(i);
            total+=full[i];
        }
        //0 1 0 1 1 0 0 0
        //0 2 3 6 7 8 9 10
        int[] rowsToCopy = new int[board.length];
        int counter = 0;
        for(int i=0;i<board.length;i++){
            if(counter>board.length-1){
                rowsToCopy[i] = counter;
            }else {
                if (full[counter] == 0) {
                    rowsToCopy[i] = counter;
                } else {
                    int start = counter;
                    while (full[counter] == 1) {
                        counter++;
                    }
                    rowsToCopy[i] = counter;
                }

                counter++;
            }
        }
        int[][] tempBoard=new int[board.length][board[0].length];
        if(rowsToCopy[board.length-1]!=board.length-1){
            for(int i=0;i<board.length-1;i++){
                if(rowsToCopy[i]>board.length-1) {
                    tempBoard[i]=new int[board[0].length];

                }else{
                    tempBoard[i] = board[rowsToCopy[i]];
                }
            }
            board=tempBoard;
        }
        piece.setDropLoc(determineDropLoc(piece));
        return total-1;

    }

    private int checkRow(int row){
        double counter=1.0;
        for(int i=0;i<board[0].length;i++){
            counter*=board[row][i]/2.0;
        }
        if(counter!=0){
            return 1;
        }
        return 0;
    }



    public Piece lowerPiece(Piece piece) {
        if (piece.checkPieceAtDropLoc()) {
            int diff = dropPiece(piece);
            //If cleared rows, then it is the negative of the number of cleared rows
            //If game over, -999
            return new Piece(null, diff);
        } else {

            piece.moveDown(board);

            return piece;
        }
    }


    public int[][] getBoard() {
        return board;
    }

    public boolean updateBoard(Piece piece) {
        BoardCoord[] coords = piece.getCoords();
        int type = piece.getType();
        for (int i = 0; i < piece.length(); i++) {
            //if coords are out of bounds, you lose
            if(coords[i].row>=board.length-1||board[coords[i].row][coords[i].col]!=0){
                return false;
            }

        }
        for (int i = 0; i < piece.length(); i++) {

            board[coords[i].row][coords[i].col] = type+1;
        }
        return true;
    }
}
