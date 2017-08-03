import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.JFrame;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import java.io.*;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;


/**
 * Created by Patrick on 7/16/17.
 */
public class TetrisFrame extends JFrame implements KeyListener {
    public int windowWidth = 800;
    public int windowHeight = 800;
    public int left = 0;
    public int right = 0;
    public int down = 0;

    public int xCounter = 0;
    public int zCounter = 0;
    private socketThread t1;
    private boolean isGameOver = false;
    public boolean receivingAndSending = true;
    private TetrisBuilder panel;
    public int speed = 75;

    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                try {
                    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
                } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException ex) {
                }

                new TetrisFrame();
            }
        });


    }


    class socketThread implements Runnable {
        private Thread t;
        private PrintWriter outs;
        private BufferedReader inFromClient;

        socketThread(PrintWriter thisWriter, BufferedReader thisReader) {
            outs = thisWriter;
            inFromClient = thisReader;
        }

        public void run() {
            try {
                while (true) {

                    String fromclient = "";
                    Thread.sleep(speed * 2);
                    //System.out.println("sending feature array");
                    String outputLine = generateFeatureArray();
                    outs.println(outputLine);
                    fromclient = inFromClient.readLine();

                    if (isGameOver) {
                        while (!fromclient.equals("reset")) {
                            fromclient = inFromClient.readLine();
                        }
                    } else {
                        System.out.println("RECEIVED:" + fromclient);

                        switch (fromclient) {
                            case "left":
                                panel.leftArrow();
                                break;
                            case "right":
                                panel.rightArrow();
                                break;
                            case "x":
                            case "up":
                                panel.upArrowAndXButton();
                                break;
                            case "down":
                                panel.downArrow();
                                break;
                            case "shift":
                                panel.shiftButton();
                                break;
                            case "space":
                                panel.spaceButton();
                                break;
                            case "z":
                                panel.zButton();
                                break;
                            case "reset":
                                break;
                            case "end":
                                System.exit(0);
                        }

                    }


                }
            } catch (Exception e) {

            }
        }

        public void pause(int mili) {
            try {
                Thread.sleep(mili);
            } catch (Exception e) {

            }
        }

        public void start() {
            System.out.println("Starting listening");
            if (t == null) {
                t = new Thread(this, "");
                t.start();
            }
        }
    }


    public void keyPressed(KeyEvent e) {
        int code = e.getKeyCode();
        switch (code) {
            case KeyEvent.VK_DOWN:
                down = 10;
                System.out.println("down");
                break;
            case KeyEvent.VK_X:
            case KeyEvent.VK_UP:
                xCounter = 10;
                System.out.println("up");
                break;
            case KeyEvent.VK_LEFT:
                System.out.println("left");
                left = 10;
                break;
            case KeyEvent.VK_RIGHT:
                System.out.println("right");
                right = 10;
                break;
            case KeyEvent.VK_SPACE:
                System.out.println("space");
                panel.spaceButton();
                break;
            case KeyEvent.VK_Z:
                System.out.println("z");
                zCounter = 10;
                resetGame();
                break;
            case KeyEvent.VK_SHIFT:
                System.out.println("shift");
                panel.shiftButton();
                break;
        }
    }

    public void keyReleased(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_DOWN:
                down = 0;
                break;
            case KeyEvent.VK_X:
            case KeyEvent.VK_UP:
                xCounter = 0;
                break;
            case KeyEvent.VK_LEFT:
                left = 0;
                break;
            case KeyEvent.VK_RIGHT:
                right = 0;
                break;
            case KeyEvent.VK_Z:
                zCounter = 0;
                break;

        }
    }

    public void keyTyped(KeyEvent e) {
    }

    public void resetGame() {
        if (receivingAndSending) {
            isGameOver = true;

            t1.pause(2 * speed);
            panel.setVisible(false);
            panel.removeAll();
            revalidate();
            repaint();
            left = 0;
            right = 0;
            down = 0;
            xCounter = 0;
            zCounter = 0;
            TetrisBuilder newPanel = new TetrisBuilder(this);
            newPanel.setVisible(true);
            add(newPanel, BorderLayout.CENTER);
            panel = newPanel;
            isGameOver = false;
        }
    }

    public TetrisFrame() {
        super();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        addKeyListener(this);
        setSize(windowWidth, windowHeight);
        setLayout(new BorderLayout());
        setVisible(true);


        setFocusable(true);
        setFocusTraversalKeysEnabled(false);


        System.out.println("Creating ");
        String fromclient = "";
        ServerSocket server;
        PrintWriter outs;

        BufferedReader inFromClient;
        if (receivingAndSending) {
            try {
                server = new ServerSocket(5000);

                System.out.println("TCPServer Waiting for client on port 5000");
                Socket connected = server.accept();
                outs = new PrintWriter(connected.getOutputStream(), true);
                System.out.println(" THE CLIENT" + " " + connected.getInetAddress() + ":" + connected.getPort() + " IS CONNECTED ");

                inFromClient = new BufferedReader(new InputStreamReader(connected.getInputStream()));

                t1 = new socketThread(outs, inFromClient);
                t1.start();

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        panel = new TetrisBuilder(this);
        add(panel, BorderLayout.CENTER);

    }

    private int[][] getBoardMatrix() {
        Board board = panel.getBoard();
        int[][] boardVals = board.getBoard();
        return boardVals;
    }

    public String generateFeatureArray() {
        String totalString = "";
        int gameOver;
        int[][] boardVals = getBoardMatrix();
        BoardCoord[] pieceCoords = panel.getCurrPiece().getCoords();

        if (isGameOver) {
            gameOver = 1;
        } else {
            gameOver = 0;
        }
        totalString += gameOver + ",";

        int score = panel.getScore();
        totalString += score + ",";

        for (int i = 0; i < boardVals.length; i++) {
            for (int j = 0; j < boardVals[0].length; j++) {
                if (boardVals[i][j] == 0) {
                    totalString += 0 + ",";
                } else {
                    totalString += 1 + ",";
                }
            }
        }
        ArrayList<Integer> pieceQueue = panel.getPieceQueue();
        for (int i = 0; i < panel.queueSize; i++) {
            totalString += pieceQueue.get(i) + ",";
        }
        for (int i = 0; i < panel.pieceSize; i++) {
            totalString += pieceCoords[i].row + ",";
            totalString += pieceCoords[i].col + ",";
        }
        //String mod = panel.getModulo() + "";
        //totalString += mod;
        return totalString;

    }
}
