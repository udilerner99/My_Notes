import java.util.Scanner;

public class work_input {
	public static void main(String[] args) {
		double studentGPA = 3.45;
		String studentFirstName = "Jhony";
		String studentLastName = "B.Good";
		System.out.println(studentFirstName + " " + studentLastName + " has a GPA of " + studentGPA);
		System.out.println("what do you want to update it to?");

		Scanner input = new Scanner(System.in);
		studentGPA =  input.nextDouble();

		System.out.println(studentFirstName + " " + studentLastName + " has a new GPA of " + studentGPA);
	}
}
