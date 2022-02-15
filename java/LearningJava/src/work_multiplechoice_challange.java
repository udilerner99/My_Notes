import java.util.Scanner;

public class work_multiplechoice_challange {

	public static void main(String[] args) {
		System.out.println("answer this : 2+2 = ? possible answers: [3] [4] [5]");
		Scanner scanner = new Scanner(System.in);
		boolean isOnRepeat = true;

		while (isOnRepeat) {
			int inputNumAnswer = scanner.nextInt();
			if (inputNumAnswer == 4) {
				System.out.println("You're correct !!!");
				isOnRepeat = false;
			} else {
				System.out.println("You're incorrect !!! please try again !");
				isOnRepeat = true;
			}
		}

	}
}
