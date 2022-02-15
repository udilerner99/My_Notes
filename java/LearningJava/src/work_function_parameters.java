public class work_function_parameters {

	public static void calculateTotalMealPrice(double listedMealPrice,
											   double tipRate,
											   double taxRate) {
		double tip = tipRate * listedMealPrice;
		double tax = taxRate * listedMealPrice;
		double result = listedMealPrice + tip + tax;
		System.out.println("your total meal price is: " + result);
	}
	public static void main(String[] args) {
		calculateTotalMealPrice(20, 0.1, 0.18);
	}
}
