public class Student {

	String studentFirstName;
	String studentLastName;
	int expectedYearGraduate;
	double GPA;
	String declaredMajor;

	public Student(String studentFirstName,
			String studentLastName,
			int expectedYearGraduate,
			double GPA,
			String declaredMajor) {
		this.studentFirstName = studentFirstName;
		this.studentLastName = studentLastName;
		this.expectedYearGraduate = expectedYearGraduate;
		this.GPA = GPA;
		this.declaredMajor = declaredMajor;
	}

	public void graduateIncrease() {
		this.expectedYearGraduate = this.expectedYearGraduate + 1;
	}
}
