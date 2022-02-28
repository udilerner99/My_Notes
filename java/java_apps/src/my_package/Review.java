package my_package;

public class Review {

	public static void main(String[] args) {
		printS("YOYO");

		Review myReview = new Review();
		myReview.print("Instance Method");
	}

	void print(String data) {
		System.out.println(data);
	}

	static void printS(String data) {
		System.out.println(data);
	}
}
