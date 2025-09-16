import java.util.Scanner;

public class work_functions {

	public static void announcedDeveloperTeaTime() {
		System.out.println("waiting for developer tea time....");
		System.out.println("type in a random word and press Enter to start the tea time");
		Scanner input = new Scanner(System.in);
		input.next();
		System.out.println("it's tea time!");
	}
	public static void main(String[] args) {
		System.out.println("welcome to your new job");

		announcedDeveloperTeaTime();

		System.out.println("write your code");
		System.out.println("review your code");

		announcedDeveloperTeaTime();

		System.out.println("you're done");
	}
}
