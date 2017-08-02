import javax.swing.*;
import java.awt.Toolkit;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Dimension;
import java.awt.RenderingHints;
import java.awt.Font;
import java.awt.Polygon;


import java.util.Collections;
import java.awt.image.BufferedImage;
import java.util.Queue;
import java.util.ArrayList;
import java.util.TimerTask;
import java.util.LinkedList;
/**
 * Created by Patrick on 7/5/17.
 */

public class TetrisBuilder extends JPanel {

    private BufferedImage background;
    Toolkit toolkit;
    java.util.Timer timer;
    public int windowWidth = 800;
    public int windowHeight = 800;
    private int speed = 50;
    public static int numRows = 20;
    public static int numCols = 10;
    public int numPieces = 7;
    public int pieceSize = 4;
    public int queueSize = 5;

    private Piece currPiece;
    private int[][] boardVals;
    private Board board;
    private RemindTask reminder;
    private Queue<Integer> pieceQueue;
    private boolean gameOver = false;
    private int score = 0;
    private BoardCoord[][] pieceCoords;
    private Color[] pieceColors;
    private BoardCoordDouble[] pieceOrigin;
    private boolean showOrigin = false;
    private int heldPiece = -1;
    private boolean keyDown = false;
    private int[] pieceCounter = new int[numPieces];

    private TetrisFrame tf;
    private int keyDelay = 1;
    private int downDelay = 1;
    private int upDelay = 3;
    private ArrayList<Integer> bagOfPieces;
    private long startTime;
    private int droppedCounter = 0;
    private int droppedDelay = 2;
    private int pointsPerLine=100;
    private boolean justDropped = false;
    private int minSpeed = 20;
    private int pointsToReachMidpoint=10000;

    private int comboCounter =-1;//thank you nintendo !
    public void drawGrid(Graphics2D g2) {
        Color gray = new Color(200, 200, 200);
        g2.setColor(gray);
        int topLeftX = 250;
        int topLeftY = 100;
        int squareWidth = 30;

        g2.fillRect(topLeftX, topLeftY, squareWidth * numCols, squareWidth * numRows);
        g2.setColor(Color.BLACK);
        for (int i = 0; i < numCols + 1; i++) {
            g2.drawLine(i * squareWidth + topLeftX, topLeftY, i * squareWidth + topLeftX, topLeftY + numRows * squareWidth);
        }
        for (int j = 0; j < numRows + 1; j++) {
            g2.drawLine(topLeftX, topLeftY + j * squareWidth, numCols * squareWidth + topLeftX, topLeftY + j * squareWidth);
        }


        //Draw Board
        for (int i = 0; i < numCols; i++) {
            for (int j = 0; j < numRows; j++) {
                if (boardVals[j][i] != 0) {
                    drawBlock(g2, i * squareWidth + topLeftX + 1, (19 - j) * squareWidth + topLeftY + 1, squareWidth - 2, pieceColors[boardVals[j][i] - 1]);
                }
            }
        }

        Color darkGray = new Color(100, 100, 100);
        g2.setColor(darkGray);

        //Color Drop Loc
        BoardCoord[] dropLoc = currPiece.getDropLoc();
        for (int i = 0; i < currPiece.length(); i++) {
            int row = dropLoc[i].row;
            int col = dropLoc[i].col;
            if (row < numRows && col < numCols) {
                int x = col * squareWidth + topLeftX + 2;
                int y = (19 - row) * squareWidth + topLeftY + 2;
                //drawBlock(g2,x,y,squareWidth-2,darkGray);
                g2.setColor(gray);
                g2.fillRect(x - 1, y - 1, squareWidth - 2, squareWidth - 2);
                g2.setColor(darkGray);
                g2.fillRect(x, y, squareWidth - 4, squareWidth - 4);
            }

        }

        //Color Current Piece
        BoardCoord[] pieceCoord = currPiece.getCoords();
        for (int i = 0; i < currPiece.length(); i++) {
            int row = pieceCoord[i].row;
            int col = pieceCoord[i].col;
            if (row < numRows && col < numCols) {
                int x = col * squareWidth + topLeftX + 1;
                int y = (19 - row) * squareWidth + topLeftY + 1;
                drawBlock(g2, x, y, squareWidth - 2, pieceColors[currPiece.getType()]);
            }
        }

        //Color Origin
        BoardCoordDouble origin = currPiece.getOrigin();
        if (showOrigin) {
            g2.setColor(Color.BLACK);

            double row = origin.row;
            double col = origin.col;
            double x = col * squareWidth + topLeftX + 1;
            double y = (19 - row) * squareWidth + topLeftY + 1;
            g2.fillRect((int) x, (int) y, squareWidth - 2, squareWidth - 2);
        }


        //Queue Section
        int topLeftQueueX = 600;
        int topLeftQueueY = 150;
        int queueWidth = 150;
        int queueHeight = 500;
        int queueRectangleDistanceApart = (int) queueHeight / ((queueSize + 1) * queueSize);
        int queueRectangleHeight = queueRectangleDistanceApart * queueSize;
        //origin is at topLeftQueueX+queueWidth/2

        BoardCoord[] queueCoord;
        for (int i = 0; i < queueSize; i++) {
            int queueType = pieceQueue.remove();
            pieceQueue.add(queueType);
            origin = pieceOrigin[queueType];
            queueCoord = pieceCoords[queueType];
            if (i == 0) {
                g2.setColor(gray);
                g2.fillRect(topLeftQueueX, topLeftQueueY, queueWidth, queueRectangleHeight);
                for (int j = 0; j < pieceSize; j++) {
                    int pieceX = (int) ((queueCoord[j].col - origin.col) * squareWidth + topLeftQueueX + queueWidth / 2 - squareWidth / 2);
                    int pieceY;
                    if (queueType == 2) {
                        pieceY = (int) (topLeftQueueY - squareWidth * (queueCoord[j].row * 1.0 - origin.row * 1.0) - squareWidth / 2 + queueRectangleHeight / 2);
                    } else {
                        pieceY = (int) (topLeftQueueY - squareWidth * (queueCoord[j].row * 1.0 - origin.row * 1.0) + queueRectangleHeight / 2);
                    }
                    drawBlock(g2, pieceX, pieceY, squareWidth, pieceColors[queueType]);
                }


            } else {
                g2.setColor(gray);
                g2.fillRect(topLeftQueueX, topLeftQueueY + i * queueRectangleHeight + (i) * queueRectangleDistanceApart, queueWidth, queueRectangleHeight);
                for (int j = 0; j < pieceSize; j++) {
                    int pieceX = (int) ((queueCoord[j].col * 1.0 - origin.col * 1.0) * squareWidth + topLeftQueueX + queueWidth / 2 - squareWidth / 2);
                    int pieceY;
                    if (queueType == 2) {
                        pieceY = (int) (-squareWidth * (queueCoord[j].row * 1.0 - origin.row * 1.0) + queueRectangleHeight / 2 - squareWidth / 2.0 + topLeftQueueY + i * queueRectangleHeight + (i) * queueRectangleDistanceApart);
                    } else {
                        pieceY = (int) (-squareWidth * (queueCoord[j].row * 1.0 - origin.row * 1.0) + queueRectangleHeight / 2 + topLeftQueueY + i * queueRectangleHeight + (i) * queueRectangleDistanceApart);
                    }
                    drawBlock(g2, pieceX, pieceY, squareWidth, pieceColors[queueType]);
                }

            }
        }


        g2.setColor(Color.BLACK);
        g2.setFont(new Font("ComicSans", Font.PLAIN, 25));
        g2.drawString("SCORE: " + score, 40, 150);

        //Color hold
        int topLeftHoldX = 50;
        int topLeftHoldY = 200;
        int holdWidth = 150;
        int holdHeight = 150;
        g2.setColor(gray);
        g2.fillRect(topLeftHoldX, topLeftHoldY, holdWidth, holdHeight);
        g2.setColor(Color.BLACK);
        g2.drawString("HOLD", 90, 225);

        if (heldPiece != -1) {
            for (int j = 0; j < pieceSize; j++) {
                int tempType = heldPiece;
                if (tempType >= 100) {
                    tempType -= 100;
                }
                queueCoord = pieceCoords[tempType];
                origin = pieceOrigin[tempType];

                int pieceX = (int) ((queueCoord[j].col - origin.col) * squareWidth + topLeftHoldX + holdWidth / 2 - squareWidth / 2);
                int pieceY = (int) (topLeftHoldY + squareWidth * (queueCoord[j].row - origin.row) + holdHeight / 2 - squareWidth);
                drawBlock(g2, pieceX, pieceY, squareWidth, pieceColors[tempType]);
            }
        }

        //Game Over Condition
        if (gameOver) {

            g2.setColor(Color.RED);
            g2.drawString("Game Over", 300, 730);
            g2.drawString("Final Score: " + score, 300, 760);
            for (int i = 0; i < numPieces; i++) {
                System.out.print(pieceCounter[i] + " ");
            }
            tf.resetGame();
        }

    }

    public Piece nextPiece(boolean valid) {

        if(valid){
            comboCounter++;
        }else{
            comboCounter=-1;
        }
        droppedCounter = 0;
        int type = pieceQueue.remove();
        pieceQueue.add(bagOfPieces.remove(0));
        Piece piece = generatePiece(type);
        if (bagOfPieces.size() == 0) {
            refillBag();
        }
        //type = (int) Math.floor(Math.random() * ((numPieces) - 1)) + 1;
        pieceCounter[type] += 1;
        return piece;
    }


    public Piece generatePiece(int type) {

        BoardCoord[] coords = pieceCoords[type];
        BoardCoordDouble origin = pieceOrigin[type];
        Piece piece = new Piece(coords, type);
        piece.dropped = false;
        piece.setOrigin(origin);
        BoardCoord[] dropLoc = board.determineDropLoc(piece);
        piece.setDropLoc(dropLoc);
        return piece;
    }


    class RemindTask extends TimerTask {

        Piece piece;
        int modulo = 1;


        public RemindTask(Piece currPiece) {
            piece = currPiece;
        }

        public void run() {

            modulo++;
            if (tf.left > keyDelay) {
                leftArrow();
                tf.left = 1;
            } else if (tf.left > 0) {
                tf.left++;
            }
            if (tf.right > keyDelay) {
                rightArrow();
                tf.right = 1;
            } else if (tf.right > 0) {
                tf.right++;
            }
            if (tf.down > downDelay) {
                downArrow();
                tf.down = 1;
            } else if (tf.down > 0) {
                tf.down++;
            }
            if (tf.xCounter > upDelay) {
                upArrowAndXButton();
                tf.xCounter = 1;
            } else if (tf.xCounter > 0) {
                tf.xCounter++;

            }
            if (tf.zCounter > upDelay) {
                zButton();
                tf.zCounter = 1;
            } else if (tf.zCounter > 0) {
                tf.zCounter++;

            }

            piece = currPiece;
            int scoreCounter=0;
            int speed=speedCalculation();

            if (speed==0 || modulo % speedCalculation() == 0) {

                if (justDropped&&droppedCounter==0) {
                    justDropped = false;
                    currPiece.setDropLoc(board.determineDropLoc(currPiece));
                }

                if ( droppedCounter > 0 && droppedCounter < droppedDelay) {
                    droppedCounter++;

                } else {
                    droppedCounter=0;
                    Piece dropped = board.lowerPiece(piece);

                    if (dropped.getType() == -999) {
                        System.out.println("modulo: " + modulo);
                        endTimer();


                        return;


                    } else if (dropped.getType() < 0) {

                        int lineDiff = board.dropPiece(currPiece);
                        if(lineDiff!=-1) {
                            scoreCounter+=lineClearCalc(lineDiff + 1);
                        }
                        piece = nextPiece(true);

                        if(comboCounter>0) {
                            scoreCounter += comboCounter * 0.5 * pointsPerLine;
                        }
                        incrementScore(scoreCounter);
                        if (heldPiece >= 100) {
                            heldPiece -= 100;
                        }
                    }
                    boardVals = board.getBoard();
                    currPiece = piece;
                }

            }
            repaint();
        }
        public int getModulo(){
            return modulo;
        }
    }
    public void spaceButton() {

        BoardCoord[] dropLoc = board.determineDropLoc(currPiece);
        BoardCoord[] currPieceCoords = currPiece.getCoords();
        int scoreCounter=2*(currPieceCoords[0].row- dropLoc[0].row);
        currPiece.setDropLoc(dropLoc);
        int lineDiff = board.dropPiece(currPiece);
        if (lineDiff == -999) {
            //tf.resetGame();
            endTimer();
        } else {

            if(comboCounter>0) {
                scoreCounter += comboCounter * 0.5 * pointsPerLine;
            }

            Piece nextPieceToPlace;
            if (lineDiff == -1) {
                nextPieceToPlace = nextPiece(false);
                currPiece.setDropLoc(board.determineDropLoc(currPiece));
            }else{
                scoreCounter+=lineClearCalc(lineDiff + 1);
                nextPieceToPlace = nextPiece(true);
                justDropped = true;
                droppedCounter=droppedDelay;
            }
            incrementScore(scoreCounter);
            if (heldPiece >= 100) {
                heldPiece -= 100;
            }
            currPiece = nextPieceToPlace;
        }


    }

    public int lineClearCalc(int linesCleared){

                int score = (int) (Math.pow(linesCleared,3)/6.0-Math.pow(linesCleared,2)+23*linesCleared/6.0-2);
                return score*pointsPerLine;
    }

    public void leftArrow() {
        //System.out.println("left");
        if (currPiece.checkPieceAtDropLoc() && droppedCounter == 0) {
            droppedCounter = 1;
        }
        currPiece.moveLeft(boardVals);
        BoardCoord[] dropLoc = board.determineDropLoc(currPiece);
        currPiece.setDropLoc(dropLoc);
    }

    public void rightArrow() {
        //System.out.println("right");
        if (currPiece.checkPieceAtDropLoc() && droppedCounter == 0) {
            droppedCounter = 1;
        }
        currPiece.moveRight(boardVals);
        BoardCoord[] dropLoc = board.determineDropLoc(currPiece);
        currPiece.setDropLoc(dropLoc);
    }

    public void upArrowAndXButton() {

        if (currPiece.checkPieceAtDropLoc() && droppedCounter == 0) {
            droppedCounter = 1;
        }
        currPiece.turnClockwise(boardVals, 0);
        BoardCoord[] dropLoc = board.determineDropLoc(currPiece);
        currPiece.setDropLoc(dropLoc);
    }

    public void downArrow() {



        Piece dropped = board.lowerPiece(currPiece);
        if(dropped.getType()>0) {
            incrementScore(1);
        }

        boardVals = board.getBoard();
        keyDown = true;
    }

    public void zButton() {
        if (currPiece.checkPieceAtDropLoc() && droppedCounter == 0) {
            droppedCounter = 1;
        }
        currPiece.turnCounterClockwise(boardVals,0);
        BoardCoord[] dropLoc = board.determineDropLoc(currPiece);
        currPiece.setDropLoc(dropLoc);
    }

    public void shiftButton() {
        if (heldPiece == -1) {
            heldPiece = currPiece.getType();
            currPiece = nextPiece(false);
            heldPiece += 100;
        } else if (heldPiece < 100) {
            int tempType = heldPiece;
            heldPiece = currPiece.getType();
            currPiece = generatePiece(tempType);
            heldPiece += 100;
        }
    }


    public TetrisBuilder(TetrisFrame theTF) {
        super(true);
        setFocusable(true);
        setFocusTraversalKeysEnabled(false);
        tf = theTF;

        pieceCoords = new BoardCoord[numPieces][pieceSize];
        pieceOrigin = new BoardCoordDouble[numPieces];
        //Orange L
        pieceCoords[0][0] = new BoardCoord(20, 3);
        pieceCoords[0][1] = new BoardCoord(20, 4);
        pieceCoords[0][2] = new BoardCoord(20, 5);
        pieceCoords[0][3] = new BoardCoord(21, 5);
        //Blue J
        pieceCoords[1][0] = new BoardCoord(20, 3);
        pieceCoords[1][1] = new BoardCoord(20, 4);
        pieceCoords[1][2] = new BoardCoord(20, 5);
        pieceCoords[1][3] = new BoardCoord(21, 3);
        //o Yellow
        pieceCoords[2][0] = new BoardCoord(20, 4);
        pieceCoords[2][1] = new BoardCoord(20, 5);
        pieceCoords[2][2] = new BoardCoord(21, 4);
        pieceCoords[2][3] = new BoardCoord(21, 5);
        //T Purple
        pieceCoords[3][0] = new BoardCoord(20, 3);
        pieceCoords[3][1] = new BoardCoord(20, 4);
        pieceCoords[3][2] = new BoardCoord(20, 5);
        pieceCoords[3][3] = new BoardCoord(21, 4);
        //S Green
        pieceCoords[4][0] = new BoardCoord(20, 3);
        pieceCoords[4][1] = new BoardCoord(20, 4);
        pieceCoords[4][2] = new BoardCoord(21, 4);
        pieceCoords[4][3] = new BoardCoord(21, 5);
        //Z Red
        pieceCoords[5][0] = new BoardCoord(20, 5);
        pieceCoords[5][1] = new BoardCoord(20, 4);
        pieceCoords[5][2] = new BoardCoord(21, 4);
        pieceCoords[5][3] = new BoardCoord(21, 3);
        //I Light Blue
        pieceCoords[6][0] = new BoardCoord(20, 6);
        pieceCoords[6][1] = new BoardCoord(20, 5);
        pieceCoords[6][2] = new BoardCoord(20, 4);
        pieceCoords[6][3] = new BoardCoord(20, 3);

        pieceOrigin[0] = new BoardCoordDouble(20.0, 4.0);
        pieceOrigin[1] = new BoardCoordDouble(20.0, 4.0);
        pieceOrigin[2] = new BoardCoordDouble(20.5, 4.5);
        pieceOrigin[3] = new BoardCoordDouble(20.0, 4.0);
        pieceOrigin[4] = new BoardCoordDouble(20.0, 4.0);
        pieceOrigin[5] = new BoardCoordDouble(20.0, 4.0);
        pieceOrigin[6] = new BoardCoordDouble(19.5, 4.5);
        /**
        pieceCoords[0][0] = new BoardCoord(19, 3);
        pieceCoords[0][1] = new BoardCoord(19, 4);
        pieceCoords[0][2] = new BoardCoord(19, 5);
        pieceCoords[0][3] = new BoardCoord(20, 5);
        //Blue J
        pieceCoords[1][0] = new BoardCoord(19, 3);
        pieceCoords[1][1] = new BoardCoord(19, 4);
        pieceCoords[1][2] = new BoardCoord(19, 5);
        pieceCoords[1][3] = new BoardCoord(20, 3);
        //o Yellow
        pieceCoords[2][0] = new BoardCoord(19, 4);
        pieceCoords[2][1] = new BoardCoord(19, 5);
        pieceCoords[2][2] = new BoardCoord(20, 4);
        pieceCoords[2][3] = new BoardCoord(20, 5);
        //T Purple
        pieceCoords[3][0] = new BoardCoord(19, 3);
        pieceCoords[3][1] = new BoardCoord(19, 4);
        pieceCoords[3][2] = new BoardCoord(19, 5);
        pieceCoords[3][3] = new BoardCoord(20, 4);
        //S Green
        pieceCoords[4][0] = new BoardCoord(19, 3);
        pieceCoords[4][1] = new BoardCoord(19, 4);
        pieceCoords[4][2] = new BoardCoord(20, 4);
        pieceCoords[4][3] = new BoardCoord(20, 5);
        //Z Red
        pieceCoords[5][0] = new BoardCoord(19, 5);
        pieceCoords[5][1] = new BoardCoord(19, 4);
        pieceCoords[5][2] = new BoardCoord(20, 4);
        pieceCoords[5][3] = new BoardCoord(20, 3);
        //I Light Blue
        pieceCoords[6][0] = new BoardCoord(19, 6);
        pieceCoords[6][1] = new BoardCoord(19, 5);
        pieceCoords[6][2] = new BoardCoord(19, 4);
        pieceCoords[6][3] = new BoardCoord(19, 3);

        pieceOrigin[0] = new BoardCoordDouble(19.0, 4.0);
        pieceOrigin[1] = new BoardCoordDouble(19.0, 4.0);
        pieceOrigin[2] = new BoardCoordDouble(19.5, 4.5);
        pieceOrigin[3] = new BoardCoordDouble(19.0, 4.0);
        pieceOrigin[4] = new BoardCoordDouble(19.0, 4.0);
        pieceOrigin[5] = new BoardCoordDouble(19.0, 4.0);
        pieceOrigin[6] = new BoardCoordDouble(18.5, 4.5);
*/
        pieceColors = new Color[numPieces];
        pieceColors[0] = new Color(234, 143, 10);
        pieceColors[1] = new Color(0, 0, 236);
        pieceColors[2] = new Color(237, 240, 11);
        pieceColors[3] = new Color(139, 0, 235);
        pieceColors[4] = new Color(32, 244, 9);
        pieceColors[5] = new Color(233, 0, 0);
        pieceColors[6] = new Color(30, 239, 236);
        background = createBackground();
        board = new Board(numRows, numCols);
        boardVals = board.getBoard();
        bagOfPieces = new ArrayList<Integer>();
        refillBag();

        //Types go from 1 to num pieces (usually 7)
        //Lets say you picked 3 last time
        //1 2 3 4 5 6
        //1 2 4 5 6 7
        pieceQueue = new LinkedList<>();
        for (int i = 0; i < queueSize; i++) {
            int top = bagOfPieces.remove(0);
            pieceQueue.add(top);
        }

        currPiece = nextPiece(false);
        callTimer();
        startTime = System.currentTimeMillis();
    }







    private void endTimer() {
        timer.cancel();
        timer.purge();
        gameOver = true;
        repaint();
        long endTime = System.currentTimeMillis();
        long duration = (endTime - startTime);
        System.out.println("total time: " + duration);
    }
    private BufferedImage createBackground() {
        BufferedImage bg = new BufferedImage(windowWidth, windowHeight, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = bg.createGraphics();
        g2.dispose();
        return bg;
    }
    public void drawBlock(Graphics2D g2, int upperX, int upperY, int sidelength, Color color) {
        Color temp = color;
        double lightnessTint = 1.0 * 3 / 4;
        //darker 2 is darker
        double darknessShade1 = 1.0 * 5 / 6;
        double darknessShade2 = 1.0 * 1 / 2;
        Color lighter = new Color((int) ((255 - temp.getRed()) * lightnessTint + temp.getRed()), (int) ((255 - temp.getGreen()) * lightnessTint + temp.getGreen()), (int) ((255 - temp.getBlue()) * lightnessTint + temp.getBlue()));
        Color darker1 = new Color((int) (temp.getRed() * darknessShade1), (int) (temp.getGreen() * darknessShade1), (int) (temp.getBlue() * darknessShade1));
        Color darker2 = new Color((int) (temp.getRed() * darknessShade2), (int) (temp.getGreen() * darknessShade2), (int) (temp.getBlue() * darknessShade2));
        g2.setColor(color);
        g2.fillRect(upperX, upperY, sidelength, sidelength);
        int insideNWX = upperX + 5;
        int insideNWY = upperY + 5;
        int insideNEX = upperX + sidelength - 5;
        int insideNEY = upperY + 5;
        int insideSWX = upperX + 5;
        int insideSWY = upperY + sidelength - 5;
        int insideSEX = upperX + sidelength - 5;
        int insideSEY = upperY + sidelength - 5;

        int xUpperPoly[] = {upperX, upperX + sidelength,
                insideNEX, insideNWX};
        int yUpperPoly[] = {upperY, upperY,
                insideNEY, insideNWY};
        int xLeftPoly[] = {upperX, upperX,
                insideSWX, insideNWX};
        int yLeftPoly[] = {upperY, upperY + sidelength,
                insideSWY, insideNWY};
        int xRightPoly[] = {upperX + sidelength, upperX + sidelength,
                insideSEX, insideNEX};
        int yRightPoly[] = {upperY, upperY + sidelength,
                insideSEY, insideNEY};
        int xLowerPoly[] = {upperX, upperX + sidelength,
                insideSEX, insideSWX};
        int yLowerPoly[] = {upperY + sidelength, upperY + sidelength,
                insideSEY, insideSWY};

        Polygon upperTrap = new Polygon(xUpperPoly, yUpperPoly, 4);
        Polygon leftTrap = new Polygon(xLeftPoly, yLeftPoly, 4);
        Polygon rightTrap = new Polygon(xRightPoly, yRightPoly, 4);
        Polygon lowerTrap = new Polygon(xLowerPoly, yLowerPoly, 4);

        g2.setColor(lighter);
        g2.fillPolygon(upperTrap);
        g2.setColor(darker1);
        g2.fillPolygon(leftTrap);
        g2.fillPolygon(rightTrap);
        g2.setColor(darker2);
        g2.fillPolygon(lowerTrap);

    }
    @Override
    public Dimension getPreferredSize() {
        return new Dimension(windowWidth, windowHeight);
    }
    private int speedCalculation() {
        //modulo is 0
        //min speed is 15
        //max speed is 5

        long endTime = System.currentTimeMillis();
        long duration = (endTime - startTime);
        double numberOfSec = ((double) duration) / 1000.0;
        double progress = numberOfSec + 5 * score;

        double speed = -(4 * Math.pow(10, -8) * Math.pow(progress, 3)) + 9 * Math.pow(10, -5) * Math.pow(progress, 2) - 0.0708 * progress + 20;
        //System.out.println(numberOfSec+ " "+progress+" "+speed);
        double sigmoidVal = minSpeed / (1 + Math.exp( (score-pointsToReachMidpoint)/10000.0 ));
        // = -4E-08x3 + 9E-05x2 - 0.0708x + 20

        return (int) (sigmoidVal);//(int) (Math.round(speed));
        //return (int) (Math.round(sigmoidVal));
    }
    private void incrementScore(int additionalScore) {
        score += additionalScore;
    }
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        Graphics2D g2 = (Graphics2D) g;
        g.drawImage(background, 0, 0, null);
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        drawGrid(g2);

    }
    public void callTimer() {
        toolkit = Toolkit.getDefaultToolkit();
        timer = new java.util.Timer();
        reminder = new RemindTask(currPiece);
        timer.schedule(reminder, 0, speed);
    }
    public ArrayList<Integer> refillBag() {
        bagOfPieces.clear();
        for (int i = 0; i < numPieces; i++) {
            bagOfPieces.add(i);
        }
        Collections.shuffle(bagOfPieces);
        return bagOfPieces;
    }
    //board = np.zeros((20, 10), dtype=object)


    //Create a board, 20 rows, 10 columns. Each square in this has 8 possibilities, and colored based on the possibilities
    //0 is empty, 1-7 are the valid pieces.


    //Create array of the 7 valid pieces
    //let all objects be 1x1 squares at first

    //Generate random pieces for which pieces are dropped
    //Hold pieces

    //Create logic for determining where pieces land


    //Logic for turning pieces


    //Read in keyboard input
    //Graphical representation
    public Board getBoard(){
        return board;
    }
    public boolean isGameOver(){
        return gameOver;
    }
    public Piece getCurrPiece(){
        return currPiece;
    }

    public ArrayList getPieceQueue(){

        ArrayList<Integer> l = new ArrayList(pieceQueue);
        return l;
    }
    public int getScore(){
        return score;
    }
    public int getModulo(){
        return reminder.getModulo();
    }
}
