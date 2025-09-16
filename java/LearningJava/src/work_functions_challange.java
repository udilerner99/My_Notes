import java.util.Scanner;

public class work_functions_challange {

	public static int calaculateSalary(int employeeHoursPerWeek, int salaryPerHour) {
		int salaryPerMonth = (employeeHoursPerWeek * 4) * salaryPerHour;
		int salaryPerYear = salaryPerMonth * 12;
		return salaryPerYear;
	}

	public static int calculateVaction(int numberOfVacationDays, int salaryPerHour) {
		int costOfVacation = (numberOfVacationDays * 8) * salaryPerHour;
		return costOfVacation;
	}

	public static void main(String[] args) {
		int salaryPerHour = 32;

		System.out.println("Year salary is :" + calaculateSalary(45, salaryPerHour));

		System.out.println("Please enter number of vacation days:");
		Scanner input = new Scanner(System.in);
		int numberOfVacationDays = input.nextInt();

		System.out.println("After Vacation subtraction salry is: " +
				(calaculateSalary(45, salaryPerHour) - calculateVaction(numberOfVacationDays, salaryPerHour)));
	}
}
