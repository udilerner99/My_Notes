public class work_student {

	public static void main(String[] args) {
		Student studentA = new Student("Jhony", "B.Good", 2024, 4.2, "Businesses");
		Student studentB = new Student("Danny", "B.Good", 2023, 4.1, "C.S");

		System.out.println(studentA.studentFirstName);
		System.out.println(studentB.studentFirstName);

		studentB.graduateIncrease();
		System.out.println(studentA.expectedYearGraduate);
	}
}
