package forensics;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("🔷 Select an operation:");
        System.out.println("1. Analyze system logs");
        System.out.println("2. Extract image metadata");
        System.out.println("3. Scan open ports");
        System.out.println("4. Run Web Vulnerability Scanner");
        System.out.print("Enter choice (1, 2, 3 or 4): ");

        int choice = scanner.nextInt();
        scanner.nextLine(); // clear buffer

        ForensicAnalyzer analyzer;

        switch (choice) {
            case 1 -> {
                analyzer = new LogAnalyzer();
                analyzer.analyze();
            }
            case 2 -> {
                analyzer = new MetadataExtractor();
                analyzer.analyze();
            }
            case 3 -> {
                PortScanner.main(new String[0]);  // directly call PortScanner
            }
            case 4 -> {
                WebVulnerabilityScanner.main(new String[0]); // call vulnerability scanner
            }
            default -> System.out.println("Invalid choice.");
        }

        scanner.close();
    }
}
