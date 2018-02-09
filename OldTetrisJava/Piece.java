/**
 * Created by Patrick on 7/5/17.
 */
public class Piece {
    private BoardCoord[] coords;
    private BoardCoordDouble origin;

    private int type;

    private int bottomBoundary;
    private BoardCoord[] dropLoc;
    public boolean dropped=false;

    public Piece(BoardCoord[] coordinates, int this_type) {
        coords = coordinates;
        type = this_type;
        determineBoundaries();

    }

    private void determineBoundaries() {

        int pieceMinHeight = Integer.MAX_VALUE;
        for (int i = 0; i < this.length(); i++) {
            if (coords[i].row < pieceMinHeight) {
                pieceMinHeight = coords[i].row;
            }
        }
        bottomBoundary = pieceMinHeight;
    }

    public BoardCoord[] getCoords() {
        return coords;
    }

    public int length() {
        if (coords == null) {
            return 0;

        }
        return coords.length;
    }

    public int getBottomBoundary() {
        return bottomBoundary;
    }
    public void updateCoords(BoardCoord[] newCoords) {
        coords = newCoords;
    }

    public int getType() {
        return type;
    }



    public boolean turnClockwise(int[][] board,int colShift) {
        BoardCoord[] tempCoord = new BoardCoord[this.length()];
        for (int i = 0; i < this.length(); i++) {
            double x = coords[i].row;
            double y = coords[i].col;
            x -= origin.row;
            y -= origin.col;
            double temp = x;
            x = -1 * y;
            y = temp;
            x += origin.row;
            y += origin.col+colShift;

            tempCoord[i] = new BoardCoord(0, 0);
            tempCoord[i].row = (int) x;
            tempCoord[i].col = (int) y;
            if(colShift==0){
                if(tempCoord[i].col < 0){
                   boolean flag =turnClockwise(board,1);
                   if(!flag && type==6) {
                       turnClockwise(board,2);
                   }
                   return false;
                }else if(tempCoord[i].col> board[0].length - 1){
                    boolean flag = turnClockwise(board,-1);
                    if(!flag && type==6) {
                        turnClockwise(board,-2);
                    }
                    return false;
                }
            }
            if(tempCoord[i].row<=board.length-1) {
                if (tempCoord[i].row < 0 || tempCoord[i].col < 0 || tempCoord[i].col > board[0].length - 1 || board[tempCoord[i].row][tempCoord[i].col] != 0) {

                    return false;
                }
            }
        }
        coords = tempCoord;
        determineBoundaries();
        origin.col+=colShift;
        return true;
    }

    public boolean turnCounterClockwise(int[][] board,int colShift) {
        BoardCoord[] tempCoord = new BoardCoord[this.length()];
        for (int i = 0; i < this.length(); i++) {
            double x = coords[i].row;
            double y = coords[i].col;
            x -= origin.row;
            y -= origin.col;
            double temp = x;
            x = y;
            y = -1*temp;
            x += origin.row;
            y += origin.col+colShift;
            tempCoord[i] = new BoardCoord(0, 0);
            tempCoord[i].row = (int) x;
            tempCoord[i].col = (int) y;
            if(colShift==0){
                if(tempCoord[i].col < 0){
                    boolean flag =turnCounterClockwise(board,1);
                    if(!flag && type==6) {
                        turnCounterClockwise(board,2);
                    }
                    return false;
                }else if(tempCoord[i].col> board[0].length - 1){
                    boolean flag = turnCounterClockwise(board,-1);
                    if(!flag && type==6) {
                        turnCounterClockwise(board,-2);
                    }
                    return false;
                }
            }
            if(tempCoord[i].row<=board.length-1) {
                if (tempCoord[i].row < 0 || tempCoord[i].col < 0 || tempCoord[i].col > board[0].length - 1 || board[tempCoord[i].row][tempCoord[i].col] != 0) {

                    return false;
                }
            }
        }
        coords = tempCoord;
        determineBoundaries();
        origin.col+=colShift;
        return true;
    }


    public boolean checkPieceAtDropLoc() {


        for (int i = 0; i < length(); i++) {
            if (dropLoc[i].row != coords[i].row || dropLoc[i].col != coords[i].col) {
                return false;
            }
        }
        return true;
    }

    public void setDropLoc(BoardCoord[] thisDropLoc) {
        dropLoc = thisDropLoc;
    }


    public void moveDown(int[][] board) {
        BoardCoord[] tempCoord=new BoardCoord[length()];
        for (int i = 0; i < this.length(); i++) {
            tempCoord[i]=new BoardCoord(0,0);
            tempCoord[i].row=coords[i].row-1;
            tempCoord[i].col=coords[i].col;
            if(tempCoord[i].row<=board.length-1){
                if (tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1||board[tempCoord[i].row][tempCoord[i].col]!=0) {
                    return;
                }
            }else if(tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1){
                return;
            }

        }
        coords=tempCoord;
        bottomBoundary--;
        origin = new BoardCoordDouble(origin.row - 1, origin.col);
    }

    public void moveLeft(int[][] board) {

            BoardCoord[] tempCoord=new BoardCoord[length()];
            for (int i = 0; i < this.length(); i++) {
                tempCoord[i]=new BoardCoord(0,0);
                tempCoord[i].row=coords[i].row ;
                tempCoord[i].col=coords[i].col-1;

                if(tempCoord[i].row<=board.length-1){
                    if (tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1||board[tempCoord[i].row][tempCoord[i].col]!=0) {
                        return;
                    }
                }else if(tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1){
                    return;
                }

            }
           coords=tempCoord;
            this.origin = new BoardCoordDouble(origin.row, origin.col - 1);

    }

    public void moveRight(int[][] board) {

        BoardCoord[] tempCoord=new BoardCoord[length()];
        for (int i = 0; i < this.length(); i++) {
            tempCoord[i]=new BoardCoord(0,0);
            tempCoord[i].row=coords[i].row ;
            tempCoord[i].col=coords[i].col+1;

            if(tempCoord[i].row<=board.length-1){
                if (tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1||board[tempCoord[i].row][tempCoord[i].col]!=0) {
                    return;
                }
            }else if(tempCoord[i].row<0||tempCoord[i].col<0||tempCoord[i].col>board[0].length-1){
                return;
            }
        }
        coords=tempCoord;
        this.origin = new BoardCoordDouble(origin.row, origin.col + 1);

    }


    public BoardCoord[] getDropLoc() {
        return dropLoc;
    }

    public void setOrigin(BoardCoordDouble orig) {
        origin = orig;
    }
    public BoardCoordDouble getOrigin(){
        return origin;
    }
}
