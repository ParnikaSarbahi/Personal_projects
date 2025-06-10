package forensics;

import java.net.*;
import java.util.*;
import java.io.*;

public class PortScanner {

    public static String getServiceName(int port) {
        switch (port) {
            case 20: return "FTP Data";
            case 21: return "FTP Control";
            case 22: return "SSH";
            case 23: return "Telnet";
            case 25: return "SMTP (Email Sending)";
            case 53: return "DNS";
            case 80: return "HTTP";
            case 110: return "POP3";
            case 143: return "IMAP";
            case 443: return "HTTPS";
            case 3306: return "MySQL";
            case 3389: return "RDP";
            default: return "Unknown Service";
        }
    }

    public static void saveToFile(String filename, List<String> results) {
        try {
            FileWriter writer = new FileWriter(filename);
            for (String line : results) {
                writer.write(line + "\n");
            }
            writer.close();
            System.out.println("Scan results saved to: " + filename);
        } catch (IOException e) {
            System.out.println("Error saving to file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter target host (e.g., 127.0.0.1): ");
        String host = sc.nextLine();

        System.out.print("Enter start port: ");
        int startPort = sc.nextInt();

        System.out.print("Enter end port: ");
        int endPort = sc.nextInt();
        sc.nextLine(); // Clear buffer

        List<String> scanResults = new ArrayList<>();
        List<Thread> threads = new ArrayList<>();

        for (int port = startPort; port <= endPort; port++) {
            PortCheckThread thread = new PortCheckThread(host, port, scanResults);
            thread.start();
            threads.add(thread);
        }

        for (Thread t : threads) {
            try {
                t.join();
            } catch (InterruptedException e) {
                System.out.println("Thread interrupted: " + e.getMessage());
            }
        }

        System.out.print("Do you want to save the results to a file? (yes/no): ");
        String saveChoice = sc.nextLine();

        if (saveChoice.equalsIgnoreCase("yes")) {
            System.out.print("Enter file name: ");
            String filename = sc.nextLine().trim();
            saveToFile(filename, scanResults);
        }

        sc.close();
    }
}

class PortCheckThread extends Thread {
    private String host;
    private int port;
    private List<String> scanResults;

    public PortCheckThread(String host, int port, List<String> scanResults) {
        this.host = host;
        this.port = port;
        this.scanResults = scanResults;
    }

    public void run() {
        try {
            Socket socket = new Socket();
            socket.connect(new InetSocketAddress(host, port), 300);
            String service = PortScanner.getServiceName(port);
            String result = "Port " + port + " is open (" + service + ")";
            System.out.println(result);

            synchronized (scanResults) {
                scanResults.add(result);
            }

            socket.close();
        } catch (Exception e) {
            // Port is closed or connection failed, do nothing
        }
    }
}
