import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Created by asherfischbaum on 14/07/2016.
 */
public class ServerDB {

    Connection c;

    public ServerDB(){
        c = null;

        connectToDB();
        createTable();
    }


    /**
     * this is here solely for testing purposes. take this out before release.
     * @param args
     */
    public static void main(String[] args) {
        ServerDB SDB = new ServerDB();
        SDB.go();
        System.out.println("we will now enter elements into the database");
        SDB.insert("London Java Community", "ljc-list@meetup.com", 5550, "London", "United Kingdom");
    }

    public void go(){
        System.out.println("hello world");
    }

    private void connectToDB(){
        try{
            Class.forName("org.postgresql.Driver");
            this.c = DriverManager.getConnection("jdbc:postgresql://localhost:5432/meetupgroups", "asherfischbaum", "123");

        } catch (Exception e){
            System.out.println("=========== ERROR OCCURED WHILE TRYING TO CONNECT TO THE DB ===========");
            e.printStackTrace();
            System.err.println(e.getClass().getName()+": "+e.getMessage());
            System.exit(0);
        }
    }

    public void createTable(){
        try {
            Statement statement = this.c.createStatement();

            String sql = "CREATE TABLE IF NOT EXISTS groupInfo " +
                    "(ID                SERIAL   NOT NULL," +
                    " GROUPNAME         TEXT    NOT NULL, " +
                    " EMAIL             TEXT   PRIMARY KEY NOT NULL, " +
                    " TOTALEMEMBERS     INT, " +
                    " CITY              TEXT," +
                    "COUNTRY            TEXT);";

            statement.executeUpdate(sql);
            statement.close();


            System.out.println("table, is definately there");

        } catch (SQLException e) {
            System.out.println("============== ERROR OCCURED WHILE CREATING THE TABLE ==============");
            e.printStackTrace();
            System.err.println(e.getClass().getName()+": "+e.getMessage());
            System.exit(0);
        }

    }

    public void insert(String groupName, String email, int memberCount, String city, String country){

        Statement stmt = null;

        try{
            stmt = this.c.createStatement();

            String SQL = "INSERT INTO groupinfo (GROUPNAME, EMAIL, TOTALEMEMBERS, CITY, COUNTRY)" +
                    " VALUES ('" + groupName + "', '" + email + "', " + memberCount +
                    ", '" + city + "', '" + country + "');" ;

            stmt.executeUpdate(SQL);

        } catch (SQLException e) {
            System.out.println("================= INSERT STATEMENT DID NOT WORK ================");
            e.printStackTrace();
        }


    }

    // again for testing purposes.


    public void shutdown(){
        try {
            this.c.close();
        } catch (SQLException e) {
            System.out.println("=========== COULD NOT CLOSE DB CONNECTION PROPERLY ============");
            e.printStackTrace();
        }
    }

}