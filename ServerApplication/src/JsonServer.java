import  java.io.FileReader;
import java.net.*;
import java.io.*;


import org.json.simple.*;
import org.json.simple.parser.JSONParser;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

/**
 * Created by asherfischbaum on 14/07/2016.
 */
public class JsonServer {

    protected Socket clientSocket;

    //@SuppressWarnings("unchecked")
    public static void main(String[] args) {

        JsonServer server = new JsonServer();
        server.start();

//        JsonServer server = new JsonServer();
//        server.go();
    }

    public void start(){
        ServerSocket serverSocket = null;

        try {
            serverSocket = new ServerSocket(10007);
            System.out.println("connection socket created");

            try {
                while (true){
                    System.out.println("waiting for connection");
                    Runnable r = new SocketThread(serverSocket.accept(), this);
                    Thread socketThread = new Thread(r);
                    socketThread.start();
                }
            } catch (IOException e){
                System.err.println("socket accept failed");
                System.exit(1);
            }

        } catch (IOException e){
            System.err.println("could not listen to port 10007");
            System.exit(1);
        } finally {
            try {
                serverSocket.close();
            } catch (IOException e){
                System.err.println("could not closs port 10007");
                System.exit(1);
            }
        }
    }

}


class SocketThread implements Runnable{

    protected Socket clientSocket;
    JsonServer server;
    ServerDB DB;

    public SocketThread(Socket socket, JsonServer jsonServer) {
        this.clientSocket = socket;
        this.server = jsonServer;
        DB = new ServerDB();
    }

    @Override
    public void run() {
        System.out.println("new thread created");

        JSONParser parser = new JSONParser();

        try {
            BufferedReader input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            String inputLine;

            while ((inputLine = input.readLine()) != null) {

                System.out.println(inputLine);

                Object groupObject = parser.parse(inputLine);
                JSONObject group = (JSONObject) groupObject;

                String[] info = messageParse(group);
                System.out.println(info[2]);

                DB.insert(info[0], info[1], Integer.parseInt(info[2]), info[3], info[4]);
            }

            System.out.println(" I got to the end of the thread and will start closing things");
            DB.shutdown();
            input.close();
            clientSocket.close();
        } catch (IOException e){
            System.err.println("shit");
            System.exit(1);
        } catch (ParseException e) {
            System.err.println("Problem with the Parser");
            System.exit(1);
        }

    }

    public String[] messageParse(JSONObject object){
        String name = (String) object.get("group name");
        String email = (String) object.get("email");
        String numUsers = (String) object.get("amount of users");
        String city = (String) object.get("City");
        String country = (String) object.get("Country");

        String[] groupInfo = {name, email, numUsers, city, country};

        return groupInfo;
    }

}